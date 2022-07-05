'''
2021/9/8
本代码挑出早年晚年，然后计算逐月平均的气候态来对比同期的越赤道气流情况
'''
import xarray as xr
import numpy as np
import json
import os

#读取时间
with open("/data5/2019swh/data/onsetdate.json",'r') as load_f:
    a = json.load(load_f)
year   =    np.array(list(a.keys()))
day    =    np.array(list(a.values()))
years  =    year.astype(int)
day    =    day.astype(int)

#读取早年晚年
with open("/data5/2019swh/data/early_date.json",'r') as load_f:
    early = json.load(load_f)
early_year  =  np.array(list(early.keys())).astype(int)
early_day   =  np.array(list(early.values())).astype(int)
with open("/data5/2019swh/data/late_date.json",'r') as load_f:
    late = json.load(load_f)
late_year  =  np.array(list(late.keys())).astype(int)
late_day   =  np.array(list(late.values())).astype(int)

path    =    "/data1/MERRA2/monthly/instM_3d_asm_Np/"
f1      =    xr.open_dataset(path+"MERRA2_400.instM_3d_asm_Np.201211.nc4")

#三月份的base数组
v3_late        =    f1.U.data[0,:,:].copy()
v3_late[:,:]   =    0
v3_early       =    f1.U.data[0,:,:].copy()
v3_early[:,:]  =    0
u3_late        =    f1.U.data[0,:,:].copy()
u3_late[:,:]   =    0
u3_early       =    f1.U.data[0,:,:].copy()
u3_early[:,:]  =    0

#四月份的base数组
v4_late        =    f1.U.data[0,:,:].copy()
v4_late[:,:]   =    0
v4_early       =    f1.U.data[0,:,:].copy()
v4_early[:,:]  =    0
u4_late        =    f1.U.data[0,:,:].copy()
u4_late[:,:]   =    0
u4_early       =    f1.U.data[0,:,:].copy()
u4_early[:,:]  =    0

len_early      =    len(early)  ;  len_late  =  len(late)
file_list      =    os.listdir("/data1/MERRA2/monthly/instM_3d_asm_Np")  ;  file_list.sort()
for i in range(0,12):
    if i < 8:
        y1  =  early_year[i]
        y2  =  late_year[i]
        ff3_early =  xr.open_dataset(path + file_list[((y1 - 1980) * 12 + 2)])
        ff3_late  =  xr.open_dataset(path + file_list[((y2 - 1980) * 12 + 2)])
        ff4_early =  xr.open_dataset(path + file_list[((y1 - 1980) * 12 + 3)])
        ff4_late  =  xr.open_dataset(path + file_list[((y2 - 1980) * 12 + 3)])

        v3_early  += ff3_early.V.data[0,:,:]
        v3_late   += ff3_late.V.data[0,:,:]
        v4_early  += ff4_early.V.data[0,:,:]
        v4_late   += ff4_late.V.data[0, :, :]
        u3_early  += ff3_early.U.data[0, :, :]
        u3_late   += ff3_late.U.data[0, :, :]
        u4_early  += ff4_early.U.data[0, :, :]
        u4_late   += ff4_late.U.data[0, :, :]
    else:
        y2 = late_year[i]
        ff3_late = xr.open_dataset(path + file_list[((y2 - 1980) * 12 + 2)])
        ff4_late = xr.open_dataset(path + file_list[((y2 - 1980) * 12 + 3)])
        v3_late  += ff3_late.V.data[0, :, :]
        v4_late  += ff4_late.V.data[0, :, :]
        u3_late  += ff3_late.U.data[0, :, :]
        u4_late  += ff4_late.U.data[0, :, :]

v3_late  /= len(late)  ; v4_late  /= len(late) ; u3_late /= len(late) ; u4_late /= len(late)
v3_early /= len(early) ; v4_early /= len(early) ; u3_early /= len(early) ; u4_early /= len(early)

pathout  =  "/data5/2019swh/data/"
wind_file  =   xr.Dataset(
    {
        "v3ewind":(["lev","lat","lon"],v3_early),
        "v3lwind":(["lev","lat","lon"],v3_late),
        "v4ewind":(["lev","lat","lon"],v4_early),
        "v4lwind":(["lev","lat","lon"],v4_late),
        "u3ewind":(["lev","lat","lon"],u3_early),
        "u4ewind":(["lev","lat","lon"],u4_early),
        "u3lwind":(["lev","lat","lon"],u3_late),
        "u4lwind":(["lev","lat","lon"],u4_late),

    },
    coords={
        "lon":(["lon"],f1.lon.data),
        "lat":(["lat"],f1.lat.data),
        "lev":(["lev"],f1.lev.data)
    },
)

varlist1 = ["v3ewind","v3lwind","v4ewind","v4lwind"]
varlist2 = ["u3ewind","u3lwind","u4ewind","u4lwind"]
for vvvv in varlist1:
    wind_file[vvvv].attrs  =  f1.V.attrs
for vvvv in varlist2:
    wind_file[vvvv].attrs  =  f1.U.attrs
wind_file["lon"].attrs   =  f1.lon.attrs
wind_file["lat"].attrs   =  f1.lat.attrs
wind_file["lev"].attrs   =  f1.lev.attrs

wind_file.attrs["time"]  =  "2021-9-8"
wind_file.attrs["description"] = "create early and late year's v-wind ,3 indicate march and 4 indicate april"

wind_file.to_netcdf(pathout+"same_period_wind_earlylate.nc")