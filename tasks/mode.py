from random import randint
from tasks.abstract import AbstractTask

def get_counts(seq):
    return { x: seq.count(str(x)) for x in range(6) }

def is_single_mode(seq):
    counts = get_counts(seq)
    return list(counts.values()).count(max(counts.values())) == 1

class Mode(AbstractTask):

    def __init__(self, test_train_break=10):
        super().__init__()
        self.ttb = test_train_break

    def vocab(self):
        return ['=', 'S', 'E'] + [str(x) for x in range(6)]
    
    def at_len(self, leng: int) -> list:
        seq = "".join([ str(randint(0, 5)) for _ in range(leng) ])
        # while there isn't a most common, keep trying

        while not is_single_mode(seq):
            seq = "".join([ str(randint(0, 4)) for _ in range(leng) ])

        # pull mode from seq
        mode = max(get_counts(seq), key=get_counts(seq).get)

        return f"S{seq}={mode}E"

    def inner(self, extend = 0):
        length = randint(4, self.ttb)
        if extend != 0 and extend is not None:
            length = self.ttb + extend
        result = self.at_len(length)
        index = result.index('=') + 1
        answer_length = len(result) - index - 1
        return result, index, answer_length