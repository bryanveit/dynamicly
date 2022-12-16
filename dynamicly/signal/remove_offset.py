import numpy as np

def remove_offset(data, n=100):
    offset = np.mean(data[:n, -1])
    data[:, -1] -= offset
    return data
