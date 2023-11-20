from random import randint
from tasks.unary import UNARY_TASKS


def unary_tests():

    lowercase = "abcdefghi"
    def rand_str(length):
        return "".join([lowercase[randint(0, len(lowercase) - 1)] for _ in range(length)])
    
    rand_strings = [rand_str(randint(6, 8)) for _ in range(25)]

    for name, func in UNARY_TASKS:
        print(f"Testing {name}...")

        number_changes = 0
        for s in rand_strings:
             if func(s) != s:
                 number_changes += 1
             print(f"{s} -> {func(s)}")

        print(f"{name} changed {number_changes} out of {len(rand_strings)} strings")

        FILTERED = [x for x in UNARY_TASKS if x[0] != name]

        # Make sure we don't undo the work of other functions
        for other_name, other_func in FILTERED:
            number_changes = 0
            for s in rand_strings:
                one = func(other_func(s)) != s
                two = other_func(func(s)) != s
                thr = func(other_func(s)) != other_func(s)
                fou = func(other_func(s)) != func(s)
                if one and two and thr and fou:
                    number_changes += 1
            print(f"{name} changed {number_changes} out of {len(rand_strings)} strings after {other_name}")




if __name__ == "__main__":
    unary_tests()