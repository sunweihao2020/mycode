'''
2020/11/12
merra2
计算湿度的合成平均
计算爆发前30天至爆发后30天
30+1+30=61个时次
'''


import matplotlib.pyplot as plt
import os
import numpy as np
import numpy.ma as ma
import Ngl, Nio
from netCDF4 import Dataset
import json
import sys
sys.path.append("/data5/2019swh/mycode/module/")
from module_composite_average import *

with open("/data5/2019swh/data/onsetdate.json",'r') as load_f:
    a = json.load(load_f)
f2 = Nio.open_file("/data5/2019swh/data/composite3.nc")
h   = f2.variables["H"][:]
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
variables=['RH']
'''初始化'''
rh = ma.array(ma.zeros((61,42,361,576)),mask=h.mask)

end = 40
first = 0
for yyyy in range(0,40):
    path1 = path+year[yyyy]+"/"
    file_list = os.listdir(path1)
    file_list.sort()
    day0 = day[yyyy]
    j = 0
    for dddd in np.arange(day0-30,day0+31):
        ff  =  Nio.open_file(path1+file_list[dddd])
        rh1  =  ff.variables['RH'][:]
        rh[j, :, :, :] += rh1[0, :, :, :] / (end - first)
        j += 1

'''存储数据'''
file=Dataset('/data5/2019swh/data/composite_rh.nc','w',format='NETCDF4')
level_out = file.createDimension("level",len(lev))
time_out  = file.createDimension("time",61)
lat_out   = file.createDimension("lat",len(lat))
lon_out   = file.createDimension("lon",len(lon))

times     = file.createVariable("time","f8",("time",))
times.long_name = 'time'
months=np.arange(61)+1
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


RH         = file.createVariable("RH","f8",("time","level","lat","lon"),fill_value=1e+15)
RH.units = '1'
RH.valid_range =	[-1e+15, 1e+15]
RH[:] = rh


file.close()






