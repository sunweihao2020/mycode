'''这波啊，这波是计算OLR的合成平均'''
import os
import numpy as np
import Ngl, Nio
import json
import numpy.ma as ma
import sys
from netCDF4 import Dataset
from datetime import datetime
sys.path.append("/data5/2019swh/mycode/module/")
from module_sun import *
path = "/data5/2019swh/down/CPC/"
with open("/data5/2019swh/data/onsetdate.json",'r') as load_f:
    a = json.load(load_f)
years = np.array(list(a.keys()))
days  = np.array(list(a.values()))
years = years.astype(np.int)
days = days.astype(np.int)
path = "/data5/2019swh/mydown/OLR/"

f = Nio.open_file(path+"olr.day.mean.nc")
olr = f.variables["olr"][:]
t = f.variables["time"][:]
'''注意这里是从1974-2019年'''
#定位1980
d0 = datetime.datetime(1974,6,1)
d1 = datetime.datetime(1980,1,1)
dd = d1-d0
time = t[2040:]
olr = olr[2040:,:,:]  #1980.1.1-2019.12.31

'''初始化
30+1+30
'''
olr0 = ma.zeros((61,73,144))
c = origin_day(1980,1,1,1981,2,2)
for yyyy in range(0,39):
     origin = origin_day(1980,1,1,years[yyyy],1,1)
     day0 = days[yyyy]
     j=0
     for dddd in np.arange(origin+day0-30,origin+day0+31):
         olr0[j,:,:] += olr[dddd,:,:]/39
         j += 1

lon = f.variables["lon"][:]
lat = f.variables["lat"][:]

time = np.arange(0,61)+1

file=Dataset('/data5/2019swh/data/composite_OLR_1021.nc','w',format='NETCDF4')

time_out  = file.createDimension("time",61)
lat_out   = file.createDimension("lat",len(lat))
lon_out   = file.createDimension("lon",len(lon))

times     = file.createVariable("time","f8",("time",))
times.long_name = 'time'
times[:] = time


latitudes = file.createVariable("lat","f4",("lat",))
latitudes.units= 'degrees_north'
latitudes[:] = lat

longitudes= file.createVariable("lon","f4",("lon",))
longitudes.units = 'degrees_east'
longitudes[:] = lon

H         = file.createVariable("OLR","f8",("time","lat","lon"),fill_value=1e+15)
H.units = 'W/m^2'
H.valid_range =	[0, 500]
H[:] = olr0


file.close()











