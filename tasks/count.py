from random import randint
from tasks.abstract import AbstractTask

class Count(AbstractTask):

    def __init__(self, test_train_break=6):
        super().__init__()
        self.ttb = test_train_break

    def vocab(self):
        return ['=', 'S', ',', 'E'] + [str(x) for x in range(10)]
    
    def at_len(self, start: int, to: int) -> list:
        seq = ",".join([ str(_) for _ in range(start, to + 1) ])
        return f"S{start},{to}={seq}E"

    def inner(self, extend = 0):
        length = randint(2, self.ttb)
        if extend != 0 and extend is not None:
            length = self.ttb + extend
        start = randint(0, 99 - length)
        result = self.at_len(start, start + length)
        index = result.index('=') + 1
        chosen_length = len(result) - index - 1
        return result, index, chosen_length