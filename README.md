# ----------------------

# ML Algo Generalization Testbed

# -----------------------

The goal here is to allow you to average performance for the following task.

1. Algorithmic task vs. algorithmic task INCLUDING subtasks
2. Algorithmic task vs. algorithmic task INCLUDING _only lower level subtasks_
3. Algorithmic task vs. algorithmic task INCLUDING _only upper-level subtasks_
4. Algorithmic task vs. algorithmic task INCLUDING _other unrelated subtasks_

Side-goal --

1. Find algorithmic tasks where you CANNOT accomplish anything, without algorithmic subtasks
2. Find algorithmic tasks where subtasks don't help, etc.

We can try to do the above across:

1. Stacked algorithmic subtasks
2. Non-stacked algorithmic subtasks.

---

Given the above goal, it makes sense to be able to make a CSV with columns

1. Non-ambigious training task | test_task | training_step | training_loss | test_task_acc

For all the above, we test generalization in some way. I.e., training to sort lists up until length 10, then testing if you can sort lists of length 11, 12; training on addition of up to 4-digit numbers, then testing to see if you can do addition on 5-digit numbers, and so on.

(There are a few algorithmic tasks that don't fall into this categorization very well, note, and simply have identical train / test distributions. The 'scramble_n' tests, for instance fall into this.)

This work is inspired by papers like the following:

- ["What Algorithms can Transformers Learn? A Study in Length Generalization](https://arxiv.org/pdf/2310.16028.pdf)
