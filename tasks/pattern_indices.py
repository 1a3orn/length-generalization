from random import randint, choice
from tasks.abstract import AbstractTask

class PatternIndices(AbstractTask):

    def __init__(self):
        super().__init__()

    def vocab(self):
        return list('abcdef1234567890.=SE')
    
    def at_len(self, leng: int) -> list:
        vocab_leng = randint(2, max(2, leng))
        vocab = [ choice(list('abcdef')) for _ in range(vocab_leng)]
        pattern = [ randint(0, len(vocab) - 1) for _ in range(leng) ]
        result = [ vocab[i] for i in pattern ]
        vocab_str = ''.join(vocab)
        pattern_str = ''.join([str(x) for x in pattern])
        output_str = ''.join(result)
        return f"S{vocab_str}.{pattern_str}={output_str}E"
    
    def inner(self, extend=0):
        leng = randint(4, 8)
        if extend != 0:
            leng = 8 + extend
        strng = self.at_len(leng)
        index = strng.index('=') + 1
        answer_length = len(strng) - index - 1
        return strng, index, answer_length