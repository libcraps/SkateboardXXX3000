import numpy as np
from scipy import signal

def MeandDat(rawDat, nbPointFilter, listMean):
    meanDat = np.array([0.,0.,0.])
    listMean.append(rawDat)

    if len(listMean) - nbPointFilter > 0:
        # remove oldest data if N unchanged(i=0 removed)
        # remove from 0 to rawdat.length - N + 1 if new N < old N
        for i in range(len(listMean) - nbPointFilter) :
            listMean.pop(0)

    for k in range(len(listMean)):
        meanDat += listMean[k]
    meanDat /= len(listMean)
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