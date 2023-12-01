import torch
import argparse
import os

from tasks.get_task import get_task
from models.get_model import get_model
from logger import Logger

def train(
        args: argparse.Namespace,
        task_str: str = "",
        test_str: str = "",
        model_str: str = "",
        global_logger: Logger = None
    ):
    print(f"Model: {model_str}\t Train: {task_str}\t Test: {test_str}...")
    

    # Setup task, test, model
    logger = Logger()
    task = get_task(task_str)
    test = get_task(test_str)
    model = get_model({
        'model_name': model_str,
        'vocab_size': task.vocab_size(),
        'ctx_len': args.train_ctx_len,
    }).to(args.device)


    loss = torch.nn.CrossEntropyLoss(reduction='none')
    optimizer = torch.optim.Adam(model.parameters(), lr=args.train_lr)
    
    steps = 0
    while steps < args.train_max_steps:
        model.train()
        x, y, y_mask = task.batch({
            'batch_size': args.train_batch_size,
            'ctx_len': args.train_ctx_len,
            'device': args.device,
        }, extend=0)

        result = model(x.to(args.device))

        y_mask = y_mask.unsqueeze(-1)  # Shape becomes [B, T, 1] to broadcast correctly
        y = y.reshape(-1)  # Shape becomes [B*T]
        result = result.reshape(-1, result.size(-1))  # Shape becomes [B*T, C]

        # Select only the non-zero entries (i.e., where y_mask was 1)
        non_zero_indices = y_mask.reshape(-1).nonzero().squeeze()  # Get indices of non-zero entries
        loss_val = loss(result[non_zero_indices], y[non_zero_indices].long())
        
        if steps % args.train_log_every == 0:
            #print("res: ", task.decode((
            #    torch.concat([torch.tensor([0]).to(args.device), y], dim=0)
            #    )[non_zero_indices].view(-1))
            #)
            #print("res: ", task.decode(y[non_zero_indices].view(-1)))
            pass
        # sum loss_val
        loss_val = loss_val.sum() / y_mask.sum()

        loss_val.backward()

        optimizer.step()
        optimizer.zero_grad()

        model.eval()

        # Test accuracy on the test task, which in this case
        # is a subset of the training task
        start, end = test.acc(extend=0)
        start = start.to(args.device)
        end = end.to(args.device)
        gen = model.generate(start, len(end.view(-1)))
        test_acc = (gen == end).float().min().item()

        logger_props = {
            'train_task': task_str,
            'test_task': task_str,
            'step': steps,
            'train_loss': loss_val.item(),
            'test_acc': test_acc
        }
        logger.add(logger_props)
        if global_logger is not None:
            global_logger.add(logger_props)

        steps += 1
        av_acc = logger.average("test_acc", args.av_over_steps)
        av_loss = logger.average("train_loss", args.av_over_steps)
        if steps % args.train_log_every == 0:
            print(f"Mdl: {model_str}, tsk: {task_str}, step: {steps}, loss: {av_loss}, test_acc: {av_acc}")
            d = task.decode
            if steps % (args.train_log_every * 5) == 0:
                print("Start: ", d(start.view(-1)))
                print("End: ", d(end.view(-1)))
                print("Gen: ", d(gen.view(-1)))
        
        if av_acc is not None and av_acc > args.train_acc_stop and steps > args.train_min_steps:
            print("On step: ", steps)
            print(f"Reached {args.train_acc_stop} accuracy, stopping...")
            break

    logger.write(os.path.join(args.folder, f"train_{task_str}_{test_str}_{model_str}.csv"))
    
    return model