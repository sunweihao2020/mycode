'''使用ersst计算1980-2019年的SST平均'''
'''从1854年开始算起 共2000个时次 166*12+8'''
import os
import numpy as np
import numpy.ma as ma
import Ngl, Nio
from netCDF4 import Dataset

f = Nio.open_file("/data5/2019swh/data/sst.mnmean.nc")
sst = f.variables['sst'][:]
time = f.variables['time'][:]
lat  = f.variables['lat'][:]
lon  = f.variables['lon'][:]
'''切出来40年的sst'''
SST = sst[1512:,:,:]
SST = sst[0:480,:,:]

sst_m = ma.getmaskarray(SST[6,:,:])

sst = ma.zeros((12,89,180))
for mon in range(0,12):
    sst[mon,:,:] =ma.array(sst[mon,:,:],mask=sst_m)

for yyyy in range(0,40):
    for mons in range(0,12):
        sst[mons,:,:] += SST[yyyy*12+mons,:,:]/40

file=Dataset('/data5/2019swh/data/mean_ersst_sst_0924.nc','w',format='NETCDF4')
#level_out = file.createDimension("level",len(lev))
time_out  = file.createDimension("time",12)
lat_out   = file.createDimension("lat",len(lat))
lon_out   = file.createDimension("lon",len(lon))

times     = file.createVariable("time","f8",("time",))
times.long_name = 'time'
months=np.arange(12)+1
times[:] = months

latitudes = file.createVariable("lat","f4",("lat",))
latitudes.units= 'degrees_north'
latitudes[:] = lat

longitudes= file.createVariable("lon","f4",("lon",))
longitudes.units = 'degrees_east'
longitudes[:] = lon

SST         = file.createVariable("SST","f8",("time","lat","lon"),fill_value=45275)
SST.units = 'degC'
SST.valid_range =	[-1.8, 45]
SST[:] = sst

file.close()

