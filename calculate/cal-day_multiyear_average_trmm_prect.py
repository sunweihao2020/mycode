'''
2021/8/30
本代码使用trmm降水资料来计算气候态的降水
'''
import os
import xarray as xr
import numpy as np

path1  =  '/data5/2019swh/mydown/trmm_precipitation/'
path3  =  '/data5/2019swh/data/year_mean/trmm_98_19/'

var         = ["precipitation"]
joint_array = np.zeros((365,1440,400))
file_list   = os.listdir(path1)
#年循环365-数据长度循环20-
for day in range(0,365):
    files_1999      =    [x for x in file_list if ("Daily.1999" in x)] ; files_1999.sort()
    base_array      =    xr.open_dataset(path1+files_1999[day])
    base_array      =    base_array[var]
    for year in range(2000,2020):
        file_list2  =    [x for x in file_list if ("Daily."+str(year) in x)] ; file_list2.sort()
        file        =    xr.open_dataset(path1+file_list2[day])
        file2       =    file[var]
        for var_name in base_array.keys():
            base_array[var_name].data += file2[var_name].data

    for vars in base_array.keys():
        base_array[vars].data /= 21

    base_array.to_netcdf(path3+"trmm_"+files_1999[day][15:19]+".climate.nc")
    joint_array[day, :, :] = base_array.precipitation.data[:, :]

time       =  np.arange(0,365,1)
lon_trmm   =  base_array.lon.data
lat_trmm   =  base_array.lat.data

trmm_file  =  xr.Dataset(
    {
        "prect":(["time","lon","lat"],joint_array),
    },
    coords={
        "lon":(["lon"],lon_trmm),
        "lat":(["lat"],lat_trmm),
        "time":(["time"],time),
    },
)

trmm_file.prect.attrs  =  base_array.precip.attrs
trmm_file.to_netcdf("/data5/2019swh/data/trmm_prect_365_climate.nc")
