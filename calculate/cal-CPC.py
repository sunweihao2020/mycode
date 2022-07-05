'''这波啊，这波是计算降水的合成平均'''
import os
import numpy as np
import Ngl, Nio
import json
import numpy.ma as ma
import sys
from netCDF4 import Dataset
sys.path.append("/data5/2019swh/paint/meri-ciru/code/module")
from module_sun import *
path = "/data5/2019swh/down/CPC/"
with open("/data5/2019swh/data/onsetdate.json",'r') as load_f:
    a = json.load(load_f)

years = np.array(list(a.keys()))
days  = np.array(list(a.values()))
years = years.astype(np.int)
days = days.astype(np.int)

year = np.arange(1980,2020)
maskf = Nio.open_file(path+"1982/precip.1982.nc")
maskp = maskf.variables["precip"]
#np.savez("/data5/2019swh/data/mask_cpc.npz",precip=m[121,:,:])

precip = initial_mask('precip',(31,360,720),"/data5/2019swh/data/mask_cpc.npz")
'''这里计算30+1+60=31天'''
for yyyy in range(0,40):
    path1 = path+str(year[yyyy])+"/"
    name  = "precip."+str(year[yyyy])+".nc"
    f = Nio.open_file(path1+name)
    lon = f.variables["lon"][:]
    lat = f.variables["lat"][:]
    precip1 = f.variables["precip"][:]
    j = 0
    day0 = days[yyyy]
    for dddd in np.arange(day0-30,day0+1):
        precip[j,:,:] += precip1[dddd,:,:]/40
        j +=1

file=Dataset('/data5/2019swh/data/composite1_cpc_1020.nc','w',format='NETCDF4')
time_out  = file.createDimension("time",31)
lat_out   = file.createDimension("lat",len(lat))
lon_out   = file.createDimension("lon",len(lon))

times     = file.createVariable("time","f8",("time",))
times.long_name = 'time'
months=np.arange(31)+1
times[:] = months


latitudes = file.createVariable("lat","f4",("lat",))
latitudes.units= 'degrees_north'
latitudes[:] = lat

longitudes= file.createVariable("lon","f4",("lon",))
longitudes.units = 'degrees_east'
longitudes[:] = lon

precipitation = file.createVariable("precip","f4",("time","lat","lon"),fill_value=1e+15)
precipitation.units = 'mm'
precipitation.valid_range =	[0,1000]
precipitation[:] = precip


file.close()
del file

precip = initial_mask('precip',(30,360,720),"/data5/2019swh/data/mask_cpc.npz")
'''这里计算30+1+60=31天'''
for yyyy in range(0,40):
    path1 = path+str(year[yyyy])+"/"
    name  = "precip."+str(year[yyyy])+".nc"
    f = Nio.open_file(path1+name)
    lon = f.variables["lon"][:]
    lat = f.variables["lat"][:]
    precip1 = f.variables["precip"][:]
    j = 0
    day0 = days[yyyy]
    for dddd in np.arange(day0+1,day0+31):
        precip[j,:,:] += precip1[dddd,:,:]/40
        j +=1

file=Dataset('/data5/2019swh/data/composite2_cpc_1020.nc','w',format='NETCDF4')
time_out  = file.createDimension("time",30)
lat_out   = file.createDimension("lat",len(lat))
lon_out   = file.createDimension("lon",len(lon))

times     = file.createVariable("time","f8",("time",))
times.long_name = 'time'
months=np.arange(30)+1
times[:] = months


latitudes = file.createVariable("lat","f4",("lat",))
latitudes.units= 'degrees_north'
latitudes[:] = lat

longitudes= file.createVariable("lon","f4",("lon",))
longitudes.units = 'degrees_east'
longitudes[:] = lon

precipitation = file.createVariable("precip","f4",("time","lat","lon"),fill_value=1e+15)
precipitation.units = 'mm'
precipitation.valid_range =	[0,1000]
precipitation[:] = precip


file.close()



