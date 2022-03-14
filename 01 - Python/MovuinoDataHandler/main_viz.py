import dataSet.SkateboardXXX3000DataSet as sk
import os
import numpy as np
import matplotlib.pyplot as plt
import tools.DisplayFunctions as df

folderPath = "..\\..\\06 - Data\\Isolated_Tricks\\"
#folderPath = "..\\..\\06 - Data\\Raw_sequences\\"
folderPath = "..\\..\\06 - Data\\Isolated_Tricks\\ollie\\ollie_1_interpolated_processed.csv"

skateDataSet = sk.SkateboardXXX3000DataSet(folderPath)
dx = skateDataSet.Te
test=np.array([[3,2,1,0], [1,1,1,1],[0,1,4,9]])
x=[0,1,2,3]
dydx = np.gradient(test, 1,axis=1)
print(test.shape)


df.plotVect(x,test,"Gyr",311)
df.plotVect(x,dydx,"Derivate Gyr",312)
plt.show()
