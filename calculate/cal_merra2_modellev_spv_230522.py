import numpy as np
import xarray as xr
import os
import math

src_path1 = '/home/sun/wd_disk/merra2_modellev/abs_vorticity/'
src_path2 = '/home/sun/wd_disk/merra2_modellev/potential_t/'
end_path = '/home/sun/wd_disk/merra2_modellev/spv/'

file_list = os.listdir(src_path1) ; file_list.sort()

# test
#f0 = xr.open_dataset(src_path + file_list[1])
#pt = f0['T'].data * np.power((100000/f0['PL'].data), 0.286)

#print(pt)
for ffff in file_list:
    f1 = xr.open_dataset(src_path1 + ffff)
    f2 = xr.open_dataset(src_path2 + ffff)

    f3 = xr.DataArray(f1['__xarray_dataarray_variable__'].data * f2['__xarray_dataarray_variable__'].data * -1, coords=[f1.time.data, f1.lev.data, f1.lat.data, f1.lon.data], dims=["time", "lev", "lat", "lon"])
    f3.to_netcdf(end_path + ffff)