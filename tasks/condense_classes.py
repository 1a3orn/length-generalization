from random import randint
from tasks.condense import CONDENSE_OPS, composited
from tasks.abstract import AbstractTask

half_alpha = list("abcdefghijklm")

CONDENSE_OPS_KEYS = [x[0] for x in CONDENSE_OPS]

class Condense(AbstractTask):

    def __init__(self, key_str):
        super().__init__()

        split_pipe = key_str.split("|")

        keys = []
        for composite_str in split_pipe:
            keys_inner = composite_str.split(",")
            for key in keys_inner:
                if key not in CONDENSE_OPS_KEYS:
                    raise ValueError(f"key {key} not found in {CONDENSE_OPS_KEYS}")
            keys.append(keys_inner)

        self.keys = keys
        self.separators = ["1", "2", "3", "4", "5", "6"][:len(self.keys)]

    def vocab(self):
        return ['S', 'E', '.', ":"] + half_alpha + self.separators
    
    def at_len(self, leng: int) -> list:
        keys_ind = randint(0, len(self.keys) - 1)
        keys = self.keys[keys_ind]
        comp = composited(keys)
        sep = self.separators[keys_ind]
        pattern = sep + comp["all_text"] + ":" + comp["output"] + sep
        return pattern

    def inner(self, extend = 0):
        result = self.at_len(0)
        index = result.index(':') + 1
        answer_length = 1
        return result, index, answer_length
    