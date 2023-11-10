from random import randint
from tasks.abstract import AbstractTask

class MathAddReverse(AbstractTask):

    def __init__(self, test_train_break=4):
        super().__init__()
        self.ttb = test_train_break

    def vocab(self):
        return list('1234567890+=SE')
    
    def at_len(self, fst: int, snd: int) -> list:
        fst_rev = "".join(reversed(str(fst)))
        snd_rev = "".join(reversed(str(snd)))
        answer = "".join(reversed(str(fst + snd)))
        return f"S{fst_rev}+{snd_rev}={answer}E"
    
    def inner(self, extend=0):
        first_mult = randint(1, randint(10, 10 ** self.ttb))
        second_mult = randint(1, randint(10, 10 ** self.ttb))
        if extend != 0:
            second_mult = randint(10 ** (extend + self.ttb - 1), 10 ** (extend + self.ttb))
        strng = self.at_len(first_mult, second_mult)
        index = strng.index('=') + 1
        answer_length = len(strng) - index - 1
        return strng, index, answer_length