'''
2021/8/31
本代码挑出早年晚年的海温分别与同期气候态求差值
'''
import xarray as xr
import numpy as np
import os
import json

#读取并拆分海温文件
path  =  "/data5/2019swh/mydown/HadlSST/"
file  =  xr.open_dataset(path+"HadISST_sst.nc")
start_time = '1980-01-01'
end_time   = '2019-12-31'
time_slice = slice(start_time, end_time)
sst   =  file["sst"].sel(time=time_slice)

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

test   =   sst.data[5,:,:]
#计算逐月的气候态海温
climate_sst  =  np.zeros((12,180,360))
early_sst    =  np.zeros((12,180,360))
late_sst     =  np.zeros((12,180,360))

start  =  1980
end    =  2020
i  =  0 ; j  =  0 ; n = 0
for yyyy in range(start,end):
    if yyyy in early_year:
        i += 1
    if yyyy in late_year:
        j += 1
    for mmmm in range(0,12):
        climate_sst[mmmm,:,:]    +=  sst.data[(12*(yyyy-1980)+mmmm),:,:]
        if yyyy in early_year:
            early_sst[mmmm,:,:]  +=  sst.data[(12*(yyyy-1980)+mmmm),:,:]
        if yyyy in late_year:
            late_sst[mmmm,:,:]   +=  sst.data[(12*(yyyy-1980)+mmmm),:,:]
        n += 1

climate_sst /=  (end-start)
early_sst   /=  i
late_sst    /=  j

climate_sst[climate_sst<0] =   np.nan
early_sst[early_sst<0]     =   np.nan
late_sst[late_sst<0]       =   np.nan

time  =  np.arange(0,12,1)
climate_sst_file  =  xr.Dataset(
    {
        "sst":(["time","lat","lon"],climate_sst),
    },
    coords={
        "lon":(["lon"],sst.longitude.data),
        "lat":(["lat"],sst.latitude.data),
        "time":(["time"],time),
    },
)
early_sst_file  =  xr.Dataset(
    {
        "sst":(["time","lat","lon"],early_sst),
    },
    coords={
        "lon":(["lon"],sst.longitude.data),
        "lat":(["lat"],sst.latitude.data),
        "time":(["time"],time),
    },
)
late_sst_file  =  xr.Dataset(
    {
        "sst":(["time","lat","lon"],late_sst),
    },
    coords={
        "lon":(["lon"],sst.longitude.data),
        "lat":(["lat"],sst.latitude.data),
        "time":(["time"],time),
    },
)

climate_sst_file.sst.attrs  =   sst.attrs
early_sst_file.sst.attrs    =   sst.attrs
late_sst_file.sst.attrs     =   sst.attrs
climate_sst_file.lon.attrs  =   sst.longitude.attrs
early_sst_file.lon.attrs    =   sst.longitude.attrs
late_sst_file.lon.attrs     =   sst.longitude.attrs
climate_sst_file.lat.attrs  =   sst.latitude.attrs
early_sst_file.lat.attrs    =   sst.latitude.attrs
late_sst_file.lat.attrs     =   sst.latitude.attrs

climate_sst_file.to_netcdf("/data5/2019swh/sst_climate_hadley.nc")
early_sst_file.to_netcdf("/data5/2019swh/sst_early_composite_hadley.nc")
late_sst_file.to_netcdf("/data5/2019swh/sst_late_composite_hadley.nc")