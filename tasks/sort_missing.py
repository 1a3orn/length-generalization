from random import randint
from tasks.abstract import AbstractTask

class SortMissing(AbstractTask):

    def __init__(self, missing_range=[55, 59]):
        super().__init__()
        self.leng = 5
        self.mr = missing_range

    def vocab(self):
        return ['S', 'e', 'E', ','] + [str(x) for x in range(10)]
    
    def seq(self, leng, train: bool=False) -> list:
        mr = self.mr
        seq_scrambled = [ randint(1, 99) for _ in range(leng) ]
        if train:
            while any([x in seq_scrambled for x in range(mr[0], mr[1])]):
                seq_scrambled = [ randint(1, 99) for _ in range(leng) ]
        else:
            while not any([x in seq_scrambled for x in range(mr[0], mr[1])]):
                seq_scrambled = [ randint(1, 99) for _ in range(leng) ]
        seq = ['S'] + [",".join([ str(x) for x in seq_scrambled ])] + ['e']
        seq = seq + [",".join([ str(x) for x in sorted(seq_scrambled) ])] + ['E']
        return "".join(seq)

    def inner(self, extend=0):
        start = 2
        end = self.leng
        if extend != 0: 
            start = self.leng + extend
            end = self.leng + extend
        result = self.seq(randint(start, end), train=extend==0)
        index = result.index('e') + 1
        answer_length = len(result) - index - 1
        return result, index, answer_length
  