import numpy as np

def smc(qtp=False, weight=50):
    # this really needs to be made more elegant
    if weight == 50:
        min_atp = np.column_stack([[20, 150, 800, 2000],
                                   [0.0053, .04, .04, 0.00644]])
        if qtp:
            min_qtp = np.column_stack([min_atp[:, 0],
                                       min_atp[:, -1] * (10 ** (6 / 10))])
            return min_qtp
        else:
            return min_atp

    elif weight == 100:
        min_atp = np.column_stack([[20, 75, 800, 2000],
                                   [0.0053, .02, .02, 0.0032]])
        if qtp:
            min_qtp = np.column_stack([min_atp[:, 0],
                                       min_atp[:, -1] * (10 ** (6 / 10))])
            return min_qtp
        else:
            return min_atp

    elif weight == 200:
        min_atp = np.column_stack([[20, 38, 800, 2000],
                                   [0.0053, .01, .01, 0.0016]])
        if qtp:
            min_qtp = np.column_stack([min_atp[:, 0],
                                       min_atp[:, -1] * (10 ** (6 / 10))])
            return min_qtp
        else:
            return min_atp
    else:
        print('this weight hasnt been defined yet')
        return None
