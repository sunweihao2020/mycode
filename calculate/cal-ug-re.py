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
path = "/data5/2019swh/data/"
f1 = Nio.open_file(path+"composite3.nc")
h  = f1.variables["H"][:]
uwind = f1.variables["uwind"][:]
lat = f1.variables["lat"][:]
lon = f1.variables["lon"][:]
time = f1.variables["time"][:]
level = f1.variables["level"][:]

ug,vg = cal_gepstrophic_wind(h,lat,lon)
'''输出地转风的文件
file = create_nc("/data5/2019swh/data/","ugvg",time,level,lon,lat)
add_variables(file,"ug",ug,a_uwind)
add_variables(file,"vg",vg,a_vwind)

file.close()
'''
disy,disx,location = cal_xydistance(lat,lon)
gradient = np.zeros((61,42,361,576))
gradient = ma.array(gradient,mask=h.mask)
gradient2 = copy.deepcopy(gradient)
gradient3 = copy.deepcopy(gradient)
for t in range(0,61):
    for lev in range(0,42):
        for yy in range(1,360):
            gradient2[t,lev,yy,:] = np.gradient(ug[t,lev,yy,:],disx[yy],axis=0)

sinlat = np.array([]) #生成科里奥利力数组
for ll in lat:
    sinlat = np.append(sinlat,math.sin(math.radians(ll)))
omega = 7.29e-5
f = 2*omega*sinlat

for t in range(0,61):
    for lev in range(0,42):
        gradient3[t,lev,:,:] = np.gradient(ug[t,lev,:,:],location,axis=0)

ita = ma.array(ma.zeros((61,42,361,576)),mask=h.mask)
for t in range(0,61):
    for lev in range(0,42):
        for yyyy in range(0,361):
            ita[t,lev,yyyy,:] = f[yyyy]-gradient3[t,lev,yyyy,:]
itata = ma.array(ma.zeros((61,42,361,576)),mask=h.mask)
for yyyy in range(0,361):
    itata[:,:,yyyy,:]=f[yyyy]*ita[:,:,yyyy,:]

variable1 = uwind*gradient2
variable2 = ma.array(ma.zeros((61,42,361,576)),mask=h.mask)
for yy in range(0,361):
    variable2[:,:,yy,:] = variable1[:,:,yy,:]*f[yy]

fin = ma.array(ma.zeros((61,42,361,576)),mask=h.mask)
for t in range(0,61):
    for lev in range(0,42):
        for yyyy in range(0,361):
            for xxxx in range(0,576):
                fin[t,lev,yyyy,xxxx] = variable2[t,lev,yyyy,xxxx]/itata[t,lev,yyyy,xxxx]

v1_gradient = np.gradient(fin,location,axis=2)

file = create_nc("/data5/2019swh/data/","special_v_gradient",time,level,lon,lat)
a_v1wind = {"longname":"v1wind","units":"m s-1","valid_range":[-1e+15,1e+15]}

add_variables(file,"v1wind",v1_gradient,a_v1wind)

file.close()
