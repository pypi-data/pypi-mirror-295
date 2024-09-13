from typing import Tuple
import torch
import torch.utils.checkpoint
from torch import nn
from torch.nn import CrossEntropyLoss
from transformers.modeling_outputs import (
    BaseModelOutputWithPastAndCrossAttentions,
    BaseModelOutputWithPoolingAndCrossAttentions,
    MaskedLMOutput,
)
from transformers.modeling_utils import (
    PreTrainedModel,
)
from transformers.utils import logging
from .configuration_prolm import ProLMConfig
from torch.nn.functional import scaled_dot_product_attention
import torch.nn.functional as F

logger = logging.get_logger(__name__)


def rotate_half(x):
    return torch.cat((-x[..., x.shape[-1] // 2 :], x[..., : x.shape[-1] // 2]), dim=-1)


def apply_prolm_rotary_pos_emb(q, k, cos, sin, unsqueeze_dim=1):
    cos = cos.unsqueeze(unsqueeze_dim)
    sin = sin.unsqueeze(unsqueeze_dim)
    q_embed = (q * cos) + (rotate_half(q) * sin)
    k_embed = (k * cos) + (rotate_half(k) * sin)
    return q_embed, k_embed


def gelu(x):
    return F.silu(x)


def cread_4d_mask(attn_mask, return_type="bool", x=None):
    # Create a 4D mask from a 2D mask (B, L) -> (B, 1, L, L)
    mask_3d = torch.eq(attn_mask.unsqueeze(2), attn_mask.unsqueeze(1))
    mask_4d = mask_3d.unsqueeze(1)
    if return_type == "bool":
        # For ScaledDotProductAttention, we can convert the mask to bool
        return mask_4d
    elif return_type == "float":
        # For naive attention, we need to convert the mask to float
        mask_4d = (1.0 - mask_4d.to(x.dtype)) * torch.finfo(x.dtype).min
        return mask_4d


class ProLMRotaryEmbedding(torch.nn.Module):
    def __init__(self, dim: int):
        super().__init__()
        inv_freq = 1.0 / (10000 ** (torch.arange(0, dim, 2, dtype=torch.int64).float() / dim))
        self.register_buffer("inv_freq", inv_freq, persistent=False)

    @torch.no_grad()
    def forward(
        self,
        x,
        position_ids,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        inv_freq_expanded = self.inv_freq[None, :, None].float().expand(position_ids.shape[0], -1, 1)
        position_ids_expanded = position_ids[:, None, :].float()
        device_type = x.device.type
        device_type = (
            device_type
            if isinstance(device_type, str) and device_type != "mps"
            else "cpu"
        )
        with torch.autocast(device_type=device_type, enabled=False):
            freqs = (
                inv_freq_expanded.float() @ position_ids_expanded.float()
            ).transpose(1, 2)
            emb = torch.cat((freqs, freqs), dim=-1)
            cos = emb.cos()
            sin = emb.sin()
        return cos.to(x.dtype), sin.to(x.dtype)


class ProLMEmbeddings(nn.Module):

    def __init__(self, config):
        super().__init__()
        self.config = config
        self.word_embeddings = nn.Embedding(
            config.vocab_size, config.hidden_size, padding_idx=config.pad_token_id
        )
        if config.emb_layer_norm_before:
            self.layer_norm = RMSNorm(config.hidden_size, eps=config.layer_norm_eps)
        else:
            self.layer_norm = None
        self.dropout = nn.Dropout(config.hidden_dropout_prob)
        self.position_embedding_type = config.position_embedding_type
        self.padding_idx = config.pad_token_id
        self.token_dropout = config.token_dropout
        self.mask_token_id = config.mask_token_id

    def forward(
        self,
        input_ids,
        attention_mask,
    ):
        binary_attention_mask = attention_mask.clone()
        binary_attention_mask[binary_attention_mask > 0] = 1
        attention_mask = binary_attention_mask
        inputs_embeds = self.word_embeddings(input_ids)
        embeddings = inputs_embeds

        if self.token_dropout and (not self.config.is_decoder):
            embeddings = embeddings.masked_fill(
                (input_ids == self.mask_token_id).unsqueeze(-1), 0.0
            )
            mask_ratio_train = 0.12  # 0.15 * 0.8
            src_lengths = attention_mask.sum(-1)
            mask_ratio_observed = (input_ids == self.mask_token_id).sum(
                -1
            ).float() / src_lengths
            embeddings = (
                embeddings
                * (1 - mask_ratio_train)
                / (1 - mask_ratio_observed)[:, None, None]
            ).to(embeddings.dtype)

        if self.layer_norm is not None:
            embeddings = self.layer_norm(embeddings)
        if attention_mask is not None:
            embeddings = (embeddings * attention_mask.unsqueeze(-1)).to(
                embeddings.dtype
            )
        return embeddings


class ProLMSelfAttention(nn.Module):
    def __init__(self, config):
        super().__init__()
        if config.hidden_size % config.num_attention_heads != 0:
            raise ValueError(
                f"The hidden size ({config.hidden_size}) is not a multiple of the number of attention "
                f"heads ({config.num_attention_heads})"
            )
        self.num_attention_heads = config.num_attention_heads
        self.attention_head_size = config.hidden_size // config.num_attention_heads
        self.all_head_size = self.num_attention_heads * self.attention_head_size
        self.query = nn.Linear(config.hidden_size, self.all_head_size, bias=False)
        self.key = nn.Linear(config.hidden_size, self.all_head_size, bias=False)
        self.value = nn.Linear(config.hidden_size, self.all_head_size, bias=False)
        self.dropout = nn.Dropout(config.attention_probs_dropout_prob)
        self.rotary_embeddings = ProLMRotaryEmbedding(dim=self.attention_head_size)
        self.flash_attention = config.flash_attention
        self.is_decoder = config.is_decoder
        self.config = config

    def transpose_for_scores(self, x: torch.Tensor) -> torch.Tensor:
        new_x_shape = x.size()[:-1] + (
            self.num_attention_heads,
            self.attention_head_size,
        )
        x = x.view(new_x_shape)
        return x.permute(0, 2, 1, 3)

    def forward(
        self,
        hidden_states: torch.Tensor,
        attention_mask: torch.Tensor,
        position_ids: torch.Tensor,
        output_attentions: bool = False,
    ) -> Tuple[torch.Tensor]:
        query_layer = self.transpose_for_scores(self.query(hidden_states))
        key_layer = self.transpose_for_scores(self.key(hidden_states))
        value_layer = self.transpose_for_scores(self.value(hidden_states))
        query_layer = query_layer * (self.attention_head_size**-0.5)
        cos, sin = self.rotary_embeddings(value_layer, position_ids)
        query_layer, key_layer = apply_prolm_rotary_pos_emb(
            query_layer, key_layer, cos, sin
        )
        if not self.flash_attention:
            attention_scores = torch.matmul(query_layer, key_layer.transpose(-1, -2))
            attention_scores = attention_scores + attention_mask
            attention_probs = nn.functional.softmax(attention_scores, dim=-1, dtype=torch.float32).to(query_layer.dtype)
            attention_probs = self.dropout(attention_probs)
            context_layer = torch.matmul(attention_probs, value_layer)
        else:
            dropout_p = self.config.attention_probs_dropout_prob if self.training else 0
            query_layer = query_layer.contiguous()
            key_layer = key_layer.contiguous()
            value_layer = value_layer.contiguous()
            context_layer = scaled_dot_product_attention(
                query_layer,
                key_layer,
                value_layer,
                attn_mask=attention_mask,
                dropout_p=dropout_p,
                scale=1,  # we have done query_layer = query_layer * (self.attention_head_size**-0.5)
            )
            attention_probs = None
        context_layer = context_layer.permute(0, 2, 1, 3).contiguous()
        new_context_layer_shape = context_layer.size()[:-2] + (self.all_head_size,)
        context_layer = context_layer.view(new_context_layer_shape)
        if output_attentions:
            return (context_layer, attention_probs)
        return (context_layer, None)


class ProLMSelfOutput(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.dense = nn.Linear(config.hidden_size, config.hidden_size, bias=False)
        self.dropout = nn.Dropout(config.hidden_dropout_prob)

    def forward(self, hidden_states, input_tensor):
        hidden_states = self.dense(hidden_states)
        hidden_states = self.dropout(hidden_states)
        hidden_states = hidden_states + input_tensor
        return hidden_states


class RMSNorm(nn.Module):
    def __init__(self, hidden_size, eps=1e-6):
        """
        LlamaRMSNorm is equivalent to T5LayerNorm
        """
        super().__init__()
        self.weight = nn.Parameter(torch.ones(hidden_size))
        self.variance_epsilon = eps

    def forward(self, hidden_states):
        input_dtype = hidden_states.dtype
        hidden_states = hidden_states.to(torch.float32)
        variance = hidden_states.pow(2).mean(-1, keepdim=True)
        hidden_states = hidden_states * torch.rsqrt(variance + self.variance_epsilon)
        return self.weight * hidden_states.to(input_dtype)

    def extra_repr(self):
        return f"{tuple(self.weight.shape)}, eps={self.variance_epsilon}"
    
class ProLMAttention(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.self = ProLMSelfAttention(config)
        self.output = ProLMSelfOutput(config)
        self.LayerNorm = RMSNorm(config.hidden_size, eps=config.layer_norm_eps)
        
    def forward(
        self,
        hidden_states,
        position_ids,
        attention_mask,
        output_attentions=False,
    ):
        hidden_states = self.LayerNorm(hidden_states)
        self_outputs, attn_probs = self.self(
            hidden_states=hidden_states,
            attention_mask=attention_mask,
            position_ids=position_ids,
            output_attentions=output_attentions,
        )
        attention_output = self.output(self_outputs, hidden_states)
        return (attention_output, attn_probs)


class ProLMIntermediate(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.dense = nn.Linear(config.hidden_size, config.intermediate_size, bias=False)

    def forward(self, hidden_states: torch.Tensor) -> torch.Tensor:
        hidden_states = self.dense(hidden_states)
        hidden_states = gelu(hidden_states)
        return hidden_states


class ProLMOutput(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.dense = nn.Linear(config.intermediate_size, config.hidden_size, bias=False)
        self.dropout = nn.Dropout(config.hidden_dropout_prob)

    def forward(self, hidden_states, input_tensor):
        hidden_states = self.dense(hidden_states)
        hidden_states = self.dropout(hidden_states)
        hidden_states = hidden_states + input_tensor
        return hidden_states


class ProLMLayer(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.attention = ProLMAttention(config)
        self.intermediate = ProLMIntermediate(config)
        self.output = ProLMOutput(config)
        self.LayerNorm = RMSNorm(config.hidden_size, eps=config.layer_norm_eps)

    def forward(
        self,
        hidden_states,
        position_ids,
        attention_mask,
        output_attentions=False,
    ):
        attention_output, attn_probs = self.attention(
            hidden_states=hidden_states,
            position_ids=position_ids,
            attention_mask=attention_mask,
            output_attentions=output_attentions,
        )
        attention_output_ln = self.LayerNorm(attention_output)
        intermediate_output = self.intermediate(attention_output_ln)
        layer_output = self.output(intermediate_output, attention_output)
        return (layer_output, attn_probs)


class ProLMEncoder(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.layer = nn.ModuleList(
            [ProLMLayer(config) for _ in range(config.num_hidden_layers)]
        )
        self.emb_layer_norm_after = RMSNorm(config.hidden_size, eps=config.layer_norm_eps)

    def forward(
        self,
        hidden_states,
        position_ids,
        attention_mask,
        output_attentions=False,
        output_hidden_states=False,
    ):
        all_hidden_states = []
        all_self_attentions = []

        for i, layer_module in enumerate(self.layer):
            if output_hidden_states:
                all_hidden_states = all_hidden_states + [hidden_states, ]
            hidden_states, attn_probs = layer_module(
                hidden_states=hidden_states,
                position_ids=position_ids,
                attention_mask=attention_mask,
                output_attentions=output_attentions,
            )
            if output_attentions:
                all_self_attentions = all_self_attentions + [attn_probs,]

        if self.emb_layer_norm_after:
            hidden_states = self.emb_layer_norm_after(hidden_states)

        if output_hidden_states:
            all_hidden_states = all_hidden_states + [hidden_states,]

        return BaseModelOutputWithPastAndCrossAttentions(
            last_hidden_state=hidden_states,
            hidden_states=all_hidden_states,
            attentions=all_self_attentions,
        )


class ProLMPreTrainedModel(PreTrainedModel):
    """
    An abstract class to handle weights initialization and a simple interface for downloading and loading pretrained
    models.
    """

    config_class = ProLMConfig
    base_model_prefix = "prolm"
    # Copied from transformers.models.bert.modeling_bert.BertPreTrainedModel._init_weights

    def _init_weights(self, module):
        """Initialize the weights"""
        if isinstance(module, nn.Linear):
            # Slightly different from the TF version which uses truncated_normal for initialization
            # cf https://github.com/pytorch/pytorch/pull/5617
            module.weight.data.normal_(mean=0.0, std=self.config.initializer_range)
            if module.bias is not None:
                module.bias.data.zero_()
        elif isinstance(module, nn.Embedding):
            module.weight.data.normal_(mean=0.0, std=self.config.initializer_range)
            if module.padding_idx is not None:
                module.weight.data[module.padding_idx].zero_()
                
class ProLMModel(ProLMPreTrainedModel):

    def __init__(self, config):
        super().__init__(config)
        self.config = config
        self.embeddings = ProLMEmbeddings(config)
        self.encoder = ProLMEncoder(config)

    def forward(
        self,
        input_ids,
        attention_mask,
        position_ids,
        output_attentions=False,
        output_hidden_states=False,
    ) -> BaseModelOutputWithPoolingAndCrossAttentions:
        hidden_states = self.embeddings(
            input_ids=input_ids,
            attention_mask=attention_mask,
        )
        if self.config.flash_attention:
            attention_mask_4d = cread_4d_mask(attention_mask, return_type="bool")
        else:
            attention_mask_4d = cread_4d_mask(attention_mask, return_type="float", x=hidden_states)
        encoder_outputs = self.encoder(
            hidden_states=hidden_states,
            position_ids=position_ids,
            attention_mask=attention_mask_4d,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
        )
        return BaseModelOutputWithPoolingAndCrossAttentions(
            last_hidden_state=encoder_outputs.last_hidden_state,
            hidden_states=encoder_outputs.hidden_states,
            attentions=encoder_outputs.attentions,
        )


class ProLMLMHead(nn.Module):

    def __init__(self, config):
        super().__init__()
        self.dense = nn.Linear(config.hidden_size, config.hidden_size, bias=False)
        self.layer_norm = RMSNorm(config.hidden_size, eps=config.layer_norm_eps)
        self.decoder = nn.Linear(config.hidden_size, config.vocab_size, bias=False)
        self.bias = nn.Parameter(torch.zeros(config.vocab_size))

    def forward(self, features, **kwargs):
        x = self.dense(features)
        x = gelu(x)
        x = self.layer_norm(x)
        x = self.decoder(x) + self.bias
        return x

class ProLMForMaskedLM(ProLMPreTrainedModel):

    def __init__(self, config):
        super().__init__(config)
        self.prolm = ProLMModel(config)
        self.lm_head = nn.Linear(config.hidden_size, config.vocab_size, bias=False)
        self.init_weights()

    def forward(
        self,
        input_ids,
        attention_mask,
        position_ids,
        labels=None,
        output_attentions=False,
        output_hidden_states=False,
    ) -> MaskedLMOutput:
        outputs = self.prolm(
            input_ids=input_ids,
            attention_mask=attention_mask,
            position_ids=position_ids,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
        )
        sequence_output = outputs.last_hidden_state
        prediction_scores = self.lm_head(sequence_output)
        loss = None
        if labels is not None:
            loss_fct = CrossEntropyLoss()
            labels = labels.to(prediction_scores.device)
            loss = loss_fct(
                prediction_scores.view(-1, self.config.vocab_size), labels.view(-1)
            )
        return MaskedLMOutput(
            loss=loss,
            logits=prediction_scores,
            hidden_states=outputs.hidden_states,
            attentions=outputs.attentions,
        )

ProLMModel.register_for_auto_class("AutoModel")
ProLMForMaskedLM.register_for_auto_class("AutoModelForMaskedLM")