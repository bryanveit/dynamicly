
################################################################################
# LENGTH
################################################################################
m_to_in = 39.3701
in_to_m = 1 / 39.3701

m_to_ft = m_to_in / 12
ft_to_m = in_to_m * 12
ft_to_in = 12
################################################################################
# VELOCITY
################################################################################
mph_to_ips = 17.6
kts_to_ips = 20.2537
fps_to_ips = ft_to_in
mps_to_ips = 39.3701
kph_to_ips = 10.9361

################################################################################
# ACCELERATION
################################################################################
# standards
g_m = 9.80665
g_in = g_m * m_to_in  # 386.1
g_ft = g_m * m_to_ft  # 32.17

################################################################################
# MASS
################################################################################
kg_to_slich = 1 / 175.126836
kg_to_snail = 1 / 175.126836
kg_to_blob = 1 / 175.126836

slinch_to_kg = 175.126836
snail_to_kg = 175.126836
blob_to_kg = 175.126836

slugs_to_slinch = 1 / 12
slinch_to_slugs = 12  # 1 snail = 12 slugs obviously

kg_to_slug = kg_to_slich * 12
slug_to_kg = 1 / kg_to_slug

lbm_to_slug = 1 / g_ft
lbm_to_slinch = lbm_to_slug / 12
slug_to_lbm = g_ft  # 32.174
slinch_to_lbm = 1 / lbm_to_slinch

lbm_to_kg = 0.453592  # lbm_to_slug*slug_to_kg
kg_to_lbm = 1 / lbm_to_kg

################################################################################
# DENSITY
################################################################################
kg_per_m3_to_slug_per_ft3 = 0.0019403203319541
slug_per_ft3_to_slug_per_in3 = (1 / 12 ** 3)

kg_per_m3_to_slinch_per_in3 = (
        kg_per_m3_to_slug_per_ft3
        * slug_per_ft3_to_slug_per_in3
        * slugs_to_slinch)

kg_per_m3_to_lbm_per_in3 = (
    kg_to_lbm
    *(1/m_to_in**3)
)

kg_per_m3_to_lbm_per_ft3 = (
    kg_to_lbm
    *(1/m_to_ft**3)
)

lbm_per_in3_to_kg_per_m3 = 1/kg_per_m3_to_lbm_per_in3

# now do lbs per...
# ...


################################################################################
# MASS MOMENT OF INERTIA
################################################################################
kg_m2_to_slinch_in2 = (
        kg_to_slich *
        m_to_in ** 2
)

slinch_in2_to_kg_m2 = (
        1 / kg_m2_to_slinch_in2
)

kg_m2_to_slug_ft2 = (
        kg_to_slug *
        m_to_ft ** 2
)

lbm_in2_to_slinch_in2 = lbm_to_slinch

lbm_ft2_to_slinch_in2 = (lbm_to_slinch * 12)

lbm_in2_to_kg_m2 = (
        lbm_to_kg *
        in_to_m ** 2
)

################################################################################
# PRESSURE
################################################################################
Pa_to_psi = 0.000145038
psi_to_Pa = 1/Pa_to_psi

################################################################################
################################################################################
################################################################################

# FEMAP/NASTRAN work is "unitless" relying on consistent unit systems
# throughout tracked by the user. Historically at Firefly a lbf, inches,
# seconds baseline has been used. This leads to the following units for
# various engineering  quanities:

# Length = inch
# Force = lbf
# Pressure/Elastic Modulus = psi (lbf/in^2)
# Mass = lbf*s^2/in  (AKA a slinch, blob, snail.... 1 snail = 12 slug... ffs)
# Density = lbf*s^2/in^4 (I guess you could call this slinch per cubic inch)
# Acceleration = in/s^2   ( 1G = 386.1 in/s^2)

# Alternately a metric based system could be used and might be pursued in the
# future - other disciplines like GNC and Aero use metric. There are pros and
# cons. Mass and density are dealt with a lot in setting up a model, and the
# current English unit system has very non-intuitive units for these IMO. One
# can use the WTMASS paramter to get around this but that's messy. The system
# works better if interested in stress analysis

# Regardless it is important to understand accelerations outputed by a
# NASTRAN solve will not be in G's and will need to be converted

# http://www.jefflewis.net/blog/2015/11/weird_engineering_unit_-_the_s.html
# Quote:
# An alternate term for this measure is the snail. It is nicknamed after the
# slug. It is normally defined as 1lbf/g where g is in 386inch/s^2. So a 1 lbm
# or lbf object would have a value of 1 snails. Alternately,
# 1 snail * 1 g (as inch/s^2) = 1 lbf
# The whole would not come up if it were not for the dynamicists.
# Stress guys are happy to work in inch, lbf, and g's. Everything else is
# derived from there. Dynamicists however have to use mass. So the whole
# system is damned when they have to blend.
