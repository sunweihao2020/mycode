'''
2021/1/6
计算PVS flux等几个量，用于后续积分运算
使用资料：合成后的模式面资料
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

f2 = Nio.open_file("/data5/2019swh/data/composite-model.nc")
u = f2.variables["U"][:]
v = f2.variables["V"][:]
h = f2.variables["H"][:]
t = f2.variables["T"][:]
omega = f2.variables["OMEGA"][:]
f3 = Nio.open_file("/data5/2019swh/data/composite-modeltheta.nc")
theta = f3.variables["theta"][:]
time = f2.variables["time"][:]
lon  = f2.variables["lon"][:]
lat  = f2.variables["lat"][:]
pl   = f3.variables["pl"][:]
level = f2.variables["level"][:]

sinlat = np.array([]) #生成科里奥利力数组
for ll in lat:
    sinlat = np.append(sinlat,math.sin(math.radians(ll)))
omega = 7.29e-5
f = 2*omega*sinlat

disy,disx,location = cal_xydistance(lat,lon)

uy = np.gradient(u,location,axis=2)
vx = copy.deepcopy(uy)
for i in range(1,360):
    vx[:,:,i,:] = np.gradient(v[:,:,i,:],disx[i],axis=2)

vorticity = vx-uy
for t in range(0,61):
    for z in range(0,33):
        for x in range(0,576):
            vorticity[t,z,:,x] += f[:]

#这里计算了水平涡度，现在计算三维涡度
#先将omega转化为w
w = omega_to_w(omega,pl,t)
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

#三维涡度分量已经计算完毕

fout = create_nc_multiple('/data5/2019swh/data/','three-dimension-vorticity',time,level,lon,lat)
a_vorticity = {'longname': 'vorticity','units': 's-1','valid_range': [-1000000000000000.0, 1000000000000000.0]}
add_variables(fout,'x_vorticity',(wy-vz),a_vorticity,1)
add_variables(fout,'y_vorticity',(uz-wx),a_vorticity,1)
add_variables(fout,'z_vorticity',vorticity,a_vorticity,1)
fout.close()




