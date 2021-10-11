import numpy as np
from scipy import signal

def MeanFilter(dat_to_filter, nbPoint):
    """

    :param dat_to_filter: rawData list to filter
    :param nbPoint: filtering level
    :return: list of filterd dat
    """
    meanDat = []

    for i in range(len(dat_to_filter)):
        meanVal = 0
        if (i < nbPoint):
            for k in range(i+1):
                meanVal += dat_to_filter[k]
            meanVal /= (i+1)
        else :
            for k in range(nbPoint):
                meanVal += dat_to_filter[i-k]

            meanVal /= nbPoint
        meanDat.append(meanVal)
    meanDat = np.array(meanDat)
    return meanDat

def LowPassFilter(x, y, Te, fc):
    """

    :param x: Absice
    :param y: Signal to filter
    :param Te: Periode d'écanhtillonage
    :param fc: Frequnce de coupure
    :return: signal filtre
    """
    tau = 1/(2*np.pi*fc)
    y_lp = [y[0]]
    for i in range(len(x)-1):
        y_lp.append(y_lp[i] + Te/tau * (y[i] - y_lp[i]))
    return y_lp

def LowPassButterworthFilter(b,a, sig):
    b,a = signal.butter(b,a)
    sig_filtre = signal.filtfilt(b,a, sig)
    return sig_filtre

def BandPassButterworthFilter(order,cutsLim,sig):
    b,a = signal.butter(order,cutsLim,btype = "bandpass")
    sig_filter = signal.filtfilt(b,a, sig)
    return sig_filter

def BandPassFilter():
    return 0

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs  # sampling frequency
    low = lowcut / nyq
    high = highcut / nyq
    sos = signal.butter(order, [low, high], analog=False, btype='band', output='sos')
    return sos


def butter_bandpass_filter(sig, lowcut, highcut, fs, order=5):
    sos = butter_bandpass(lowcut, highcut, fs, order=order)
    sig_filtered = signal.sosfilt(sos, sig)
    return sig_filtered