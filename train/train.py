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
    loss = torch.nn.CrossEntropyLoss(reduction='none')
    optimizer = torch.optim.Adam(model.parameters(), lr=args.train_lr)
    
    steps = 0
    while steps < args.train_max_steps:
        x, y, y_mask = task.batch({
            'batch_size': args.train_batch_size,
            'ctx_len': args.train_ctx_len,
            'device': args.device,
        }, extend=0)

        result = model(x.to(args.device))

        y_mask = y_mask.unsqueeze(-1)  # Shape becomes [B, T, 1] to broadcast correctly

        # Flatten the tensors to 2D for loss calculation
        # Assuming y is a class index for each time step (not one-hot encoded)
        y = y.reshape(-1)  # Shape becomes [B*T]
        result = result.reshape(-1, result.size(-1))  # Shape becomes [B*T, C]

        # Select only the non-zero entries (i.e., where y_mask was 1)
        non_zero_indices = y_mask.reshape(-1).nonzero().squeeze()  # Get indices of non-zero entries
        loss_val = loss(result[non_zero_indices], y[non_zero_indices].long())
        
        if steps % args.train_log_every == 0:
            print("res: ", task.decode((
                torch.concat([torch.tensor([0]).to(args.device), y], dim=0)
                )[non_zero_indices].view(-1))
            )
            print("res: ", task.decode(y[non_zero_indices].view(-1)))
        # sum loss_val
        loss_val = loss_val.sum() / y_mask.sum()

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
        av_acc = logger.average("train_acc", 200)
        av_loss = logger.average("loss", 200)
        if steps % args.train_log_every == 0:
            print(f"Mdl: {model_str}, tsk: {task_str}, step: {steps}, loss: {av_loss}, train_acc: {av_acc}")
            d = task.decode
            print("Start: ", d(start.view(-1)))
            print("End: ", d(end.view(-1)))
            print("Gen: ", d(gen.view(-1)))
        
        if av_acc is not None and av_acc > args.train_acc_stop and steps > 1000:
            print(f"Reached {args.train_acc_stop} accuracy, stopping...")
            break

    
    logger.write(os.path.join(args.folder, f"train_{task_str}_{model_str}.csv"))
    
    return model