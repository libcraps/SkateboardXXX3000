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
        self.acceleration = np.array([self.rawData["ax"], self.rawData["ay"], self.rawData["az"]])
        self.gyroscope = np.array([self.rawData["gx"], self.rawData["gy"], self.rawData["gz"]]) * 180 / np.pi

        # norms
        self.normAcceleration = np.linalg.norm(self.acceleration, axis=0)
        self.normGyroscope = np.linalg.norm(self.gyroscope, axis=0)
        self.rawData["normAccel"] = self.normAcceleration
        self.rawData["normGyr"] = self.normGyroscope

        #Integration values
        self.velocity = [np.array([0, 0, 0])]
        self.pos = [np.array([0, 0, 0])]
        self.ThetaGyr = [np.array([0, 0, 0])]

        #self.interpolate_skate_data()
        self.interpolateData = self.rawData
        # Time list in seconds
        self.time = list(self.interpolateData["time"])
        self.interpolateData["time"] = self.time


        # Sample rate
        self.Te = (self.time[-1] - self.time[0]) / (len(self.time))

        # Number of row
        self.nb_row = len(self.time)



    def interpolate_skate_data(self, ecart_min=0.01):
        new_time = []
        interpolateDf = pd.DataFrame()
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

        interpolateDf["time"] = new_time
        interpolateDf["ax"] = ax_interp
        interpolateDf["ay"] = ay_interp
        interpolateDf["az"] = az_interp
        interpolateDf["gx"] = gx_interp
        interpolateDf["gy"] = gy_interp
        interpolateDf["gz"] = gz_interp

        return interpolateDf

    @staticmethod
    def movuinoExtraction(serialPort, folderpath, gen_filename):
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

    def dispRawData(self):
        time_list = self.time
        df.plotVector(time_list, self.acceleration, 'Acceleration (m/s2)', 221)
        df.plotVector(time_list, self.gyroscope, 'Gyroscope (deg/s)', 223)
        plt.subplot(224)
        plt.plot(time_list, self.normGyroscope, label="Norme gyroscope", color="black")
        plt.legend(loc='upper right')
        plt.subplot(222)
        plt.plot(time_list, self.normAcceleration, label='Norme Accélération',color="black")
        plt.legend(loc='upper right')
        plt.show()

    def dispProcessedData(self):
        """
        Add processed data usefull for skateboarding
        :return:
        """
        time_list = self.time
        df.plotVector(time_list, self.acceleration, 'Acceleration (m/s2)', 331)
        df.plotVector(time_list, self.gyroscope, 'Gyroscope (deg/s)', 333)
        df.plotVector(time_list, self.acceleration_lp, 'Acceleration filtered (LP)', 334)



        normAcc = plt.subplot(337)
        normAcc.plot(time_list, self.normAcceleration, color="black")
        normAcc.set_title("Norm Acceleration")


        plt.show()

