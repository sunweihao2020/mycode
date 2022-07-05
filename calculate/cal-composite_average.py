'''这波啊，这波是计算合成分析的数据
计算爆发前30天至爆发后30天
30+1+30=61个时次
'''

import matplotlib
import matplotlib.pyplot as plt
import os
import numpy as np
import numpy.ma as ma
import Ngl, Nio
from netCDF4 import Dataset
import json
import sys
sys.path.append("/data5/2019swh/paint/meri-ciru/code/")
from module_composite_average import *

with open("/data5/2019swh/data/onsetdate.json",'r') as load_f:
    a = json.load(load_f)

dimension = np.load('/data5/2019swh/data/dimension.npz')
lon = dimension['lon']
lat = dimension['lat']
lev = dimension['lev']
time = dimension['time']

year = np.array(list(a.keys()))
day = np.array(list(a.values()))
years = year.astype(int)
day = day.astype(np.int)
day -= 1
location = [str(x) for x in day]  #从日期回归文件位置
path='/data1/MERRA2/daily/plev/'
variables=['EPV','H','OMEGA','T','U','V']
'''初始化'''
epv = initial_mask('epv',(31,42,361,576))
h   = initial_mask('u',(31,42,361,576))
omega = initial_mask('omega',(31,42,361,576))
t   = initial_mask('t',(31,42,361,576))
u   = initial_mask('u',(31,42,361,576))
v   = initial_mask('v',(31,42,361,576))
end = 40
first = 0
for yyyy in range(0,40):
    path1 = path+year[yyyy]+"/"
    file_list = os.listdir(path1)
    file_list.sort()
    day0 = day[yyyy]
    j = 0
    for dddd in np.arange(day0-30,day0+1):
        ff  =  Nio.open_file(path1+file_list[dddd])
        epv1 = ff.variables["EPV"][:]
        h1   = ff.variables["H"][:]
        omega1 = ff.variables["OMEGA"][:]
        t1   =  ff.variables["T"][:]
        u1   =  ff.variables["U"][:]
        v1   =  ff.variables["V"][:]
        epv[j,:,:,:]  +=  epv1[0,:,:,:]/(end-first)
        h[j, :, :, :] += h1[0, :, :, :]/(end-first)
        omega[j, :, :, :] += omega1[0, :, :, :]/(end-first)
        t[j, :, :, :] += t1[0, :, :, :]/(end-first)
        u[j, :, :, :] += u1[0, :, :, :]/(end-first)
        v[j, :, :, :] += v1[0, :, :, :]/(end-first)
        j += 1

'''存储数据'''
file=Dataset('/data5/2019swh/data/composite1_merra2_1020.nc','w',format='NETCDF4')
level_out = file.createDimension("level",len(lev))
time_out  = file.createDimension("time",31)
lat_out   = file.createDimension("lat",len(lat))
lon_out   = file.createDimension("lon",len(lon))

times     = file.createVariable("time","f8",("time",))
times.long_name = 'time'
months=np.arange(31)+1
times[:] = months

levels    = file.createVariable("level","f8",("level",))
levels.units = 'hPa'
levels[:] = lev

latitudes = file.createVariable("lat","f4",("lat",))
latitudes.units= 'degrees_north'
latitudes[:] = lat

longitudes= file.createVariable("lon","f4",("lon",))
longitudes.units = 'degrees_east'
longitudes[:] = lon

uwinds    = file.createVariable("uwind","f8",("time","level","lat","lon"),fill_value=45275)
uwinds.units = 'm s-1'
uwinds.valid_range =	[-1000,1000]
uwinds[:] = u

vwinds    = file.createVariable("vwind","f8",("time","level","lat","lon"),fill_value=45275)
vwinds.units = 'm s-1'
vwinds.valid_range =	[-1000,1000]
vwinds[:] = v

OMEGA     = file.createVariable("OMEGA","f8",("time","level","lat","lon"),fill_value=45275)
OMEGA.units  = 'Pa s-1'
OMEGA.valid_range =	[-1000,1000]
OMEGA[:] = omega

