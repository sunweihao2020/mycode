'''
2021/8/24
本代码对于模式输出进行插值
实验为control_intel
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

path       =     '/home/sun/cesm_output/replace_india8/atm/hist/'
path_out   =     '/home/sun/cesm_output/replace_india8/atm/vinth2p/'
file_list  =     os.listdir(path)
file_list.sort()

pnew     = np.array([1000, 975, 950, 925, 900, 875, 850, 825, 800, 775, 750, 700, 650, 600, 550, 500, 450, 400, 350, 300, 250, 225, 200, 175, 150, 125, 100, 70, 50, 30, 20, 10, 7, 5, 3, 2, 1])
for name in file_list:
    if "replace_india8.cam.h1." in name:
        out_ds  =  cesm_vin2p(path,name,pnew)
        out_ds.attrs["description"]  =  "after vin2p"
        out_ds.to_netcdf(path_out+name)

        del out_ds
        print("successfully transform "+name)
    else:
        continue