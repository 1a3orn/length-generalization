from random import random, randint
from tasks.abstract import AbstractTask

def check_if_balanced(seq):
    stack = 0
    for char in seq:
        if char == '(':
            stack += 1
        elif char == ')':
            stack -= 1
        if stack < 0:
            return False
    return stack == 0

class BalanceParens(AbstractTask):

    def __init__(self, test_train_break=10):
        super().__init__()
        self.ttb = test_train_break

    def vocab(self):
        return ['(', ')', '#', '.', 'g', 'b', 'S', 'E']
    
    def at_len(self, leng: int) -> list:
        stack = 0
        seq = []
        # Make a balanced paren sequence, randomly including
        # the # as filler on 1/3 the rows, or if necessary to
        # balance the parens for the length
        success = False
        while not success:
            seq = []
            stack = 0
            for _ in range(leng):
                if stack + _ > leng:
                    seq.append(')')
                    stack += 1
                if stack == 0 and random() < 0.33:
                    seq.append('#')
                else:
                    if stack > 0:
                        seq.append('(' if random() < 0.5 else ')')
                        stack += 1 if seq[-1] == '(' else -1
                    else:
                        seq.append('(')
                        stack += 1
            success = stack == 0
        balanced = random() < 0.5
        seq.append('.')
        # if not balanced, randomly switch a paren
        if not balanced:
            index = randint(0, leng - 1)
            seq[index] = ')' if seq[index] == '(' else '('
        if balanced:
            assert check_if_balanced(seq)
        seq.append('g' if balanced else 'b')
        seq = seq + ['E']
        return "S" + "".join(seq)

    def inner(self, extend = 0):
        start = 2
        end = self.ttb
        if extend != 0 and extend is not None:
            start = self.ttb + extend
            end = self.ttb + extend
        chosen_length = randint(start, end)
        result = self.at_len(chosen_length)
        index = result.index('.') + 1
        answer_length = len(result) - index - 1
        return result, index, answer_length
  