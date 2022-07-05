'''
2021/9/12
本代码对庄默然的模式输出数据进行处理
原实验是1983-2004，因此从1985开始往后取
更改海陆分布实验
_1是只计算了降水，在这里计算multiple的U和V
计算时间段为1985-2003
'''
import os
import xarray as xr
import numpy as np
import math

path_con     =    '/data5/dam/zhmr/data/FAMIL_ICIDMC/CTRL_4/daily/atm-daily-plev/'
path_icid    =    '/data5/dam/zhmr/data/FAMIL_ICIDMC/ICIDnoLD/daily/atm-daily-plev/'
path_ic      =    '/data5/dam/zhmr/data/FAMIL_ICIDMC/InChnoLD/daily/atm-daily-plev/'
path_id      =    '/data5/dam/zhmr/data/FAMIL_ICIDMC/InDnoLD/daily/atm-daily-plev/'
varsname     =    ["T","OMEGA","Q","U","V","Z3"]
paths        =    [path_con,path_icid,path_ic,path_id]
#paths        =    [path_con]

def get_flist(path,var):
    list1  =  [x for x in os.listdir(path) if (var+"-" in x)]
    list1.sort()
    return list1

#base_1      =     xr.open_dataset(path_icid+get_flist(path_icid,"V")[0])
#base_2      =     xr.open_dataset(path_ic+get_flist(path_ic,"V")[0])
#base_3      =     xr.open_dataset(path_id+get_flist(path_id,"V")[0])

#base_icid   =     np.zeros((365,base_1.V.data.shape[1],base_1.V.data.shape[2],base_1.V.data.shape[3]))
#base_ic     =     base_icid.copy()
#base_id     =     base_icid.copy()

#因为里面的文件都是按月存放的，所以需要先拼接一下
def joint_month(path,var,year,base):
    #获取yyyy年vvvv变量的文件列表
    list2    =    [x for x in os.listdir(path) if (var+"-" in x and str(year) in x)] ; list2.sort()
    base2    =    np.zeros((365,base[var].data.shape[1],base[var].data.shape[2],base[var].data.shape[3]))
    start    =    0
    if len(list2) == 12:
        for ffff in list2:
            f0    =  xr.open_dataset(path+ffff)
            end   =  f0[var].data.shape[0]
            base2[start:(start+end),:,:,:]  =  f0[var].data
            start+=end
        return base2
    else:
        return 0

def create_nc(out,base,time,path,name,var):
    ncfile  =  xr.Dataset(
        {
            var: (["time", "lev","lat", "lon"], out),
        },
        coords={
            "lon": (["lon"], base.lon.data),
            "lat": (["lat"], base.lat.data),
            "time": (["time"], time),
            "lev":(["lev"],base.lev_p.data)
        },
    )
    ncfile["lev"].attrs  =  base["lev_p"].attrs
    ncfile["lat"].attrs  =  base["lat"].attrs
    ncfile["lon"].attrs  =  base["lon"].attrs
    ncfile[var].attrs  =  base[var].attrs
    ncfile.to_netcdf(path+name)


time       =  np.arange(0,365,1)
for var in varsname:
    base_0 = xr.open_dataset(path_con + get_flist(path_con, var)[0])
    base_1 = xr.open_dataset(path_icid + get_flist(path_icid, var)[0])
    base_2 = xr.open_dataset(path_ic + get_flist(path_ic, var)[0])
    base_3 = xr.open_dataset(path_id + get_flist(path_id, var)[0])
    base_con  = np.zeros((365, base_0[var].data.shape[1], base_0[var].data.shape[2], base_0[var].data.shape[3]))
    base_icid = np.zeros((365, base_0[var].data.shape[1], base_0[var].data.shape[2], base_0[var].data.shape[3]))
    base_ic   = np.zeros((365, base_0[var].data.shape[1], base_0[var].data.shape[2], base_0[var].data.shape[3]))
    base_id   = np.zeros((365, base_0[var].data.shape[1], base_0[var].data.shape[2], base_0[var].data.shape[3]))
    bases = {paths[0]: base_con,paths[1]:base_icid,paths[2]:base_ic,paths[3]:base_id}
    for pathname in paths:
        for jjjj in range(0,math.floor(len(get_flist(pathname,var))/12)):
            array  =  joint_month(pathname,var,jjjj+1985,base_0)
            bases[pathname]  += (array/math.floor(len(get_flist(pathname,var))/12))
    create_nc(base_icid, base_1, time, "/data5/2019swh/data/zhuang_plev/", "plev_icid_"+var+".nc",var)
    create_nc(base_ic  , base_2, time, "/data5/2019swh/data/zhuang_plev/", "plev_ic_" + var + ".nc", var)
    create_nc(base_id  , base_3, time, "/data5/2019swh/data/zhuang_plev/", "plev_id_" + var + ".nc", var)
    create_nc(base_con , base_0, time, "/data5/2019swh/data/zhuang_plev/", "plev_con_" + var + ".nc", var)