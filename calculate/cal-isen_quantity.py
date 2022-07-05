'''
2020/11/23
merra2合成分析插值到等熵面
计算等熵面上物理量用以诊断对称不稳定 绝对动量M
计算等熵面上的绝对涡度
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
#from attribute import *

path = "/data5/2019swh/data/"
f1 = Nio.open_file(path+"isentropic_theate_data.nc")
lon = f1.variables["lon"][:]
lat = f1.variables["lat"][:]
time = f1.variables["time"][:]
level = f1.variables["lev"][:]
ug  =   f1.variables["ug"][:]
ug1  =  copy.deepcopy(ug[:,:,180:,:])
disy,disx,location = cal_xydistance(lat[180:],lon)

sinlat = np.array([]) #生成科里奥利力数组
for ll in lat[180:]:
    sinlat = np.append(sinlat,math.sin(math.radians(ll)))
omega = 7.29e-5
f = 2*omega*sinlat

#从0.5°开始


#mg = copy.deepcopy(ug1)
#
#for t in range(0,61):
#    for l in range(0,9):
#        for y in range(0,181):
#            mg[t,l,y,:] = f[y]*location[y] - ug1[t,l,y,:]
#
#
#
#mgy = copy.deepcopy(ug1)
#for t in range(0,61):
#    for lev in range(0,9):
#        mgy[t,lev,:,:] = np.gradient(mg[t,lev,:,:],location,axis=0)


ugy = copy.deepcopy(ug1)
for t in range(0,61):
    for lev in range(0,9):
        ugy[t,lev,:,:]  =   np.gradient(ug1[t,lev,:,:],location,axis=0)

for t in range(0,61):
    for lev in range(0,9):
        for y in range(0,181):
            ugy[t,lev,y,:] = f[y] - ugy[t,lev,y,:]

file = create_nc_multiple("/data5/2019swh/data/","isen_quantity_e",time,level,lon,lat[180:])
#a_mg   = {"longname":"dongliang","units":"m/s","valid_range":[-1e+15,1e+15]}
#a_mgy   = {"longname":"aboslute_vorticity","units":"s-1","valid_range":[-1e+15,1e+15]}
a_av    = {"longname":"aboslute_vorticity2","units":"s-1","valid_range":[-1e+15,1e+15]}
#add_variables(file,"M",mg,a_mg)
#add_variables(file,"My",mgy,a_mgy)
add_variables(file,"av",ugy,a_av,1)
file.close()