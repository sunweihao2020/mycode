'''
2021/8/28
本代码计算GPCP降水的日平均
时间跨度为1997~2019 23年
'''
import os
import xarray as xr
import numpy as np

path1  =  '/data5/2019swh/mydown/GPCP/'
path3  =  '/data5/2019swh/data/year_mean/gpcp_97_19/'

var  =  ["precip"]
joint_array = np.zeros((365,180,360))
#年循环365-数据长度循环20-
for day in range(0,365):
    files_1997      =    os.listdir(path1+"1997/")  ;  files_1997.sort()
    base_array      =    xr.open_dataset(path1+"1997/"+files_1997[day])
    base_array      =    base_array[var]
    for year in range(1998,2020):
        path        =    path1+str(year)+"/"
        file_list   =    os.listdir(path) ; file_list.sort()
        file        =    xr.open_dataset(path+file_list[day])
        file2       =    file[var]
        for var_name in base_array.keys():
            base_array[var_name].data += file2[var_name].data

    for vars in base_array.keys():
        base_array[vars].data /= 23

    base_array.to_netcdf(path3+"gpcp_"+files_1997[day][23:27]+".climate.nc")
    joint_array[day, :, :] = base_array.precip.data[0, :, :]

time       =  np.arange(0,365,1)
lon_gpcp   =  base_array.longitude.data
lat_gpcp   =  base_array.latitude.data

gpcp_file  =  xr.Dataset(
    {
        "prect":(["time","lat","lon"],joint_array),
    },
    coords={
        "lon":(["lon"],lon_gpcp),
        "lat":(["lat"],lat_gpcp),
        "time":(["time"],time),
    },
)

gpcp_file.prect.attrs  =  base_array.precip.attrs
gpcp_file.to_netcdf("/data5/2019swh/data/gpcp_prect_365_climate.nc")