import dataSet.SkateboardXXX3000DataSet as sk

############   SETTINGS   #############
device = 'skateboardXXX3000'  # devices available : skateboardXXX3000 / sensitivePen / globalDataSet

folderPath = "..\\..\\06 - Data\\sesh_011221\\"
gen_filename = "record"  # generic name, numbers will be added for duplicates

serialPort = 'COM6'

# --------- Data Extraction from Movuino ----------

print("data extraction")
sk.SkateboardXXX3000DataSet.MovuinoExtraction(serialPort, folderPath, gen_filename)



