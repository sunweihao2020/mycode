import numpy as np
import xarray as xr


f1     =  xr.open_dataset('/home/sun/mydown/model_input/b1850/gx1v6_090205.nc')
bathy  =  np.fromfile("/home/sun/data/cesm/topography_20090204.ieeei4",dtype='>i4')

lat1      =  0.0
lat2      =  0.4014257279586958
lon1      =  1.1344640137963142
lon2      =  1.5707963267948966


new_mask   =  f1.grid_imask.data
new_lat    =  f1.grid_center_lat.data
new_lon    =  f1.grid_center_lon.data
print(new_lat)
import math

for i in range(0,len(f1.grid_imask)):
    if (f1.grid_center_lat.data[i] > lat1) and (f1.grid_center_lat.data[i] < lat2) and (f1.grid_center_lon.data[i] > lon1) and (f1.grid_center_lon.data[i] < lon2):
        new_mask[i]  =  1

print((new_mask==f1.grid_imask.data).all())
    
ncfile  =  xr.Dataset(
    {
        "grid_dims": (["grid_rank"], f1.grid_dims.data),
        "grid_center_lat": (["grid_size"], f1.grid_center_lat.data),
        "grid_center_lon": (["grid_size"], f1.grid_center_lon.data),     
        "grid_area": (["grid_size"], f1.grid_area.data), 
        "grid_imask": (["grid_size"],new_mask), 
        "grid_corner_lat": (["grid_size","grid_corners"], f1.grid_corner_lat.data),
        "grid_corner_lon": (["grid_size","grid_corners"], f1.grid_corner_lon.data),
    },
)
ncfile.grid_center_lat.attrs  =  f1.grid_center_lat.attrs
ncfile.grid_center_lon.attrs  =  f1.grid_center_lon.attrs
ncfile.grid_imask.attrs       =  f1.grid_imask.attrs
ncfile.grid_corner_lat.attrs  =  f1.grid_corner_lat.attrs
ncfile.grid_corner_lon.attrs  =  f1.grid_corner_lon.attrs
ncfile.attrs  =  f1.attrs

ncfile.to_netcdf('/home/sun/data/cesm/gx1v6_220610_indian.nc')