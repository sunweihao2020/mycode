'''
2022-7-26
This script modify rest file for experiment b1850_tx_indian_h0_220718
Because in the spin up I forget remove the topography, here I modify restart file and continue experiment
'''
import xarray as xr


path  =  "/public1/home/lym/swh/cesm/scratch/b1850_tx_indian_h0_220718/run/"

f0    =  xr.open_dataset(path+'b1850_tx_indian_h0_220718.cam.h0.0058-12.nc')
f1    =  xr.open_dataset(path+'b1850_tx_indian_h0_220718.cam.i.0059-01-01-00000.nc')
f2    =  xr.open_dataset(path+'b1850_tx_indian_h0_220718.cam.r.0059-01-01-00000.nc')
f3    =  xr.open_dataset(path+'b1850_tx_indian_h0_220718.cam.rs.0059-01-01-00000.nc')
# f0 和 f2文件里面有PHIS这个量

lat1  =  0
lat2  =  23
lon1  =  65
lon2  =  90

for i in range(len(f2.lon)):
    for j in range(len(f2.lat)):
        if (f2.lat.data[j] > lat1 and f2.lat.data[j] < lat2 and f2.lon.data[i] < lon2 and f2.lon.data[i] > lon1):
            f0.PHIS.data[0,j,i] = 0
            f2.PHIS.data[j,i]   = 0
            
f0.to_netcdf('/public1/home/lym/swh/code/b1850_tx_indian_h0_220718.cam.h0.0058-12.nc')
f2.to_netcdf('/public1/home/lym/swh/code/b1850_tx_indian_h0_220718.cam.r.0059-01-01-00000.nc')