from random import randint, shuffle
from tasks.abstract import AbstractTask

def random_char_one(n):
    return "".join("abcdefghijklmnopqrs"[randint(0, 18)] for _ in range(n))

class Scramble(AbstractTask):

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
            return to_peel.pop()
        
        def rs():
            return "".join(["." for _ in range(randint(0, 3))])

        random_vars = [peel() for _ in range(leng)]
        assignments = {var: str(randint(1, 9)) for var in random_vars}
        while len(set(assignments.values())) < len(assignments):
            assignments = {var: str(randint(1, 9)) for var in random_vars}

        initial_code_lst = [ f"{var}={val}{rs()}" for var, val in assignments.items()]
        shuffle(initial_code_lst)
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
            rsc = [f"{var2}={var1}{rs()}" for var1, var2 in zip(random_vars, new_vars)]
            shuffle(rsc)
            reassign_code += sep.join(rsc) + sep
            random_vars = new_vars

        # Generate print statements
        var_index = randint(0, len(random_vars) - 1)
        rand_var_1 = random_vars[var_index]
        print_code_1 = f"{rand_var_1}#{assignments[rand_var_1]}"
        rand_var_2 = random_vars[1 - var_index]
        print_code_2 = f"{rand_var_2}#{assignments[rand_var_2]}"
        print_code = sep.join([print_code_1, print_code_2])

        return f"S{initial_code}{sep}{reassign_code}{print_code}E"
    
    def inner(self, extend=0):
        # doesn't use extend
        leng = self.shuffles_base
        strng = self.at_len(leng)
        index = strng.index('#') + 1
        return strng, index, len(strng)