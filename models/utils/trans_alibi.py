import torch
import torch.nn as nn
 
def get_relative_positions(seq_len: int) -> torch.tensor:
    x = torch.arange(seq_len)[None, :]
    y = torch.arange(seq_len)[:, None]
    return x - y

class AlibiEncoding(nn.Module):
    '''
    Create a mask which can be used
    to zero out the attention of the
    future tokens.
    '''
    def __init__(self, max_seq_length, n_heads):
        super(AlibiEncoding, self).__init__()
        msl = max_seq_length
        self.max_seq_length = max_seq_length
        self.n_heads = n_heads
        # Get [t, t] matrix of relative positions.
        relative = get_relative_positions(msl)
        # Move dim to be [n_heads, t, t]
        increased = torch.tile(relative, [n_heads, 1, 1])
        # scale for different heads
        scaler = (1 / torch.pow(torch.arange(1, n_heads + 1), 2)).unsqueeze(1).unsqueeze(2)
        scaled = (increased * scaler) / 8.0
        #print("scaled", scaled.size())
        self.register_buffer("alibi", scaled)

    def forward(self, attention):
        # This code should work with [b * num_heads, t, t]
        sizes = attention.size()
        t1, t2 = sizes[-2:]
        assert t1 == t2, "attention must be square"
        assert t1 <= self.max_seq_length, "attention must be smaller than max_seq_length"
        reshaped_att = attention.view(-1, self.n_heads, t1, t1)
        return (reshaped_att + self.alibi[:,:t1,:t1]).view([-1, t1, t1])
