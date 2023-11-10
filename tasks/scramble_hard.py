from random import randint, shuffle
from tasks.abstract import AbstractTask

def random_char_one(n):
    return "".join("abcdefghijklmnopqrs"[randint(0, 18)] for _ in range(n))

class ScrambleHard(AbstractTask):

    def __init__(self, shuffles_base=1):
        super().__init__()
        self.shuffles_base = shuffles_base

    def vocab(self):
        return list('abcdefghijklmnopqr1234567890SE.#=\n')
    
    def at_len(self, shuffles: int) -> list:
        leng = 2
        sep = "\n"
        to_peel = list('abcdefghijklmnopqr')
        shuffle(to_peel)
        def peel():
            char = to_peel.pop()
            return char

        random_vars = [peel() for _ in range(leng)]
        assignments = {var: str(randint(1, 9)) for var in random_vars}
        while len(set(assignments.values())) < len(assignments):
            assignments = {var: str(randint(1, 9)) for var in random_vars}

        initial_code_lst = [ f"{var}={val}" for var, val in assignments.items()]
        shuffle(initial_code_lst)
        init_r_vars = [var[0] for var in initial_code_lst]
        initial_code = sep.join(initial_code_lst)

        # Generate reassignments
        reassign_code = ""
        for _ in range(shuffles):
            new_vars = [peel() for _ in range(leng)]
            assignments = {
                new_vars[i]: assignments[random_vars[i]]
                for i
                in range(len(random_vars))
            }
            rsc = [f"{var2}={var1}" for var1, var2 in zip(random_vars, new_vars)]
            shuffle(rsc)
            reassign_code += sep.join(rsc) + sep
            random_vars = new_vars

        # Generate print statements
        var_index = randint(0, len(random_vars) - 1)
        rand_var = random_vars[var_index]
        rv = rand_var
        rv_ass = assignments[rv]
        print_code = f"{rv}#{rv_ass}"

        return f"S{initial_code}{sep}{reassign_code}{print_code}E"
    
    def inner(self, extend=0):
        # doesn't use extend
        leng = self.shuffles_base
        strng = self.at_len(leng)
        index = strng.index('#') + 1
        return strng, index, 1