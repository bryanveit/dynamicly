import numpy as np

def gevs_vibe(qtp=False, weight=50):
    if weight < 50:
        weight = 50

    if weight > 400:
        weight = 400

    if weight == 50:
        min_atp = np.column_stack([[20, 50, 800, 2000],
                                   [0.013, .08, .08, 0.013]])
        if qtp:
            min_qtp = np.column_stack([min_atp[:, 0],
                                       min_atp[:, -1] * 2])
            return min_qtp
        else:
            return min_atp

    if weight > 50:
        min_atp = np.column_stack([[20, 50, 800, 2000],
                                   [0.013, .08, .08, 0.013]])

        db = 10 * np.log10(weight / 50)
        scaled_atp = np.column_stack([min_atp[:, 0],
                                      min_atp[:, -1] / (10 ** (db / 10))])

        if qtp:
            scaled_qtp = np.column_stack([scaled_atp[:, 0],
                                          scaled_atp[:, -1] * 2])
            if scaled_qtp[0, 1] < 0.01:
                scaled_qtp[0, 1] = 0.01
            if scaled_qtp[-1, 1] < 0.01:
                scaled_qtp[-1, 1] = 0.01
            return scaled_qtp
        else:
            if scaled_atp[0, 1] < 0.01:
                scaled_atp[0, 1] = 0.01
            if scaled_atp[-1, 1] < 0.01:
                scaled_atp[-1, 1] = 0.01
            return scaled_atp


def gevs_workmanship():
    pass

def gevs_shock():
    # This is not GEVs but whats in the PUG
    return np.column_stack([[100, 1000, 10000],
                            [30, 1000, 1000]])

