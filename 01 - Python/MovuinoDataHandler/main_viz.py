import dataSet.SkateboardXXX3000DataSet as sk
import os
import numpy as np
import matplotlib.pyplot as plt
import tools.displayFunctions as df
import tools.integratinoFunctions as i

folderPath = "..\\..\\06 - Data\\Isolated_Tricks\\notTricks\\notTricks_success_7.csv"
#folderPath = "..\\..\\06 - Data\\Raw_sequences\\"
#folderPath = "..\\..\\06 - Data\\Raw_Sequences\\sesh_190322\\"


pop = sk.SkateboardXXX3000DataSet(folderPath)
print(pop.time[0])
print(pop.time[-1])
print(pop.nb_row)
pop.dispRawData()

"""
for (repertoire, sousRepertoires, fichiers) in os.walk(folderPath):
    for file in fichiers:
        f = os.path.join(repertoire, file)
        skateDataSet = sk.SkateboardXXX3000DataSet(f)
        print("Frequency rate : {}".format(round(1/skateDataSet.Te,3)))
        #skateDataSet.dispRawData()

        v = i.EulerIntegration(skateDataSet.acceleration[1,:], skateDataSet.Te)
        p = i.EulerIntegration(v, skateDataSet.Te)

        plt.subplot(311)
        plt.plot(skateDataSet.time, skateDataSet.acceleration[1, :])
        plt.subplot(312)
        plt.plot(skateDataSet.time, v)
        plt.subplot(313)
        plt.plot(skateDataSet.time, p)
        plt.show()


skateDataSet = sk.SkateboardXXX3000DataSet(folderPath)
dx = skateDataSet.Te
test=np.array([[3,2,1,0], [1,1,1,1],[0,1,4,9]])
x=skateDataSet.time
f = skateDataSet.normGyroscope
dydx = np.gradient(f,dx)
print(len(dydx))

plt.subplot(211)
plt.plot(x,f)
plt.subplot(212)
plt.plot(x,dydx)
plt.show()
"""