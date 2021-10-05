from dataSet.MovuinoDataSet import *

class GlobalDataSet(MovuinoDataSet):
    """
    Class created mainly for debugging, it has for purpose to stock most of the data that we may need
    """

    def __init__(self, filepath, nbPointfilter = 25):
        """

        :param filepath:
        :param nbPointfilter:
        """
        MovuinoDataSet.__init__(self, filepath, nbPointfilter)

        self.name = "globalDataSet"

        self.velocity = [np.array([0, 0, 0])]
        self.pos = [np.array([0, 0, 0])]
        self.ThetaGyr = [np.array([0, 0, 0])]

        self.posAngAcc = []
        self.rotationMatrix = []
        self.angleTest = []

        self.e1 = []
        self.e2 = []
        self.e3 = []

    def DataManage(self):
        """
        Calculate
        :return:
        """
        MovuinoDataSet.DataManage(self)

        # --- Getting initial euler angles
        for k in range(len(self.time)):
            #Get inclinaison of pen
            inc = gam.getInclinaison(self.acceleration_lp[k])
            self.posAngAcc.append(inc)

            #--- Getting euler angles from filtered data
            rotMat = gam.rotationMatrixCreation(self.acceleration_lp[k], self.magnetometer_lp[k])
            self.rotationMatrix.append(rotMat)

            a00 = rotMat[0, 0]
            a10 = rotMat[1, 0]
            a20 = rotMat[2, 0]
            a01 = rotMat[0, 1]
            a11 = rotMat[1, 1]
            a21 = rotMat[2, 1]
            a02 = rotMat[0, 2]
            a12 = rotMat[1, 2]
            a22 = rotMat[2, 2]

            theta = (inc[0]-90)

            if (abs(theta)>360):
                psi = 0
            else:
                psi = math.atan2(a01, a00) * 180/math.pi

            self.angleTest.append(np.array([theta, psi]))
            self.e1.append(np.array([a00, a10, a20]))
            self.e2.append(np.array([a01, a11, a21]))
            self.e3.append(np.array([a02, a12, a22]))

        self.angleTest = np.array(self.angleTest)
        self.e1 = np.array(self.e1)
        self.e2 = np.array(self.e2)
        self.e3 = np.array(self.e3)

        df.PlotVector(self.time, self.e1, "x", 337)
        df.PlotVector(self.time, self.e2, "y", 338)
        df.PlotVector(self.time, self.e3, "z", 339)



        self.velocity = ef.EulerIntegration(self.acceleration, self.Te)
        self.ThetaGyr = ef.EulerIntegration(self.gyroscope, self.Te)
        self.pos = ef.EulerIntegration(self.velocity, self.Te)

        #------ list into np array conversion ------
        self.ThetaGyr = np.array(self.ThetaGyr)
        self.pos = np.array(self.pos)
        self.velocity = np.array(self.velocity)
        self.posAngAcc = np.array(self.posAngAcc)
        self.rotationMatrix = np.array(self.rotationMatrix)

        # file managing
        self.AddingRawData()
        self.StockIntoNewFile(self.filepath)

    def AddingRawData(self):
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

        """
        a correspond to the rotation matrix : 
        [a00 a01 a02]
        [a10 a11 a12]
        [a20 a21 a22]
        """
        self.rawData["a00"] = self.rotationMatrix[:,0][:,0]
        self.rawData["a01"] = self.rotationMatrix[:,0][:,1]
        self.rawData["a02"] = self.rotationMatrix[:,0][:,2]
        self.rawData["a10"] = self.rotationMatrix[:,1][:,0]
        self.rawData["a11"] = self.rotationMatrix[:,1][:,1]
        self.rawData["a12"] = self.rotationMatrix[:,1][:,2]
        self.rawData["a20"] = self.rotationMatrix[:,2][:,0]
        self.rawData["a21"] = self.rotationMatrix[:,2][:,1]
        self.rawData["a22"] = self.rotationMatrix[:,2][:,2]

    def StockIntoNewFile(self, filepath):
        self.rawData.to_csv(filepath + "_treated_" + self.name + ".csv", sep=",", index=False, index_label=False)

    def VisualizeData(self):
        self.PlotImage()
        plt.show()

    def PlotImage(self):
        MovuinoDataSet.PlotImage(self)

        #df.PlotVector(self.time, self.acceleration_lp, 'Acceleration filtered (LP)', 334)
        #df.PlotVector(self.time, self.magnetometer_lp, 'Magnetometer filtered (LP)', 335)

        normMag = plt.subplot(335)
        normMag.plot(self.time, self.normMagnetometer, color="black")
        normMag.set_title("Norm Magnetometer")

        normAcc = plt.subplot(334)
        normAcc.plot(self.time, self.normAcceleration, color="black")
        normAcc.set_title("Norm Acceleration")

        patchX = mpatches.Patch(color='red', label='x')
        patchY = mpatches.Patch(color='green', label='y')
        patchZ = mpatches.Patch(color='blue', label='z')
        plt.legend(handles=[patchX, patchY, patchZ], loc="center right", bbox_to_anchor=(-2.5,3.6),ncol=1)

    @staticmethod
    def PlotCompleteFile(filepath, sep, dec):
        """

        :param filepath:
        :return: --
        """
        data = pd.read_csv(filepath + ".csv", sep=sep, decimal=dec)
        timeList = data["time"]
        accel = np.array([data["ax"], data["ay"], data["az"]])
        gyr = np.array([data["gx"], data["gy"], data["gz"]])
        mag = np.array([data["mx"], data["my"], data["mz"]])


        df.plotVect(timeList, accel, "Acceleration m/s2", 331)
        df.plotVect(timeList, gyr, "Gyroscope deg/s", 332)
        df.plotVect(timeList, mag, "Magnetometer mag unit", 333)
        plt.show()

        return