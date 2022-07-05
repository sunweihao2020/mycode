'''
2021/1/20
使用下载的era5数据ps数据进行合成
'''
import os
import numpy as np
import numpy.ma as ma
import Ngl, Nio
from netCDF4 import Dataset
import json
import sys
import time
sys.path.append("/data5/2019swh/mycode/module/")
from module_sun import *
from module_writenc import *
from attribute import *
with open("/data5/2019swh/data/onsetdate.json",'r') as load_f:
    a = json.load(load_f)

#求ps日平均
def daily_mean_single(var, alltime, times):
    days = alltime // times
    mean = ma.zeros((int(var.shape[1]), int(var.shape[2])))
    mean = ma.array(mean, mask=var[0,:,:].mask)
    for tttt in range(0, var.shape[0], times):
        mean[:, :] = np.sum(var[tttt:tttt + times, :, :], axis=0) / times

    return mean

years = np.array(list(a.keys()))
days  = np.array(list(a.values()))
years = years.astype(np.int)
days = days.astype(np.int)

path = "/data5/2019swh/mydown/era5-single/surface_pressure/"
ps0 = ma.zeros((61,121,91))
for y in range(0,40):
    dy = days[y]
    if leap_year(years[y]):
        dy -= 61
    else:
        dy -= 60

    files = os.listdir(path+str(years[y]))
    files.sort()

    j = 0
    for z in range(dy-30,dy+31):
        f = Nio.open_file(path+str(years[y])+"/"+files[z])
        sp1 = f.variables["sp"]
        sp2 = short2flt(sp1)
        lon = f.variables["longitude"][:]
        lat = f.variables["latitude"][:]
        sp_mean = daily_mean_single(sp2,8,8)
        ps0[j,:,:] += sp_mean/40
        j += 1

time = np.arange(0,61)
fout = create_nc_single('/data5/2019swh/data/','composite-era5ps',time,lon,lat)
add_variables(fout,'ps',ps0,a_ps,0)
fout.close()

