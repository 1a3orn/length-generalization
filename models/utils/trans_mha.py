from numpy import dtype, uint8
import torch
import torch.nn as nn
import torch.nn.functional as F

from models.utils.trans_causal import CausalMask
from models.utils.trans_alibi import AlibiEncoding

class MultiHeadAttention(nn.Module):
    '''
    Simple multi-headed attention layer with masking and no dropout.
    [b, t, k] --> [b, t, k]
    '''
    def __init__(self, config, alibi=True):
        super(MultiHeadAttention, self).__init__()
        self.dim = dim = config["hidden_dim"]
        self.num_heads = config["num_heads"]
        self.seq_length = seq_length = config["ctx_len"]
        assert self.dim % self.num_heads == 0, "dim must be evenly divisible by num_heads"

        # Actually create everything
        if alibi:
            self.alibi = AlibiEncoding(seq_length, self.num_heads)
        self.alibi_bool = alibi
        self.mask = CausalMask(seq_length)
        self.to_key = nn.Linear(dim, dim)
        self.to_query = nn.Linear(dim, dim)
        self.to_value = nn.Linear(dim, dim)
        self.proj = nn.Linear(dim, dim)

    def _reshape(self, x):
        '''
        Reshapes x from [b, t, k] to [b * nh, t, k // nh]
        where nh is the number of heads, and where k
        might be k * scale_kq.
        '''
        b, t, k = x.size()
        nh = self.num_heads
        x = x.view(b, t, nh, k // nh).transpose(1, 2)
        cont_x = x.contiguous()
        return cont_x.view(b * nh, t, k // nh)

    def forward(self, x):
        b, t, k = x.size()
        nh = self.num_heads

        # Create the keys and queries, resizing to [b * nh, t, k // nh].
        # This makes the heads independently learn the keys and queries.
        # We also scale so that dot product is scaled by the square root of k.
        scale = (k ** 0.25)
        # From [b, t, k] to [b, t, k * scale_kq]
        x_key = x
        x_query = x
        keys = self._reshape(self.to_key(x_key)) / scale
        queries = self._reshape(self.to_query(x_query)) / scale
        
        # Create the attention matrix to linearly combine the values.
        # This is multiplying two entries of [b * nh, t, (k * scale_kq) // nh]
        # to get one that is [b * nh, t, t].
        attention = torch.bmm(queries, keys.transpose(-2, -1))
        if self.alibi_bool:
            attention = self.alibi(attention)
        attention = self.mask(attention)
        attention = F.softmax(attention, dim=-1)

        # Attention is at thuis point [b * nh, t, t].
        # reshaped = attention.view(b, nh, t, t)
        # The sum along the last axis, is, because of softmax, 1
        # This means the AVERAGE value of non-zero attention is 1 / t
        # where t is the number of tokens before it.
        x_value = x
        values = self._reshape(self.to_value(x_value))

        # [b * nh, t, t] x [b * nh, t, out_dim // nh] --> [b * nh, t, out_dim // nh].
        output = torch.bmm(attention, values)
        reshaped = output.view(b, nh, t, self.dim // nh)
        reshaped = reshaped.transpose(1, 2).contiguous().view(b, t, self.dim)
        
        # Project to output, [b, t, out_dim] --> [b, t, out_dim]
        return self.proj(reshaped)