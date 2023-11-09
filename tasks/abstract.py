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
        mask = []
        while len(res) < ctx_len:
            strg, start, ln = self.inner(extend=extend)
            res += strg
            total_leng = len(strg)
            mask += [0] * start + [1] * ln + [0] * (total_leng - start - ln)
        return self.encode(res[:ctx_len]), mask[:ctx_len]
    
    def batch(self, args: dict, extend=0):
        base_l = []
        mask_l = []
        for _ in range(args['batch_size']):
            res_one, mask_one = self.one_seq(args['ctx_len'] + 1, extend=extend)
            base_l.append(res_one)
            mask_l.append(mask_one)
        base = torch.tensor(base_l, device=args['device']).int()
        mask = torch.tensor(mask_l, device=args['device']).int()
        return base[:,:-1], base[:,1:], mask[:,1:]
    
    def acc(self, extend=0):
        strg, start, end = self.inner(extend=extend)
        strg_start = torch.tensor(self.encode(strg[:start])).unsqueeze(0)
        strg_end = torch.tensor(self.encode(strg[start:end])).unsqueeze(0)
        return strg_start, strg_end
 