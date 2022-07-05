'''
2021/7/12
本代码计算海温的序列，时间跨度为1982-2016
'''
import os
import numpy as np
import numpy.ma as ma
import Ngl, Nio
from netCDF4 import Dataset
import json
import sys
import time
import math
import copy
import xarray as xr
sys.path.append("/data5/2019swh/mycode/module/")
from module_sun import *
from module_writenc import *
from attribute import a_sst

def add_variables(file,name,variable,attribute,bool):
    if bool == 0:
        var = file.createVariable(name,"f8",("year","time","lat","lon"),fill_value=1e+15)
    else:
        var = file.createVariable(name,"f8",("year","time","level","lat","lon"),fill_value=1e+15)

    a = list(attribute.items())
    for i in range(0,3):
        key,value = list(attribute.items())[i]
        exec("var."+key+" = value")

    var[:] = variable


def create_nc_single(path, name, year, time, lon, lat):
    list_path = os.listdir(path)
    if name in list_path:
        os.system("rm -rf " + path + name + ".nc")

    file = Dataset(path + name + ".nc", "w", format='NETCDF4')

    year_out   =    file.createDimension("year", len(year))
    time_out   =    file.createDimension("time", len(time))
    lat_out    =    file.createDimension("lat", len(lat))
    lon_out    =    file.createDimension("lon", len(lon))

    years = file.createVariable("year", "f4", ("year",))
    years.long_name = 'year'
    years[:] = year

    times = file.createVariable("time", "f4", ("time",))
    times.long_name = 'time'
    times[:] = time

    latitudes = file.createVariable("lat", "f4", ("lat",))
    latitudes.units = 'degrees_north'
    latitudes[:] = lat

    longitudes = file.createVariable("lon", "f4", ("lon",))
    longitudes.units = 'degrees_east'
    longitudes[:] = lon

    return file

path_out = "/data5/2019swh/data/burst_seris/"

#海温资料存放位置
path1    = "/data5/2019swh/mydown/OISST/"

#获取经纬度
#获取经纬度以及mask
f0        = Nio.open_file(path1+"1988_290.nc")
lat       = f0.variables["lat"][:]
lon       = f0.variables["lon"][:]

#初始化数组
sst       = ma.zeros((35,40,720,1440))

#获取日期
with open("/data5/2019swh/data/onsetdate.json",'r') as load_f:
    a = json.load(load_f)

year = np.array(list(a.keys()))
day = np.array(list(a.values()))
years = year.astype(int)[2:-3]
day = day.astype(np.int)[2:-3]

def transfer(path1,year,location):
    sst   =   ma.zeros((40,720,1440))
    j     =   0
    for dddd in range(location-30,location+10):
        name        =  str(year)+"_"+str(dddd)+".nc"
        ff          =  Nio.open_file(path1+name)
        sst1        =  ff.variables["sst"][:]
        sst[j,:,:]  =  sst1
        j+=1
    return sst

j = 0
for yyyy in range(1982,2017):
    sst[j,:,:,:]  =  transfer(path1,yyyy,day[j])
    j += 1

year = np.arange(0,35)
time = np.arange(0,40)
fout1 = create_nc_single('/data5/2019swh/data/burst_seris/','composite_sst',year,time,lon,lat)
add_variables(fout1,'sea_surface_temperature',sst,a_sst,0)
fout1.close()