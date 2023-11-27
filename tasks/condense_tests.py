
from random import randint
from tasks.unary_utils import half_alphabet
from tasks.condense import CONDENSE_OPS, composited
from tasks.condense_classes import Condense

IN_KEY_COND = {
    x[0]: x[1] for x in CONDENSE_OPS
}

def rand_str(leng):
    return [half_alphabet[randint(0, 12)] for _ in range(leng)]

def condense_tests():

    mod = IN_KEY_COND['mod']
    assert mod("a") == ("a", False)
    assert mod("ab") == ("a", False)
    assert mod("abc") == ("a", False)
    assert mod("baa") == ("a", True)
    assert mod("bba") == ("b", True)
    assert mod("bbaa") == ("b", True)
    assert mod("bbaaa") == ("a", True)

    bef = IN_KEY_COND['bef']
    # Either pulls the last element if it doesn't find
    # anything in _every_ fourth element, or pulls the
    # element right after the first instance of every fourth
    assert bef("a") == ("a", False)
    assert bef("ab") == ("b", True)
    assert bef("abc") == ("b", True)
    assert bef("baa") == ("a", True)
    assert bef("bac") == ("c", True)
    assert bef("bbbbbbac") == ("c", True)

    ind = IN_KEY_COND['ind']
    assert ind("a") == ("a", True)
    assert ind("cba") == ("c", True)
    assert ind("bca") == ("b", True)
    assert ind("bcccccccccca") == ("b", True)
    assert ind("bccccccccccb") == ("c", True)
    
    hig = IN_KEY_COND['hig']
    # pulls the highest_indexed character
    assert hig("a") == ("a", True)
    assert hig("cba") == ("c", True)
    assert hig("bca") == ("c", True)
    assert hig("bcga") == ("g", True)

    for cond_key, fnc in CONDENSE_OPS:
        percent_trans = 0
        for _ in range(100):
            seq = rand_str(randint(3, 4))
            seq = "".join(seq)
            _, ops = fnc(seq)
            if ops:
                percent_trans += 1
        print(f"{cond_key} - {percent_trans / 100}")

    composited(['hig'])
    composited(['ind', 'hig'])
    composited(['mod', 'hig'])
    composited(['bef', 'hig', 'ind'])

    c = Condense("hig|ind|hig,ind")
    print(c.vocab())
    print(c.at_len(10))
    b = c.batch({'batch_size': 2, 'ctx_len': 64, 'device': 'cpu'})
    print(b[0])
    print(b[1])
    print(b[2])
    print(c.decode(b[0][0].tolist()))
    print(c.decode(b[1][0][b[2][0].bool()].tolist()))
    #composited(['hig', 'ind', 'bef'])
    


