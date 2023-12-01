import argparse
import time

parser = argparse.ArgumentParser(description="Testing skills.")

parser.add_argument("--device", help="Device to run on.", default="cpu")
parser.add_argument("--folder", help="Directory to save results to.", default="")
parser.add_argument("--train_ctx_len", type=int, default=96)
parser.add_argument('--train_max_steps', type=int, default=25000)
parser.add_argument('--train_min_steps', type=int, default=10000)
parser.add_argument('--train_batch_size', type=int, default=64)
parser.add_argument("--train_acc_stop", type=float, default=0.999)
parser.add_argument("--train_log_every", type=int, default=250)
parser.add_argument("--train_lr", type=float, default=0.0005)
parser.add_argument("--av_over_steps", type=int, default=100)

parser.add_argument("--tasks", help="Mode of operation.")
parser.add_argument("--tasks_test", help="What you test on")
parser.add_argument("--models", help="Models to run.", default="trans_karp_8")

def get_args():
    result = parser.parse_args()
    result.tasks = result.tasks.split(",")
    result.tasks_test = result.tasks_test.split(",")

    assert len(result.tasks) == len(result.tasks_test), "Must have same number of tasks and tests"

    result.models = result.models.split(",")
    if result.folder == "":
        # save to yyyy-mm-dd-hh-mm-ss
        result.folder = f"./results/{time.strftime('%Y-%m-%d-%H-%M-%S')}"

    return result


