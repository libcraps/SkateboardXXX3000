

import numpy as np

def mean_time(dat):
    """
    Return the mean index of the incoming data
    :param dat:
    :return:
    """
    i_mean = 0
    E_t = 0
    E = 0
    for i in range(len(dat)):
        E_t += i*dat[i]**2
        E += dat[i]**2

    i_mean = int(E_t/E)
    return i_mean

def normalizeDat(dat):
    """
    Normalized the data using the energie of the signal
    :param dat:
    :return:
    """
    dat_normalized = dat.copy()

    norm_dat = np.sqrt(np.sum(dat**2))
    for i in range(len(dat)):
        dat_normalized[i]/=norm_dat

    return dat_normalized

def areaUnderCurve(x,y):
    """
    Calculate the area under a curve of a signal y given its timeLine x

    :param x:
    :param y:
    :return:
    """
    area = 0
    for k in range(len(x) - 1):
        dt = x[k + 1] - x[k]
        area += (y[k + 1] + y[k]) * dt / 2

    return area
