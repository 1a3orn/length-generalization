import numpy as np
import torch

class AbstractTask:

    def __init__(self):
        pass

    def vocab(self):
        raise NotImplementedError("Implement me!")
    
    def vocab_size(self):
        return len(self.vocab())

    def encode(self, chars: str) -> int:
        v = self.vocab()
        return [ v.index(str(c)) for c in chars ]
    
    def decode(self, ints: list) -> str:
        v = self.vocab()
        return "".join([ v[i] for i in ints ])

    def inner(self, extend=0):
        raise NotImplementedError("Implement me!")

    def one_seq(self, ctx_len: int, extend=0) -> str:
        res = ""
        while len(res) < ctx_len:
            res += self.inner(extend=extend)[0]
        return self.encode(res[:ctx_len])
    
    def batch(self, args: dict, extend=0):
        base = torch.tensor([
            self.one_seq(args['ctx_len'] + 1, extend=extend)
            for _ in range(args['batch_size'])
        ], device=args['device']).int()
        return base[:,:-1], base[:,1:]
    
    def acc(self, extend=0):
        strg, start, end = self.inner(extend=extend)
        strg_start = torch.tensor(self.encode(strg[:start])).unsqueeze(0)
        strg_end = torch.tensor(self.encode(strg[start:end])).unsqueeze(0)
        return strg_start, strg_end
 