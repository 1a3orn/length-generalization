import numpy as np
import torch
import math

def _gen_timing_signal(length, channels, min_timescale=1.0, max_timescale=1.0e4):
    """
    Generates a [1, length, channels] timing signal consisting of sinusoids
    Adapted from:
    https://github.com/tensorflow/tensor2tensor/blob/master/tensor2tensor/layers/common_attention.py
    """
    # [0, 1, 2, ..., length-1]
    position = np.arange(length)

    # Filling with sin / cos in different places
    num_ts = channels // 2
    
    # We need to scale up from min_timescale and max_timescale
    div = float(max_timescale) / float(min_timescale)

    # This is the log-space increment for each step that we make 
    # for inv-timescales, which makes (num_timescales - 1) steps
    # because a list of length N has N-1 steps
    log_timescale_increment = math.log(div) / (float(num_ts) - 1)
    print("log_timescale_increment: ", log_timescale_increment)
   
    # inv-timecales gives you 'num_timescales' ranging
    # from min_timescale to the inverse of max_timescale
    # and operating in log-space.
    # Example:
    # min_timescale = 1.0
    # max_timescale = 10000.0
    # num_timescales = 3
    #
    # get [1, 1/100, 1/10,000].
    ts_range = np.arange(num_ts).astype(np.float)
    inv_timescales = min_timescale * np.exp(ts_range * -log_timescale_increment)
    
    scaled_time = np.expand_dims(position, 1) * np.expand_dims(inv_timescales, 0)
    print("scaled_time: ", scaled_time)
    # This gets you an increment of * step in the 
    # time direction -- i.e., outermost dimension
    # and an increment of whatever the inv-timescale
    # is in the innermost dimension

    # Use sin for even channels and cos for odd channels
    signal = np.concatenate([np.sin(scaled_time), np.cos(scaled_time)], axis=1)

    # With sine added, you have the fastest cycle at the beginning
    # and the slowest cycle at the end
    # i.e, for argument of 8, 4:

    #tensor([[[ 0.0000e+00,  0.0000e+00,  1.0000e+00,  1.0000e+00],
    #     [ 8.4147e-01,  1.0000e-04,  5.4030e-01,  1.0000e+00],
    #     [ 9.0930e-01,  2.0000e-04, -4.1615e-01,  1.0000e+00],
    #     [ 1.4112e-01,  3.0000e-04, -9.8999e-01,  1.0000e+00],
    #     [-7.5680e-01,  4.0000e-04, -6.5364e-01,  1.0000e+00],
    #     [-9.5892e-01,  5.0000e-04,  2.8366e-01,  1.0000e+00],
    #     [-2.7942e-01,  6.0000e-04,  9.6017e-01,  1.0000e+00],
    #     [ 6.5699e-01,  7.0000e-04,  7.5390e-01,  1.0000e+00]]])
   
    # Padding in case of uneven channels etc
    signal = np.pad(signal, [[0, 0], [0, channels % 2]], 
                    'constant', constant_values=[0.0, 0.0])
    signal =  signal.reshape([1, length, channels])

    return torch.from_numpy(signal).type(torch.FloatTensor)

if __name__ == "__main__":
    print(_gen_timing_signal(8, 4))