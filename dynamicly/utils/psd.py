import numpy as np
from dynamicly.signal.sample_rate import calc_sample_rate
from dynamicly.misc.dictionary import quick_dict
from dynamicly.misc.extrema import maximax
import dynamicly as dyn
from scipy.signal import welch

def calc_psd(time_history, df=4, overlap=0.5, window='hann', nfft=None):
    fs = calc_sample_rate(time_history)
    n = len(time_history)
    time = time_history[:, 0]
    mag = time_history[:, -1]

    if nfft is None:
        nfft = np.round(fs / df)
    else:
        nfft = nfft
    noverlap = np.round(nfft * overlap)

    if nfft > n:
        nfft = n
        noverlap = 0

    psd = welch(mag, fs=fs, window=window, nperseg=nfft, nfft=nfft,
                noverlap=noverlap)
    psd = np.column_stack([psd[0], psd[1]])
    return psd


def make_windows(time_history, window_size=1, window_overlap=0.5):
    window_size = int(calc_sample_rate(time_history) * window_size)
    n = len(time_history)
    if window_size > n:
        window_overlap = 0
        window_size = n
    overlap_portion = int(window_size * window_overlap)
    step = window_size - overlap_portion

    window_dict = {}

    win = 1
    while True:
        end_i = int(win * window_size - (win - 1) * overlap_portion)
        if end_i > len(time_history):
            break
        start_i = int(end_i - window_size)
        time_history_i = time_history[start_i:end_i, :]
        window_dict[win] = time_history_i
        win += 1

    return window_dict


def calc_psd_windows(time_history, window_size=1, window_overlap=0.5,
                     return_max=False,return_time_windows=False):
    # window size input in seconds, convert to data points
    # overlap input in decimal fraction of full window, 0.5=50%
    window_size = int(calc_sample_rate(time_history) * window_size)
    n = len(time_history)
    if window_size > n:
        window_overlap = 0
        window_size = n
    overlap_portion = int(window_size * window_overlap)
    step = window_size - overlap_portion

    psd_list = []
    time_list = []

    # n_windows = int(np.floor(n / window_size) - 1)
    # for win in np.linspace(1, n_windows, n_windows):
    #     end_i = int(win * window_size - (win - 1) * overlap_portion)
    #     start_i = int(end_i - window_size)
    #     time_history_i = time_history[start_i:end_i, :]
    #     psd_i = calc_psd(time_history_i)
    #     psd_list.append(psd_i)
    win = 1
    # for win in np.linspace(1, n_windows, n_windows):
    while True:
        end_i = int(win * window_size - (win - 1) * overlap_portion)
        if end_i > len(time_history):
            break
        start_i = int(end_i - window_size)
        time_history_i = time_history[start_i:end_i, :]
        time_list.append(time_history_i)
        psd_i = calc_psd(time_history_i)
        psd_list.append(psd_i)
        win += 1

    if return_max:
        return psd_list, maximax(quick_dict(psd_list))
    elif return_time_windows:
        return psd_list, time_list
    else:
        return psd_list


def calc_psd_max(time_history, window_size=1, window_overlap=0.5):
    psd_list = calc_psd_windows(time_history,
                                window_size=window_size,
                                window_overlap=window_overlap)
    psd_max = maximax(quick_dict(psd_list))
    return psd_max


