import serial
import dataSet.SensitivePenDataSet as sp
import dataSet.SkateboardXXX3000DataSet as sk
import dataSet.GlobalDataSet as gds
import dataSet.MovuinoDataSet as dm
import tools.DisplayFunctions as df
import tools.FilterMethods as fm
import tools.integratinoFunctions as ef
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

filter = 5

##### If only data manage
file_start =7
nbRecord = 16

###################################

nb_files = 0

path = folderPath

# --------- Data Extraction from Movuino ----------
if toExtract:
    print("data extraction")
    sk.SkateboardXXX3000DataSet.MovuinoExtraction(serialPort, path)

# -------- Data processing ----------------------
if toDataManage:
    for filename in os.listdir(folderPath):
        print("Processing : " + folderPath + filename)
        skateDataSet = sk.SkateboardXXX3000DataSet(folderPath + filename, filter)
        #skateDataSet.DataManage()
        Te = skateDataSet.Te
        print("sample frequency : "+str(1/Te))

        #Filtering
        skateDataSet.acceleration_lp = fm.MeanFilter(skateDataSet.acceleration, filter)
        skateDataSet.gyroscope_lp = fm.MeanFilter(skateDataSet.gyroscope, filter)
        skateDataSet.magnetometer_lp = fm.MeanFilter(skateDataSet.magnetometer, filter)

        #Integration of values :
        skateDataSet.velocity = ef.EulerIntegration(skateDataSet.acceleration, Te)
        skateDataSet.ThetaGyr = ef.EulerIntegration(skateDataSet.gyroscope, Te)
        skateDataSet.pos = ef.EulerIntegration(skateDataSet.velocity, Te)

        #Stock in processed.csv
        skateDataSet.stockProcessedData(folderPath+filename[:-4]+"_treated.csv")

        #Display
        if toVisualize:
            skateDataSet.VisualizeData()
            """

            """


