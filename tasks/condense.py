import json
from random import randint, random
from tasks.unary_utils import half_alphabet

def mode(text):
    if len(text) == 0:
        raise ValueError("Cannot take mode of empty string")
    if len(text) == 1:
        return text, False
    counts = {}
    max_dirty = False
    max_count = 0
    max_char = text[0]
    for c in text:
        if c not in counts:
            counts[c] = 0
        counts[c] += 1
        if counts[c] > max_count:
            max_count = counts[c]
            max_char = c
            if counts[c] > 1:
                max_dirty = True
    return max_char, max_dirty

def before(text):
    every_fourth = half_alphabet[::4]
    for i, c in enumerate(text):
        if i > 0 and text[i - 1] in every_fourth:
            return c, True
    return text[-1], False

def index(text):
    indexable = text[-1]
    index = half_alphabet.index(indexable) % 3
    return text[index % len(text)], True

def highest_indexed(text):
    highest_index = 0
    highest_char = text[0]
    for c in text:
        index = half_alphabet.index(c)
        if index > highest_index:
            highest_index = index
            highest_char = c
    return highest_char, True

def rand_str(leng):
    return "".join([half_alphabet[randint(0, 12)] for _ in range(leng)])

CONDENSE_OPS = [
    ('mod', mode),
    ('bef', before),
    ('ind', index),
    ('hig', highest_indexed),
]

IN_KEY_COND = {
    x[0]: x[1] for x in CONDENSE_OPS
}

def composited(
        ops,
        len_gen=lambda: randint(3, 5) if random() > 0.8 else randint(3, 4),
        rand_gen=rand_str,
        separator="."):

    # make_stk(1): 3
    # make_stk(2): [3, 4, 2]
    # make_stk(3): [[3, 3, 4],[2, 3, 4],[3, 3, 4]]
    def make_stk(depth):
        if depth == 1:
            return len_gen()
        return [make_stk(depth - 1) for _ in range(len_gen())]

    def get_output(ops, stack):
        ops_fnc = [IN_KEY_COND[op] for op in ops]
        def inner(stack_inner, depth):
            if depth==1:
                assert isinstance(stack_inner, int)
                text = rand_gen(stack_inner)
                output, _ = ops_fnc[-depth](text)
                return {
                    "text": text,
                    "all_text": text,
                    "output": output
                }
            else:
                assert isinstance(stack_inner, list)
                below = [
                    inner(stack_inner[i], depth - 1)
                    for i
                    in range(len(stack_inner))
                ]
                level_sep = separator * (depth - 1)
                all_text = level_sep.join([x["all_text"] for x in below])
                text = "".join([x["output"] for x in below])
                output, _ = ops_fnc[-depth](text)
                return {
                    "text": text,
                    "all_text": all_text,
                    "output": output
                }

        a = inner(stack, len(ops))
        #print(a)
        return a
    
    return get_output(ops, make_stk(len(ops)))
    