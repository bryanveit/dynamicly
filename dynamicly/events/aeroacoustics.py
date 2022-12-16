import numpy as np
from dynamicly.misc.unit_conversion import (m_to_in, ft_to_m, m_to_ft,
                                            kg_per_m3_to_slug_per_ft3, )
from dynamicly.misc.octave import octave
from ambiance import Atmosphere
from scipy.interpolate import interp1d
from dynamicly.signal.calc_oaspl import calc_oaspl
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

spl_ref = 2.9e-9 * 144  # psi to psf, standard 20 microPa reference

flow_types = {
    1: 'Attached Turbulent Boundary Layer',
    2: 'Expansion Corner Separated Flow Plateau',
    3: 'Expansion Corner Separated Flow Reattachment',
    4: 'Compression Corner Separated Flow Plateau',
    5: 'Compression Corner Flow Separation or Reattachment Shock',
}
def c_atmosphere(altitude):
    # assumes altitude in feet
    altitude_meters = altitude * ft_to_m
    return Atmosphere(altitude_meters).speed_of_sound[0] * m_to_ft

def density_atmosphere(altitude):
    # assumes altitude in feet
    altitude_meters = altitude * ft_to_m
    return Atmosphere(altitude_meters).density[0] * kg_per_m3_to_slug_per_ft3

def viscosity_atmospheres(altitude):
    # assumes altitude in feet
    altitude_meters = altitude * ft_to_m
    return Atmosphere(altitude_meters).kinematic_viscosity[0] * (m_to_ft ** 2)

def wilby_flow_types(number=None):
    if number is not None:
        print(flow_types[number])
    else:
        for key, val in flow_types.items():
            print(f'{key} : {val}')

