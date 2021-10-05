from dataSet.MovuinoDataSet import *

class SkateboardXXX3000DataSet(MovuinoDataSet):
    """

    """
    def __init__(self, filepath, nbPointfilter = 50):
        """

        :param filepath:
        :param nbPointfilter:
        """
        MovuinoDataSet.__init__(self, filepath, nbPointfilter)
        self.name = "skateboardXXX3000"

        self.velocity = [np.array([0, 0, 0])]
        self.pos = [np.array([0, 0, 0])]
        self.ThetaGyr = [np.array([0, 0, 0])]


    def DataManage(self):
        """

        :return:
        """
        MovuinoDataSet.DataManage(self)

        self.velocity = ef.EulerIntegration(self.acceleration, self.Te)
        self.ThetaGyr = ef.EulerIntegration(self.gyroscope, self.Te)
        self.pos = ef.EulerIntegration(self.velocity, self.Te)

        #------ list into np array conversion ------
        self.ThetaGyr = np.array(self.ThetaGyr)
        self.pos = np.array(self.pos)
        self.velocity = np.array(self.velocity)

        self.AddingRawData()
        self.StockIntoNewFile(self.filepath)

    def StockIntoNewFile(self, filepath):
        """

        :param filepath:
        :return:
        """
        self.rawData.to_csv(filepath + "_treated_" + self.name + ".csv", sep=",", index=False, index_label=False)

    def VisualizeData(self):
        self.PlotImage()
        plt.show()

    def PlotImage(self):
        """

        :return:
        """
        MovuinoDataSet.PlotImage(self)

        df.PlotVector(self.time, self.acceleration_lp, 'Acceleration filtered (LP)', 334)
        df.PlotVector(self.time, self.gyroscope_lp, "Gyrocope filtered (LP)", 336)
        df.PlotVector(self.time, self.ThetaGyr, 'Angle (integration of gyroscope) (deg)', 339)

        normAcc = plt.subplot(335)
        normAcc.plot(self.time, self.normAcceleration, color="black")
        normAcc.set_title("Norm Acceleration")

        patchX = mpatches.Patch(color='red', label='x')
        patchY = mpatches.Patch(color='green', label='y')
        patchZ = mpatches.Patch(color='blue', label='z')
        plt.legend(handles=[patchX, patchY, patchZ], loc="center right", bbox_to_anchor=(-2.5, 3.6), ncol=1)

    def AddingRawData(self):
        """

        :return:
        """
        MovuinoDataSet.AddingRawData(self)

        self.rawData["thetaGyrx"] = self.ThetaGyr[:, 0]
        self.rawData["thetaGyry"] = self.ThetaGyr[:, 1]
        self.rawData["thetaGyrz"] = self.ThetaGyr[:, 2]

        self.rawData["vx"] = self.velocity[:, 0]
        self.rawData["vy"] = self.velocity[:, 1]
        self.rawData["vz"] = self.velocity[:, 2]

        self.rawData["posx"] = self.pos[:, 0]
        self.rawData["posy"] = self.pos[:, 1]
        self.rawData["posz"] = self.pos[:, 2]

    @staticmethod
    def PlotCompleteFile(filepath, sep, dec):
        """

        :param filepath:
        :param sep:
        :param dec:
        :return:
        """
        data = pd.read_csv(filepath + ".csv", sep=sep, decimal=dec)
        timeList = data["time"]
        accel = [data["ax"], data["ay"], data["az"]]
        gyr = [data["gx"], data["gy"], data["gz"]]
        mag = [data["mx"], data["my"], data["mz"]]
        thetaGyr = [data["thetaGyrx"], data["thetaGyry"],data["thetaGyrz"]]
        pos = [data["posx"], data["posy"],data["posz"]]
        velocity = [data["vx"], data["vy"],data["vz"]]
        df.plotVect(timeList, accel, "Acceleration m/s2", 331)
        df.plotVect(timeList, gyr, "Gyroscope m/s", 332)
        df.plotVect(timeList, mag, "Magnetometer unit mag", 333)
        df.plotVect(timeList, velocity, "Velocity m/s", 334)
        df.plotVect(timeList, thetaGyr, "gyr integration deg", 335)
        df.plotVect(timeList, pos, "Position m", 337)

        plt.show()
        return

