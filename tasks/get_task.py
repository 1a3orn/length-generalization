
from tasks.math_mult import MathMult
from tasks.math_add import MathAdd
from tasks.math_mult_reverse import MathMultReverse
from tasks.math_add_reverse import MathAddReverse
from tasks.parity_sum import ParitySum
from tasks.parity_count import ParityCount
from tasks.sort_len import SortLen
from tasks.sort_len_twodigit import SortLenTwodigit
from tasks.sort_missing import SortMissing
from tasks.copy_len import CopyLen
from tasks.copy_len_rep import CopyLenRep
from tasks.copy_len_unique import CopyLenUnique
from tasks.balance_parens import BalanceParens
from tasks.reverse import Reverse
from tasks.pattern_indices import PatternIndices
from tasks.pattern_repeats import PatternRepeats
from tasks.count import Count
from tasks.mode import Mode
from tasks.mode_hard import ModeHard
from tasks.scramble import Scramble
from tasks.scramble_hard import ScrambleHard
from tasks.unary_classes import Unary


def get_task(task_name: str) -> object:
    if task_name == "count":
        return Count()
    elif task_name == "mode":
        return Mode()
    elif task_name == "mode_hard":
        return ModeHard()
    elif task_name == "math_mult":
        return MathMult()
    elif task_name == "math_add":
        return MathAdd()
    elif task_name == "math_mult_reverse":
        return MathMultReverse()
    elif task_name == "math_add_reverse":
        return MathAddReverse()
    elif task_name == "pattern_indices":
        return PatternIndices()
    elif task_name == "pattern_repeats":
        return PatternRepeats()
    if task_name == "parity_sum":
        return ParitySum()
    elif task_name == "parity_count":
        return ParityCount()
    elif task_name == "sort_len":
        return SortLen()
    elif task_name == "sort_len_twodigit":
        return SortLenTwodigit()
    elif task_name == "sort_missing":
        return SortMissing()
    elif task_name == "copy_len":
        return CopyLen()
    elif task_name == "copy_len_rep":
        return CopyLenRep()
    elif task_name == "copy_len_unique":
        return CopyLenUnique()
    elif task_name == "balance_parens":
        return BalanceParens()
    elif task_name == "reverse":
        return Reverse()
    elif task_name == "scramble_0":
        return Scramble(0)
    elif task_name == "scramble_1":
        return Scramble(1)
    elif task_name == "scramble_2":
        return Scramble(2)
    elif task_name == "scramble_3":
        return Scramble(3)
    elif task_name == "scramble_hard_0":
        return ScrambleHard(0)
    elif task_name == "scramble_hard_1":
        return ScrambleHard(1)
    elif task_name == "scramble_hard_2":
        return ScrambleHard(2)
    elif task_name.startswith("unary_"):
        to_split = task_name[6:]
        print("Trying to make unary task with", to_split)
        split = to_split.split("X")
        return Unary(keys=split)

    else:
        raise ValueError(f"Unknown task: {task_name}")