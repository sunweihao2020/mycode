'''计算1980-2019 39年平均'''
'''计算了以下几个量 ：
2-meter_specific_humidity
10-meter_air_temperature
2-meter_air_temperature
surface_skin_temperature
10-meter_eastward_wind
2-meter_eastward_wind
2-meter_northward_wind
10-meter_northward_wind
'''


import os
import numpy as np
import numpy.ma as ma
import Ngl, Nio
from netCDF4 import Dataset

def zero_mask(variable_in,variable_out):
    mask=ma.getmaskarray(variable_in[0,:,:])
    variable_out=ma.array(variable_out,mask=mask)
    return variable_out

'''这里我对每个变量都取出掩码数组'''
variables=['QV2M','T10M','T2M','TS','U10M','V10M','U2M','V2M']

PS=ma.zeros((12,361,576))
masked = np.load('/data5/2019swh/data/single-layer.npz')
dimension = np.load('/data5/2019swh/data/dimension.npz')
for i in range(0,8):
    exec(variables[i]+"_m=masked['"+variables[i]+"']")
    exec(variables[i]+"=ma.zeros((12,361,576))")
    for mon in range(0,12):
        exec(variables[i]+"["+str(mon)+",:,:]=zero_mask("+variables[i]+"_m,"+variables[i]+"["+str(mon)+",:,:])")
        PS[mon,:,:]=zero_mask(QV2M_m,PS[mon,:,:])

lon = dimension['lon']
lat = dimension['lat']
lev = dimension['lev']
time = dimension['time']

path = '/data1/MERRA2/monthly/instM_2d_asm_Nx'
file_list = os.listdir("/data1/MERRA2/monthly/instM_2d_asm_Nx")
file_list.sort()


j = 0
for year in range(1980, 1992):
    for month in range(1, 13):
        if month < 10:
            f = Nio.open_file('/data1/MERRA2/monthly/instM_2d_asm_Nx/MERRA2_100.instM_2d_asm_Nx.' + str(year) + '0' + str(month) + '.SUB.nc')
            f2 = Nio.open_file('/data1/MERRA2/monthly/instM_3d_asm_Np/MERRA2_100.instM_3d_asm_Np.'+str(year) + '0'+str(month) + '.nc4')
        else:
            f = Nio.open_file('/data1/MERRA2/monthly/instM_2d_asm_Nx/MERRA2_100.instM_2d_asm_Nx.' + str(year) + str(month) + '.SUB.nc')
            f2 = Nio.open_file('/data1/MERRA2/monthly/instM_3d_asm_Np/MERRA2_100.instM_3d_asm_Np.' + str(year) + str(month) + '.nc4')
        qv2m = f.variables['QV2M'][:]
        t10m = f.variables['T10M'][:]
        t2m = f.variables['T2M'][:]
        ts = f.variables['TS'][:]
        u10m = f.variables['U10M'][:]
        u2m = f.variables['U2M'][:]
        v10m = f.variables['V10M'][:]
        v2m = f.variables['V2M'][:]
        ps   = f2.variables['PS'][:]
        QV2M[month-1,:,:] += qv2m[0, :, :] / 39
        T10M[month-1,:,:] += t10m[0, :, :] / 39
        T2M[month-1,:,:] += t2m[0, :, :] / 39
        TS[month-1,:,:] += ts[0, :, :] / 39
        U10M[month-1,:,:] += u10m[0, :, :] / 39
        V10M[month-1,:,:] += v10m[0, :, :] / 39
        U2M[month-1,:,:] += u2m[0, :, :] / 39
        V2M[month-1,:,:] += v2m[0, :, :] / 39
        PS[month-1,:,:] += ps[0,:,:] / 39
    j += 1

