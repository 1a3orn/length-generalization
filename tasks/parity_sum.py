from random import randint
from tasks.abstract import AbstractTask

class ParitySum(AbstractTask):

    def __init__(self, test_train_break=15):
        super().__init__()
        self.ttb = test_train_break

    def vocab(self):
        return ['0', '1', '.', 'e', 'o', 'S', 'E']
    
    def at_len(self, leng: int) -> list:
        seq = ['S'] + [
            ['0', '1'][randint(0, 1)]
            for _ in range(leng)
        ]
        total = sum([1 for x in seq if x == '1'])
        seq.append('.')
        seq.append('e' if total % 2 == 0 else 'o')
        seq.append('E')
        return "".join(seq)
    
    def inner(self, extend = 0):
        start = 2
        end = self.ttb
        if extend != 0:
            start = self.ttb + extend
            end = self.ttb + extend
        result = self.at_len(randint(start, end))
        index = result.index('.') + 1
        answer_length = len(result) - index - 1
        return result, index, answer_length

  