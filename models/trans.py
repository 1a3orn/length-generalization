import torch
from torch import nn
from torch.nn import functional as F

from models.utils.trans_mha import MultiHeadAttention

class TransformerBlock(nn.Module):
    '''
    A transformer block consists of a self-attention layer,
    two layer norms, and a dimension-wise standard transform
    '''
    def __init__(self, config):
        super(TransformerBlock, self).__init__()
        self.dim = dim = config['hidden_dim']
        self.expand_proportion = 4

        self.attention = MultiHeadAttention(config, alibi=False)
        self.layer_norm1 = nn.LayerNorm(dim)
        self.layer_norm2 = nn.LayerNorm(dim)

        self.ff1 = nn.Sequential(
            nn.Linear(dim, round(dim * self.expand_proportion)),
            nn.ReLU(),
            nn.Linear(round(dim * self.expand_proportion), dim),
        )

    def forward(self, x):
        x = x + self.attention(self.layer_norm1(x))
        x = x + self.ff1(self.layer_norm2(x))
        return x
    
class Transformer(nn.Module):
    '''
    A transformer consists of a stack of transformer blocks
    '''
    def __init__(self, config):
        super(Transformer, self).__init__()
        self.dim = dim = config['hidden_dim']
        self.num_layers = num_layers = config['num_layers']
        self.embd = nn.Embedding(config['vocab_size'], dim)
        self.pos_embd = nn.Embedding(config['ctx_len'], dim)
        self.transformer_blocks = nn.ModuleList([
            TransformerBlock(config)
            for _ in range(num_layers)
        ])
        self.layer_norm = nn.LayerNorm(dim)
        self.output = nn.Linear(dim, config['vocab_size'])

    def forward(self, x):
        xx = self.embd(x)
        xxx = self.pos_embd(torch.arange(x.size(1), device=x.device))[None, :, :]
        x = xx + xxx
        for block in self.transformer_blocks:
            x = block(x)
        return self.output(self.layer_norm(x))
    
    def generate(self, x, n_tokens):
        '''
        Generate n_tokens after x
        '''
       
        out_tokens = []
        for _ in range(n_tokens):
            x = x.int()
            out = self.forward(x)
            last_token = out[:, -1, :]
            max_token = torch.argmax(last_token, dim=-1)
            out_tokens.append(max_token)
            x = torch.cat([x, max_token.view(1, 1)], dim=1)

        return torch.stack(out_tokens, dim=1)
            