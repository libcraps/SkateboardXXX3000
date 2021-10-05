import serial
import dataSet.SensitivePenDataSet as sp
import dataSet.SkateboardXXX3000DataSet as sk
import dataSet.GlobalDataSet as gds
import dataSet.MovuinoDataSet as dm
import tools.DisplayFunctions as df
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal



############   SETTINGS   #############

device = 'skateboardXXX3000'  # devices available : skateboardXXX3000 / sensitivePen / globalDataSet

folderPath = "..\\data_usefull\\tricks_come\\"
fileName = "record"  # generic name numbers will be added for duplicates

serialPort = 'COM6'

toExtract = False
toDataManage = True
toVisualize = True

filter = 25

##### If only data manage
file_start = 15
nbRecord = 16

###################################

nb_files = 0

path = folderPath + fileName

c=0
# --------- Data Extraction from Movuino ----------
if toExtract:
    print("data extraction")
    isReading = False
    ExtractionCompleted = False
    arduino = serial.Serial(serialPort, baudrate=115200, timeout=1.)
    line_byte = ''
    line_str = ''
    datafile = ''
    nbRecord = 1

    while ExtractionCompleted != True:
        line_byte = arduino.readline()
        line_str = line_byte.decode("utf-8")

        if "XXX_end" in line_str and isReading == True :
            isReading = False
            ExtractionCompleted = True
            print("End of data sheet")

            with open(path + "_" + str(nbRecord) + ".csv", "w") as file:
                file.write(datafile)

        if "NEW RECORD" in line_str and isReading == True :
            print("Add new file")
            with open(path + "_" + str(nbRecord) + ".csv", "w") as file:
                file.write(datafile)

            datafile = ''
            line_str = ''
            nbRecord += 1

        if (isReading):
            if line_str != '':
                datafile += line_str.strip() + '\n'
                c+=1
                if c%1000==1:
                    print("Adding data")


        if ("XXX_beginning" in line_str):
            isReading = True
            print("Record begins")



if toDataManage:
    print(nbRecord)
    #nbRecord = 1
    for i in range(file_start, file_start+nbRecord+1):
        if (device == 'sensitivePen'):
            print("--- Processing : " + folderPath + fileName + "_" + str(i) + " --- ")
            dataSet = sp.SensitivePenDataSet(folderPath + fileName + "_" + str(i), filter)
        elif (device == 'skateboardXXX3000'):
            print("Processing : " + folderPath + fileName + "_" + str(i))
            dataSet = sk.SkateboardXXX3000DataSet(folderPath + fileName + "_" + str(i), filter)
        elif (device == 'globalDataSet'):
            print("Processing : " + folderPath + fileName + "_" + str(i))
            dataSet = gds.GlobalDataSet(folderPath + fileName + "_" + str(i), filter)
        else:
            print("No device matching")

        dataSet.DataManage()
        Te = dataSet.Te
        print("sample frequency : "+str(1/Te))

        if toVisualize:
            dataSet.VisualizeData()



