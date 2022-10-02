'''
2022-9-24
This code interpolate mask data to the new coordination
old is (361,576) new is (181,360)
'''
import xarray as xr
import numpy as np

f0  =  xr.open_dataset("/home/sun/qomo-data/composite-single_merra2_stream_vp_function.nc")
f1  =  xr.open_dataset("/home/sun/qomo-data/merra2_land_sea_mask.nc")

lat_old  =  f1.lat.data
lon_old  =  f1.lon.data

# new coordination to interpolate
lat_new  =  f0.lat.data
lon_new  =  f0.lon.data

ocean_fraction  =  f1.FROCEAN.data[0].copy()


in_frc_1  =  np.zeros((ocean_fraction.shape[0],lon_new.shape[0]))
in_frc_2  =  np.zeros((lat_new.shape[0],lon_new.shape[0]))

for yy in range(0,lat_old.shape[0]):
    in_frc_1[yy,:]  =  np.interp(lon_new,lon_old,ocean_fraction[yy,:])

for xx in range(0,lon_new.shape[0]):
    in_frc_2[:,xx]  =  np.interp(lat_new,lat_old,in_frc_1[:,xx])

ncfile  =  xr.Dataset(
    {
        "ocean_fraction": (["lat","lon"], in_frc_2),
    },
    coords={
        "lat": (["lat"], lat_new),
        "lon": (["lon"], lon_new),
    },
)
ncfile.ocean_fraction.attrs  =  f1.FROCEAN.attrs
ncfile["lon"].attrs  =  f1["lon"].attrs
ncfile["lat"].attrs  =  f1["lat"].attrs
ncfile.attrs['description']  =  '20220924 This file include ocean fraction in which 1 means ocean. For paint goals I interpolate raw data to the new lat/lon of shape (180,361)'


ncfile.to_netcdf("/home/sun/qomo-data/merra2_land_sea_mask_low_resolution.nc")