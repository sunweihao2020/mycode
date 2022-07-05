'''
本代码为原本复制品留存用
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
from attribute import *

path_out = "/data5/2019swh/data/burst_seris/"

#计算多层的UV、T、q、omega
path1    = "/data1/MERRA2/daily/plev/"

#获取经纬度以及mask
f0        = Nio.open_file(path1+"1980/MERRA2_100.inst3_3d_asm_Np.19800402.SUB.nc")
lev       = f0.variables["lev"][:]
lat       = f0.variables["lat"][:]
lon       = f0.variables["lon"][:]

'''
截取范围：经度（336，528）纬度（100，260）垂直（0，24）
'''


#获取日期
with open("/data5/2019swh/data/onsetdate.json",'r') as load_f:
    a = json.load(load_f)

year = np.array(list(a.keys()))
day = np.array(list(a.values()))
years = year.astype(int)
day = day.astype(np.int)
day -= 1
location = [str(x) for x in day]  #从日期回归文件位置

path='/data1/MERRA2/daily/plev/'
#def transfer(path1,year,location):
#    path  = path1+str(year)+"/"
#    lists = os.listdir(path)
#    lists.sort()
#    uwind = ma.zeros((40, 42, 361, 576))
#    vwind = ma.zeros((40, 42, 361, 576))
#    rh    = ma.zeros((40, 42, 361, 576))
#    t     = ma.zeros((40, 42, 361, 576))
#    omega = ma.zeros((40, 42, 361, 576))
#    j     = 0
#    for dddd in range(location-30,location+10):
#        ff      =  Nio.open_file(path+lists[dddd])
#        uwind1  =  ff.variables["U"][:][0,:,:,:]
#        vwind1  =  ff.variables["V"][:][0,:,:,:]
#        rh1     =  ff.variables["RH"][:][0,:,:,:]
#        t1      =  ff.variables["T"][:][0,:,:,:]
#        omega1  =  ff.variables["OMEGA"][:][0,:,:,:]
#
#        uwind[j,:,:,:]  =  uwind1
#        vwind[j,:,:,:]  =  vwind1
#        rh[j,:,:,:]     =  rh1
#        t[j,:,:,:]      =  t1
#        omega[j,:,:,:]  =  omega1
#
#    time = np.arange(0, 40)
#    fout1 = create_nc_multiple('/data5/2019swh/data/burst_seris/', str(year)+'_composite_uwind',time, lev, lon, lat)
#    add_variables(fout1, 'uwind', uwind, a_uwind, 1)
#    fout1.close()
#    fout1 = create_nc_multiple('/data5/2019swh/data/burst_seris/', str(year)+'_composite_vwind',time, lev, lon, lat)
#    add_variables(fout1, 'vwind', vwind, a_vwind, 1)
#    fout1.close()
#    fout1 = create_nc_multiple('/data5/2019swh/data/burst_seris/', str(year)+'_composite_rh',time, lev, lon, lat)
#    add_variables(fout1, 'rh', rh, a_rh, 1)
#    fout1.close()
#    fout1 = create_nc_multiple('/data5/2019swh/data/burst_seris/', str(year)+'_composite_t',time, lev, lon, lat)
#    add_variables(fout1, 'temperature', t, a_T, 1)
#    fout1.close()
#    fout1 = create_nc_multiple('/data5/2019swh/data/burst_seris/', str(year)+'_composite_omega',time, lev, lon, lat)
#    add_variables(fout1, 'omega', omega, a_omega, 1)
#    fout1.close()

year = 2002

path2  = path1+str(year)+"/"
lists = os.listdir(path2)
lists.sort()
uwind = ma.zeros((40, 42, 361, 576))
vwind = ma.zeros((40, 42, 361, 576))
rh    = ma.zeros((40, 42, 361, 576))
t     = ma.zeros((40, 42, 361, 576))
omega = ma.zeros((40, 42, 361, 576))
j     = 0
location = day[22]
for dddd in range(location-30,location+10):
    ff      =  Nio.open_file(path2+lists[dddd])
    uwind1  =  ff.variables["U"][:][0,:,:,:]
    vwind1  =  ff.variables["V"][:][0,:,:,:]
    rh1     =  ff.variables["RH"][:][0,:,:,:]
    t1      =  ff.variables["T"][:][0,:,:,:]
    omega1  =  ff.variables["OMEGA"][:][0,:,:,:]
    uwind[j,:,:,:]  =  uwind1
    vwind[j,:,:,:]  =  vwind1
    rh[j,:,:,:]     =  rh1
    t[j,:,:,:]      =  t1
    omega[j,:,:,:]  =  omega1

    j+=1
time = np.arange(0, 40)
fout1 = create_nc_multiple('/data5/2019swh/data/burst_seris/', str(year)+'_composite_uwind',time, lev, lon, lat)
add_variables(fout1, 'uwind', uwind, a_uwind, 1)
fout1.close()
fout1 = create_nc_multiple('/data5/2019swh/data/burst_seris/', str(year)+'_composite_vwind',time, lev, lon, lat)
add_variables(fout1, 'vwind', vwind, a_vwind, 1)
fout1.close()
fout1 = create_nc_multiple('/data5/2019swh/data/burst_seris/', str(year)+'_composite_rh',time, lev, lon, lat)
add_variables(fout1, 'rh', rh, a_rh, 1)
fout1.close()
fout1 = create_nc_multiple('/data5/2019swh/data/burst_seris/', str(year)+'_composite_t',time, lev, lon, lat)
add_variables(fout1, 'temperature', t, a_T, 1)
fout1.close()
fout1 = create_nc_multiple('/data5/2019swh/data/burst_seris/', str(year)+'_composite_omega',time, lev, lon, lat)
add_variables(fout1, 'omega', omega, a_omega, 1)
fout1.close()