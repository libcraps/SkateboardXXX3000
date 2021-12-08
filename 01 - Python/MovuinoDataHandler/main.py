import dataSet.SkateboardXXX3000DataSet as sk
import tools.FilterMethods as fm
import tools.integratinoFunctions as ef
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal



############   SETTINGS   #############

device = 'skateboardXXX3000'  # devices available : skateboardXXX3000 / sensitivePen / globalDataSet
# choose btw : ollie, kickflip, heelflip, pop_shovit, fs_shovit, 360_flip
folderPath = "..\\..\\06 - Data\\Isolated_Tricks\\360_flip\\"
gen_filename = "record"  # generic name numbers will be added for duplicates

serialPort = 'COM6'

toExtract = False
toDataManage = False
toVisualize = True

filter = 5



# --------- Data Extraction from Movuino ----------
if toExtract:
    print("data extraction")
    sk.SkateboardXXX3000DataSet.MovuinoExtraction(serialPort, folderPath, gen_filename)

# -------- Data processing ----------------------
if toDataManage:
    for filename in os.listdir(folderPath):
        print("Processing : " + folderPath + filename)
        skateDataSet = sk.SkateboardXXX3000DataSet(folderPath + filename)
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
#Display
if toVisualize:
    for filename in os.listdir(folderPath):
        print("Processing : " + folderPath + filename)
        skateDataSet = sk.SkateboardXXX3000DataSet(folderPath + filename)
        #skateDataSet.DataManage()
        Te = skateDataSet.Te
        skateDataSet.DispRawData()
        """
        
        """

