import argparse
import os

from tasks.get_task import get_task
from logger import Logger

def evaluate(model: any, task_str: str, model_str: str, args: argparse.Namespace):
    print(f"Training {task_str}...")
    
    logger = Logger()
    task = get_task(task_str)
    for extend in range(8):
    
        for step in range(100):

            start, end = task.acc(extend=extend)
            gen = model.generate(start, len(end.view(-1)))
            test_acc = (gen == end).float().min().item()
            
            logger.add({
                'model': model_str,
                'task': task_str,
                'extend': extend,
                'step': step,
                'test_acc': test_acc
            })

            av_acc = logger.average("test_acc", 100)
            if step % args.train_log_every == 0:
                print(f"Extend {extend}: Step {step}, train_acc {av_acc}")
                print(task.decode(end.view(-1)), task.decode(gen.view(-1)))

    
    logger.write(os.path.join(args.folder, f"test_{task_str}_{model_str}.csv"))
    
    # copy the file I just wrote to the universal "test.csv" file
    # so that I can compare all models on all tasks
    with open(os.path.join(args.folder, f"test_{task_str}_{model_str}.csv"), 'r') as f:
        lines = f.readlines()
        with open(os.path.join(args.folder, f"test.csv"), 'a') as f2:
            for line in lines:
                f2.write(line)
    
    return model