def aeroacoustics(stations, mach, altitude,
                  flow_type=1,
                  frustum_angle=None,
                  units='metric',
                  ansi=True):
    orig_station = stations
    # THE WILBY METHOD
    # http: // www.vibrationdata.com / tutorials2 / flow.pdf

    # the stations variable is expected to be the traditional definition of a
    # station for a launch vehicle, distance from the nozzle exit plane. However,
    # the wilby method is unique uses measurements relative
    # to the rocket nose, so make this correction within the code

    # if metric:
    # stations in meters, alitude in meters, density in kg/m3, angle in degrees

    # if english:
    # stations in inches, alitude in feet, density in % lb/in3, angle in degrees

    # now all stations, altitude, density in english units which the method
    # was defined using, do checks for physics validity

    if altitude < 0 or altitude > 65000:
        print('Altitude cannot be less than 0 ft or greater than 65000 ft.')
        return None
    if flow_type not in flow_types.keys():
        print('Flow type integer not recognized.')
        return None
    if flow_type == 4 or flow_type == 5:
        if frustum_angle is None:
            print('Frustum angle needed for flow types 4 and 5.')
            return None
        if mach < 1.0:
            print('Upstream mach must be >= 1.0 for flow types 4 and 5.')
            return None
    ############################################################################

    # F variable from Tom Irvine's paper assumeing Tw, wall temperature is
    # equal to Taw, adiabatic wall temperature
    F = 0.5 + (0.5 + 0.09 * mach ** 2) + 0.04 * mach ** 2
    c = c_atmosphere(altitude)  # speed of sound in ft/s
    v = c * mach  # free stream velocfity
    if v < 1.0:
        v = 1.0
    rho = density_atmosphere(altitude)  # density of atmo, slug/ft3
    q = 0.5 * rho * v ** 2  # dynamic pressure psi
    mu = viscosity_atmospheres(altitude)  # kinematic viscosity, ft2/s
    Re = [(sta / 12) * v / mu for sta in stations]
    delta_stars = [
        (sta / 12) * 0.0371 * Re[i] ** -0.2 * ((9 / 7) + 0.475 * mach ** 2) / (
                1 + 0.13 * mach ** 2) ** 0.64 for i, sta in enumerate(stations)]
    freq = octave(20, 10000)
    freq[-1] = 10000

    ############################################################################
    spl_dictionary = {}
    # prms is the root mean square oscillating pressure per wilby's method
    # poq is p over q
    for sta, delta_star in zip(orig_station, delta_stars):
        if flow_type == 1:
            prms = (0.01 / F) * q
            poq = prms / q
            constant = (((
                                 4 * poq ** 2 * F ** 1.433) * q ** 2 * delta_star / v) /
                        spl_ref ** 2)

            G = [(constant /
                  (1 + F ** 2.867 * (2 * np.pi * f * delta_star / v) ** 2))
                 for f in freq]

        elif flow_type == 2:
            poq_exp = 0.04 / (1 + mach ** 2)
            prms = poq_exp * q
            constant = (((4 * poq_exp ** 2 * 3 * F ** 1.433) * (
                    q ** 2 * delta_star / v)) / spl_ref ** 2)

            G = [(constant / (
                    1 + F ** 2.867 * (3 * 2 * np.pi * f * delta_star / v) ** 2))
                 for f in freq]

        elif flow_type == 3:
            poq_exp = 0.16 / (1 + mach ** 2)
            prms = poq_exp * q
            constant = (((4 * poq_exp ** 2 * 9 * F ** 1.433) * (
                    q ** 2 * delta_star / v)) / spl_ref ** 2)

            G = [(constant / (
                    1 + F ** 2.867 * (9 * 2 * np.pi * f * delta_star / v) ** 2))
                 for f in freq]
        elif flow_type == 4:
            frustum_angle *= (np.pi / 180)  # deg to radians
            theta = frustum_angle + np.arcsin(1 / mach)
            P2P1 = ((2.8 * mach ** 2 * (np.sin(theta)) ** 2 - 0.4) / 2.4)

            poq_comp = (0.006 / F) * P2P1
            comp = 10

            constant = (((4 * poq_comp ** 2 * comp * F ** 1.433) *
                         q ** 2 * delta_star / v) / spl_ref ** 2)
            G = [(constant / (1 + F ** 2.867 * (
                    comp * 2 * np.pi * f * delta_star / v) ** 2))
                 for f in freq]
        else:
            # flow type 5 because check earlier
            frustum_angle *= (np.pi / 180)  # deg to radians
            theta = frustum_angle + np.arcsin(1 / mach)
            P2P1 = ((2.8 * mach ** 2 * (np.sin(theta)) ** 2 - 0.4) / 2.4)
            poq_comp = ((-1.181 + 1.713 * P2P1 + 0.468 * P2P1 ** 2) * (
                    0.006 / F))
            comp = 30
            constant = (((4 * poq_comp ** 2 * comp * F ** 1.433) *
                         q ** 2 * delta_star / v) / spl_ref ** 2)
            G = [(constant / (1 + F ** 2.867 * (
                    comp * 2 * np.pi * f * delta_star / v) ** 2))
                 for f in freq]

        G_oct = [g * freq[i] * 0.2301 for i, g in
                 enumerate(G)]  # ??? what is this
        SPL = [10 * np.log10(g) for g in G_oct]
        spl_dictionary[sta] = np.column_stack([np.asarray(freq),
                                               np.asarray(SPL)])
    if ansi:
        f3 = octave(f1=20, f2=10000, n=1 / 3, ansi=True)
        spl_dictionary = {
            key: np.column_stack([f3,
                                  interp1d(val[:, 0], val[:, -1])(f3)])
            for key, val in spl_dictionary.items()
        }
    return spl_dictionary
    # answers differ slightly from matlab implementation due to using the
    # python library for the standard atmosphere


def wilby_parameters(trajectory_df, flow_type, station = None, units='metric'):
    # This requires a datraframe of trajectory information including altitude and
    # mach over time. Used to determin the maximum stage of oscillating pressure to
    # use in bounding the aeroacoustic vibration environment.
    # PROBABLY CAN BE SPED UP
    if units != 'metric':
        print('English/imperial units not implemented yet.')
        return None
    # find altitude and mach column name
    for col in trajectory_df.columns:
        if 'altitude' in col.lower():
            alt_key = col
        if 'mach' in col.lower():
            mach_key = col

    max_oaspl = 0
    max_index = 0
    if station is None:
        station = 1
    trajectory_df['OASPL (dB)'] = np.ones_like(trajectory_df.index, dtype=float)
    for i, row in trajectory_df.iterrows():
        altitude = row[alt_key]
        if units == 'metric' and altitude > (65000-1)*ft_to_m:
            continue
        mach = row[mach_key]
        spl = aeroacoustics([station, ], mach, altitude,
                            flow_type=flow_type,
                            frustum_angle=None,
                            units='metric',
                            ansi=False)[station]
        oaspl = calc_oaspl(spl)
        trajectory_df['OASPL (dB)'][i] = oaspl
        if oaspl > max_oaspl:
            max_oaspl = oaspl
            max_index = i
    series = trajectory_df.iloc[max_index]
    mach = trajectory_df.iloc[max_index][mach_key]
    altitude = trajectory_df.iloc[max_index][alt_key]

    return series, mach, altitude