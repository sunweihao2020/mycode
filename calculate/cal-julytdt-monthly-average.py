'''
2021/2/13
本代码使用日平均的加热资料计算七月的月平均加热率，和吴老师提供的图像进行对比
资料路径：/data5/2019swh/mydown/merra-tdt/2010/daymean
'''
import os
import numpy as np
import numpy.ma as ma
import Ngl, Nio
from netCDF4 import Dataset
import json
import sys
sys.path.append("/data5/2019swh/mycode/module/")
from module_sun import *
from module_writenc import *
from attribute import *

mst_mean = ma.zeros((42,181,360))
rad_mean = ma.zeros((42,181,360))
tot_mean = ma.zeros((42,181,360))
tur_mean = ma.zeros((42,181,360))
path = "/data5/2019swh/mydown/merra-tdt/2010/daymean/"
for day in range(1,32):
    ff = Nio.open_file(path+str(day)+".nc")
    mst = ff.variables["DTDTMST"][0,:,:,:]
    rad = ff.variables["DTDTRAD"][0,:,:,:]
    tot = ff.variables["DTDTTOT"][0,:,:,:]
    tur = ff.variables["DTDTTRB"][0,:,:,:]
    mst_mean += mst/31
    rad_mean += rad/31
    tot_mean += tot/31
    tur_mean += tur/31

time = np.arange(0,1)
#获取维度
f0  = Nio.open_file("/data5/2019swh/mydown/merra-tdt/2010/daymean/15.nc")
lev = f0.variables["lev"][:]
lat = f0.variables["lat"][:]
lon = f0.variables["lon"][:]

a_tdt = {'longname': 'temperature tendency','units': 'K day-1','valid_range': [-1000000000000000.0, 1000000000000000.0]}
fout = create_nc_multiple('/data5/2019swh/data/','JULY_tdt',time,lev,lon,lat)
add_variables(fout,'mst',mst_mean*60*60*24,a_tdt,1)
add_variables(fout,'rad',rad_mean*60*60*24,a_tdt,1)
add_variables(fout,'tot',tot_mean*60*60*24,a_tdt,1)
add_variables(fout,'tur',tur_mean*60*60*24,a_tdt,1)


fout.close()
