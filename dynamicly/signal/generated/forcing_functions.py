import numpy as np
from dynamicly.misc.interpolation import linear_interp


def haversine():
    pass # to be coded later

def ramp():
    pass # to be coded later

def smooth_ramp(length=1, dt=0.001, magnitude=1):
    # maybe this is haversine based
    copy_paste = np.column_stack([[0,
                                   0.1,
                                   0.2,
                                   0.3,
                                   0.4,
                                   0.5,
                                   0.6,
                                   0.7,
                                   0.8,
                                   0.9,
                                   1,
                                   1.1,
                                   1.2,
                                   1.3,
                                   1.4,
                                   1.5,
                                   1.6,
                                   1.7,
                                   1.8,
                                   1.9,
                                   2,
                                   2.1,
                                   2.2,
                                   2.3,
                                   2.4,
                                   2.5,
                                   2.6,
                                   2.7,
                                   2.8,
                                   2.9,
                                   3,
                                   3.1,
                                   3.2,
                                   3.3,
                                   3.4,
                                   3.5,
                                   3.6,
                                   3.7,
                                   3.8,
                                   3.9,
                                   4,
                                   ],
                                  [0,
                                   0.001541333,
                                   0.00615583,
                                   0.01381504,
                                   0.02447174,
                                   0.03806023,
                                   0.05449674,
                                   0.07367992,
                                   0.0954915,
                                   0.119797,
                                   0.1464466,
                                   0.175276,
                                   0.2061074,
                                   0.2387507,
                                   0.2730048,
                                   0.3086583,
                                   0.3454915,
                                   0.3832773,
                                   0.4217828,
                                   0.4607705,
                                   0.5,
                                   0.5392295,
                                   0.5782172,
                                   0.6167227,
                                   0.6545085,
                                   0.6913417,
                                   0.7269952,
                                   0.7612493,
                                   0.7938926,
                                   0.824724,
                                   0.8535534,
                                   0.880203,
                                   0.9045085,
                                   0.9263201,
                                   0.9455033,
                                   0.9619398,
                                   0.9755283,
                                   0.986185,
                                   0.9938442,
                                   0.9984587,
                                   1,
                                   ]])
    copy_paste = np.column_stack([copy_paste[:,0]/(4/length),
                                  copy_paste[:,1]])
    time = np.arange(0, length + dt, dt)
    function = linear_interp(copy_paste[:, 0], copy_paste[:, -1], time)
    function = np.column_stack([function[:,0],
                                function[:,-1]*magnitude])
    return function
