'''
2020/11/29
计算多年平均的候平均SST
资料：OISST
时间跨度：1982-2016  18候-30候
'''

import sys
import os
import numpy as np
import numpy.ma as ma
import Ngl, Nio
from netCDF4 import Dataset
import datetime
from numba import jit
sys.path.append("/data5/2019swh/mycode/module/")
#from attribute import *
#from module_writenc import *

def pentad_mean(pen,variable,mask,year):
    path = '/data5/2019swh/data/OISST/'
    var_m = ma.zeros((720,1440))
    var_m = ma.array(var_m,mask=mask)
    daystat = pen*5
    for day in range(0,5):
        f = Nio.open_file(path+str(year)+"_"+str(daystat+day+1)+".nc")
        var = f.variables[variable][:]
        var_m += var[:,:]/5

    return var_m

path1 = "/data5/2019swh/data/OISST/"
f0 = Nio.open_file("/data1/OISST/daily/2007/AVHRR/avhrr-only-v2.20070511.nc")
s1 = f0.variables["sst"][:]
lat = f0.variables["lat"][:]
lon = f0.variables["lon"][:]
mask = s1.mask[0,0,:,:]

#生成一个[10,720,1440]数组
pentad_sst = ma.zeros((13,720,1440))
for i in range(0,13):
    pentad_sst[i,:,:] = ma.array(pentad_sst[i,:,:],mask=mask)

for yyyy in range(1982,2016):
    for p in range(0,13):
        pentad_sst[p,:,:] += pentad_mean((p+18-1),'sst',mask,yyyy)/(2016-1982+1)

file = Dataset('/data5/2019swh/data/18-30_pentad_OISST_1130.nc', 'w', format='NETCDF4')

time_out = file.createDimension("time", 13)
lat_out = file.createDimension("lat", len(lat))
lon_out = file.createDimension("lon", len(lon))

times = file.createVariable("time", "f8", ("time",))
times.long_name = 'time'
months = np.arange(13) + 1
times[:] = months



latitudes = file.createVariable("lat", "f4", ("lat",))
latitudes.units = 'degrees_north'
latitudes[:] = lat

longitudes = file.createVariable("lon", "f4", ("lon",))
longitudes.units = 'degrees_east'
longitudes[:] = lon

SST = file.createVariable("SST", "f8", ("time", "lat", "lon"), fill_value= 1e+15)
SST.units = 'degC'
SST.valid_range = [-1e+15,  1e+15]
SST[:] = pentad_sst

file.close()







