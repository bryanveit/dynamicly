import numpy as np
from scipy.interpolate import interp1d
from dynamicly.misc.octave import octave

acoustic_efficieny_options = {
    # THESE ARE NOTIONAL VALUES. SOHULD BE TAILORED FOR LV + LAUNCH SITE
    'Undeflected': 0.5 / 100,
    'Flight': 0.5 / 100,
    ############################################################################
    'VAFB': 0.15 / 100,
    'VSFB': 0.15 / 100,
    'SLC-2': 0.15 / 100,
    'SLC2': 0.15 / 100,
    ############################################################################
    'KSC': 0.065 / 100,
    'CCSFS': 0.065 / 100,
    'SLC-20': 0.065 / 100,
    'SLC20': 0.065 / 100,
    ################################################################################
    # And so on
}

termination = {
    # THESE ARE NOTIONAL VALUES. SOHULD BE TAILORED FOR LV + LAUNCH SITE
    'Undeflected': 'equation',
    'Flight': 'equation',
    ############################################################################
    'VAFB': 8,  # meters
    'VSFB': 8,  # meters

    ############################################################################
    'KSC': 4,  # meters
    'CCSFS': 4,  # meters
    ############################################################################
    # And so on
}

tranmission_loss = {
    'Undeflected': False,
    'Flight': False,
    ############################################################################
    # VAFB Deck Length, tranmission loss in db
    'VAFB': (14, 30),  # meters, dB TL of a 4in concrete fence in 250 Hz range
    'VSFB': (14, 30),  # meters, dB TL of a 4in concrete fence in 250 Hz range
    ############################################################################
    # Currently no covering of the plume in FL
    'KSC': False,
    'CCSFS': False,
}

directivity = {
    # The undeflected plume has a directdivity pattern such that the fraction of
    # power radiated fwd is about 10dB down.
    'Undeflected': (0.1, False),
    'Flight': (0.1, False),
    ############################################################################
    'VAFB': (2, 0.1),  # multiplier when refelcted normally, "" when blocked
    'VSFB': (2, 0.1),
    # once the sound emerges from the trench it will be radiating over a
    # ground plane. This only accounts for the vertical section of the plume
    # when reducing directivity (out to core termination)
    ############################################################################
    # Currently no covering of the plume in so all is reflecected despite
    # being on ground
    'KSC': (2, False),
    'CCSFS': (2, False),
}

