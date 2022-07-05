'''
2021/5/25
本代码计算热成风
使用模式倒数第二层
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
sys.path.append("/data5/2019swh/mycode/module/")
from module_sun import *
from module_writenc import *


#获取文件列表
files  =  os.listdir("/data5/2019swh/mydown/merra_modellev/")
files.sort()
path   =  "/data5/2019swh/mydown/merra_modellev/"

def reading_var(file):
    path  =  "/data5/2019swh/mydown/merra_modellev/"
    f     =  Nio.open_file(path+file)
    t     =  f.variables["T"][:,:,110:151,48:]
    p     =  f.variables["PL"][:,:,110:151,48:]
    return np.average(t,axis=0),np.average(p,axis=0)

def transform_t_p(t,p):
    #分别求出平均温度以及lnσ
    #这里我把顺序调过来了，自下往上
    a_t   =  ma.zeros((70,41,97))
    for ll in range(2,72):
        a_t[ll-2,:,:]  =  (t[71-ll,:,:] + t[70,:,:])/2
    p0    =  p[71,:,:]
    sigma =  copy.deepcopy(p)
    for ll in range(0,p.shape[0]):
        sigma[ll,:,:] = p[71-ll,:,:]/p0
    return a_t,np.log(sigma[1,:,:]/sigma[2:,:,:])  #!!注意这里返回的是对数

#获取经度纬度
f0  =  Nio.open_file(path+files[10])
lat =  f0.variables["lat"][110:151]
lon =  f0.variables["lon"][48:]
lev =  f0.variables["lev"][::-1]

#获取水平距离
disy,disx,location = cal_xydistance(lat,lon)

#获取科里奥利力数组
sinlat = np.array([])
for ll in lat:
    sinlat = np.append(sinlat,math.sin(math.radians(ll)))
omega = 7.29e-5
ff = 2*omega*sinlat

#气体常数 J/mol*K
r  = 8.314

constant1  =  r/ff
#计算T的水平导数
def cal_tem_gradient(a_t,location,disx):
    T_y  =  np.gradient(a_t,location,axis=1)
    T_x  =  ma.zeros(T_y.shape)
    for yy in range(0,a_t.shape[1]):
        T_x[:,yy,:]  =  np.gradient(a_t[:,yy,::],disx[yy],axis=1)
    return T_x,T_y

def cal_thermal_wind(T_x,T_y,sigma,constant1):
    vt  =  ma.zeros(T_y.shape)
    ut  = ma.zeros(T_y.shape)
    for zz in range(0,70):
        for xx in range(0,97):
            vt[zz,:,xx]  =  constant1*sigma[zz,:,xx]*T_x[zz,:,xx]
            ut[zz,:,xx]  =  -1*constant1*sigma[zz,:,xx]*T_y[zz,:,xx]

    return vt,ut

a_v = {'longname': 'thermal_wind', 'units': 'm s-1', 'valid_range': [-1000000000000000.0, 1000000000000000.0]}
time = np.arange(0,1)
for f1 in files:
    t1,p1       =    reading_var(f1)
    a_t,sigma   =    transform_t_p(t1,p1)
    TX,TY       =    cal_tem_gradient(a_t,location,disx)
    vt_1,ut_1   =    cal_thermal_wind(TX,TY,sigma,constant1)  #在前面加个时间维
    vt          = ma.zeros((1, 70, 41, 97))
    ut          = ma.zeros((1, 70, 41, 97))
    vt[0, :, :, :]  =  vt_1
    ut[0, :, :, :]  =  ut_1
    fout = create_nc_multiple('/data5/2019swh/data/cal_thermal_2/', f1, time,lev[2:], lon, lat)
    add_variables(fout, 'thermal_u', ut, a_v, 1)
    add_variables(fout, 'thermal_v', vt, a_v, 1)
    fout.close()
    del fout

