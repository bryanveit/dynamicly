import numpy as np
from dynamicly.signal.sample_rate import calc_sample_rate

def calc_rms_time(time_history):
    return np.std(time_history[:-1])

def calc_rms_psd(data, round=True):
    freq = data[:,0]
    psd = data[:,-1]

    area_sum = 0
    for i in range(len(psd)):
        if i == 0:
            continue
        f_minus = freq[i-1]
        f = freq[i]
        p_minus = psd[i-1]
        p = psd[i]

        dB = 10*np.log10(p/p_minus)
        oct = np.log10(f/f_minus)/np.log10(2)
        dB_per_oct = dB/oct # slope

        if dB_per_oct == -10*np.log10(2):
            area_sum += p_minus*f_minus*np.log(f/f_minus)
        else:
            area_sum += (10*np.log10(2)*p/(10*np.log10(2)+dB_per_oct)) * (f-(f_minus/f)**(dB_per_oct/(10*np.log10(2)))*f_minus)
    rms = np.sqrt(area_sum)
    if round:
        rms = np.round(rms, 2)
        if not isinstance(round, bool):
            rms = np.round(rms, round)
    return rms

def calc_rms_psd_alt(data, log_x=True, log_y=True,round=True):
    # eventually able to calc the rms of varios data (psi-rms, etc not just
    # g-rms for psd)
    # emulates matlab method but for some narrow band data this has proved to
    # be problematic (NaNs!), so should revisit
    if log_x and log_y:
        # regular calc for PSD
        x = data[:, 0]
        y = data[:, -1]
        x_log = np.log10(x)
        y_log = np.log10(y)

        sum = 0
        # for i, xi in enumerate(x_log):
        #     if i == len(data):
        #         break
        for i in range(len(x_log) - 1):
            # if i > 160:
            #     print('hold')
            c_num = (x_log[i] * y_log[i + 1] - y_log[i] * x_log[i + 1])
            c_den = (x_log[i] - x_log[i + 1])
            c = c_num / c_den

            m = (y_log[i] - y_log[i + 1]) / (x_log[i] - x_log[i + 1])
            if m == -1:
                m = -1.00000000000001

            val = ((data[i + 1, 0] ** (m + 1) -
                              data[i, 0] ** (m + 1)) / (m + 1))
            # if np.isnan(val):
            #     continue
            # if np.isinf(val):
            #     continue
            sum += 10 ** c * val

        rms = np.sqrt(sum)
        if round:
            rms = np.round(rms,2)
            if not isinstance(round, bool):
                rms = np.round(rms, round)
        return rms

    else:
        return None

def rms_by_window(time_history, window_size=1, window_overlap=0.5):
    # window size input in seconds, convert to data points
    # overlap input in decimal fraction of full window, 0.5=50%
    window_size = int(calc_sample_rate(time_history) * window_size)
    n = len(time_history)
    if window_size > n:
        window_overlap = 0
        window_size = n
    overlap_portion = int(window_size * window_overlap)
    step = window_size - overlap_portion

    time_list = []
    rms_list = []

    win = 1
    while True:
        end_i = int(win * window_size - (win - 1) * overlap_portion)
        if end_i > len(time_history):
            break
        start_i = int(end_i - window_size)
        time_history_i = time_history[start_i:end_i, :]

        rms_i = np.std(time_history_i[:,-1])
        rms_list.append(rms_i)

        time_i = np.mean(time_history_i[:,0])
        time_list.append(time_i)
        win += 1

    return np.column_stack([time_list,
                            rms_list])
