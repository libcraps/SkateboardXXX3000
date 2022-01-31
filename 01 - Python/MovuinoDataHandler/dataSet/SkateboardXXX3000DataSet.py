from dataSet.MovuinoDataSet import *
from scipy.interpolate import interp1d
import serial
import os

class SkateboardXXX3000DataSet():
    """

    """
    def __init__(self, filepath):
        """

        :param filepath:
        :param nbPointfilter:
        """
        self.name = "skateboardXXX3000"

        self.filepath = filepath
        print("Reading : " + filepath)
        self.rawData = pd.read_csv(filepath, sep=",")
        self.processedData = self.rawData.copy()
        self.interpolateData = pd.DataFrame()
        self.time = []

        # basic data from the movuino
        self.acceleration = []
        self.gyroscope = []

        # basic data filtered
        self.acceleration_lp = []
        self.gyroscope_lp = []

        # norms
        self.normAcceleration = []
        self.normGyroscope = []

        #Integration values
        self.velocity = [np.array([0, 0, 0])]
        self.pos = [np.array([0, 0, 0])]
        self.ThetaGyr = [np.array([0, 0, 0])]

        self.interpolate_skate_data()

        # Time list in seconds
        self.time = list(self.interpolateData["time"])
        self.interpolateData["time"] = self.time
        print(len(self.time))


        # Sample rate
        self.Te = (self.time[-1] - self.time[0]) / (len(self.time))

        # Number of row
        self.nb_row = len(self.time)

        #Linear interpolation if missing data :

        # ------ STOCK COLUMN OF DF IN VARIABLES ------
        for k in range(self.nb_row):  # We stock rawData in variables
            self.acceleration.append(np.array([self.interpolateData["ax"][k], self.interpolateData["ay"][k], self.interpolateData["az"][k]]))
            self.gyroscope.append(
                np.array([self.interpolateData["gx"][k], self.interpolateData["gy"][k], self.interpolateData["gz"][k]]) * 180 / np.pi)

            self.normAcceleration.append(np.linalg.norm(self.acceleration[k]))
            self.normGyroscope.append(np.linalg.norm(self.gyroscope[k]))

        self.acceleration = np.array(self.acceleration)
        self.gyroscope = np.array(self.gyroscope)

        self.interpolateData["normAccel"] = self.normAcceleration
        self.interpolateData["normGyr"] = self.normGyroscope

    def interpolate_skate_data(self, ecart_min=0.01):
        new_time = []
        time = self.rawData["time"]
        # ------ CREATION D'UNE NOUVELLE LISTE DE TEMPS -----
        for k in range(len(time) - 1):
            t_0 = time[k]
            t_1 = time[k + 1]
            dt = t_1 - t_0
            new_time.append(time[k])
            if dt > ecart_min:
                nb_pt_lost = round(dt / ecart_min - 1)
                for i in range(1, nb_pt_lost + 1):
                    new_time.append(time[k] + i * ecart_min)

        xp = time
        ax = self.rawData["ax"]
        ay = self.rawData["ay"]
        az = self.rawData["az"]
        gx = self.rawData["gx"]
        gy = self.rawData["gy"]
        gz = self.rawData["gz"]

        f = interp1d(xp, ax)
        ax_interp = f(new_time)
        f = interp1d(xp, ay)
        ay_interp = f(new_time)
        f = interp1d(xp, az)
        az_interp = f(new_time)
        f = interp1d(xp, gx)
        gx_interp = f(new_time)
        f = interp1d(xp, gy)
        gy_interp = f(new_time)
        f = interp1d(xp, gz)
        gz_interp = f(new_time)

        self.interpolateData["time"] = new_time
        self.interpolateData["ax"] = ax_interp
        self.interpolateData["ay"] = ay_interp
        self.interpolateData["az"] = az_interp
        self.interpolateData["gx"] = gx_interp
        self.interpolateData["gy"] = gy_interp
        self.interpolateData["gz"] = gz_interp

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
        self.processedData["normGyr"] = self.normGyroscope

        self.processedData["ax_filter"] = self.acceleration_lp[:, 0]
        self.processedData["ay_filter"] = self.acceleration_lp[:, 1]
        self.processedData["az_filter"] = self.acceleration_lp[:, 2]

        self.processedData["gx_filter"] = self.gyroscope_lp[:, 0]
        self.processedData["gy_filter"] = self.gyroscope_lp[:, 1]
        self.processedData["gz_filter"] = self.gyroscope_lp[:, 2]

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
        thetaGyr = [data["thetaGyrx"], data["thetaGyry"],data["thetaGyrz"]]
        pos = [data["posx"], data["posy"],data["posz"]]
        velocity = [data["vx"], data["vy"],data["vz"]]
        df.plotVect(timeList, accel, "Acceleration m/s2", 331)
        df.plotVect(timeList, gyr, "Gyroscope m/s", 332)
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
        self.processedData["normGyr"] = self.normGyroscope

        self.processedData["ax_filter"] = self.acceleration_lp[:, 0]
        self.processedData["ay_filter"] = self.acceleration_lp[:, 1]
        self.processedData["az_filter"] = self.acceleration_lp[:, 2]

        self.processedData["gx_filter"] = self.gyroscope_lp[:, 0]
        self.processedData["gy_filter"] = self.gyroscope_lp[:, 1]
        self.processedData["gz_filter"] = self.gyroscope_lp[:, 2]

        self.processedData["gx"] = self.gyroscope[:, 0]
        self.processedData["gy"] = self.gyroscope[:, 1]
        self.processedData["gz"] = self.gyroscope[:, 2]

        self.processedData["thetaGyrx"] = self.ThetaGyr[:, 0]
        self.processedData["thetaGyry"] = self.ThetaGyr[:, 1]
        self.processedData["thetaGyrz"] = self.ThetaGyr[:, 2]

        self.processedData["vx"] = self.velocity[:, 0]
        self.processedData["vy"] = self.velocity[:, 1]
        self.processedData["vz"] = self.velocity[:, 2]

        self.processedData["posx"] = self.pos[:, 0]
        self.processedData["posy"] = self.pos[:, 1]
        self.processedData["posz"] = self.pos[:, 2]
        print("Stocking data in : " + filepath)
        self.processedData.to_csv(filepath, sep=",", index=False, index_label=False)


    @staticmethod
    def MovuinoExtraction(serialPort, folderpath, gen_filename):
        isReading = False
        ExtractionCompleted = False
        print("-> Opening serial port {}".format(serialPort))
        arduino = serial.Serial(serialPort, baudrate=115200, timeout=1.)
        line_byte = ''
        line_str = ''
        datafile = ''
        nbRecord = 1

        filename = gen_filename + "_" + str(nbRecord) + ".csv"
        dir = os.path.dirname(folderpath)
        if not os.path.exists(dir):
            os.makedirs(dir)
        while ExtractionCompleted != True:
            line_byte = arduino.readline()
            line_str = line_byte.decode("utf-8")

            if "XXX_end" in line_str and isReading == True:
                isReading = False
                ExtractionCompleted = True
                print("End of data sheet")

                with open(folderpath + filename + ".csv", "w") as file:
                    print("Add new file : {}".format(folderpath + filename))
                    file.write(datafile)

            if "XXX_newRecord" in line_str and isReading == True:
                with open(folderpath +filename, "w") as file:
                    print("Add new file : {}".format(folderpath + filename))
                    file.write(datafile)

                datafile = ''
                line_str = ''
                nbRecord += 1
                filename = gen_filename + "_" + str(nbRecord) + ".csv"

            if (isReading):
                if line_str != '':
                    datafile += line_str.strip() + '\n'

            if ("XXX_beginning" in line_str):
                isReading = True
                print("Record begins")

    def DispRawData(self):
        time_list = self.time
        df.PlotVector(time_list, self.acceleration, 'Acceleration (m/s2)', 221)
        df.PlotVector(time_list, self.gyroscope, 'Gyroscope (deg/s)', 223)
        plt.subplot(224)
        plt.plot(time_list, self.normGyroscope, label="Norme gyroscope", color="black")
        plt.legend(loc='upper right')
        plt.subplot(222)
        plt.plot(time_list, self.normAcceleration, label='Norme Accélération',color="black")
        plt.legend(loc='upper right')
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



        normAcc = plt.subplot(337)
        normAcc.plot(time_list, self.normAcceleration, color="black")
        normAcc.set_title("Norm Acceleration")


        plt.show()

