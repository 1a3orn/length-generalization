from random import randint
from tasks.abstract import AbstractTask

class SortLenTwodigit(AbstractTask):

    def __init__(self):
        super().__init__()
        self.leng = 5

    def vocab(self):
        return ['S', 'e', 'E', ','] + [str(x) for x in range(10)]
    
    def seq(self, leng: int) -> list:
        seq_scrambled = [ randint(1, 99) for _ in range(leng) ]
        seq = ['S'] + [",".join([ str(x) for x in seq_scrambled ])] + ['e']
        seq = seq + [",".join([ str(x) for x in sorted(seq_scrambled) ])] + ['E']
        return "".join(seq)

    def inner(self, extend=0):
        start = 2
        end = self.leng
        if extend != 0: 
            start = self.leng + extend - 1
            end = self.leng + extend
        result = self.seq(randint(start, end))
        index = result.index('e') + 1
        return result, index, len(result)