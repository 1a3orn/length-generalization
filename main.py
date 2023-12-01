#
# AI Generalization Testbed
#
import os
from args import get_args
from utils import make_folder
from train.train import train
from logger import Logger
from evaluate.evaluate import evaluate

def main(args):
    
    make_folder(args.folder)

    for model_str in args.models:

        model_logger = Logger()

        for tsk_i, task_str in enumerate(args.tasks):
            test_str = args.tasks_test[tsk_i]
            model = train(
                args,
                task_str=task_str,
                test_str=test_str,
                model_str=model_str,
                global_logger=model_logger,
            )
            #evaluate(model, task_str, model_str, args)
        model_logger.write(os.path.join(args.folder, f"train_{model_str}.csv"))

if __name__ == "__main__":
    main(get_args())