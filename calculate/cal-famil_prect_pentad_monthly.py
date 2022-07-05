'''
2021/9/22
本代码对去除海陆分布的四个实验来计算降水的pentad平均及monthly平均
'''
import os
import sys
import xarray as xr
import numpy as np
module_path = ["/home/sun/mycode/module/","/data5/2019swh/mycode/module/"]
sys.path.append(module_path[1])
from module_sun import *

def create_nc(out,base,time,path,name,var):
    ncfile  =  xr.Dataset(
        {
            var: (["time","lat", "lon"], out),
        },
        coords={
            "lon": (["lon"], base.lon.data),
            "lat": (["lat"], base.lat.data),
            "time": (["time"], time),
        },
    )
    ncfile["lat"].attrs  =  base["lat"].attrs
    ncfile["lon"].attrs  =  base["lon"].attrs
    ncfile[var].attrs  =  base[var].attrs
    ncfile.to_netcdf(path+name)

path      =  "/data5/2019swh/data/zhuang_plev/"
path_out  =  "/data5/2019swh/data/zhuang_plev/"
expe  =  ["icid","ic","id","con"]
pentads = np.arange(1,74)
months  = np.arange(1,13)

for name in expe:
    f  =  xr.open_dataset(path+"famil_zhuang_"+name+"_prect.nc")
    avg_pen  =  cal_pentad_average_daily(f["prect"])
    avg_mon  =  cal_monthly_average_daily(f["prect"])

    create_nc(avg_pen,f,pentads,path_out,"single_pentad_"+name+"_prect.nc","prect")
    create_nc(avg_mon, f, months, path_out, "single_monthly_" + name + "_prect.nc", "prect")