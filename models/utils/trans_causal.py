import torch
import torch.nn as nn
 
class CausalMask(nn.Module):
    '''
    Create a mask which can be used
    to zero out the attention of the
    future tokens.
    '''
    def __init__(self, max_seq_length):
        super(CausalMask, self).__init__()
        msl = max_seq_length
        self.max_seq_length = max_seq_length
        # The use of torch.tril is to create a triangular matrix
        # with zeros above the diagonal.
        # >>> a = torch.randn(3, 3)
        # >>> a
        # tensor([[-0.0491,  0.0491, -0.0491],
        #         [ 0.0491,  0.0491,  0.0491],
        #         [-0.0491,  0.0491,  0.0491]])
        # >>> torch.tril(a)
        # tensor([[ -0.0491,  0.0000,  0.0000],
        #         [  0.0491,  0.0491,  0.0000],
        #         [  0.0491,  0.0491,  0.0491]])
        #print("msl", msl)
        self.register_buffer("mask", torch.tril(torch.ones(msl, msl)))

    def forward(self, attention):
        # This coat should be able to handle
        # attention with either three or four dimensions
        # [b, t, t] or [b, num_heads, t, t], respectively,
        # because of broadcasting
        sizes = attention.size()
        t1, t2 = sizes[-2:]
        assert t1 == t2, "attention must be square"
        assert t1 <= self.max_seq_length, "attention must be smaller than max_seq_length"

        return attention.masked_fill(self.mask[:t1,:t1] == 0, float('-inf'))
