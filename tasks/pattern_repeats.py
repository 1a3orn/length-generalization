from random import randint, choice
from tasks.abstract import AbstractTask

class PatternRepeats(AbstractTask):

    def __init__(self):
        super().__init__()

    def vocab(self):
        return list('abcdefghi1234567890.=SE')
    
    def at_len(self, leng: int) -> list:
        vocab = [ choice(list('abcdef')) for _ in range(leng)]
        repea = [ randint(0, len(vocab) - 1) for _ in range(leng) ]
        result = [ "".join([vocab[index] for _ in range(rep)]) for index, rep in enumerate(repea) ]
        vocab_str = ''.join(vocab)
        repea_str = ''.join([str(x) for x in repea])
        output_str = ''.join(result)
        return f"S{vocab_str}.{repea_str}={output_str}E"
    
    def inner(self, extend=0):
        leng = randint(2, 5)
        if extend != 0:
            leng = 5 + extend
        strng = self.at_len(leng)
        index = strng.index('=') + 1
        return strng, index, len(strng)