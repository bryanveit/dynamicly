import numpy as np
from dynamicly.misc.dictionary import quick_dict
from dynamicly.misc.octave import to_narrow, narrow


def log_mean(data):
    # if in list format just change it to a dict w arbitrary keys
    if isinstance(data, list):
        data = quick_dict(data)
    if isinstance(data, dict):
        # Assume is a dictionary of n x 2 numpy arrays with the frequency in
        # the first column
        all_freq = [val[:, 0] for key, val in data.items()]
        freq = data[list(data.keys())[0]][:, 0]
        data_list = []
        data_list_full = []
        for key, val in data.items():
            data_list.append(val[:, -1])
            data_list_full.append(val)
        try:
            data_np = np.array(data_list).T
            data_log = np.log(data_np)
            data_logmean = np.exp(np.mean(data_log, axis=1))
            lm = np.column_stack([freq,
                                  data_logmean])
        except:
            bounding_start = [val[0] for val in all_freq]
            bounding_start = np.max(np.asarray(bounding_start))
            bounding_end = [val[-1] for val in all_freq]
            bounding_end = np.min(np.asarray(bounding_end))
            data_list_narrow = [to_narrow(val, f1=bounding_start,
                                          f2=bounding_end) for
                                val in data_list_full]
            data_list_narrow = [val[:, -1] for val in data_list_narrow]
            new_freq = narrow(f1=bounding_start, f2=bounding_end, df=1)

            data_np = np.array(data_list_narrow).T
            data_log = np.log(data_np)
            data_logmean = np.exp(np.mean(data_log, axis=1))
            lm = np.column_stack([new_freq,
                                  data_logmean])

    elif isinstance(data, np.ndarray):
        # Assume is a n x m numpy array with the frequency in
        # the first column and log mean to be calculated across axis 1 (->)
        freq = data[:, 0]
        data_np = data[:, 1:]
        data_log = np.log(data_np)
        data_logmean = np.exp(np.mean(data_log, axis=1))
        lm = np.column_stack([freq,
                              data_logmean])
    else:
        lm = None
    return lm

def linear_mean(data):
    # if in list format just change it to a dict w arbitrary keys
    if isinstance(data, list):
        data = quick_dict(data)
    if isinstance(data, dict):
        # Assume is a dictionary of n x 2 numpy arrays with the frequency in
        # the first column
        all_freq = [val[:, 0] for key, val in data.items()]
        freq = data[list(data.keys())[0]][:, 0]
        data_list = []
        data_list_full = []
        for key, val in data.items():
            data_list.append(val[:, -1])
            data_list_full.append(val)
        try:
            data_np = np.array(data_list).T

            data_mean = np.mean(data_np, axis=1)
            m = np.column_stack([freq,
                                  data_mean])
        except:
            bounding_start = [val[0] for val in all_freq]
            bounding_start = np.max(np.asarray(bounding_start))
            bounding_end = [val[-1] for val in all_freq]
            bounding_end = np.min(np.asarray(bounding_end))
            data_list_narrow = [to_narrow(val, f1=bounding_start,
                                          f2=bounding_end, log=False) for
                                val in data_list_full]
            data_list_narrow = [val[:, -1] for val in data_list_narrow]
            new_freq = narrow(f1=bounding_start, f2=bounding_end, df=1)

            data_np = np.array(data_list_narrow).T
            data_mean = np.mean(data_np, axis=1)
            m = np.column_stack([new_freq,
                                  data_mean])
    else:
        m = None
    return m

def log_mean_weighted(data, weights):
    pass
    # for a quick assume dictionary with consistent frequency spacing/range
    # https: // en.wikipedia.org / wiki / Weighted_geometric_mean
    # if not isinstance(data,dict):
    #     return None
    # freq = data[list(data.keys())[0]][:, 0]
    # data_list = []
    # weight_sum = 0
    # for key, val in data.items():
    #     w = weights[key]
    #     data_list.append(w*np.log(val[:, -1]))
    #     weight_sum += w
    #
    # numerator = sum(data_list)
    #
    # return None
    # data_np = np.array(data_list).T
    # data_log = data_np # its already log
    # data_logmean = np.exp(np.mean(data_log, axis=1))
    # lm = np.column_stack([freq,
    #                       data_logmean])


    # if in list format just change it to a dict w arbitrary keys
    # if isinstance(data, list):
    #     data = quick_dict(data)
    # if isinstance(data, dict):
    #     # Assume is a dictionary of n x 2 numpy arrays with the frequency in
    #     # the first column
    #     all_freq = [val[:, 0] for key, val in data.items()]
    #     freq = data[list(data.keys())[0]][:, 0]
    #     data_list = []
    #     data_list_full = []
    #     for key, val in data.items():
    #         data_list.append(val[:, -1])
    #         data_list_full.append(val)
    #
    #
    #     try:
    #         data_np = np.array(data_list).T
    #         data_log = np.log(data_np)
    #         data_logmean = np.exp(np.mean(data_log, axis=1))
    #         lm = np.column_stack([freq,
    #                               data_logmean])
    #     except:
    #         bounding_start = [val[0] for val in all_freq]
    #         bounding_start = np.max(np.asarray(bounding_start))
    #         bounding_end = [val[-1] for val in all_freq]
    #         bounding_end = np.min(np.asarray(bounding_end))
    #         data_list_narrow = [to_narrow(val, f1=bounding_start,
    #                                       f2=bounding_end) for
    #                             val in data_list_full]
    #         data_list_narrow = [val[:, -1] for val in data_list_narrow]
    #         new_freq = narrow(f1=bounding_start, f2=bounding_end, df=1)
    #
    #         data_np = np.array(data_list_narrow).T
    #         data_log = np.log(data_np)
    #         data_logmean = np.exp(np.mean(data_log, axis=1))
    #         lm = np.column_stack([new_freq,
    #                               data_logmean])
    #
    # elif isinstance(data, np.ndarray):
    #     # Assume is a n x m numpy array with the frequency in
    #     # the first column and log mean to be calculated across axis 1 (->)
    #     freq = data[:, 0]
    #     data_np = data[:, 1:]
    #     data_log = np.log(data_np)
    #     data_logmean = np.exp(np.mean(data_log, axis=1))
    #     lm = np.column_stack([freq,
    #                           data_logmean])
    # else:
    #     lm = None
    # return lm

def normalize(data, dictionary_extrema=False):
    if isinstance(data, dict):
        norm_data = {}

        if dictionary_extrema:
            y_min = np.min(data[list(data.keys())[0]][:, -1])
            y_max = np.max(data[list(data.keys())[0]][:, -1])
            for key, val in data.items():
                if np.min(val[:, -1]) < y_min:
                    y_min = np.min(val[:, -1])
                if np.max(val[:, -1]) > y_max:
                    y_max = np.max(val[:, -1])
            for key, val in data.items():
                norm_data[key] = np.column_stack([val[:, 0],
                                                  (val[:, -1] - y_min) / (
                                                          y_max - y_min)])
        else:
            for key, val in data.items():
                y_min = min(val[:, -1])
                y_max = max(val[:, -1])
                norm_data[key] = np.column_stack([val[:, 0],
                                                  (val[:, -1] - y_min) / (
                                                          y_max - y_min)])
    else:
        y_min = min(data[:, -1])
        y_max = max(data[:, -1])
        norm_data = np.column_stack([data[:, 0],
                                     (data[:, -1] - y_min) / (
                                             y_max - y_min)])

    return norm_data
