'''
2021/9/21
本代码根据daily的数据来计算monthly
'''
import os
import sys
import xarray as xr
import numpy as np

vars  =  ["OMEGA","Q","T","U","V","Z3"]
expe  =  ["icid","ic","id","con"]

sys.path.append("/data5/2019swh/mycode/module/")
from module_sun import *

def create_nc(out,base,time,path,name,var):
    ncfile  =  xr.Dataset(
        {
            var: (["time", "lev","lat", "lon"], out),
        },
        coords={
            "lon": (["lon"], base.lon.data),
            "lat": (["lat"], base.lat.data),
            "time": (["time"], time),
            "lev":(["lev"],base.lev.data)
        },
    )
    ncfile["lev"].attrs  =  base["lev"].attrs
    ncfile["lat"].attrs  =  base["lat"].attrs
    ncfile["lon"].attrs  =  base["lon"].attrs
    ncfile[var].attrs  =  base[var].attrs
    ncfile.to_netcdf(path+name)

path      =  "/data5/2019swh/data/zhuang_plev/"
path_out  =  "/data5/2019swh/data/zhuang_plev/"
months = np.arange(1,13)
for var in vars:
    for name in expe:
        f  =  xr.open_dataset(path+"plev_"+name+"_"+var+".nc")
        avg_mon  =  cal_monthly_average_daily(f[var])

        create_nc(avg_mon,f,months,path_out,"plev_monthly_"+name+"_"+var+".nc",var)