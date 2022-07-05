'''
2021/1/9
计算三维涡度等几个量，用于后续积分运算
使用资料：合成后的等气压面资料
注：另外一个计算涡度的是模式层上的资料

量纲：空气密度：1.293 kg/m^3
'''
import os
import numpy as np
import Ngl, Nio
import numpy.ma as ma
from geopy.distance import distance
import sys
from netCDF4 import Dataset
import math
import copy
sys.path.append("/data5/2019swh/mycode/module/")
from module_sun import *
from module_writenc import *
from attribute import *

f = Nio.open_file("/data5/2019swh/data/composite3.nc")
u = f.variables["uwind"][:]
v = f.variables["vwind"][:]
h = f.variables["H"][:]
tem = f.variables["T"][:]
p = f.variables["level"][:]
level = f.variables["level"][:]
lon  = f.variables["lon"][:]
lat  = f.variables["lat"][:]
omega1 = f.variables["OMEGA"][:]
time = np.arange(0,61)+1

sinlat = np.array([]) #生成科里奥利力数组
for ll in lat:
    sinlat = np.append(sinlat,math.sin(math.radians(ll)))
omega = 7.29e-5
ff = 2*omega*sinlat
disy,disx,location = cal_xydistance(lat,lon)

uy = np.gradient(u,location,axis=2)
vx = copy.deepcopy(uy)
for i in range(1,360):
    vx[:,:,i,:] = np.gradient(v[:,:,i,:],disx[i],axis=2)

vorticity = vx-uy
for t in range(0,61):
    for z in range(0,33):
        for x in range(0,576):
            vorticity[t,z,:,x] += ff[:]

#计算垂直涡度
p *= 1000
#pp = np.zeros((t.shape))
#for t in range(0,61):
#    for y in range(0,361):
#        for x in range(0,576):
#            pp[t,:,y,x] = p
p = conform(p,tem.shape,0,2,3)
w = omega_to_w(omega1,p,tem)

wx = copy.deepcopy(vx)
wy = copy.deepcopy(vx)
vz = copy.deepcopy(vx)
uz = copy.deepcopy(vx)

for t in range(0,61):
    for y in range(0,361):
        for x in range(0,576):
            uz[t,:,y,x] = np.gradient(u[t,:,y,x],h[t,:,y,x],axis=0)
            vz[t, :, y, x] = np.gradient(v[t, :, y, x], h[t, :, y, x], axis=0)

for i in range(1,360):
    wx[:,:,i,:] = np.gradient(w[:,:,i,:],disx[i],axis=2)


wy = np.gradient(w,location,axis=2)

fout = create_nc_multiple('/data5/2019swh/data/','three-dimension-vorticity-pressure',time,level,lon,lat)
a_vorticity = {'longname': 'vorticity','units': 's-1','valid_range': [-1000000000000000.0, 1000000000000000.0]}
add_variables(fout,'x_vorticity',(wy-vz),a_vorticity,1)
add_variables(fout,'y_vorticity',(uz-wx),a_vorticity,1)
add_variables(fout,'z_vorticity',vorticity,a_vorticity,1)
fout.close()