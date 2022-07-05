'''计算1980-2019 40年平均'''
'''计算了以下几个量 ：u v omega epv temperature'''
import os
import numpy as np
import numpy.ma as ma
import Ngl, Nio
from netCDF4 import Dataset

masked=np.load('/data5/2019swh/data/merra2_mask-3d.npz')
dimension=np.load('/data5/2019swh/data/dimension.npz')
umask=masked['u'];vmask=masked['v'];omegamask=masked['omega'];epvmask=masked['epv'];tmask=masked['t']
lon=dimension['lon']
lat=dimension['lat']
lev=dimension['lev']
time=dimension['time']

path='/data1/MERRA2/monthly/instM_3d_asm_Np/'
file_list = os.listdir("/data1/MERRA2/monthly/instM_3d_asm_Np")
file_list.sort()

u=ma.zeros((12,42,361,576))
v=ma.zeros((12,42,361,576))
omega=ma.zeros((12,42,361,576))
epv  = ma.zeros((12,42,361,576))
t    = ma.zeros((12,42,361,576))
h    = ma.zeros((12,42,361,576))
for mon in range(0,12):
    u[mon,:,:,:]=ma.array(u[mon,:,:,:],mask=umask[0,:,:,:])
    v[mon, :, :, :] = ma.array(v[mon,:,:,:], mask=vmask[0,:,:,:])
    omega[mon, :, :, :] = ma.array(omega[mon,:,:,:], mask=omegamask[0,:,:,:])
    epv[mon, :, :, :] = ma.array(epv[mon,:,:,:], mask=epvmask[0,:,:,:])
    t[mon, :, :, :] = ma.array(t[mon,:,:,:], mask=tmask[0,:,:,:])
    h[mon, :, :, :] = ma.array(h[mon,:,:,:], mask=tmask[0,:,:,:])
'''
f=Nio.open_file(path+file_list[0])
u=f.variables['U'][:]
v=f.variables['V'][:]
lon  =f.variables["lon"][:]
lat  =f.variables["lat"][:]
lev  =f.variables["lev"][:]
time =f.variables["time"][:]
'''
j=0
for year in range(1980,1992):
    for month in range(1,13):
        if month <10:
            f=Nio.open_file('/data1/MERRA2/monthly/instM_3d_asm_Np/MERRA2_100.instM_3d_asm_Np.'+str(year)+'0'+str(month)+'.nc4')
        else:
            f = Nio.open_file('/data1/MERRA2/monthly/instM_3d_asm_Np/MERRA2_100.instM_3d_asm_Np.' + str(year) +str(month) + '.nc4')
        u1 = f.variables['U'][:]
        v1 = f.variables['V'][:]
        omega1 = f.variables['OMEGA'][:]
        epv1 = f.variables['EPV'][:]
        t1  =  f.variables['T'][:]
        h1  =  f.variables['H'][:]
        u[month - 1, :, :, :] += u1[0, :, :, :] / 39
        v[month - 1, :, :, :] += v1[0, :, :, :] / 39
        omega[month - 1, :, :, :] += omega1[0, :, :, :] / 39
        epv[month -1, :, :, :] += epv1[0,:,:,:]/39
        t[month - 1, :, :, :] += t1[0, :, :, :] / 39
        h[month - 1, :, :, :] += h1[0, :, :, :] / 39
    j+=1


for year in range(1992,2001):
    for month in range(1,13):
        if month <10:
            f=Nio.open_file('/data1/MERRA2/monthly/instM_3d_asm_Np/MERRA2_200.instM_3d_asm_Np.'+str(year)+'0'+str(month)+'.nc4')
        else:
            f = Nio.open_file('/data1/MERRA2/monthly/instM_3d_asm_Np/MERRA2_200.instM_3d_asm_Np.' + str(year) +str(month) + '.nc4')
        u1 = f.variables['U'][:]
        v1 = f.variables['V'][:]
        omega1 = f.variables['OMEGA'][:]
        epv1 = f.variables['EPV'][:]
        t1 = f.variables['T'][:]
        h1 = f.variables['H'][:]
        u[month - 1, :, :, :] += u1[0, :, :, :] / 39
        v[month - 1, :, :, :] += v1[0, :, :, :] / 39
        omega[month - 1, :, :, :] += omega1[0, :, :, :] / 39
        epv[month - 1, :, :, :] += epv1[0, :, :, :] / 39
        t[month - 1, :, :, :] += t1[0, :, :, :] / 39
        h[month - 1, :, :, :] += h1[0, :, :, :] / 39
    j += 1

