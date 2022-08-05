import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def Display(title, time, shape, *args):
    """

    :param title:
    :param time:
    :param args:
    :return:
    """
    nbGraph = len(args)
    for i in range(nbGraph):
        plt.subplot(shape * 10 + i+1)
        plt.plot(time, args[i][0], color = "red", label="x")
        plt.plot(time, args[i][1], color = "green", label="y")
        plt.plot(time, args[i][2], color = "blue", label="z")
        plt.legend()
    plt.title(title)
    plt.show()

def plotVector(t, v, title, pos):
    """

    :param t:
    :param v: List of Vector numpy
    :param title:
    :param pos:
    :return:
    """
    fig = plt.subplot(pos)
    fig.plot(t, v[:, 0], color="r", alpha=0.8, label="x")
    fig.plot(t, v[:, 1], color="green", alpha=0.8, label="y")
    fig.plot(t, v[:, 2], color="blue", alpha=0.8, label="z")
    fig.legend()
    fig.grid()
    fig.set_title(title)


def plotVect(t, v, title, pos):
    """

    :param t:
    :param vx:
    :param vy:
    :param vz:
    :param title:
    :param pos:
    :return:
    """
    fig = plt.subplot(pos)
    fig.plot(t, v[0], color="r",label="x")
    fig.plot(t, v[1], color="green",label="y")
    fig.plot(t, v[2], color="blue",label="z")
    fig.grid()
    fig.set_title(title)

def plot_tricks_recognition_result(complete_sequence, events_interval, label, Y_pred, save=False,path=""):
    plt.figure(figsize=(10, 20))
    time_list = np.array(complete_sequence.time)

    plotVect(time_list, complete_sequence.acceleration, 'Acceleration (m/s2)', 221)
    plt.xlabel("Temps (s)")
    plt.legend(loc='upper right')
    plt.grid()
    plt.subplot(223)
    plt.plot(time_list, complete_sequence.normAcceleration, label='Norme Accélération', color="black")
    plt.legend(loc='upper right')
    plt.grid()
    plotVect(time_list, complete_sequence.gyroscope, 'Gyroscope (deg/s)', 222)
    plt.xlabel("Temps (s)")
    plt.legend(loc='upper right')
    plt.grid()
    plt.subplot(224)
    plt.plot(time_list, complete_sequence.normGyroscope, label='Norme Accélération', color="black")
    plt.legend(loc='upper right')
    plt.grid()
    plt.show()

    plotVect(time_list, complete_sequence.gyroscope, 'Gyroscope (deg/s)', 211)
    for i, interval in enumerate(events_interval):
        i_start = interval[0]
        i_end = interval[1]
        plt.plot(
            [complete_sequence.time[i_start], complete_sequence.time[i_start], complete_sequence.time[i_end],
             complete_sequence.time[i_end],
             complete_sequence.time[i_start]], [-abs(max(complete_sequence.normGyroscope[i_start:i_end])),
                                                abs(max(complete_sequence.normGyroscope[i_start:i_end])),
                                                abs(max(complete_sequence.normGyroscope[i_start:i_end])),
                                                -abs(max(complete_sequence.normGyroscope[i_start:i_end])),
                                                -abs(max(complete_sequence.normGyroscope[i_start:i_end]))], color="r")
        plt.text(complete_sequence.time[i_start], max(complete_sequence.normGyroscope[i_start:i_end]) + 50,
                 "{}".format(label[Y_pred[i]], fontsize=20))
    plt.legend(loc='upper right')
    plt.xlabel("Temps (s)")
    plt.grid()
    plt.ylim([-max(complete_sequence.normGyroscope) * 1.2, max(complete_sequence.normGyroscope) * 1.2])
    plt.subplot(212)
    plt.plot(time_list, complete_sequence.normGyroscope, label="Norme gyroscope", color="black")
    plt.legend(loc='upper right')
    plt.grid()
    if save:
        plt.savefig(path)
    plt.show()