for year in range(1992, 2001):
    for month in range(1, 13):
        if month < 10:
            f = Nio.open_file('/data1/MERRA2/monthly/instM_2d_asm_Nx/MERRA2_200.instM_2d_asm_Nx.' + str(year) + '0' + str(month) + '.SUB.nc')
            f2 = Nio.open_file('/data1/MERRA2/monthly/instM_3d_asm_Np/MERRA2_200.instM_3d_asm_Np.' + str(year) + '0' + str(month) + '.nc4')
        else:
            f = Nio.open_file('/data1/MERRA2/monthly/instM_2d_asm_Nx/MERRA2_200.instM_2d_asm_Nx.' + str(year) + str(month) + '.SUB.nc')
            f2 = Nio.open_file('/data1/MERRA2/monthly/instM_3d_asm_Np/MERRA2_200.instM_3d_asm_Np.' + str(year) + str(month) + '.nc4')
        qv2m = f.variables['QV2M'][:]
        t10m = f.variables['T10M'][:]
        t2m = f.variables['T2M'][:]
        ts = f.variables['TS'][:]
        u10m = f.variables['U10M'][:]
        u2m = f.variables['U2M'][:]
        v10m = f.variables['V10M'][:]
        v2m = f.variables['V2M'][:]
        ps   = f2.variables['PS'][:]
        QV2M[month-1,:,:] += qv2m[0, :, :] / 39
        T10M[month-1,:,:] += t10m[0, :, :] / 39
        T2M[month-1,:,:] += t2m[0, :, :] / 39
        TS[month-1,:,:] += ts[0, :, :] / 39
        U10M[month-1,:,:] += u10m[0, :, :] / 39
        V10M[month-1,:,:] += v10m[0, :, :] / 39
        U2M[month-1,:,:] += u2m[0, :, :] / 39
        V2M[month-1,:,:] += v2m[0, :, :] / 39
        PS[month-1,:,:] += ps[0,:,:] / 39
    j += 1

for year in range(2001, 2011):
    for month in range(1, 13):
        if month < 10:
            f = Nio.open_file('/data1/MERRA2/monthly/instM_2d_asm_Nx/MERRA2_300.instM_2d_asm_Nx.' + str(year) + '0' + str(month) + '.SUB.nc')
            f2 = Nio.open_file('/data1/MERRA2/monthly/instM_3d_asm_Np/MERRA2_300.instM_3d_asm_Np.' + str(year) + '0' + str(month) + '.nc4')
        else:
            f = Nio.open_file('/data1/MERRA2/monthly/instM_2d_asm_Nx/MERRA2_300.instM_2d_asm_Nx.' + str(year) + str(month) + '.SUB.nc')
            f2 = Nio.open_file('/data1/MERRA2/monthly/instM_3d_asm_Np/MERRA2_300.instM_3d_asm_Np.' + str(year) + str(month) + '.nc4')
        qv2m = f.variables['QV2M'][:]
        t10m = f.variables['T10M'][:]
        t2m = f.variables['T2M'][:]
        ts = f.variables['TS'][:]
        u10m = f.variables['U10M'][:]
        u2m = f.variables['U2M'][:]
        v10m = f.variables['V10M'][:]
        v2m = f.variables['V2M'][:]
        ps   = f2.variables['PS'][:]
        QV2M[month-1,:,:] += qv2m[0, :, :] / 39
        T10M[month-1,:,:] += t10m[0, :, :] / 39
        T2M[month-1,:,:] += t2m[0, :, :] / 39
        TS[month-1,:,:] += ts[0, :, :] / 39
        U10M[month-1,:,:] += u10m[0, :, :] / 39
        V10M[month-1,:,:] += v10m[0, :, :] / 39
        U2M[month-1,:,:] += u2m[0, :, :] / 39
        V2M[month-1,:,:] += v2m[0, :, :] / 39
        PS[month-1,:,:] += ps[0,:,:] / 39
    j += 1

