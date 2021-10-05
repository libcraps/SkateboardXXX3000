import threading
from threading import Thread
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np

class MovuinoDataSetThread(Thread):

    def __init__(self, filepath):

        self.filepath = filepath
        self.rawData = pd.read_csv(filepath + ".csv", sep=",")

        self.time = []

        # liste de vecteurs numpy
        self.acceleration = []
        self.gyroscope = []
        self.magnetometer = []

        self.normAcceleration = []
        self.normGyroscope = []
        self.normMagnetometer = []

        self.velocity = [np.array([0, 0, 0])]
        self.pos = [np.array([0, 0, 0])]
        self.posAng = [np.array([0, 0, 0])]

        posAngX = 0
        posAngY = 0
        posAngZ = 0

        posX = 0
        posY = 0
        posZ = 0

        vx = 0
        vy = 0
        vz = 0

        self.time = list(self.rawData["time"])

        self.nb_line = len(self.time)

        self.compteur_line = 0
        self.thread = Thread.__init__(self)

    def run(self):
        for k in range(self.nb_line):
            self.acceleration.append(np.array([self.rawData["ax"][k], self.rawData["ay"][k], self.rawData["az"][k]]))
            self.gyroscope.append(np.array([self.rawData["gx"][k], self.rawData["gy"][k], self.rawData["gz"][k]]))
            self.magnetometer.append(np.array([self.rawData["mx"][k], self.rawData["my"][k], self.rawData["mz"][k]]))

            self.normAcceleration.append(np.linalg.norm(self.acceleration[k]))
            self.normGyroscope.append(np.linalg.norm(self.gyroscope[k]))

            #---- integration -----
            if k < self.nb_line-1:
                pas = self.time[k+1] - self.time[k]

                posAngX = self.gyroscope[k][0]*pas*0.001*180/np.pi + self.posAng[k][0]  # 360/2np.pi
                posAngY = self.gyroscope[k][1]*pas*0.001*180/np.pi + self.posAng[k][1]
                posAngZ = self.gyroscope[k][2]*pas*0.001*180/np.pi + self.posAng[k][2]
                self.posAng.append(np.array([posAngX, posAngY, posAngZ]))

                vx = self.acceleration[k][0]*pas*0.001*180/np.pi + self.velocity[k][0]  # 360/2np.pi
                vy = self.acceleration[k][1]*pas*0.001*180/np.pi + self.velocity[k][1]
                vz = self.acceleration[k][2]*pas*0.001*180/np.pi + self.velocity[k][2]
                self.posAng.append(np.array([vx, vy, vz]))

                posX = self.velocity[k][0]*pas*0.001*180/np.pi + self.posX[k][0]  # 360/2np.pi
                posY = self.velocity[k][1]*pas*0.001*180/np.pi + self.posY[k][1]
                posZ = self.velocity[k][2]*pas*0.001*180/np.pi + self.posZ[k][2]
                self.pos.append(np.array([posX, posY, posZ]))



            if k == self.nb_line-1:
                self.ConvertArray()
                self.StockIntoNewFile()
                self.plotImage()

    def ConvertArray(self):
        self.acceleration = np.array(self.acceleration)
        self.gyroscope = np.array(self.gyroscope)
        self.magnetometer = np.array(self.magnetometer)

        self.posAng = np.array(self.posAng)
        self.pos = np.array(self.pos)
        self.velocity = np.array(self.velocity)

        self.rawData["normAccel"] = self.normAcceleration
        self.rawData["normGyr"] = self.normGyroscope

    def StockIntoNewFile(self):
        self.rawData.to_csv(self.filepath + "_treated" + ".csv", sep=",", index=False, index_label=False)

    def plotImage(self):

        a = plt.subplot(331)

        a.plot(self.time, self.acceleration[:, 0], color = "r")
        a.plot(self.time, self.acceleration[:, 1], color = "green")
        a.plot(self.time, self.acceleration[:, 2], color = "blue")
        a.set_title('Acceleration')

        g = plt.subplot(332)
        g.plot(self.time, self.self.gyroscope[:, 0], color="r")
        g.plot(self.time, self.self.gyroscope[:, 1], color="green")
        g.plot(self.time, self.self.gyroscope[:, 2], color="blue")
        g.set_title('Gyroscope')
        plt.show()

    def TrapezeIntegration(self, y1, y2, t1, t2, dt=0):
        return np.trapz([y1, y2], [t1, t2])