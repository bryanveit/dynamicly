import numpy as np
from scipy import stats

def calc_zero_crossings(time_history, mode = False):
    times = []
    reference = time_history[0, 1]
    dt = np.mean(np.diff(time_history[:, 0]))
    for row in time_history:
        t = row[0]
        val = row[1]

        ref_sign = np.sign(reference)
        val_sign = np.sign(val)

        if ref_sign != val_sign:
            times.append(t - dt)
            reference = val
    times = np.asarray(times)
    if mode:
        n = int(abs(np.ceil(np.log10(np.mean(np.diff(times)) / 10)))) + 1
        dt = stats.mode(np.round(np.diff(times), n))[0]
        freq = (1 / dt) / 2
        freq = freq[0]
    else:
        freq = (1 / np.mean(np.diff(times))) / 2
    return freq
