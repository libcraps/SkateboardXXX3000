from dataSet.MovuinoDataSet import *
import serial
class SkateboardXXX3000DataSet(MovuinoDataSet):
    """

    """
    def __init__(self, filepath, nbPointfilter):
        """

        :param filepath:
        :param nbPointfilter:
        """
        self.name = "skateboardXXX3000"

        self.filepath = filepath
        print("Reading : " + filepath)
        self.rawData = pd.read_csv(filepath, sep=",")
        self.processedData = self.rawData.copy()

        self.nbPointFilter = nbPointfilter

        self.time = []

        # basic data from the movuino
        self.acceleration = []
        self.gyroscope = []
        self.magnetometer = []

        # basic data filtered
        self.acceleration_lp = []
        self.gyroscope_lp = []
        self.magnetometer_lp = []

        # norms
        self.normAcceleration = [0]
        self.normGyroscope = [0]
        self.normMagnetometer = [0]

        #Integration values
        self.velocity = [np.array([0, 0, 0])]
        self.pos = [np.array([0, 0, 0])]
        self.ThetaGyr = [np.array([0, 0, 0])]

        # Time list in seconds
        self.time = list(self.rawData["time"])
        self.rawData["time"] = self.time

        # Sample rate
        self.Te = (self.time[-1] - self.time[0]) / (len(self.time))

        # Number of row
        self.nb_row = len(self.time)

        # ------ STOCK COLUMN OF DF IN VARIABLES ------
        for k in range(self.nb_row):  # We stock rawData in variables
            self.acceleration.append(np.array([self.rawData["ax"][k], self.rawData["ay"][k], self.rawData["az"][k]]))
            self.gyroscope.append(
                np.array([self.rawData["gx"][k], self.rawData["gy"][k], self.rawData["gz"][k]]) * 180 / np.pi)
            self.magnetometer.append(np.array([self.rawData["mx"][k], self.rawData["my"][k], self.rawData["mz"][k]]))

            if k < self.nb_row - 1:  # Calculation of the norm
                self.normAcceleration.append(np.linalg.norm(self.acceleration[k]))
                self.normGyroscope.append(np.linalg.norm(self.gyroscope[k]))
                self.normMagnetometer.append(np.linalg.norm(self.magnetometer[k]))

        self.acceleration = np.array(self.acceleration)
        self.gyroscope = np.array(self.gyroscope)
        self.magnetometer = np.array(self.magnetometer)




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

    def StockProcessedData(self, filepath):
        """

        :return:
        """
        self.processedData["normAccel"] = self.normAcceleration
        self.processedData["normMag"] = self.normMagnetometer
        self.processedData["normGyr"] = self.normGyroscope

        self.processedData["ax_filter"] = self.acceleration_lp[:, 0]
        self.processedData["ay_filter"] = self.acceleration_lp[:, 1]
        self.processedData["az_filter"] = self.acceleration_lp[:, 2]

        self.processedData["gx_filter"] = self.gyroscope_lp[:, 0] * 180 / np.pi
        self.processedData["gy_filter"] = self.gyroscope_lp[:, 1] * 180 / np.pi
        self.processedData["gz_filter"] = self.gyroscope_lp[:, 2] * 180 / np.pi

        self.processedData["mx_filter"] = self.magnetometer_lp[:, 0]
        self.processedData["my_filter"] = self.magnetometer_lp[:, 1]
        self.processedData["mz_filter"] = self.magnetometer_lp[:, 2]

        self.processedData["thetaGyrx"] = self.ThetaGyr[:, 0]
        self.processedData["thetaGyry"] = self.ThetaGyr[:, 1]
        self.processedData["thetaGyrz"] = self.ThetaGyr[:, 2]

        self.processedData["vx"] = self.velocity[:, 0]
        self.processedData["vy"] = self.velocity[:, 1]
        self.processedData["vz"] = self.velocity[:, 2]

        self.processedData["posx"] = self.pos[:, 0]
        self.processedData["posy"] = self.pos[:, 1]
        self.processedData["posz"] = self.pos[:, 2]
        self.processedData.to_csv(filepath + "_treated_" + self.name + ".csv", sep=",", index=False, index_label=False)

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
    def stockProcessedData(self, filepath):
        """

        :param self:
        :param folderpath:
        :return:
        """

        self.processedData = self.rawData.copy()

        self.processedData["normAccel"] = self.normAcceleration
        self.processedData["normMag"] = self.normMagnetometer
        self.processedData["normGyr"] = self.normGyroscope

        self.processedData["ax_filter"] = self.acceleration_lp[:, 0]
        self.processedData["ay_filter"] = self.acceleration_lp[:, 1]
        self.processedData["az_filter"] = self.acceleration_lp[:, 2]

        self.processedData["gx_filter"] = self.gyroscope_lp[:, 0] * 180 / np.pi
        self.processedData["gy_filter"] = self.gyroscope_lp[:, 1] * 180 / np.pi
        self.processedData["gz_filter"] = self.gyroscope_lp[:, 2] * 180 / np.pi

        self.processedData["mx_filter"] = self.magnetometer_lp[:, 0]
        self.processedData["my_filter"] = self.magnetometer_lp[:, 1]
        self.processedData["mz_filter"] = self.magnetometer_lp[:, 2]


        self.processedData.to_csv(filepath, sep=",", index=False, index_label=False)


    @staticmethod
    def MovuinoExtraction(serialPort, path):
        isReading = False
        ExtractionCompleted = False
        print("-> Opening serial port {}".format(serialPort))
        arduino = serial.Serial(serialPort, baudrate=115200, timeout=1.)
        line_byte = ''
        line_str = ''
        datafile = ''
        nbRecord = 1

        while ExtractionCompleted != True:
            line_byte = arduino.readline()
            line_str = line_byte.decode("utf-8")

            if "XXX_end" in line_str and isReading == True:
                isReading = False
                ExtractionCompleted = True
                print("End of data sheet")

                with open(path + "_" + str(nbRecord) + ".csv", "w") as file:
                    print("Add new file : {}".format(path + "_" + str(nbRecord) + ".csv"))
                    file.write(datafile)

            if "XXX_newRecord" in line_str and isReading == True:
                with open(path + "_" + str(nbRecord) + ".csv", "w") as file:
                    print("Add new file : {}".format(path + "_" + str(nbRecord) + ".csv"))
                    file.write(datafile)

                datafile = ''
                line_str = ''
                nbRecord += 1

            if (isReading):
                if line_str != '':
                    datafile += line_str.strip() + '\n'

            if ("XXX_beginning" in line_str):
                isReading = True
                print("Record begins")

    def DispRawData(self):
        time_list = self.time
        df.PlotVector(time_list, self.acceleration, 'Acceleration (m/s2)', 221)
        df.PlotVector(time_list, self.magnetometer, 'Magnetometer', 222)
        df.PlotVector(time_list, self.gyroscope, 'Gyroscope (deg/s)', 223)
        plt.show()

    def DispProcessedData(self):
        """
        Add processed data usefull for skateboarding
        :return:
        """
        time_list = self.time
        df.PlotVector(time_list, self.acceleration, 'Acceleration (m/s2)', 331)
        df.PlotVector(time_list, self.gyroscope, 'Gyroscope (deg/s)', 333)
        df.PlotVector(time_list, self.acceleration_lp, 'Acceleration filtered (LP)', 334)
        df.PlotVector(time_list, self.magnetometer_lp, 'Magnetometer filtered (LP)', 335)


        normAcc = plt.subplot(337)
        normAcc.plot(time_list, self.normAcceleration, color="black")
        normAcc.set_title("Norm Acceleration")


        plt.show()

