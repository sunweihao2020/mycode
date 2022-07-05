'''
2021/9/12
本代码对庄默然的模式输出数据进行处理
原实验是1983-2004，因此从1985开始往后取
更改海陆分布实验
'''
import os
import xarray as xr
import numpy as np

path_con     =    '/data5/dam/zhmr/data/FAMIL_ICIDMC/CTRL_4/daily/vars_daily/'
path_icid    =    '/data5/dam/zhmr/data/FAMIL_ICIDMC/ICIDnoLD/daily/vars_daily/'
path_ic      =    '/data5/dam/zhmr/data/FAMIL_ICIDMC/InChnoLD/daily/vars_daily/'
path_id      =    '/data5/dam/zhmr/data/FAMIL_ICIDMC/InDnoLD/daily/vars_daily/'
file0        =    os.listdir(path_con)
file1        =    os.listdir(path_icid)
file2        =    os.listdir(path_ic)
file3        =    os.listdir(path_id)
con_prect    =    [x for x in file0 if ("PRECT-" in x)] ; con_prect.sort()
icid_prect   =    [x for x in file1 if ("PRECT-" in x)] ; icid_prect.sort()
ic_prect     =    [x for x in file2 if ("PRECT-" in x)] ; ic_prect.sort()
id_prect     =    [x for x in file3 if ("PRECT-" in x)] ; id_prect.sort() ; id_prect.pop()

#以1985作为base array,这里注：有的是从1984开始的，有的是从1985，这里就不挑了，除的时候要注意
base_con     =     xr.open_dataset(path_con+con_prect[0])
base_icid    =     xr.open_dataset(path_icid+icid_prect[0])
base_ic      =     xr.open_dataset(path_ic+ic_prect[0])
base_id      =     xr.open_dataset(path_id+id_prect[0])

def cal_prect(base,path,list):
    for yyyy in range(1,len(list)):
        array  =  xr.open_dataset(path+list[yyyy])
        base   += array["PRECT"].data

    return base*86400000/len(list)

def create_nc(out,base,time,path,name):
    ncfile  =  xr.Dataset(
        {
            "prect": (["time", "lat", "lon"], out),
        },
        coords={
            "lon": (["lon"], base.lon.data),
            "lat": (["lat"], base.lat.data),
            "time": (["time"], time),
        },
    )

    ncfile.prect.attrs  =  base.PRECT.attrs
    ncfile.prect.attrs["units"] = "mm/day"
    ncfile["lat"].attrs  =  base["lat"].attrs
    ncfile["lon"].attrs  =  base["lon"].attrs
    ncfile.to_netcdf(path+name)

average_icid   =    cal_prect(base_icid.PRECT.data,path_icid,icid_prect)
average_ic     =    cal_prect(base_ic.PRECT.data,path_ic,ic_prect)
average_id     =    cal_prect(base_id.PRECT.data,path_id,id_prect)

time       =  np.arange(0,365,1)
create_nc(average_icid,base_icid,time,"/data5/2019swh/data/","famil_zhuang_icid_prect.nc")
create_nc(average_ic,base_ic,time,"/data5/2019swh/data/","famil_zhuang_ic_prect.nc")
create_nc(average_id,base_id,time,"/data5/2019swh/data/","famil_zhuang_id_prect.nc")