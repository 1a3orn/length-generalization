from tasks.unary_utils import swap_alt, unique, rotate_by_n, back_by_index_mod, chunk_parity, half_alphabet, rot13


# unary_if holds functions that
# - take a string as input
# - return a string as output
# - involve some conditional branching
#   depending on the input string
every_other_half_alpha = half_alphabet[::2]

def starts_with_half_alpha(text):
    return text[0] in every_other_half_alpha

def ends_with_half_alpha(text):
    return text[-1] in every_other_half_alpha

def odd_length(text):
    return len(text) % 2 == 1

def has_repeating_elements(text):
    for i, c in enumerate(text):
        if i > 0 and c == text[i - 1]:
            return True
    return False
    
def contains_incrementing(text):
    for i, c in enumerate(text):
        if i > 0 and half_alphabet.index(c) == half_alphabet.index(text[i - 1]) + 1:
            return True
    return False

def first_two_characters_sorted(text):
    return text[:2] == "".join(sorted(text[:2]))

UNARY_COND_OP = [
    ('starts_with_half_alpha', starts_with_half_alpha),
    ('ends_with_half_alpha', ends_with_half_alpha),
    ('odd_length', odd_length),
    ('has_repeating_elements', has_repeating_elements),
    ('contains_incrementing', contains_incrementing),
    ('first_two_characters_sorted', first_two_characters_sorted),
]

UNARY_TRANS_OP = [
    ('reverse', lambda x: x[::-1]),
    ('swap_alt', swap_alt),
    ('trim', lambda y: "".join([x for x in list(y)[2:-2]])),
    ('rot13', rot13),
    ('rot_by_4', lambda s: rotate_by_n(s, 4)),
    ('unique', unique),
    ('back_by_index', lambda s: back_by_index_mod(s, 3)),
    ('chunk_parity', chunk_parity),
]

def combiner(trans_name, cond_name):
    cond = [x[1] for x in UNARY_COND_OP if x[0] == cond_name][0]
    trans = [x[1] for x in UNARY_TRANS_OP if x[0] == trans_name][0]
    def combined(text):
        if cond(text):
            return trans(text)
        else:
            return text
    return combined

