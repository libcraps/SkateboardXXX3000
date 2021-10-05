from dataSet.MovuinoDataSet import *
import numpy as np

class SensitivePenDataSet(MovuinoDataSet):
    """Class that represent a data set of the sensitiv pen.

    """
    def __init__(self, filepath, nbPointfilter=25):
        """
        Constructor of the sensitivePen
        :param filepath: filepath of the raw data set
        :param nbPointfilter: level of filtering for the datamanage
        """
        MovuinoDataSet.__init__(self, filepath, nbPointfilter)
        self.name = "SensitivePen"

        # Relevant angle for the pen
        self.sensitivePenAngles = []

        self.posAngAcc = []
        self.initEulerAngles = []
        self.eulerAngles = []

    def DataManage(self):
        """
        Do the MovuinoDataSet.DataManage and a special DataManager= for the sensitivePen :
        We calculate the orientation (psi) and the inclination of the pen (theta)
        :return:
        """
        MovuinoDataSet.DataManage(self)

        # --- Getting initial euler angles
        initRotationMatrix = gam.rotationMatrixCreation(self.acceleration_lp[15], self.magnetometer_lp[15])
        self.initPsi = math.atan2(initRotationMatrix[0, 1], initRotationMatrix[0,0])

        for k in range(len(self.time)):
            # --- Getting rotation matrix from filtered data
            rotationMatrix = gam.rotationMatrixCreation(self.acceleration_lp[k], self.magnetometer_lp[k])

            # --- Get inclinaison of the pen (theta)
            self.posAngAcc.append(gam.getInclinaison(self.acceleration_lp[k]))
            theta = self.posAngAcc[k][0] - 90

            # --- getting oriantation of the pen (for psi)
            a00 = rotationMatrix[0, 0] # N.x
            a01 = rotationMatrix[0, 1] # E.x

            if (abs(theta) > 360): #set the lim to 80 but not usefull now
                psi = 0
            else:
                psi = (math.atan2(a01, a00) - self.initPsi) * 180/math.pi

                if -180 > psi >= -360:
                    psi += 360
                elif 180 < psi <= 360:
                    psi -= 360

            self.sensitivePenAngles.append(np.array([psi, theta]))

        self.posAngAcc = np.array(self.posAngAcc)
        self.sensitivePenAngles = np.array(self.sensitivePenAngles)

        self.rawData["psi"] = self.sensitivePenAngles[:, 0]
        self.rawData["theta"] = self.sensitivePenAngles[:, 1]

        MovuinoDataSet.AddingRawData(self)
        self.StockIntoNewFile(self.filepath)



    def StockIntoNewFile(self, filepath):
        self.rawData.to_csv(filepath + "_treated_" + self.name + ".csv", sep=",", index=False, index_label=False)

    def PlotImage(self):
        """
        Configure the plot figure
        :return:
        """
        MovuinoDataSet.PlotImage(self)

        df.PlotVector(self.time, self.acceleration_lp, 'Acceleration filtered (LP)', 334)
        df.PlotVector(self.time, self.magnetometer_lp, 'Magnetometer filtered (LP)', 335)

        normMag = plt.subplot(338)
        normMag.plot(self.time, self.normMagnetometer, color="black")
        normMag.set_title("Norm Magnetometer")

        normAcc = plt.subplot(337)
        normAcc.plot(self.time, self.normAcceleration, color="black")
        normAcc.set_title("Norm Acceleration")

        sensitivePenAngle = plt.subplot(336)
        sensitivePenAngle.plot(self.time, self.sensitivePenAngles[:, 0], color="red", label= 'psi')
        sensitivePenAngle.plot(self.time, self.sensitivePenAngles[:, 1], color="blue", label= 'theta')
        sensitivePenAngle.grid(b=True, which='major')
        sensitivePenAngle.grid(b=True, which='minor', color='#999999', linestyle='dotted')
        sensitivePenAngle.tick_params(axis='y', which='minor', labelsize=12, color="#999999")
        sensitivePenAngle.minorticks_on()
        sensitivePenAngle.set_yticks([-180, -90, 0, 90, 180])
        sensitivePenAngle.set_ylim(-220, 220)
        sensitivePenAngle.yaxis.set_minor_locator(MultipleLocator(45))
        sensitivePenAngle.legend(loc='upper right')
        sensitivePenAngle.set_title("Relevant angle (psi, theta) (deg)")

        """
        magCal = plt.subplot(338)
        magCal.plot(self.magnetometer_lp[:, 0], self.magnetometer_lp[:, 1], marker = "^", linestyle="None", color="red", label="X, Y")
        magCal.plot(self.magnetometer_lp[:, 0], self.magnetometer_lp[:, 2], marker = "o", linestyle="None", color="green", label="X, Z")
        magCal.plot(self.magnetometer_lp[:, 1], self.magnetometer_lp[:, 2], marker = "s", linestyle="None", color="blue", label="Y, Z")
        magCal.legend(loc='upper right')
        magCal.grid(True)
        magCal.set_title("Mag calibrattion")
        magCal.set_aspect('equal')
        """


        patchX = mpatches.Patch(color='red', label='x')
        patchY = mpatches.Patch(color='green', label='y')
        patchZ = mpatches.Patch(color='blue', label='z')
        plt.legend(handles=[patchX, patchY, patchZ], loc="upper right", bbox_to_anchor=(2.5,3.6),ncol=1)

    def VisualizeData(self):
        """
        Plot the figure
        :return:
        """
        self.PlotImage()
        plt.subplots_adjust(hspace=0.3, wspace=0.2)
        plt.show()


    @staticmethod
    def PlotCompleteFile(filepath, sep, dec):
        """

        :param filepath:
        :return:
        """

        data = pd.read_csv(filepath + ".csv", sep=sep, decimal=dec)
        timeList = data["time"]
        accel = [data["ax"], list(data["ay"]), list(data["az"])]
        gyr = [list(data["gx"]), list(data["gy"]), list(data["gz"])]
        mag = [list(data["mx"]), list(data["my"]), list(data["mz"])]
        psi = list(data["psi"])
        theta = list(data["theta"])
        print("NAAAAAAA")
        print(accel[0])

        df.plotVect(timeList, accel, "Acceleration m/s2", 221)
        df.plotVect(timeList, gyr, "Gyroscope m/s", 222)
        df.plotVect(timeList, mag, "Magnetometer unit mag", 223)

        sensitivePenAngle = plt.subplot(224)
        sensitivePenAngle.plot(timeList, psi, color="red", label='psi')
        sensitivePenAngle.plot(timeList, theta, color="blue", label='theta')
        sensitivePenAngle.grid(b=True, which='major')
        sensitivePenAngle.grid(b=True, which='minor', color='#999999', linestyle='dotted')
        sensitivePenAngle.tick_params(axis='y', which='minor', labelsize=12, color="#999999")
        sensitivePenAngle.minorticks_on()
        sensitivePenAngle.set_yticks([-180, -90, 0, 90, 180])
        sensitivePenAngle.yaxis.set_minor_locator(MultipleLocator(45))
        sensitivePenAngle.legend(loc='upper right')
        sensitivePenAngle.set_title("Relevant angle (psi, theta) (deg)")

        plt.show()






