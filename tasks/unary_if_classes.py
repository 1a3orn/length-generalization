from random import randint
from tasks.unary_if import UNARY_COND_OP, UNARY_TRANS_OP, combiner
from tasks.abstract import AbstractTask

IN_KEY_COND = {
    x[0]: x[1] for x in UNARY_COND_OP
}
IN_KEY_TRANS = {
    x[0]: x[1] for x in UNARY_TRANS_OP
}

half_alpha = list("abcdefghijklm")
def rand_str(leng):
    return [half_alpha[randint(0, 12)] for _ in range(leng)]

class UnaryIf(AbstractTask):

    def __init__(self, keys=None, ttb=12):
        super().__init__()
        self.ttb = ttb

        for cond_key, trans_key in keys:
            if cond_key not in IN_KEY_COND:
                raise ValueError(f"key {cond_key} not found in {IN_KEY_COND.keys()}")
            if trans_key not in IN_KEY_TRANS:
                raise ValueError(f"key {trans_key} not found in {IN_KEY_TRANS.keys()}")
            

        if keys is None:
            raise ValueError("key must be specified")
        else:
            def fnc(seq):
                for cond_key, trans_key in keys:
                    seq = combiner(trans_key, cond_key)(seq)
                return seq

            self.transform = fnc

    def vocab(self):
        return ['S', 'E', '='] + half_alpha
    
    def at_len(self, leng: int) -> list:
        seq_scrambled = rand_str(leng)
        seq = ['S'] + seq_scrambled + ['=']
        seq = seq + list(self.transform(seq_scrambled)) + ['E']
        return "".join(seq)

    def inner(self, extend = 0):
        start = 6
        end = self.ttb
        if extend != 0 and extend is not None:
            start = self.ttb + extend
            end = self.ttb + extend
        chosen_length = randint(start, end)
        result = self.at_len(chosen_length)
        index = result.index('=') + 1
        answer_length = len(result) - index - 1
        return result, index, answer_length
    