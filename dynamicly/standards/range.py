import numpy as np

def rcc319_breakup():
    lvl = np.column_stack([[100, 2000, 10000],
                           [100, 1300, 1300]])
    return lvl


def rcc319_transport(duration=180, b=6.4):
    base = np.column_stack([[10, 40, 500],
                            [.015, .015, .00015]])
    base_duration = 60 * 60
    # duration is in seconds
    # another common b coeff is 4
    scaling = (base_duration / duration) ** (2 / b)
    lvl = np.column_stack([base[:, 0],
                           base[:, -1] * scaling])
    return lvl

def rcc319_workmanship():
    lvl = np.column_stack([[20,150,600,2000],
                           [.0053,.04,.04,.0036]])

    return lvl