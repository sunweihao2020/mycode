'''
2021/8/26
本代码将cesm2的output中降水数据以及merra2降水拼接起来以供画图
'''
import os
import numpy as np
import xarray as xr

path_cesm  =  '/data5/2019swh/model_data/control/year_mean/'
path_merra2 =  '/data5/2019swh/data/year_mean/single/'

file_cesm   =   os.listdir(path_cesm) ; file_cesm.sort()
file_merra2 =   os.listdir(path_merra2) ; file_merra2.sort()

array_cesm = np.zeros((365,192,288)) ; array_merra2 = np.zeros((365,361,576))

for i in range(0,365):
    file2_cesm  =  xr.open_dataset(path_cesm+file_cesm[i])
    file2_merra2 =  xr.open_dataset(path_merra2+file_merra2[i])
    array_cesm[i,:,:]     =  file2_cesm.PRECT.data[0,:,:]
    array_merra2[i,:,:]   =  file2_merra2.TPRECMAX.data[0,:,:]

time       =  np.arange(0,365,1)
lon_cesm   =  file2_cesm.lon.data
lon_merra2 =  file2_merra2.lon.data
lat_cesm   =  file2_cesm.lat.data
lat_merra2 =  file2_merra2.lat.data

cesm_file  =  xr.Dataset(
    {
        "prect":(["time","lat","lon"],array_cesm),
    },
    coords={
        "lon":(["lon"],lon_cesm),
        "lat":(["lat"],lat_cesm),
        "time":(["time"],time),
    },
)

merra2_file  =  xr.Dataset(
    {
        "prect":(["time","lat","lon"],array_merra2),
    },
    coords={
        "lon":(["lon"],lon_merra2),
        "lat":(["lat"],lat_merra2),
        "time":(["time"],time),
    },
)

#处理属性赋值
cesm_file.prect.attrs  =  file2_cesm.PRECT.attrs
merra2_file.prect.attrs=  file2_merra2.TPRECMAX.attrs

cesm_file.to_netcdf("/data5/2019swh/data/cesm_control_prect_365_climate.nc")
merra2_file.to_netcdf("/data5/2019swh/data/merra2_prect_365_climate.nc")