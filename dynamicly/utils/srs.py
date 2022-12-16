import numpy as np
from scipy.signal import lfilter
from numpy import zeros


def calc_srs(time_history, Q=10, fn=None, return_max=True):
    t = time_history[:, 0]
    amplitude = time_history[:, -1]
    dt = np.mean(np.diff(t))
    fs = 1 / dt

    damp = 1 / (2 * Q)

    if fn is None:
        fn = natural_frequency()

    positive = zeros(len(fn))
    negative = zeros(len(fn))
    for i, freq in enumerate(fn):
        omega = 2 * np.pi * freq
        omegad = omega * np.sqrt(1 - damp ** 2)

        E = np.exp(-damp * omega * dt)
        K = omegad * dt
        C = E * np.cos(K)
        S = E * np.sin(K)
        Sp = S / K

        b = np.array([1 - Sp, 2 * (Sp - C), E ** 2 - Sp])
        a = np.array([1, -2 * C, E ** 2])

        response = lfilter(b, a, amplitude, zi=None)  # axis=-1
        positive[i] = np.max(response)
        negative[i] = np.abs(np.min(response))
    positive = np.asarray(positive)
    negative = np.asarray(negative)
    if return_max:
        max = np.column_stack(
            [fn, np.max(np.column_stack([negative, positive]), axis=1)])
        return max
    else:
        pos = np.column_stack([fn, positive])
        neg = np.column_stack([fn, negative])
        return pos, neg

def srs_damping_adjustment(srs1, q1, q2):
    fn = srs1[:,0]
    response = srs1[:,-1]
    #SOMETHINGGGG
    srs2 = None #placeholder
    return srs2

def natural_frequency():
    fn = [10]
    n = 61
    oct = 1 / 6
    for i in range(1, n):
        fn.append(fn[i - 1] * (2. ** oct))
    return np.asarray(fn)
