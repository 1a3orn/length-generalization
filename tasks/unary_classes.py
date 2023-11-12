from random import randint
from tasks.unary import UNARY_TASKS
from tasks.abstract import AbstractTask

IN_KEY = {
    x[0]: x[1] for x in UNARY_TASKS
}

alpha = list("abcdefghijklmnopqrstuvwxyz")
half_alpha = list("abcdefghijklm")
def rand_str(leng):
    return [half_alpha[randint(0, 12)] for _ in range(leng)]

class Unary(AbstractTask):

    def __init__(self, keys=None, ttb=12):
        super().__init__()
        self.ttb = ttb

        for key in keys:
            if key not in IN_KEY:
                raise ValueError(f"key {key} not found in {IN_KEY.keys()}")

        if keys is None:
            raise ValueError("key must be specified")
        else:
            def fnc(seq):
                for key in keys:
                    seq = IN_KEY[key](seq)
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
    