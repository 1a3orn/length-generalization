from random import randint
from tasks.abstract import AbstractTask

class CopyLenUnique(AbstractTask):

    def __init__(self, test_train_break=10):
        super().__init__()
        self.ttb = test_train_break

    def vocab(self):
        return ['S', 'E', '='] + [str(x) for x in range(8)]
    
    def at_len(self, leng: int) -> list:
        seq_scrambled = [ str(randint(0, 7)) for _ in range(leng) ]
        seq = ['S'] + seq_scrambled + ['=']
        # get seq_scrambeled, just unique elements in order
        found = []
        for x in seq_scrambled:
            if x not in found:
                found.append(x)
        seq = seq + found + ['E']
        return "".join(seq)

    def inner(self, extend = 0):
        start = 3
        end = self.ttb
        if extend != 0 and extend is not None:
            start = self.ttb
            end = self.ttb + extend
        result = self.at_len(randint(start, end))
        index = result.index('=') + 1
        return result, index, len(result)