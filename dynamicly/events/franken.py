import numpy as np
from dynamicly.misc.units import (m_to_in, kg_per_m3_to_lbm_per_in3,
                                  Pa_to_psi)
from scipy.interpolate import interp1d

franken_curve = np.column_stack(
    [[1, 2, 2.7, 3, 3.3, 3.6, 3.7,
      3.78, 3.9, 4, 4.1, 4.3, 4.7],
     [-158, -146, -140.5, -136, -130, -121, -119,
      -118.8, -119, -120, -121.7, -123, -124.5]])

def franken_method(spl, rho, E, d, t, units='metric'):
    # This function wraps the implementation of the Franken method for
    # converting an SPL to a PSD used in Gary's initial liftoff code. This is to
    # be ran on a single SPL and single zone. The SPL is expected to be a two
    # column array of frequency and SPL in dB, and the rest of the inputs are
    # floats or ints
    # http: // www.vibrationdata.com / tutorials2 / Franken.pdf
    # look into the barret method
    ############################################################################
    if units.lower() == 'metric':
        rho *= kg_per_m3_to_lbm_per_in3
        E *= Pa_to_psi
        d *= m_to_in
        t *= m_to_in
    elif units.lower() == 'english' or units.lower() == 'imperial':
        pass
    else:
        print('Unsupported unit system. What the heck you using?')
        return None

    ############################################################################
    c_ref = 200000 / 12  # ft/s (speed of sound in aluminum for reference
    c_rocket = np.sqrt(E / rho * (32.2 / 12))  # ft/s
    scale_factor = c_rocket / c_ref

    rho *= 12 ** 3  # lb/ft3
    d /= 12  # ft
    t /= 12  # ft
    rho_areal = rho * t

    franken_tailored = np.column_stack(
        [np.log10(10 ** franken_curve[:, 0] * scale_factor),
         franken_curve[:, -1]])

    # franken_spl_freq = np.column_stack(
    #     [np.log10(spl[:, 0] * d),
    #      interp1d(franken_tailored[:, 0],
    #               franken_tailored[:, -1],
    #               fill_value=(franken_tailored[0, -1],
    #                           franken_tailored[-1, -1]))(
    #          np.log10(spl[:, 0] * d))])

    franken_spl_freq = np.column_stack(
        [np.log10(spl[:, 0] * d),
         interp1d(franken_tailored[:, 0],
                  franken_tailored[:, -1],
                  fill_value='extrapolate')(
             np.log10(spl[:, 0] * d))])

    dB = np.column_stack([franken_spl_freq[:, 0],
                          franken_spl_freq[:, -1] - 20 * np.log10(
                              rho_areal) + spl[:, 1]])
    psd = []
    for i, (f_i, dB_i) in enumerate(zip(spl[:, 0], dB[:, -1])):

        if i == 0:
            f_i_plus = spl[i + 1, 0]
            psd.append(
                (10 ** (dB_i / 20)) ** 2 / (f_i_plus - f_i / (2 ** (1 / 3))))
        elif i >= (len(dB) - 2):
            psd.append((10 ** (dB_i / 20)) ** 2 / (
                    f_i * 2 ** (1 / 3) - f_i / 2 ** (1 / 3)))
        else:
            f_i_plus = spl[i + 1, 0]
            f_i_minus = spl[i - 1, 0]

            psd.append((10 ** (dB_i / 20)) ** 2 / (f_i_plus - f_i_minus))

    psd = np.column_stack([spl[:, 0],
                           np.asarray(psd)])

    return psd