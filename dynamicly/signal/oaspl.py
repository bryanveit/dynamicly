import numpy as np

def calc_oaspl(spl, units='dB'):
    # sound power level, hence use factor of 10 not 20
    frequency = spl[:, 0]
    if units == 'dB':
        spl_dB = spl[:, -1]
        spl_decimal = 10 ** (spl_dB / 10)
        sum = np.sum(spl_decimal)
        oaspl = 10 * np.log10(sum)
        return oaspl
    else:
        return None