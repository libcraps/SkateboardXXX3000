import numpy as np

def array_gyr_normalize(rawData):
    return np.array([rawData["gx_normalized"], rawData["gy_normalized"], rawData["gz_normalized"]])
