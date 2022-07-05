'''
2021/8/25
本代码计算365天的多年日平均
使用资料为cesm2 control实验
计算时间为1981-2000 20年
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


path1  =  '/data5/2019swh/model_data/control/raw/'
path3  =  '/data5/2019swh/model_data/control/year_mean/'

file_list  =  os.listdir(path1)
test       =  [x for x in file_list if (".1981-" in x)]

var  =  ["DTV","OMEGA","PS","TS","Q","Z3","T","U","V","SHFLX","LHFLX","PRECT"]
#年循环365-数据长度循环40-
for day in range(0,365):
    files_1981      =  [x for x in file_list if (".1981-" in x)] ; files_1981.sort()
    base_array      =  xr.open_dataset(path1+files_1981[day])
    base_array      =  base_array[var]
    for year in range(1982,2001):
        file_list2  =  [x for x in file_list if ("."+str(year)+"-" in x)] ; file_list2.sort()
        file       =  xr.open_dataset(path1+file_list[day])
        file2      =  file[var]
        for var_name in base_array.keys():
            base_array[var_name].data += file2[var_name].data

    for vars in base_array.keys():
        base_array[vars].data /= 20

    base_array.to_netcdf(path3+"control_intel-"+files_1981[day][26:31]+".climate.nc")