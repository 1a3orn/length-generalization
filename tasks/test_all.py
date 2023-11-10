import sys
from pathlib import Path
parent_dir = str(Path(__file__).resolve().parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from tasks.get_task import get_task

tasks = [
    "reverse",
    "math_mult",
    "math_add",
    "math_mult_reverse",
    "math_add_reverse",
    "copy_len",
    "copy_len_rep",
    "copy_len_unique",
    "balance_parens",
    "count",
    "mode",
    "mode_hard",
    "sort_len",
    "sort_len_twodigit",
    "sort_missing",
    "scramble_0",
    "scramble_1",
    "scramble_2",
    "pattern_indices",
    "pattern_repeats",
    "scramble_hard_0",
    "scramble_hard_1",
    "scramble_hard_2",
    "parity_sum",
    "parity_count",
]

def test():
    print("\n\n\n\n\n")
    for task_str in tasks:

        print(f"\n\nTesting {task_str}")
        all_str = ""
        start_starts = []
        start_ends = []
        end_ends = []
        for i, ext in enumerate([0, 0, 0, 0, 1, 2, 3, 4]):
            task = get_task(task_str)
            res = task.inner(extend=ext)

            result = res[0]
            answer_start = res[1]
            answer_length = res[2]
            all_str += result
            start = result[:answer_start]
            answer = result[answer_start:answer_start+answer_length]
            start_starts.append(start[0])
            start_ends.append(start[-1])
            end_ends.append(result[-1])
            if i == 0:
                print(f"For extend = {ext}")
                print("total ", result)
                print("start ", start)
                print("target ", answer)
            if ext == 0:
                assert len(result) < 32
            if result[-2] != answer[-1]:
                print(result)
                print(answer)
            assert result[-2] == answer[-1]
        
        # Check all start starts are same
        assert len(set(start_starts)) == 1
        assert start_starts[0] == 'S'
        # Check all start ends are same
        assert len(set(start_ends)) == 1
        assert len(set(end_ends)) == 1
        # Check all end ends are same

        



        # Check all vocab is same
        dif = set(all_str).difference(set(task.vocab()))
        if len(dif) != 0:
            print("task_str", task_str)
            print("all_str", all_str)
            print("all_str set", set(all_str))
            print("vocab", task.vocab())
            print(dif)
        assert len(dif) == 0
        


if __name__ == "__main__":
    test()