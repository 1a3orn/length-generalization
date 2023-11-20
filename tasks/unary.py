from tasks.unary_utils import swap_alt, unique, rotate_by_n, back_by_index_mod, chunk_parity, half_alphabet, double_other, rot13

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