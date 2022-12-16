import numpy as np
from dynamicly.misc.octave import to_narrow, narrow
from dynamicly.misc.dictionary import quick_dict
from dynamicly.misc.shape import crop_data

def maximax(data, make_narrow=False):
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
            max = np.max(data_np, axis=1)
            maximax = np.column_stack([freq,
                                       max])
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
            max = np.max(data_np, axis=1)
            maximax = np.column_stack([new_freq,
                                       max])

    elif isinstance(data, np.ndarray):
        # Assume is a n x m numpy array with the frequency in
        # the first column and log mean to be calculated across axis 1 (->)
        freq = data[:, 0]
        data_np = data[:, 1:]
        max = np.max(data_np, axis=1)
        maximax = np.column_stack([freq,
                                   max])
    else:
        maximax = None
    return maximax


def max_in_range(data, n1, n2):
    range = crop_data(data,n1,n2)
    return max(range[:,-1])


def minimum(data, make_narrow=False):
    # if in list format just change it to a dict w arbitrary keys
    if isinstance(data, list):
        data = quick_dict(data)
    if isinstance(data, dict):
        # Assume is a dictionary of n x 2 numpy arrays with the frequency in
        # the first column
        if make_narrow:
            data = {key: to_narrow(val, f1=np.min(val[:, 0]), f2=np.max(val[:,
                                                                        0])) for
                    key, val in data.items()}
        all_freq = [val[:, 0] for key, val in data.items()]
        freq = data[list(data.keys())[0]][:, 0]
        data_list = []
        data_list_full = []
        for key, val in data.items():
            data_list.append(val[:, -1])
            data_list_full.append(val)
        try:
            data_np = np.array(data_list).T
            mini = np.min(data_np, axis=1)
            minimum = np.column_stack([freq,
                                       mini])
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
            mini = np.min(data_np, axis=1)
            minimum = np.column_stack([new_freq,
                                       mini])

    elif isinstance(data, np.ndarray):
        # Assume is a n x m numpy array with the frequency in
        # the first column and log mean to be calculated across axis 1 (->)
        freq = data[:, 0]
        data_np = data[:, 1:]
        min = np.min(data_np, axis=1)
        minimum = np.column_stack([freq,
                                   min])
    else:
        minimum = None
    return minimum
