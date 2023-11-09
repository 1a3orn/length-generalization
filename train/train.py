import torch
import argparse
import os

from tasks.get_task import get_task
from models.get_model import get_model
from logger import Logger

def train(task_str: str, model_str: str, args: argparse.Namespace):
    print(f"Training {model_str} on {task_str}...")
    
    logger = Logger()
    task = get_task(task_str)
    model = get_model({
        'model_name': model_str,
        'vocab_size': task.vocab_size(),
        'ctx_len': args.train_ctx_len,
    }).to(args.device)
    loss = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=args.train_lr)
    
    steps = 0
    while steps < args.train_max_steps:
        x, y = task.batch({
            'batch_size': args.train_batch_size,
            'ctx_len': args.train_ctx_len,
            'device': args.device,
        }, extend=0)

        result = model(x.to(args.device))

        result_flat = result.view(-1, result.size(-1))
        loss_val = loss(result_flat, y.reshape(-1).long())
        loss_val.backward()

        optimizer.step()
        optimizer.zero_grad()

        start, end = task.acc(extend=0)
        start = start.to(args.device)
        end = end.to(args.device)
        gen = model.generate(start, len(end.view(-1)))
        train_acc = (gen == end).float().min().item()

        logger.add({ 'step': steps, 'loss': loss_val.item(), 'train_acc': train_acc })

        steps += 1
        av_acc = logger.average("train_acc", 400)
        av_loss = logger.average("loss", 400)
        if steps % args.train_log_every == 0:
            print(f"Mdl: {model_str}, tsk: {task_str}, step: {steps}, loss: {av_loss}, train_acc: {av_acc}")
            print(task.decode(end.view(-1)), task.decode(gen.view(-1)))
        
        if av_acc is not None and av_acc > args.train_acc_stop:
            print(f"Reached {args.train_acc_stop} accuracy, stopping...")
            break
        

        

    
    logger.write(os.path.join(args.folder, f"train_{task_str}_{model_str}.csv"))
    
    return model