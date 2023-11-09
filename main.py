#
# AI Generalization Testbed
#
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