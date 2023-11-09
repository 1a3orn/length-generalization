import argparse
import time

parser = argparse.ArgumentParser(description="A simple argparse example.")

TASKS = [
    "parity_sum",
    "parity_count",
    "math_mult",
    "math_add",
    "count",
    "mode",
    "reverse",
    "sort_len",
    "sort_len_twodigit",
    "sort_missing",
    "copy_len",
    "copy_len_rep",
    "pattern_indices",
    "pattern_repeats",
    "balance_parens",
    "scramble_1",
    "scramble_2",
]
parser.add_argument(
    "--tasks",
    help="Mode of operation.",
    default=",".join(TASKS),
)

MODELS = [
    "trans_karp_sm",
    "trans_karp_md",
    "trans_karp_sm_rot",
    "trans_karp_md_rot",
    "rwkv_sm",
    "ut_sm",
    "sut_sm",
]
parser.add_argument("--models",  default=",".join(MODELS[:1]))
parser.add_argument("--device", help="Device to run on.", default="cpu")

parser.add_argument("--folder", help="Directory to save results to.", default="")
parser.add_argument("--train_ctx_len", type=int, default=64)
parser.add_argument('--train_max_steps', type=int, default=8000)
parser.add_argument('--train_batch_size', type=int, default=32)
parser.add_argument("--train_acc_stop", type=float, default=0.999)
parser.add_argument("--train_log_every", type=int, default=100)
parser.add_argument("--train_lr", type=float, default=0.001)

def get_args():
    result = parser.parse_args()
    result.tasks = result.tasks.split(",")
    result.models = result.models.split(",")
    if result.folder == "":
        # save to yyyy-mm-dd-hh-mm-ss
        result.folder = f"./results/{time.strftime('%Y-%m-%d-%H-%M-%S')}"

    return result


