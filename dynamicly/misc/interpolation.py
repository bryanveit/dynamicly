import numpy as np
from scipy import interpolate

def log_log_interp(x_old, y_old, x_new):
    if min(x_old) == 0:
        temp = []
        for val in list(x_old):
            if val == 0:
                temp.append(1)
            else:
                temp.append(val)
        x_old = np.asarray(temp)
    x_log = np.log10(x_old)
    if min(y_old) == 0:
        temp = []
        for val in list(y_old):
            if val == 0:
                temp.append(1e-7)
            else:
                temp.append(val)
        y_old = np.asarray(temp)
    y_log = np.log10(y_old)
    x_log_new = np.log10(x_new)

    y_log_new = np.interp(x_log_new, x_log, y_log)
    # y_log_new = interpolate.interp1d(x_log_new, x_log, y_log,
    #                                  fill_value='extrapolate')

    y_new = 10 ** y_log_new
    new = np.column_stack([x_new,
                           y_new])
    # return y_new
    return new

def linear_interp(x_old, y_old, x_new):
    y_new = np.interp(x_new, x_old, y_old)

    new = np.column_stack([x_new,
                           y_new])

    return new