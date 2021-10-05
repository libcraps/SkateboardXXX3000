import matplotlib.pyplot as plt
import pandas as pd

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

def PlotVector(t, v, title, pos):
    """

    :param t:
    :param v: List of Vector numpy
    :param title:
    :param pos:
    :return:
    """
    fig = plt.subplot(pos)
    fig.plot(t, v[:, 0], color="r")
    fig.plot(t, v[:, 1], color="green")
    fig.plot(t, v[:, 2], color="blue")
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
    fig.plot(t, v[0], color="r")
    fig.plot(t, v[1], color="green")
    fig.plot(t, v[2], color="blue")
    fig.set_title(title)
