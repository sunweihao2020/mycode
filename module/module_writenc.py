import os
import numpy as np
import numpy.ma as ma
from geopy.distance import distance
import sys
from netCDF4 import Dataset

def create_nc_multiple(path,name,time,level,lon,lat):
    list_path = os.listdir(path)
    if name in list_path:
        os.system("rm -rf "+path+name+".nc")
    
    file = Dataset(path+name+".nc","w",format = 'NETCDF4')


    time_out  = file.createDimension("time",len(time))
    level_out = file.createDimension("level",len(level))
    lat_out   = file.createDimension("lat",len(lat))
    lon_out   = file.createDimension("lon",len(lon))

    levels    = file.createVariable("level","f8",("level",))
    levels.units = 'hPa'
    levels[:] = level

    times     = file.createVariable("time","f4",("time",))
    times.long_name = 'time'
    tttt=np.arange(len(time))+1
    times[:] = tttt

    latitudes = file.createVariable("lat","f4",("lat",))
    latitudes.units= 'degrees_north'
    latitudes[:] = lat
    
    longitudes= file.createVariable("lon","f4",("lon",))
    longitudes.units = 'degrees_east'
    longitudes[:] = lon

    return file


def create_nc_single(path, name, time, lon, lat):
    list_path = os.listdir(path)
    if name in list_path:
        os.system("rm -rf " + path + name + ".nc")

    file = Dataset(path + name + ".nc", "w", format='NETCDF4')

    time_out = file.createDimension("time", len(time))
    lat_out = file.createDimension("lat", len(lat))
    lon_out = file.createDimension("lon", len(lon))

    times = file.createVariable("time", "f4", ("time",))
    times.long_name = 'time'
    tttt = np.arange(len(time)) + 1
    times[:] = tttt

    latitudes = file.createVariable("lat", "f4", ("lat",))
    latitudes.units = 'degrees_north'
    latitudes[:] = lat

    longitudes = file.createVariable("lon", "f4", ("lon",))
    longitudes.units = 'degrees_east'
    longitudes[:] = lon

    return file


def add_variables(file,name,variable,attribute,bool):
    if bool == 0:
        var = file.createVariable(name,"f8",("time","lat","lon"),fill_value=1e+15)
    else:
        var = file.createVariable(name,"f8",("time","level","lat","lon"),fill_value=1e+15)

    a = list(attribute.items())
    for i in range(0,3):
        key,value = list(attribute.items())[i]
        exec("var."+key+" = value")

    var[:] = variable    