for year in range(2001,2011):
    for month in range(1,13):
        if month <10:
            f=Nio.open_file('/data1/MERRA2/monthly/instM_3d_asm_Np/MERRA2_300.instM_3d_asm_Np.'+str(year)+'0'+str(month)+'.nc4')
        else:
            f = Nio.open_file('/data1/MERRA2/monthly/instM_3d_asm_Np/MERRA2_300.instM_3d_asm_Np.' + str(year) +str(month) + '.nc4')
        u1 = f.variables['U'][:]
        v1 = f.variables['V'][:]
        omega1 = f.variables['OMEGA'][:]
        epv1 = f.variables['EPV'][:]
        t1 = f.variables['T'][:]
        h1 = f.variables['H'][:]
        u[month - 1, :, :, :] += u1[0, :, :, :] / 39
        v[month - 1, :, :, :] += v1[0, :, :, :] / 39
        omega[month - 1, :, :, :] += omega1[0, :, :, :] / 39
        epv[month - 1, :, :, :] += epv1[0, :, :, :] / 39
        t[month - 1, :, :, :] += t1[0, :, :, :] / 39
        h[month - 1, :, :, :] += h1[0, :, :, :] / 39
    j += 1

for year in range(2011,2019):
    for month in range(1,13):
        if month < 10:
            f = Nio.open_file('/data1/MERRA2/monthly/instM_3d_asm_Np/MERRA2_400.instM_3d_asm_Np.' + str(year) + '0' + str(month) + '.nc4')
        else:
            f = Nio.open_file('/data1/MERRA2/monthly/instM_3d_asm_Np/MERRA2_400.instM_3d_asm_Np.' + str(year) + str(month) + '.nc4')
        u1 = f.variables['U'][:]
        v1 = f.variables['V'][:]
        omega1 = f.variables['OMEGA'][:]
        epv1 = f.variables['EPV'][:]
        t1 = f.variables['T'][:]
        h1 = f.variables['H'][:]
        u[month - 1, :, :, :] += u1[0, :, :, :] / 39
        v[month - 1, :, :, :] += v1[0, :, :, :] / 39
        omega[month - 1, :, :, :] += omega1[0, :, :, :] / 39
        epv[month - 1, :, :, :] += epv1[0, :, :, :] / 39
        t[month - 1, :, :, :] += t1[0, :, :, :] / 39
        h[month - 1, :, :, :] += h1[0, :, :, :] / 39
    j += 1
        
file=Dataset('/data5/2019swh/data/mean_merra2_multilayer_0921.nc','w',format='NETCDF4')
level_out = file.createDimension("level",len(lev))
time_out  = file.createDimension("time",12)
lat_out   = file.createDimension("lat",len(lat))
lon_out   = file.createDimension("lon",len(lon))

times     = file.createVariable("time","f8",("time",))
times.long_name = 'time'
months=np.arange(12)+1
times[:] = months

levels    = file.createVariable("level","f8",("level",))
levels.units = 'hPa'
levels[:] = lev

latitudes = file.createVariable("lat","f4",("lat",))
latitudes.units= 'degrees_north'
latitudes[:] = lat

longitudes= file.createVariable("lon","f4",("lon",))
longitudes.units = 'degrees_east'
longitudes[:] = lon

uwinds    = file.createVariable("uwind","f8",("time","level","lat","lon"),fill_value=45275)
uwinds.units = 'm s-1'
uwinds.valid_range =	[-1000,1000]
uwinds[:] = u

vwinds    = file.createVariable("vwind","f8",("time","level","lat","lon"),fill_value=45275)
vwinds.units = 'm s-1'
vwinds.valid_range =	[-1000,1000]
vwinds[:] = v

OMEGA     = file.createVariable("OMEGA","f8",("time","level","lat","lon"),fill_value=45275)
OMEGA.units  = 'Pa s-1'
OMEGA.valid_range =	[-1000,1000]
OMEGA[:] = omega

EPV       = file.createVariable("EPV","f8",("time","level","lat","lon"),fill_value=45275000)
EPV.units= 'K m+2 kg-1 s-1'
EPV.valid_range = [-10000,10000]
EPV[:] = epv

T         = file.createVariable("T","f8",("time","level","lat","lon"),fill_value=45275)
T.units = 'K'
T.valid_range =	[-1000,1000]
T[:] = t

H         = file.createVariable("H","f8",("time","level","lat","lon"),fill_value=1e+15)
H.units = 'm'
H.valid_range =	[-1e+15, 1e+15]
H[:] = h


file.close()

print(j)
