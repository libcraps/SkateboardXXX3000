import matplotlib.pyplot as plt

def Display(title, time, *args):

    nbGraph = len(args)
    for i in range(nbGraph):
        plt.subplot(nbGraph, 1, i+1)
        plt.plot(time, args[i][0], label="x")
        plt.plot(time, args[i][1], label="y")
        plt.plot(time, args[i][2], label="z")
        plt.legend()
    plt.title(title)
    plt.show()