EPV       = file.createVariable("EPV","f8",("time","level","lat","lon"),fill_value=45275000)
EPV.units= 'K m+2 kg-1 s-1'
EPV.valid_range = [-10000,10000]
EPV[:] = epv

T         = file.createVariable("T","f8",("time","level","lat","lon"),fill_value=45275)
T.units = 'K'
T.valid_range =	[-1000,1000]
T[:] = t

H         = file.createVariable("H","f8",("time","level","lat","lon"),fill_value=1e+15)
H.units = 'm'
H.valid_range =	[-1e+15, 1e+15]
H[:] = h


file.close()

del file

'''计算爆发后30天'''
epv = initial_mask('epv',(30,42,361,576))
h   = initial_mask('u',(30,42,361,576))
omega = initial_mask('omega',(30,42,361,576))
t   = initial_mask('t',(30,42,361,576))
u   = initial_mask('u',(30,42,361,576))
v   = initial_mask('v',(30,42,361,576))
end = 40
first = 0
for yyyy in range(0,40):
    path1 = path+year[yyyy]+"/"
    file_list = os.listdir(path1)
    file_list.sort()
    day0 = day[yyyy]
    j = 0
    for dddd in np.arange(day0+1,day0+31):
        ff  =  Nio.open_file(path1+file_list[dddd])
        epv1 = ff.variables["EPV"][:]
        h1   = ff.variables["H"][:]
        omega1 = ff.variables["OMEGA"][:]
        t1   =  ff.variables["T"][:]
        u1   =  ff.variables["U"][:]
        v1   =  ff.variables["V"][:]
        epv[j,:,:,:]  +=  epv1[0,:,:,:]/(end-first)
        h[j, :, :, :] += h1[0, :, :, :]/(end-first)
        omega[j, :, :, :] += omega1[0, :, :, :]/(end-first)
        t[j, :, :, :] += t1[0, :, :, :]/(end-first)
        u[j, :, :, :] += u1[0, :, :, :]/(end-first)
        v[j, :, :, :] += v1[0, :, :, :]/(end-first)
        j += 1

'''存储数据'''
file=Dataset('/data5/2019swh/data/composite2_merra2_1020.nc','w',format='NETCDF4')
level_out = file.createDimension("level",len(lev))
time_out  = file.createDimension("time",30)
lat_out   = file.createDimension("lat",len(lat))
lon_out   = file.createDimension("lon",len(lon))

times     = file.createVariable("time","f8",("time",))
times.long_name = 'time'
months=np.arange(30)+1
times[:] = months

levels    = file.createVariable("level","f8",("level",))
levels.units = 'hPa'
levels[:] = lev

latitudes = file.createVariable("lat","f4",("lat",))
latitudes.units= 'degrees_north'
latitudes[:] = lat

longitudes= file.createVariable("lon","f4",("lon",))
longitudes.units = 'degrees_east'
longitudes[:] = lon

uwinds    = file.createVariable("uwind","f8",("time","level","lat","lon"),fill_value=45275)
uwinds.units = 'm s-1'
uwinds.valid_range =	[-1000,1000]
uwinds[:] = u

vwinds    = file.createVariable("vwind","f8",("time","level","lat","lon"),fill_value=45275)
vwinds.units = 'm s-1'
vwinds.valid_range =	[-1000,1000]
vwinds[:] = v

OMEGA     = file.createVariable("OMEGA","f8",("time","level","lat","lon"),fill_value=45275)
OMEGA.units  = 'Pa s-1'
OMEGA.valid_range =	[-1000,1000]
OMEGA[:] = omega

EPV       = file.createVariable("EPV","f8",("time","level","lat","lon"),fill_value=45275000)
EPV.units= 'K m+2 kg-1 s-1'
EPV.valid_range = [-10000,10000]
EPV[:] = epv

T         = file.createVariable("T","f8",("time","level","lat","lon"),fill_value=45275)
T.units = 'K'
T.valid_range =	[-1000,1000]
T[:] = t

H         = file.createVariable("H","f8",("time","level","lat","lon"),fill_value=1e+15)
H.units = 'm'
H.valid_range =	[-1e+15, 1e+15]
H[:] = h


file.close()






