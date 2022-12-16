from dynamicly.misc.units import *
def vortex_shedding_freq(wind_speed,
                         wind_unit='mph',
                         diameter=72,
                         diameter_unit='in',
                         strouhal=1 / 5):
    # convert to consistent units
    # get wind speed to in/s
    if wind_unit == 'ips' or wind_unit == 'in/s':
        wind_speed = wind_speed
    elif wind_unit == 'mph':
        wind_speed *= mph_to_ips
    elif wind_unit == 'kts' or wind_unit == 'knots':
        wind_speed *= kts_to_ips
    elif wind_unit == 'fps' or wind_unit == 'ft/s':
        wind_speed *= fps_to_ips
    elif wind_unit == 'm/s' or wind_unit == 'mps':
        wind_speed *= mps_to_ips
    elif wind_unit == 'kph':
        wind_speed *= kph_to_ips
    else:
        print('This wind speed unit has not been implemented yet.')
        return
    # get diameter in inches:
    if diameter_unit == 'in' or diameter_unit == 'inch':
        diameter = diameter
    elif diameter_unit == 'ft' or diameter_unit == 'feet':
        diameter *= ft_to_in
    elif diameter_unit == 'm' or diameter_unit == 'meter':
        diameter *= m_to_in
    else:
        print('This diameter unit has not been implemented yet.')
        return

    return strouhal * (wind_speed / diameter)
