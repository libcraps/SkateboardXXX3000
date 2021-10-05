import pandas as pd
import numpy as np
import os
import serial

# --------- Data Extraction from Movuino ----------
def ExtractData(serialPort, path):

    """

    :param serialPort: port to listen
    :param path: path of extracted files
    :return: number of files created
    """

    isReading = False
    ExtractionCompleted = False
    arduino = serial.Serial(serialPort, baudrate=115200, timeout=1.)
    line_byte = ''
    line_str = ''
    datafile = []
    nbRecord = 1

    while ExtractionCompleted != True :
        line_byte = arduino.readline()
        line_str = line_byte.decode("utf-8")

        if ("XXX_end" in line_str and isReading == True):
            isReading = False
            ExtractionCompleted = True
            print("End of data sheet")

            with open(path + "_" + str(nbRecord) + ".csv", "w") as file:
                file.writelines(datafile)

        if ("NEW RECORD" in line_str and isReading == True):
            with open(path + "_" + str(nbRecord) + ".csv", "w") as file:
                file.writelines(datafile)

            datafile = []
            line_str = ''
            nbRecord += 1

        if (isReading):
            if line_str != '':
                datafile.append(line_str[:-1])
                print("Add Data")

        if ("XXX_beginning" in line_str):
            isReading = True

        return nbRecord
