import numpy as np
from dynamicly.signal.rms import rms_by_window
from dynamicly.misc.interpolation import linear_interp
from dynamicly.signal.sample_rate import calc_sample_rate

def pad_back(array, pad_value=None, time=None, n=None):
    if time is None and n is None:
        print('Must enter either time in seconds to add or number of points '
              'based on current sample rate')
        return array
    fs = calc_sample_rate(array)
    dt = 1 / fs
    if time:
        n = time / dt
    else:
        pass
    if pad_value is None:
        pad_value = array[-1, -1]
    start_of_new = array[-1, 0] + dt
    ############################################################################
    new_time = np.arange(start_of_new, start_of_new + n * dt, dt)
    new_value = np.ones_like(new_time) * pad_value

    addition = np.column_stack([new_time, new_value])

    return np.row_stack([array, addition])


def pad_front(array, pad_value=None, time=None, n=None):
    if time is None and n is None:
        print('Must enter either time in seconds to add or number of points '
              'based on current sample rate')
        return array
    fs = calc_sample_rate(array)
    dt = 1 / fs
    if time:
        n = time / dt
    else:
        pass
    if pad_value is None:
        pad_value = array[0, -1]
    start_of_new = array[0, 0] - dt
    ############################################################################
    new_time = np.arange(start_of_new - (n-1) * dt, start_of_new+dt, dt)
    new_value = np.ones_like(new_time) * pad_value

    addition = np.column_stack([new_time, new_value])

    return np.row_stack([addition, array])


def crop_data(data, t1, t2, zero=False):
    if isinstance(t1, str):
        index1 = 0
    else:
        index1 = np.where(data[:, 0] >= t1)[0][0]

    if isinstance(t2, str):
        index2 = len(data) - 1
    else:
        try:
            index2 = np.where(data[:, 0] >= t2)[0][0]
        except:
            index2 = np.where(data[:, 0] >= t2)[0][0]
    cropped = data[index1:index2, :]
    if zero:
        cropped[:, 0] -= cropped[0, 0]
    return cropped


def crop_data_by_rms(time_history,
                     active_threshold=1,  # g
                     pad_time=2,  # seconds
                     round=True,
                     window_size=0.1,  # seconds
                     window_overlap=0.5,
                     zero=False
                     # noise_floor=None,
                     ):
    fs = calc_sample_rate(time_history)
    rms_history = rms_by_window(time_history,
                                window_size=window_size,
                                window_overlap=window_overlap)
    rms_history = linear_interp(rms_history[:, 0],
                                rms_history[:, -1],
                                time_history[:, 0])
    # if noise_floor is None:
    #     # This could also default to something like 0.1 grms or 0.5 grms,
    #     # but the time histories being passed into this likely will start
    #     # with an inactive segment before a hotfire or sep test etc
    #     noise_floor = (np.mean(time_history[:100, 1]) +
    #                    np.std(time_history[:100, 1]))
    #     # on second thought imma jsut set an "active threshold" for now,
    #     # but can make more dynamic based on RMS transistions (and sustained
    #     # magnitude) later

    index_start = np.where(rms_history[:, 1] > active_threshold)[0][0]
    index_end = np.where(rms_history[:, 1] > active_threshold)[0][-1]

    index_start -= fs * pad_time
    if index_start < 0:
        index_start = 0
    index_end += fs * pad_time
    if index_end > (len(time_history) - 1):
        index_end = (len(time_history) - 1)

    time_start = time_history[index_start, 0]
    time_end = time_history[index_end, 0]

    if round:
        time_start = np.floor(time_start)
        time_end = np.ceil(time_end)
        if time_end > time_history[-1, 0]:
            time_end = time_history[-1, 0]

    return crop_data(time_history, time_start, time_end, zero=zero)


def shift_time(data, dt=0):
    if isinstance(data, dict):
        shifted_data = {}
        for key, val in data.items():
            shifted_data[key] = np.column_stack([val[:, 0] + dt,
                                                 val[:, 1]])
    else:
        shifted_data = np.column_stack([data[:, 0] + dt,
                                        data[:, 1]])
    return shifted_data


def crop_data_inclusive(data, i1, i2):
    index1 = np.where(data[:, 0] >= i1)[0][0]
    index2 = np.where(data[:, 0] > i2)[0][0]
    return data[index1:index2 + 1, :]
