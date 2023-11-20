
import string

half_alphabet = list("abcdefghijklm")

def rot13(text):
    # Define the ROT13 translation table
    half_alpha = list("abcdefghijklm")
    if not isinstance(text, str):
        text = "".join(text)
    return [
        half_alpha[(half_alpha.index(c) + 13) % 13] if c in half_alpha else c
        for c in text
    ]

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
