import os
import pandas as pd
import numpy as np
from ThermalConductivityOS.Moleculars import Moleculars
from ThermalConductivityOS.SingleMolecular import SingleMolecular




def existence_file(csv_path):
    if not os.path.exists(csv_path):
        raise IOError("File or directory doesn't exist")
     
    
def load_csv(csv_path):
    molecularsList = []
    
    existence_file(csv_path)
    data = pd.read_csv(csv_path,dtype={'c1':str,'c2':str},names=["MF","Name","100K","200K","300K","400K","500K","600K"])
    
    for index,row in data.iterrows():
        sm = SingleMolecular(str(row[0]),str(row[1]),np.array(row[2:],dtype=np.float64))
        molecularsList.append(sm)

    mObjects = Moleculars(data)
    return mObjects
 



