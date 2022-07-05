'''
2021/8/24
本代码计算365天的多年日平均
使用资料为merra2
有多层的  单层的是降水
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
sys.path.append("/data5/2019swh/mycode/module/")
from module_sun import *

path1  =  '/data5/2019swh/mydown/merra2_precipitation/'
path2  =  '/data1/MERRA2/daily/plev/'
path3  =  '/data5/2019swh/data/year_mean/'

#先计算多层的
#生成初始数组
#t0     =  np.zeros((42,361,576))
#t1     =  xr.open_dataset(path2+"1992/MERRA2_200.inst3_3d_asm_Np.19920301.SUB.nc")
#t      =  t1.T.data[0,:,:,:]

#读取第一年的
#first_year  =  "1980"
#first_array =  xr.open_dataset(path2+first_year+"/MERRA2_100.inst3_3d_asm_Np.19800101.SUB.nc")
#
#base_array  =  first_array.drop_vars(("EPV","QL","QV","time_bnds"))  #这里记得除以40
#for var_name in base_array.keys():
#    base_array[var_name].data  /= 40


var  =  ["H","OMEGA","PS","RH","SLP","T","U","V"]
#年循环365-数据长度循环40-
for day in range(0,365):
    files_1980      =  os.listdir(path2+"1980/")  ;  files_1980.sort()
    base_array      =  xr.open_dataset(path2+"1980/"+files_1980[day])
    base_array      =  base_array[var]
    for year in range(1981,2020):
        path       =  path2+str(year)+"/"
        file_list  =  os.listdir(path) ; file_list.sort()
        file       =  xr.open_dataset(path+file_list[day])
        file2      =  file[var]
        for var_name in base_array.keys():
            base_array[var_name].data += file2[var_name].data

    for vars in base_array.keys():
        base_array[vars].data /= 40

    base_array.to_netcdf(path3+files_1980[day][31:35]+".climate.nc")