for year in range(2011, 2019):
    for month in range(1, 13):
        if month < 10:
            f = Nio.open_file('/data1/MERRA2/monthly/instM_2d_asm_Nx/MERRA2_400.instM_2d_asm_Nx.' + str(year) + '0' + str(month) + '.SUB.nc')
            f2 = Nio.open_file('/data1/MERRA2/monthly/instM_3d_asm_Np/MERRA2_400.instM_3d_asm_Np.' + str(year) + '0' + str(month) + '.nc4')
        else:
            f = Nio.open_file('/data1/MERRA2/monthly/instM_2d_asm_Nx/MERRA2_400.instM_2d_asm_Nx.' + str(year) + str(month) + '.SUB.nc')
            f2 = Nio.open_file('/data1/MERRA2/monthly/instM_3d_asm_Np/MERRA2_400.instM_3d_asm_Np.' + str(year) + str(month) + '.nc4')
        qv2m = f.variables['QV2M'][:]
        t10m = f.variables['T10M'][:]
        t2m = f.variables['T2M'][:]
        ts = f.variables['TS'][:]
        u10m = f.variables['U10M'][:]
        u2m = f.variables['U2M'][:]
        v10m = f.variables['V10M'][:]
        v2m = f.variables['V2M'][:]
        ps   = f2.variables['PS'][:]
        QV2M[month-1,:,:] += qv2m[0, :, :] / 39
        T10M[month-1,:,:] += t10m[0, :, :] / 39
        T2M[month-1,:,:] += t2m[0, :, :] / 39
        TS[month-1,:,:] += ts[0, :, :] / 39
        U10M[month-1,:,:] += u10m[0, :, :] / 39
        V10M[month-1,:,:] += v10m[0, :, :] / 39
        U2M[month-1,:,:] += u2m[0, :, :] / 39
        V2M[month-1,:,:] += v2m[0, :, :] / 39
        PS[month-1,:,:] += ps[0,:,:] / 39
    j += 1

file = Dataset('/data5/2019swh/data/mean_merra2_singlelayer_0919.nc', 'w', format='NETCDF4')
level_out = file.createDimension("level", len(lev))
time_out = file.createDimension("time", 12)
lat_out = file.createDimension("lat", len(lat))
lon_out = file.createDimension("lon", len(lon))

times = file.createVariable("time", "f8", ("time",))
times.long_name = 'time'
months = np.arange(12) + 1
times[:] = months

levels = file.createVariable("level", "f8", ("level",))
levels.units = 'hPa'
levels[:] = lev

latitudes = file.createVariable("lat", "f4", ("lat",))
latitudes.units = 'degrees_north'
latitudes[:] = lat

longitudes = file.createVariable("lon", "f4", ("lon",))
longitudes.units = 'degrees_east'
longitudes[:] = lon

qv2ms = file.createVariable("QV2M", "f8", ("time", "lat", "lon"), fill_value=45275)
qv2ms.units = 'kg kg-1'
qv2ms.valid_range = [-1000, 1000]
qv2ms[:] = QV2M

t10ms = file.createVariable("T10M", "f8", ("time", "lat", "lon"), fill_value=45275)
t10ms.units = 'K'
t10ms.valid_range = [-1000, 1000]
t10ms[:] = T10M

t2ms = file.createVariable("T2M", "f8", ("time", "lat", "lon"), fill_value=45275)
t2ms.units = 'Pa s-1'
t2ms.valid_range = [-1000, 1000]
t2ms[:] = T2M

tss = file.createVariable("TS", "f8", ("time", "lat", "lon"), fill_value=45275000)
tss.units = 'K'
tss.valid_range = [-10000, 10000]
tss[:] = TS

u10ms = file.createVariable("U10M", "f8", ("time", "lat", "lon"), fill_value=45275)
u10ms.units = 'm s-1'
u10ms.valid_range = [-1000, 1000]
u10ms[:] = U10M

v10ms = file.createVariable("V10M", "f8", ("time", "lat", "lon"), fill_value=45275)
v10ms.units = 'm s-1'
v10ms.valid_range = [-1000, 1000]
v10ms[:] = V10M

u2ms = file.createVariable("U2M", "f8", ("time", "lat", "lon"), fill_value=45275)
u2ms.units = 'm s-1'
u2ms.valid_range = [-1000, 1000]
u2ms[:] = U2M

v2ms = file.createVariable("V2M", "f8", ("time", "lat", "lon"), fill_value=45275)
v2ms.units = 'm s-1'
v2ms.valid_range = [-1000, 1000]
v2ms[:] = V2M

ps = file.createVariable("PS", "f8", ("time", "lat", "lon"), fill_value=1e+15)
u2ms.units = 'Pa'
u2ms.valid_range = [-1e+15, 1e+15]
ps[:] = PS

file.close()

print(j)
