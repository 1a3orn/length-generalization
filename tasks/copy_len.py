from random import randint
from tasks.abstract import AbstractTask

class CopyLen(AbstractTask):

    def __init__(self, test_train_break=10):
        super().__init__()
        self.ttb = test_train_break

    def vocab(self):
        return ['S', 'E', '='] + [str(x) for x in range(10)]
    
    def at_len(self, leng: int) -> list:
        seq_scrambled = [ str(randint(0, 9)) for _ in range(leng) ]
        seq = ['S'] + seq_scrambled + ['=']
        seq = seq + seq_scrambled + ['E']
        return "".join(seq)

    def inner(self, extend = 0):
        start = 3
        end = self.ttb
        if extend != 0 and extend is not None:
            start = self.ttb + extend
            end = self.ttb + extend
        chosen_length = randint(start, end)
        result = self.at_len(chosen_length)
        index = result.index('=') + 1
        answer_length = len(result) - index - 1
        return result, index, answer_length
  