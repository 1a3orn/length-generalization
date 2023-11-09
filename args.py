import argparse
import time

parser = argparse.ArgumentParser(description="A simple argparse example.")

TASKS = [
    "reverse",
    "pattern_indices",
    "pattern_repeats",
    "math_mult",
    "math_add",
    "math_mult_reverse",
    "math_add_reverse",
    "copy_len",
    "copy_len_rep",
    "copy_len_unique",
    "balance_parens",
    "scramble_0",
    "scramble_1",
    "scramble_2",
    "parity_sum",
    "parity_count",
    "count",
    "mode",
    "mode_hard",
    "sort_len",
    "sort_len_twodigit",
    "sort_missing",
]

parser.add_argument(
    "--tasks",
    help="Mode of operation.",
    default=",".join(TASKS),
)

MODELS = [
    "trans_karp_sm",
    "trans_karp_md",
    "trans_karp_lg",
    "trans_karp_sm_rot",
    "trans_karp_md_rot",
    "trans_karp_lg_rot",
    "rwkv_sm",
    "rwkv_md",
    "rwkv_lg",
    "ut_sm",
    "sut_sm",
]
parser.add_argument("--models",  default=",".join(MODELS[:1]))
parser.add_argument("--device", help="Device to run on.", default="cpu")

parser.add_argument("--folder", help="Directory to save results to.", default="")
parser.add_argument("--train_ctx_len", type=int, default=96)
parser.add_argument('--train_max_steps', type=int, default=10000)
parser.add_argument('--train_batch_size', type=int, default=64)
parser.add_argument("--train_acc_stop", type=float, default=0.999)
parser.add_argument("--train_log_every", type=int, default=200)
parser.add_argument("--train_lr", type=float, default=0.001)

def get_args():
    result = parser.parse_args()
    result.tasks = result.tasks.split(",")
    result.models = result.models.split(",")
    if result.folder == "":
        # save to yyyy-mm-dd-hh-mm-ss
        result.folder = f"./results/{time.strftime('%Y-%m-%d-%H-%M-%S')}"

    return result