def liftoff(stations, deflection='Undeflected',
            a_ambient=335, a_exhaust=896,
            u_exhaust=3096, thrust=164000,
            n_nozzles=4, d_nozzles=0.51,
            units='metric'):
    # NASA-SP-8072, Distributed Source Method II. Will be improved upon and
    # expanded later. Verify modifications from Ares 1X work.

    # a_ambient = speed of sound in ambient medium (air)
    # a_exhaust = spped of sound at nozzle exit in exhaust
    # u_exhasut = exit velocity of the exhasut
    # thrust = single engine thrust
    # n_nozzles = number of nozzles
    # d_nozzles = diameter of a single nozzle

    if units != 'metric':
        print('Only metric units supported at this time.')
        return None

    try:
        eta = acoustic_efficieny_options[deflection]

    except:
        print(
            f'Deflection scheme "{deflection}" not recognized. '
            f'The following options are currently accepted.\n')
        for key in acoustic_efficieny_options.keys():
            print(key)
        print('\n')
        return None

    ############################################################################
    # Sound Power Calculation and Plume Descretization
    ############################################################################
    # Define the overall total sound power, given the efficency etc
    L_watts_overall = (120 + 10 * np.log10(0.5 * eta * thrust * u_exhaust)
                       + 10 * np.log10(n_nozzles))
    # First we need to digitize some of the relations that are given as plots
    # in 8072. This one describes the distribution of the overall sound power
    # in terms of the core length xt. The distance relative to xt ie. x/xt is
    # here called xxt, and the raltive sound power is here nrLw

    xxt = np.array([0.1, 0.2, 0.5, 1, 1.6, 2, 3.5, 4.6])
    nrLw = np.array([-19, -15, -9, -5, -3, -4, -14, -20])

    effective_diameter = d_nozzles * np.sqrt(n_nozzles)
    mach_exhaust = u_exhaust / a_exhaust

    try:
        xt = termination[deflection]
    except:
        print('Unknown core termination value.')
        print(
            f'Deflection scheme "{deflection}" not recognized. '
            f'The following options are currently accepted.\n')
        for key in acoustic_efficieny_options.keys():
            print(key)
        print('\n')
        return None

    if isinstance(xt, str):
        # core length undeflected using varnier eqn 9.5 meters:
        xt = 1.75 * effective_diameter * (1 + 0.38 * mach_exhaust) ** 2
    # xt in meters, core length to deflector otherwise, now construct the x
    # vector based on xt.

    x1 = xxt * xt

    # The overall sound power distributed over the plumes per length x is
    L_watts_x1 = (nrLw + L_watts_overall - 10 * np.log10(xt))

    # We want much more dense slices if the point-source approximation is to
    # be good. so we shall use a 1m slice with, extending to 5 xt (the limit
    # of the distribution).
    start = x1[0]
    end = x1[-1]
    step = (end - start) / np.ceil(end - start)
    x = np.linspace(start, end, int((end - start) / step) + 1)

    # Now interpolate the L_watts_x1 functions
    # Lwux=interp1(xu1,Lwux1,xu,'spline');
    L_watts_x = interp1d(x1, L_watts_x1, kind='cubic')(x)

    dx = np.asarray([1, *np.diff(x)])

    L_watts_check = 10 * np.log10(np.sum((10 ** (L_watts_x / 10) * dx)))

    # figure 13 in NASA SP 8072
    strouhal = np.asarray(
        [0.05, 0.1, 0.2, 0.5, 1, 1.5, 2, 3, 5, 10, 20, 50, 100])
    norm_rel_spectrum = [-20, -17, -14, -10, -8, -7.5, -8,
                         -10, -13, -21, -28, -37, -43]

    # find the frequency vector at each station x, given by the stroughal number
    freq = [strouhal * u_exhaust * a_ambient / (a_exhaust * xi) for xi in x]
    freq = np.asarray(freq).T

    # Now find the sound power spectrum per Hz for each slice corresponding to
    # the frequency vectors.  We will just use the coarse slicing for now.
    # Say the x's are centers of the slices and the slice length is the delta
    x_L_watts_freq = [norm_rel_spectrum + L_watts_x[i] +
                      10 * np.log10(xi) + 10 * np.log10(dx[i]) -
                      10 * np.log10(u_exhaust * a_ambient / a_exhaust)
                      for i, xi in enumerate(x)]
    x_L_watts_freq = np.asarray(x_L_watts_freq).T

    # Here we compute the total sound power to make sure we've got it all.
    # First the sound power in each slice, accounting for frequency span.
    # The units of Lwuf are power/Hz, and also 7005 says so. Find the mid
    # points in the Lwf functions corresponding to these delta f segments
    dfreq = np.diff(freq, axis=0)
    midpoints = (x_L_watts_freq[:-1, :] + x_L_watts_freq[1:, :]) / 2

    # now find the overall power in each slice
    x_L_watts_overall = [
        10 * np.log10(np.sum((10 ** (midpoints[:, i] / 10)) * dfreq[:, i]))
        for i, temp in enumerate(x)]
    x_L_watts_overall = np.asarray(x_L_watts_overall)
    L_watts_overall2 = 10 * np.log10(np.sum(10 ** (x_L_watts_overall / 10)))

    # There is a slight discrepancy with the totals 1dB, so we adjust the
    # profile by this delta. Now we have to recalculate with this new norm
    # rel spectrum
    # TO MATCH EXACTLY THE MATLAB VERSION (MEAN of KSC, VANDY, and UNDEF)
    # dL_watts_overall = 2.3635
    # OTHERWISE IT WOULD BE:
    dL_watts_overall = L_watts_overall - L_watts_overall2

    norm_rel_spectrum += dL_watts_overall

    x_L_watts_freq = [norm_rel_spectrum + L_watts_x[i] +
                      10 * np.log10(xi) + 10 * np.log10(dx[i]) -
                      10 * np.log10(u_exhaust * a_ambient / a_exhaust)
                      for i, xi in enumerate(x)]
    x_L_watts_freq = np.asarray(x_L_watts_freq).T
    midpoints = (x_L_watts_freq[:-1, :] + x_L_watts_freq[1:, :]) / 2
    x_L_watts_overall = [
        10 * np.log10(np.sum((10 ** (midpoints[:, i] / 10)) * dfreq[:, i]))
        for i, temp in enumerate(x)]
    x_L_watts_overall = np.asarray(x_L_watts_overall)
    L_watts_overall2 = 10 * np.log10(np.sum(10 ** (x_L_watts_overall / 10)))
    f3 = octave(f1=20, f2=10000, n=1 / 3, ansi=True)
    x_L_watts_freq3 = [interp1d(freq[:, i],
                                x_L_watts_freq[:, i],
                                fill_value='extrapolate')(f3)
                       for i, temp in enumerate(x)]
    x_L_watts_freq3 = np.asarray(x_L_watts_freq3).T

    r = []
    for i, station in enumerate(stations):
        if deflection == 'Undeflected':
            r.append(x + station)
        else:
            this_station = []
            for slice in x:
                if slice <= xt:
                    this_station.append(slice + station)
                else:
                    this_station.append(
                        np.sqrt((slice - xt) ** 2 + (xt + station) ** 2))
            r.append(this_station)
    r = np.asarray(r).T
    # Define the transmission loss (dB) along each path to account for barriers.
    # This is freq dependent, but since the sound is dominated by flanking
    # for these exhaust noise problems, it is sufficient to put in an overall TL.
    # Here is also where we would enter the effect of  suppression.

    tl = []
    if tranmission_loss[deflection]:
        for station in stations:
            blocking_length = tranmission_loss[deflection][0]
            loss = tranmission_loss[deflection][1]
            tl_by_slice = []
            for slice in x:
                if slice > xt and slice <= (blocking_length + xt):
                    tl_by_slice.append(loss)
                else:
                    tl_by_slice.append(0)
            tl.append(np.asarray(tl_by_slice))
    else:
        tl = np.zeros(np.shape(r))
    if not isinstance(tl, np.ndarray):
        tl = np.asarray(tl).T

    # Define the directivities that describe the focusing or fractionalizing
    # of the sound power that can be radiated from the given slice due to
    # such things as a ground plane radiating half the sound back up,
    # a trench that is focusing sound into a quadrant, or an apperture that
    # is cutting off a fraction of the sound. These numbers are multipliers
    # of the sound power, so they are not dB's at this point.
    nominal, blockage = directivity[deflection][:]

    d = np.ones(np.shape(tl)) * nominal
    if blockage:
        for i, slice in enumerate(x):
            # assuming first slice always exposed as the rocket is lifted a
            # bit from MLP or similar GSE
            if i == 0:
                continue
            if slice < xt:
                d[i, :] = blockage
    # We now have all the pieces to compute the sound pressure spectrum at
    # each of the reciever locations (stations).
    df3 = (2 ** (1 / 5) * f3 - 2 ** (-1 / 6) * f3)

    L_pressure = []
    for i, station in enumerate(stations):
        L_pressure_slice = []
        for j, slice in enumerate(x):
            a = (x_L_watts_freq3[:, j]
                 + 10 * np.log10(df3)
                 - 10 * np.log10(4 * np.pi * r[j, i] ** 2)
                 + 10 * np.log10(d[j, i])
                 - tl[j, i])
            L_pressure_slice.append(a)

        L_pressure_slice = np.asarray(L_pressure_slice).T

        L_pressure_station = []
        for q, f in enumerate(f3):
            b = 10 * np.log10(np.sum(10 ** (L_pressure_slice[q, :] / 10)))
            L_pressure_station.append(b)

        L_pressure.append(np.asarray(L_pressure_station))

    the_data = {}
    for i, sta in enumerate(stations):
        the_data[sta] = np.column_stack([f3,
                                         L_pressure[i]])

    return the_data


def water_attenuation():
    pass
    # Dependent on launch site

if __name__ == '__main__':
    for d in ['Undeflected', 'VAFB', 'KSC']:
        test = liftoff(stations=[8, 22.5], deflection=d)