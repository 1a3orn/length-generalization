
import string

half_alphabet = list("abcdefghijklm")

def rot13(text):
    # Define the ROT13 translation table
    rot13_trans = str.maketrans(
        string.ascii_lowercase + string.ascii_uppercase,
        string.ascii_lowercase[13:] + string.ascii_lowercase[:13] +
        string.ascii_uppercase[13:] + string.ascii_uppercase[:13]
    )
    if not isinstance(text, str):
        text = "".join(text)
    return list(text.translate(rot13_trans))

def unique(text):
    ret = ""
    for c in text:
        if c not in ret:
            ret += c
    return ret

def swap_alt(text):
    ret = ""
    copied = "".join([c for c in text])
    while len(copied) > 1:
        ret += copied[1] + copied[0]
        copied = copied[2:]
    if len(copied) == 1:
        ret += copied[0]
    return ret

def rotate_by_n(text, n):
    copied = "".join([c for c in text])
    for i in range(n):
        copied = copied[1:] + copied[0]
    return copied

def double_other(text):
    ret = ""
    for i, c in enumerate(text):
        if i % 2 == 0:
            ret += c
        else:
            ret += text[i - 1]
    return ret

def back_by_index_mod(text, mod_amount):
    ret = ""
    indices = half_alphabet
    for i, c in enumerate(text):
        if c not in indices:
            ret += c
        else:
            index = indices.index(c)
            mod = index % mod_amount
            if i - mod >= 0:
                ret += text[i - mod]
    return ret

def chunk_parity(text, chunk_size=2):
    ret = ""
    indices = half_alphabet
    for i in range(0, len(text), chunk_size):
        chunk_chars = text[i:i + chunk_size]
        if not all([c in indices for c in chunk_chars]):
            ret += "".join(chunk_chars)
        chunk_indices = [indices.index(c) for c in chunk_chars]
        total = sum(chunk_indices)
        ret += "".join([ indices[indices.index(x) - total] for x in chunk_chars ])

    return ret

UNARY_TASKS = [
    ('reverse', lambda x: x[::-1]),
    ('swap_alt', swap_alt),
    ('trim', lambda y: "".join([x for x in list(y)[2:-2]])),
    ('rot13', rot13),
    ('rot_by_4', lambda s: rotate_by_n(s, 4)),
    ('unique', unique),
    ('back_by_index', lambda s: back_by_index_mod(s, 3)),
    ('chunk_parity', chunk_parity),
     #('double_other', double_other),
    #('sort', sort),
]

if __name__ == "__main__":
    print(",".join(list(map(lambda x: "unary_" + x[0], UNARY_TASKS))))