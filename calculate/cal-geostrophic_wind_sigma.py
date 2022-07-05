'''
2021/5/25
本代码计算sigma层上的地转风
'''
import os
import numpy as np
import numpy.ma as ma
import Ngl, Nio
from netCDF4 import Dataset
import json
import sys
import time
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
    h     =  f.variables["H"][:,::-1,110:151,48:]
    p     =  f.variables["PL"][:,::-1,110:151,48:]
    return np.average(h,axis=0),np.average(p,axis=0)

#这里得求pi
def transform_p(h,p):
    #分别求出平均温度以及lnσ
    h1   =   h*9.8  #h在前面调过了
    p0    =  p[0,:,:]
    sigma =  copy.deepcopy(p)
    for ll in range(0,p.shape[0]):
        sigma[ll,:,:] = p[ll,:,:]/p0
    return h1,sigma

def cal_gp_ps(h1,p,sigma):
    #计算地转风的后两项
    gp = ma.zeros(p.shape)
    ps = ma.zeros(p.shape)
    for yy in range(0,p.shape[1]):
        for xx in range(0,p.shape[2]):
            gp[:,yy,xx]  =  np.gradient(h1[:,yy,xx],p[:,yy,xx],axis=0)
            ps[:,yy,xx]  =  np.gradient(p[:,yy,xx],sigma[:,yy,xx],axis=0)
    return gp,ps

#获取维度信息
f0  =  Nio.open_file(path+files[10])
lat =  f0.variables["lat"][110:151]
lon =  f0.variables["lon"][48:]
lev =  f0.variables["lev"][::-1]

disy,disx,location = cal_xydistance(lat,lon)

sinlat = np.array([])
for ll in lat:
    sinlat = np.append(sinlat,math.sin(math.radians(ll)))
omega = 7.29e-5
ff = 2*omega*sinlat

def cal_gradient(h1,ps,location,disx):
    h1_y  =  np.gradient(h1,location,axis=1)
    ps_y  =  np.gradient(ps,location,axis=1)
    h1_x  =  ma.zeros(h1.shape)
    ps_x  =  ma.zeros(h1.shape)
    for yy in range(0,ps.shape[1]):
        h1_x[:,yy,:]  =  np.gradient(h1[:,yy,:],disx[yy],axis=1)
        ps_x[:,yy,:]  =  np.gradient(ps[:,yy,:],disx[yy],axis=1)
    return h1_y,h1_x,ps_y,ps_x

def conform_1(p,shape,axis0,axis1):
    conformx  =  np.zeros(shape)
    for t in range(0,shape[axis0]):
        for y in range(0,shape[axis1]):
                conformx[t,:,y] = p
    return conformx

a_v = {'longname': 'geostrophic_wind', 'units': 'm s-1', 'valid_range': [-1000000000000000.0, 1000000000000000.0]}
time = np.arange(0,1)
for f1 in files[0:1]:
    h,p          =       reading_var(f1)
    h1,sigma     =       transform_p(h,p)
    gp,ps        =       cal_gp_ps(h1,p,sigma)
    h1_y, h1_x, ps_y, ps_x = cal_gradient(h1,ps,location,disx)
    term1        =       ma.zeros(h.shape)
    term2        =       ma.zeros(h.shape)
    ff_conform   =       conform_1(ff,h.shape,0,2)

    ug_1           =       -1*h1_y/ff_conform+sigma/ff_conform*gp*ps_y
    vg_1           =       h1_x/ff_conform-sigma/ff_conform*gp*ps_x
    ug_2           = -1 * h1_y / ff_conform
    vg_2           = h1_x / ff_conform
    vg             =       ma.zeros((1, 72, 41, 97))
    ug             =       ma.zeros((1, 72, 41, 97))
    #vg[0, :, :, :]  =  vg_1
    #ug[0, :, :, :]  =  ug_1
    #fout = create_nc_multiple('/data5/2019swh/data/cal_geostrophic/', f1, time,lev, lon, lat)
    #add_variables(fout, 'geostrophic_u', ug, a_v, 1)
    #add_variables(fout, 'geostrophic_v', vg, a_v, 1)
    #fout.close()
    #del fout

