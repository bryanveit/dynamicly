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


def omit_transient_windows(time_history, psd_windows=None,
                           window_size=1, window_overlap=0.5,
                           count_threshold=.15):
    # THIS IS HIGHLY EXPERIMENTAL AND WHAT IS DEEMED TO BE A "BAD" WINDOW
    # SHOULD BE EVALUATED WITH EACH USE
    # But it's rooted in sound logic. Transeient events are better
    # characterized as shock. There is a separaate test for that. Omitting
    # transient windows from a final maximax calc should theortically give
    # you a better characterization of the stationary random content of the
    # signal. The base quanitiy to evaluate transient-ness of a window is the
    # PSD of the full time signal... sometime referred to as the average.
    # Note this is not the log mean of all windows.
    # The PSD value at each frequency in each window is compared to the
    # average value at that frequency. If lower, nothing is noted... it wont
    # influence the maximax caluations. If higher than 3dB (3 sigma, assuming
    # gaussian normal distribution), an exceedance is noted in a count. If the
    # number of exceedances for a given window is more than 15% of the
    # total length of the psd it is deemed worthy of omission. This may be
    # tuned, but seemed to work well for narrow band data. A window can also
    # be deemed worthy of omission is a signal spectral peak exceeds 6dB of
    # the average.

    # eventually it would be cool to have this check frequency range so
    # so if a low frquency hump walks during the duration of a vibe event,
    # or any spectral peak for that matter, only truly spurious, one-off
    # transient windows are ar removed.
    avg = calc_psd(time_history)
    avg_3dB = dyn.db_scale(avg, 3)
    if psd_windows is None:
        psd_windows = calc_psd_windows(time_history, window_size=window_size,
                                       window_overlap=window_overlap)

    omit = {}
    for window, psd in enumerate(psd_windows):
        count = 0
        len_psd = len(psd)
        for i, row in enumerate(psd):
            limit_for_row = avg_3dB[i, 1]
            freq = row[0]
            this_row = row[1]
            if this_row > limit_for_row:
                count += 1
                if freq <= 10:
                    omit[window] = True
            if this_row > 2 * limit_for_row:
                omit[window] = True
        if count > int(len_psd * count_threshold):
            omit[window] = True
    clean_windows = []
    for i, psd in enumerate(psd_windows):
        if i in omit.keys():
            continue
        else:
            clean_windows.append(psd)
    return clean_windows

