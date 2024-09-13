from dataclasses import replace

import torch
from torch import nn
from apex.normalization import FusedLayerNorm

from .seq2seq import BaseSeq2Seq
from ..types import Seq


class _Conv(nn.Module):
    def __init__(self, dim: int, kernel_size: int):
        super().__init__()
        self.layers = nn.Sequential(
            nn.ZeroPad1d((kernel_size - 1, 0)),
            nn.Conv1d(dim, dim, kernel_size),
        )

    def forward(self, x: torch.Tensor, _) -> torch.Tensor:
        x = x.permute(1, 2, 0)
        x = self.layers(x)
        x = x.permute(2, 0, 1)
        return x


class _GRU(nn.Module):
    def __init__(self, dim: int):
        super().__init__()
        self.gru = nn.GRU(dim, dim)

    def forward(self, x: torch.Tensor, _) -> torch.Tensor:
        x, _ = self.gru(x)
        return x


class _MHA(nn.Module):
    def __init__(self, dim: int, num_heads: int, dropout: float):
        super().__init__()
        self.mha = nn.MultiheadAttention(dim, num_heads, dropout)

    def forward(self, x: torch.Tensor, lengths: torch.Tensor) -> torch.Tensor:
        padding_mask = torch.arange(x.shape[0], device=x.device) >= lengths[:, None]
        x, _ = self.mha(x, x, x, key_padding_mask=padding_mask, need_weights=False)
        return x


class SeqnasLayer(BaseSeq2Seq):
    def __init__(
        self,
        input_size: int,
        gru: bool = False,
        conv: bool = False,
        conv_kernel_size: int = 3,
        attn: bool = False,
        attn_num_heads: int = 1,
        dropout: float = 0.1,
    ):
        super().__init__()
        if (attn and input_size < attn_num_heads * (attn + gru + conv)) or (
            not attn and input_size < gru + conv
        ):
            raise ValueError("Too small input size for provided configuration")

        self.norm = FusedLayerNorm(input_size)

        self.layers = nn.ModuleList()
        self.sizes = []
        remaining_blocks = gru + conv + attn
        remaining_size = input_size
        if attn:
            emb_sz = (
                round(remaining_size / remaining_blocks / attn_num_heads)
                * attn_num_heads
            )
            remaining_size -= emb_sz
            remaining_blocks -= 1
            self.sizes.append(emb_sz)
            self.layers.append(_MHA(emb_sz, attn_num_heads, dropout))
        if conv:
            emb_sz = remaining_size // remaining_blocks
            remaining_size -= emb_sz
            remaining_blocks -= 1
            self.sizes.append(emb_sz)
            self.layers.append(_Conv(emb_sz, conv_kernel_size))
        if gru:
            emb_sz = remaining_size
            self.sizes.append(emb_sz)
            self.layers.append(_GRU(emb_sz))

        self.actual_size = sum(self.sizes)
        self.dropout = nn.Dropout(dropout)
        self.ff = nn.Sequential(
            FusedLayerNorm(self.actual_size),
            nn.Linear(self.actual_size, self.actual_size),
            nn.Dropout(dropout),
            nn.Mish(),
            FusedLayerNorm(self.actual_size),
            nn.Linear(self.actual_size, self.actual_size),
            nn.Dropout(dropout),
        )

    @property
    def output_dim(self):
        return self.actual_size

    def forward(self, seq: Seq) -> Seq:
        x = self.norm(seq.tokens)

        start_idx = 0
        outs = []
        for layer, sz in zip(self.layers, self.sizes):
            outs.append(layer(x[:, :, start_idx : start_idx + sz], seq.lengths))
            start_idx += sz
        x = torch.cat(outs, 2)

        x = self.dropout(x) + seq.tokens[:, :, : self.actual_size]
        x = self.ff(x) + x

        return replace(seq, tokens=x)
