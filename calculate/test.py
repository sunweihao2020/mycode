import os
import numpy as np
import numpy.ma as ma
import Ngl, Nio
from netCDF4 import Dataset
file = open("/data5/2019swh/data/5d.txt","r")
file_data = file.readlines()
data = np.loadtxt("/data5/2019swh/data/5d.txt")
r = np.zeros((73,312))
for x in range(0,73):
    for y in range(0,42):
        r[x,:] += data[x+y*73,:]/42
