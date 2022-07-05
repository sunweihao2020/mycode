'''
2021/9/11
本代码对庄默然的模式输出数据进行处理
原实验是1983-2004，因此从1985开始往后取
'''
import os
import xarray as xr
import numpy as np

path_control  =  '/data5/dam/zhmr/data/FAMIL_ICIDMC/CTRL_4/daily/vars_daily/'
file1         =  os.listdir(path_control)
file_prect    =  [x for x in file1 if ("PRECT-" in x)] ; file_prect.sort()

#以1985作为base array
base          =  xr.open_dataset(path_control+file_prect[0])
base_array    =  base.PRECT.data


for yyyy in range(1,len(file_prect)):
    array2    =  xr.open_dataset(path_control+file_prect[yyyy])
    base_array  +=  array2["PRECT"].data

base_array    /=   20
base_array    *=   86400000

time       =  np.arange(0,365,1)
famil_file  =  xr.Dataset(
    {
        "prect":(["time","lat","lon"],base_array),
    },
    coords={
        "lon":(["lon"],base.lon.data),
        "lat":(["lat"],base.lat.data),
        "time":(["time"],time),
    },
)
famil_file.prect.attrs  =  base.PRECT.attrs
famil_file.prect.attrs["units"]  =  "mm/day"
famil_file.to_netcdf("/data5/2019swh/data/famil_zhuang_climate_prect.nc")
#base_array.to_netcdf("/data5/2019swh/data/famil_zhuang_climate_prect.nc")
