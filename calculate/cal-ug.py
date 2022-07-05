import os
import numpy as np
import Ngl, Nio
import numpy.ma as ma
from geopy.distance import distance
import sys
from netCDF4 import Dataset
import math
import copy
sys.path.append("/data5/2019swh/paint/meri-ciru/code/module/")
from module_sun import *
from module_writenc import *
path = "/data5/2019swh/data/"
f1 = Nio.open_file(path+"composite3.nc")
h  = f1.variables["H"][:]
uwind = f1.variables["uwind"][:]
lat = f1.variables["lat"][:]
lon = f1.variables["lon"][:]
time = f1.variables["time"][:]
level = f1.variables["level"][:]
omega = 7.29e-5
sinlat = np.array([])
for ll in lat:
    sinlat = np.append(sinlat,math.sin(math.radians(ll)))

f = 2*omega*sinlat
disy = np.array([])
disx = np.array([])
for i in range(0,360):
    disy = np.append(disy,distance((lat[i],0),(lat[i+1],0)).m)

for i in range(0,361):
    disx = np.append(disx, distance((lat[i], lon[0]), (lat[i], lon[1])).m)


location = np.array([0])
for dddd in range(0,360):
    location = np.append(location,np.sum(disy[:dddd+1]))

gradient = np.zeros((61,42,361,576))
gradient = ma.array(gradient,mask=h.mask)
gradient2 = copy.deepcopy(gradient)
gradient3 = copy.deepcopy(gradient)
for t in range(0,61):
    for lev in range(0,42):
        gradient[t,lev,:,:] = np.gradient(h[t,lev,:,:],location,axis=0)


ug = ma.zeros((61,42,361,576))
ug = ma.array(ug, mask=h.mask)
vg = copy.deepcopy(ug)

for t in range(0,61):
    for lev in range(0,42):
        for latt in range(0,361):
            ug[t,lev,latt,:] = -1*gradient[t,lev,latt,:]/f[latt]
'''乘以重力加速度'''
ug = ug*9.8
#ug[:,:,180,:] = ma.masked

'''计算vg'''
for t in range(0,61):
    for lev in range(0,42):
        for latt in range(1,360):
            vg[t,lev,latt,:] = np.gradient(h[t,lev,latt,:],disx[latt],axis=0)
            vg[t,lev,latt,:] = 9.8*vg[t,lev,latt,:]/f[latt]

'''计算偏ug偏x'''

for t in range(0,61):
    for lev in range(0,42):
        for yy in range(1,360):
            gradient2[t,lev,yy,:] = np.gradient(ug[t,lev,yy,:],disx[yy],axis=0)

variable1 = uwind*gradient2
variable2 = ma.array(ma.zeros((61,42,361,576)),mask=h.mask)
for yy in range(0,361):
    variable2[:,:,yy,:] = variable1[:,:,yy,:]*f[yy]
'''计算lamda
λ^2 = fη-K^2
'''
#计算η
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

fin = ma.array(ma.zeros((61,42,361,576)),mask=h.mask)
for t in range(0,61):
    for lev in range(0,42):
        for yyyy in range(0,361):
            for xxxx in range(0,576):
                fin[t,lev,yyyy,xxxx] = variable2[t,lev,yyyy,xxxx]/itata[t,lev,yyyy,xxxx]

fin[ fin>100 ] = ma.masked

file=Dataset('/data5/2019swh/data/ugvg.nc','w',format='NETCDF4')
level_out = file.createDimension("level",len(level))
time_out  = file.createDimension("time",61)
lat_out   = file.createDimension("lat",len(lat))
lon_out   = file.createDimension("lon",len(lon))

times     = file.createVariable("time","f8",("time",))
times.long_name = 'time'
months=np.arange(61)+1
times[:] = months

levels    = file.createVariable("level","f8",("level",))
levels.units = 'hPa'
levels[:] = level

latitudes = file.createVariable("lat","f4",("lat",))
latitudes.units= 'degrees_north'
latitudes[:] = lat

longitudes= file.createVariable("lon","f4",("lon",))
longitudes.units = 'degrees_east'
longitudes[:] = lon

uwinds    = file.createVariable("uwind","f8",("time","level","lat","lon"),fill_value=45275)
uwinds.units = 'm s-1'
uwinds.valid_range =	[-1000,1000]
uwinds[:] = ug

vwinds    = file.createVariable("vwind","f8",("time","level","lat","lon"),fill_value=45275)
vwinds.units = 'm s-1'
vwinds.valid_range =	[-1000,1000]
vwinds[:] = vg

file.close()
