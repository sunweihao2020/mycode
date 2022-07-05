'''
2021/8/23
本代码对于模式输出进行插值
本代码仅为测试用
'''
import matplotlib
import matplotlib.pyplot as plt
import os
import numpy as np
from geopy.distance import distance
import numpy.ma as ma
import xarray as xr
import math
import json
import copy
import sys
from netCDF4 import Dataset
import datetime
import Ngl
sys.path.append("/home/sun/mycode/module/")
from module_sun import *
#from module_writenc import *
#from attribute import *

vars  =  ["KVH","DTV","LHFLX","OMEGA","OMEGAT","PRECT","PS","Q","SHFLX","T","TS","U","V","Z3"]

path1 = '/home/sun/cesm_output/control_intel/atm/hist/'
testfile = "control_intel.cam.h1.1980-05-31-00000.nc"
pnew     = np.array([1000, 975, 950, 925, 900, 875, 850, 825, 800, 775, 750, 700, 650, 600, 550, 500, 450, 400, 350, 300, 250, 225, 200, 175, 150, 125, 100, 70, 50, 30, 20, 10, 7, 5, 3, 2, 1])
a = cesm_vin2p(path1,testfile,pnew)
test  = xr.open_dataset(path1+testfile)
pnew     = np.array([1000, 975, 950, 925, 900, 875, 850, 825, 800, 775, 750, 700, 650, 600, 550, 500, 450, 400, 350, 300, 250, 225, 200, 175, 150, 125, 100, 70, 50, 30, 20, 10, 7, 5, 3, 2, 1])
test2    = Ngl.vinth2p(test.T.data,test.hyam.data,test.hybm.data,pnew,test.PS.data,1,test.P0.data,1,True)

t        = xr.DataArray(
    test2,
    coords={
        "lon":(["lon"],test.lon.data),
        "lat":(["lat"],test.lat.data),
        "time":(["time"],test.time.data),
        "lev":(["lev"],pnew)
    },
    dims=["time","lev","lat","lon"]
)
t.attrs  = test.T.attrs

ds       = xr.Dataset(
    {
        "temp":(["time","lev","lat","lon"],test2)
    },
    coords={
        "lon":(["lon"],test.lon.data),
        "lat":(["lat"],test.lat.data),
        "time":(["time"],test.time.data),
        "lev":(["lev"],pnew)
    },
)
ds.temp.attrs  =  test.T.attrs
