from random import randint
from tasks.unary_if import UNARY_COND_OP, UNARY_TRANS_OP

lowercase = "abcdefghi"
def rand_str(length):
    return "".join([lowercase[randint(0, len(lowercase) - 1)] for _ in range(length)])
    
def unary_if_tests():

    for cond_name, cond_func in UNARY_COND_OP:

        times_true = 0
        for i in range(100):

            strg = rand_str(randint(6, 12))
            if cond_func(strg):
                times_true += 1
        print(f"{cond_name} was true {times_true} out of 100 times")



        
    
