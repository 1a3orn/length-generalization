# The overall structure here is as follows:
#
# - We have a set of algorithmic generalization tasks
#   (e.g., "parity", "multiplication", "addition", "sort", etc.)
# - We have a set of models (e.g., Transformer, etc.)
#
# - So, then, for each of these tasks and models
# 1. We train a model
# 2. We evaluate the model
# 3. We save the results
from args import get_args
from utils import make_folder
from train.train import train
from evaluate.evaluate import evaluate

def main(args):
    
    make_folder(args.folder)

    for task_str in args.tasks:
        for model_str in args.models:
            model = train(task_str, model_str, args)
            evaluate(model, task_str, model_str, args)

if __name__ == "__main__":
    main(get_args())