from random import randint
from tasks.abstract import AbstractTask

class MathAdd(AbstractTask):

    def __init__(self, test_train_break=4):
        super().__init__()
        self.ttb = test_train_break

    def vocab(self):
        return list('1234567890+=SE')
    
    def at_len(self, fst: int, snd: int) -> list:
        return f"S{fst}+{snd}={fst + snd}E"
    
    def inner(self, extend=0):
        first_mult = randint(1, randint(10, 10 ** self.ttb))
        second_mult = randint(1, randint(10, 10 ** self.ttb))
        if extend != 0:
            second_mult = randint(10 ** (extend + self.ttb - 1), 10 ** (extend + self.ttb))
        strng = self.at_len(first_mult, second_mult)
        index = strng.index('=') + 1
        return strng, index, len(strng)