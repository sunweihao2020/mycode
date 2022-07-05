'''
2020/1/30
使用资料：composite-heating-merra.nc
选取两个点的垂直加热廓线转换到σ坐标系上
'''
import os
import numpy as np
import numpy.ma as ma
import Ngl, Nio
from netCDF4 import Dataset
import json
import sys
import datetime
sys.path.append("/data5/2019swh/mycode/module/")
from module_sun import *
from module_writenc import *
from attribute import *

start = datetime.datetime.now()

#读取文件
f = Nio.open_file("/data5/2019swh/data/composite-heating-merra.nc")
total = f.variables["total"][:]
dynamic = f.variables["dynamic"][:]
moist = f.variables["moist"][:]
radiation = f.variables["radiation"][:]
physics = f.variables["physics"][:]
turbulence = f.variables["turbulence"][:]
lon = f.variables["lon"][:]
lat = f.variables["lat"][:]
lev = f.variables["level"][:]

#读取地面气压数据
f2 = Nio.open_file("/data5/2019swh/data/composite_PS.nc") #注意该文件里ps的纬度是60~-60
ps = f2.variables["PS"][:,:,:]
ps1 = ps[:,200,416]
ps2 = ps[:,200,448]
#两个点（50，70）(70,70)
total1 = total[:,:,70,50]
total2 = total[:,:,70,70]
turbulence1 = turbulence[:,:,70,50]
turbulence2 = turbulence[:,:,70,70]
radiation1 = radiation[:,:,70,50]
radiation2 = radiation[:,:,70,70]
moist1 = moist[:,:,70,50]
moist2 = moist[:,:,70,70]
physics1 = physics[:,:,70,50]
physics2 = physics[:,:,70,70]
dynamic1 = dynamic[:,:,70,50]
dynamic2 = dynamic[:,:,70,70]

#把这些写入文件
fout = Dataset("/data5/2019swh/data/heating_vertical_profile.nc","w",format='NETCDF4')
time_out = fout.createDimension("time",61)
level    = fout.createDimension("level",26)

tttt = np.arange(61) + 1
times = fout.createVariable("time", "f8",("time",))
times.long_name = 'time'
times[:] = tttt

levels = fout.createVariable("level", "f8", ("level",))
levels.units = 'hPa'
levels[:] = lev



def addvar(fout,vars,name):
    var = fout.createVariable(name,"f8",("time","level"),fill_value=1e+15)
    attribute = {'longname': 'name', 'units': 'K s-1', 'valid_range': [-10000000000, 10000000]}
    attribute['longname'] = name
    a = list(attribute.items())
    for i in range(0,3):
        key,value = list(attribute.items())[i]
        exec("var."+key+" = value")
    var[:] = vars

addvar(fout,total1,"total1")
addvar(fout,total2,"total2")
addvar(fout,turbulence1,"turbulence1")
addvar(fout,turbulence2,"turbulence2")
addvar(fout,radiation1,"radiation1")
addvar(fout,radiation2,"radiation2")
addvar(fout,moist1,"moist1")
addvar(fout,moist2,"moist2")
addvar(fout,physics1,"physics1")
addvar(fout,physics2,"physics2")
addvar(fout,dynamic1,"dynamic1")
addvar(fout,dynamic2,"dynamic2")

fout.close()