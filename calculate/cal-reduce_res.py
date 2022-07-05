'''
2020/11/11
目的：把分辨率降低一倍
'''
import os
import numpy as np
import Ngl, Nio
import numpy.ma as ma
from geopy.distance import distance
import sys
from netCDF4 import Dataset
import math
import copy
sys.path.append("/data5/2019swh/mycode/module/")
from module_sun import *
from module_writenc import *
from attribute import *
import datetime

def reduce_resolution(variable,highlat,highlon):
    lat = variable.shape[2]
    lon = variable.shape[3]
    lat_out = int((lat+1)/2)
    lon_out = int(lon/2)
    variable_out = ma.zeros((61,42,lat_out,lon_out))
    lowlat = np.array([])
    lowlon = np.array([])
    for x in range(0,lon_out):
        lowlon = np.append(lowlon,highlon[2*x])
    for y in range(0,lat_out):
        lowlat = np.append(lowlat,highlat[2*y])

    for t in range(0,61):
        for lev in range(0,42):
            for y in range(0,lat_out):
                for x in range(0,lon_out):
                    variable_out[t,lev,y,x] = variable[t,lev,2*y,2*x]

    return variable_out,lowlat,lowlon


path = "/data5/2019swh/data/"
f1 = Nio.open_file(path+"composite3.nc")
lon = f1.variables["lon"][:]
lat = f1.variables["lat"][:]
level = f1.variables["level"][:]
time = f1.variables["time"][:]
h = f1.variables["H"][:]

h_out,llat,llon = reduce_resolution(h,lat,lon)


file = create_nc("/data5/2019swh/data/","lowresolution_H",time,level,llon,llat)
add_variables(file,"lowres_h",h_out,a_h)


file.close()



