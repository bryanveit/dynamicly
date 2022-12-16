import numpy as np


def scale(data, scale_factor):
    new_data = np.column_stack([data[:, 0],
                                data[:, -1] * scale_factor])
    return new_data


def dB_to_scalefactor(dB, units='g2'):
    if units in ('g2', 'g^2', 'power'):
        return 10 ** (dB / 10)
    else:
        return 10 ** (dB / 20)


def scalefactor_to_dB(factor, units='g2'):
    if units in ('g2', 'g^2', 'power'):
        return 10 * np.log10(factor)
    else:
        return 20 * np.log10(factor)


def db_scale(data, db, units='g2', round=False):
    # if isinstance(db, int) or isinstance(db, float):
    if units == 'g2':
        factor = 10 ** (db / 10)
    elif units == 'g':
        factor = 10 ** (db / 20)

    elif units == 'dB':
        new_data = np.column_stack([data[:, 0],
                                    data[:, -1] + db])
        return new_data
    else:
        print('invalid units')
        return None

    if round:
        # this should do the x2, x4 simplifcations for 6 dB, etc.
        if db < 0:
            factor = 1/np.round(1/factor,0)
        else:
            factor = np.round(factor,0)

    return scale(data, factor)


def scale_duration(data,
                   from_time,
                   to_time,
                   fatigue_coeff=6.4,
                   return_factor=False):
    # if to_time > from_time:
    #     return None
    #     # dont think its valid to scale data down
    factor = (from_time / to_time) ** (2 / fatigue_coeff)

    if return_factor:
        return scale(data, factor), factor
    else:
        return scale(data, factor)


if __name__ == '__main__':
    print('\n\n')
