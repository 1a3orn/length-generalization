from random import randint
from tasks.abstract import AbstractTask

class SortLen(AbstractTask):

    def __init__(self, test_train_break=8):
        super().__init__()
        self.ttb = test_train_break

    def vocab(self):
        return ['S', 'e', 'E'] + [str(x) for x in range(10)]
    
    def at_len(self, leng: int) -> list:
        seq_scrambled = [ randint(0, 9) for _ in range(leng) ]
        seq = ['S'] + [ str(x) for x in seq_scrambled ] + ['e']
        seq = seq + [ str(x) for x in sorted(seq_scrambled) ] + ['E']
        return "".join(seq)

    def inner(self, extend = 0):
        start = 2
        end = self.ttb
        if extend != 0: 
            start = self.ttb + extend - 1
            end = self.ttb + extend
        result = self.at_len(randint(start, end))
        index = result.index('e') + 1
        return result, index, len(result)
  