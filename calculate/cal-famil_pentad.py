'''
2021/9/22
本代码计算pentad平均的数据
针对famil的四个海陆分布实验
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
vars  =  ["OMEGA","Q","T","U","V","Z3"]
expe  =  ["icid","ic","id","con"]
pentads = np.arange(1,74)
for var in vars:
    for name in expe:
        f  =  xr.open_dataset(path+"plev_"+name+"_"+var+".nc")
        avg_mon  =  cal_pentad_average_daily(f[var])

        create_nc(avg_mon,f,pentads,path_out,"plev_pentad_"+name+"_"+var+".nc",var)

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
