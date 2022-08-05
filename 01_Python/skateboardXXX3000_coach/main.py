import os

import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

import dataSet.SkateboardXXX3000DataSet as sk
import tools.FilterMethods as fm
import tools.integratino_functions as ef

############   SETTINGS   #############

device = 'skateboardXXX3000'  # devices available : skateboardXXX3000 / sensitivePen / globalDataSet
# choose btw : ollie, kickflip, heelflip, pop_shovit, fs_shovit, 360_flip
folderPath = "..\\..\\06 - Data\\Isolated_Tricks\\360_flip\\"

toExtract = False
toDataManage = False
toVisualize = True

filter = 10

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
        skateDataSet.dispRawData()
        """
        
        """

