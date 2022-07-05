'''
2021/1/20
使用资料：era5模式层资料
注意：资料是不完整的 共30年
资料处理：合成分析
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

with open("/data5/2019swh/data/onsetdate.json",'r') as load_f:
    a = json.load(load_f)

year = np.array(list(a.keys()))
day = np.array(list(a.values()))
years = year.astype(int)
day = day.astype(np.int)
yyyy = [1982,1985,1986,1987,1988,1989,1990,1991,1992,1993,1994,1996,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2012,2013,2014,2015,2016,2017,2018]

#查看原数据数据结构
path0 = '/data5/2019swh/mydown/era5-model/wind/'
f0 = Nio.open_file(path0+"1998_float.nc")
lat = f0.variables["latitude"][:]
lon = f0.variables["longitude"][:]
level = f0.variables["level"][:]

#模式层数据是从3.1开始的

#声明合成后数组
u0     = ma.zeros((61,4,121,91))
v0     = ma.zeros((61,4,121,91))
t0     = ma.zeros((61,4,121,91))
#先处理成daily
for i in yyyy:
    dy = int(a[str(i)])
    if leap_year(i):
        dy -= 61
    else:
        dy -= 60 #定位到爆发当日
    f = Nio.open_file(path0+str(i)+"_float.nc")
    u     = f.variables["u"][:]
    v     = f.variables["v"][:]
    t     = f.variables["t"][:]

    u_mean = daily_mean(u,240,2)
    v_mean = daily_mean(v, 240, 2)
    t_mean = daily_mean(t,240,2)
    j = 0
    for dddd in range(dy-30,dy+31):
        u0[j,:,:,:] += u_mean[dddd,:,:,:]/30
        v0[j,:,:,:] += v_mean[dddd,:,:,:]/30
        t0[j,:,:,:] += t_mean[dddd,:,:,:]/30
        j += 1

time = np.arange(0,61)
fout = create_nc_multiple('/data5/2019swh/data/','composite-modeluv',time,level,lon,lat)
add_variables(fout,'uwind',u0,a_uwind,1)
add_variables(fout,'vwind',v0,a_vwind,1)
add_variables(fout,'temperature',t0,a_T,1)


fout.close()

