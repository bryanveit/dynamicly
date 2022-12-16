import numpy as np
from dynamicly.misc.interpolation import log_log_interp
from dynamicly.misc.shape import crop_data

# Written by Bryan Veit, September 2020
# Based on Tom Irvines "Slightly better than miles equation / generalizes" method

def vrs_engine(fi, ai, damping=0.05, df=1, limit=False):
    fn = [5, ]
    a_vrs = []
    oct = 1 / 24
    tpi = 2 * np.pi
    tpi_sq = tpi ** 2
    last = len(fi) - 1

    for i in np.arange(0, 1000, 1):
        sum = 0
        for j in np.arange(0, last, 1):
            rho = fi[j] / fn[i]
            tdr = 2 * damping * rho

            c1 = tdr ** 2
            c2 = (1 - (rho ** 2)) ** 2

            t = (1 + c1) / (c2 + c1)
            sum += t * ai[j] * df
        a_vrs.append(np.sqrt(sum))

        if fn[i] > 10000:
            break
        if fn[i] > 2 * fi[last]:
            if limit:
                break
        fn.append(fn[i] * (2 ** oct))
    fn = np.asarray(fn)
    a_vrs = np.asarray(a_vrs)
    return fn, a_vrs


def calc_fvrs(psd, Q=10, sigma=3, duration=None, crop=True, limit=True):
    if isinstance(sigma, str):
        if sigma != 'crest':
            print("If string, sigma must be 'crest'.")
            return None
        if sigma == 'crest' and duration == None:
            print('Duration must be provided for crest factor.')
            return None

    f = psd[:, 0]
    a = psd[:, -1]
    damp = 1 / (2 * Q)

    f_narrow = np.arange(f[0], f[-1] + 1, 1)
    psd_narrow = log_log_interp(f, a, f_narrow)
    a_narrow = psd_narrow[:, -1]

    fn, a_vrs = vrs_engine(f_narrow, a_narrow, damping=damp, df=1,limit=limit)

    if isinstance(sigma, str) and sigma == 'crest':
        sigma = np.sqrt(2 * np.log(fn * duration))

    a_vrs = sigma * a_vrs

    fvrs = np.column_stack([fn,
                            a_vrs])
    if crop:
        f1 = f[0]
        f2 = f[-1]
        if f2 == 2000:
            #bump it up to include above 2000 based on octave spacing
            f2 = 2050
        fvrs = crop_data(fvrs, f1, f2)
    return fvrs

def fvrs_to_psd(vrs):
    # Reverse implementation of the miles equation based fVRS calculations
    pass

def miles_equation(psd_value, fn, Q = 10):
    # add ability to interpolate psd for fn
    grms = np.sqrt( (np.pi/2) * fn * Q *psd_value )
    return grms
