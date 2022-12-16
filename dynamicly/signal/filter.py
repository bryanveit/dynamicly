import numpy as np
from scipy.signal import butter, buttord, filtfilt
from dynamicly.signal.sample_rate import calc_sample_rate


def filter(time_history, type='high', cutoff=5, order=4):
    # butterworth filter applied forward and back with filtfilt
    fsamp = calc_sample_rate(time_history)
    f_nyquist = fsamp / 2

    try:
        fnorm = cutoff / f_nyquist
    except:
        fnorm = [cut / f_nyquist for cut in cutoff]
    b, a = butter(order, fnorm, btype=type)
    time = time_history[:, 0]
    mag = time_history[:, -1]

    filtered_mag = filtfilt(b, a, mag)

    filtered_time_history = np.column_stack([time,
                                             filtered_mag])
    return filtered_time_history

def filter_limited(time_history, type='high', cutoff=5, order=4,
                   db_limit = 10):
    print('not implemeted yet.')
    pass
