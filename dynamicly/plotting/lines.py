import numpy as np
from dynamicly.misc.octave import octave


def line_constant_velocity(velocity, units='ips'):
    if units == 'ips' or units == 'in/s':
        factor = 1 / 386.1  # to g
    else:
        # THIS IS TEMPORARY
        factor = 0

    x = np.array([.01, 100000]) # adpative in future based on current axes
    y = 2 * np.pi * x * velocity * factor
    line = np.column_stack([x, y])
    return line


def line_horizontal(y, x_range=None, ):
    if x_range is None:
        x_range = np.array([.01, 100000])
    line = np.column_stack([[x_range[0], x_range[-1]],
                            [y, y]])
    return line


def line_vertical(x, y_range=None):
    if y_range is None:
        y_range = np.array([1e-8, 10000])
    line = np.column_stack([[x, x],
                            [y_range[0], y_range[-1]]])
    return line
