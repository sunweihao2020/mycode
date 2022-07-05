'''
2021/1/24
使用合成的era5数据计算地表位涡制造
使用数据：composite-era5theta.nc composite-modeluv.nc
垂直高度上使用的是底端两层
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

def conform(p,shape,axis1,axis2):
    conformx  =  np.zeros(shape)
    for t in range(0,shape[axis1]):
        for x in range(0,shape[axis2]):
            conformx[t,:,x] = p
    return conformx

f1 = Nio.open_file("/data5/2019swh/data/composite-era5theta.nc")
f2 = Nio.open_file("/data5/2019swh/data/composite-modeluv.nc")

theta = f1.variables["theta"][:,::-1,:]
u     = f2.variables["uwind"][:,:,::-1,:]
v     = f2.variables["vwind"][:,:,::-1,:]

time = f2.variables["time"][:]
lat  = f2.variables["lat"][::-1]
lon  = f2.variables["lon"][:]
level = f2.variables["level"][:] #第四层是地表层

#计算动力作用
'''1.三维涡度计算'''
vz = (v[:,2,:,:]-v[:,3,:,:])/20
uz = (u[:,2,:,:]-u[:,3,:,:])/20

disy,disx,location = cal_xydistance(lat,lon)
sinlat = np.array([]) #生成科里奥利力数组
for ll in lat:
    sinlat = np.append(sinlat,math.sin(math.radians(ll)))
omega = 7.29e-5
f = 2*omega*sinlat

uy = np.zeros((61,4,121,91))
vx = np.zeros((61,4,121,91))
for t in range(0,u.shape[0]):
    for z in range(0,u.shape[1]):
        uy[t,z,:,:] = -1*np.gradient(u[t,z,:,:],location,axis=0)
        for latt in range(1,len(lat)-1):
            vx[t,z,latt,:] = np.gradient(v[t,z,latt,:],disx[latt],axis=0)
#三维涡度
ff = conform(f,theta.shape,0,2)
vorticity = -vz+uz+ff+vx[:,3,:,:]-uy[:,3,:,:]

J_thermal = -1*np.gradient(theta,np.arange(1,62,1),axis=0)*vorticity
J_dynamic = -1*np.gradient(vorticity,np.arange(1,62,1),axis=0)*theta

J = J_thermal + J_dynamic


time = np.arange(0,61)
fout = create_nc_single('/data5/2019swh/data/','composite-era5pvcreate',time,lon,lat)
a_w = {'longname': 'PVS', 'units': 'K m-1 s-1', 'valid_range': [-1000000000000000.0, 1000000000000000.0]}
add_variables(fout,'j_dynamic',J_dynamic,a_w,0)
add_variables(fout,'j_thermal',J_thermal,a_w,0)
add_variables(fout,'j_all',J,a_w,0)

fout.close()