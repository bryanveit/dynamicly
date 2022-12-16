import numpy as np


def calc_sample_rate(time_history,round=True):
    # assumes 2 col np array with first col time
    # in future should probably make a mode-based calculation, histogram
    try:
        time = time_history[:, 0]
    except:
        time = time_history
    fs = 1 / (np.mean(np.diff(time)))
    if round:
        fs = int(fs)
    return fs
