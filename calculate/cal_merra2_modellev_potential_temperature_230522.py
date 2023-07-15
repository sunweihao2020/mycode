import numpy as np
import xarray as xr
import os
import math

src_path = '/home/sun/wd_disk/merra2_modellev/daymean/'
end_path = '/home/sun/wd_disk/merra2_modellev/potential_t/'

file_list = os.listdir(src_path) ; file_list.sort()

# test
f0 = xr.open_dataset(src_path + file_list[1])
pt = f0['T'].data * np.power((100000/f0['PL'].data), 0.286)

#print(pt)
for ffff in file_list:
    f1 = xr.open_dataset(src_path + ffff)

    f2 = xr.DataArray(f1['T'].data * np.power((100000/f1['PL'].data), 0.286), coords=[f1.time.data, f1.lev.data, f1.lat.data, f1.lon.data], dims=["time", "lev", "lat", "lon"])
    f2.to_netcdf(end_path + ffff)