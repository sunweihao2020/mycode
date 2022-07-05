#!/usr/bin/env python
# coding: utf-8

# # 2022/4/21
# # 本代码计算CESM输出文件的climate
# # 实验是replace_indian



import os
import sys
import xarray as xr
import numpy as np
module_path = ["/home/sun/mycode/module/","/data5/2019swh/mycode/module/"]
sys.path.append(module_path[0])
from module_sun import *
import time




start = time.time()
path_in  =  "/home/sun/f2000_replace_inch_220519_vin2p/vin2p/"
path_out =  "/home/sun/f2000_replace_inch_220519_vin2p/average/"

year_range  =  np.array([3,22],dtype=int)

f0  =  xr.open_dataset(path_in+'f2000_replace_inch_220519.cam.h1.0022-12-06-00000.nc')
vars  =  ["LHFLX","OMEGA","PRECT","Q","SHFLX","T","U","V","Z3","PS","TS"]

# 定义原始的climate变量

#三维
lhflx     =  np.zeros((365,192,288),dtype=np.float32)
prect     =  lhflx.copy()
shflx     =  lhflx.copy()
ps        =  lhflx.copy()
ts        =  lhflx.copy()

#四维
omega     =  np.zeros((365,37,192,288),dtype=np.float32)
q         =  omega.copy()
t         =  omega.copy()
u         =  omega.copy()
v         =  omega.copy()
z3        =  omega.copy()




for yyyy in range(year_range[0],year_range[1]+1):
    # 先获取这一年的文件列表
    list0  =  []
    for f1 in os.listdir(path_in):
        if yyyy < 10:
            if ".h1.000"+str(yyyy) in f1:
                list0.append(f1)
        else:
            if ".h1.00"+str(yyyy) in f1:
                list0.append(f1)
    list0.sort()
    print("it is in "+str(yyyy))
    
    j = 0 # j 0->365 account
    for f2 in list0:
        f3  =  xr.open_dataset(path_in+f2)
        lhflx[j,:]  +=  f3.LHFLX.data[0,:]/(year_range[1]-year_range[0]+1)
        prect[j,:]  +=  f3.PRECT.data[0,:]/(year_range[1]-year_range[0]+1)
        shflx[j,:]  +=  f3.SHFLX.data[0,:]/(year_range[1]-year_range[0]+1)
        ps[j,:]     +=  f3.PS.data[0,:]/(year_range[1]-year_range[0]+1)
        ts[j,:]     +=  f3.TS.data[0,:]/(year_range[1]-year_range[0]+1)

        omega[j,:]  +=  f3.OMEGA.data[0,:]/(year_range[1]-year_range[0]+1)
        q[j,:]      +=  f3.Q.data[0,:]/(year_range[1]-year_range[0]+1)
        t[j,:]      +=  f3.T.data[0,:]/(year_range[1]-year_range[0]+1)
        u[j,:]      +=  f3.U.data[0,:]/(year_range[1]-year_range[0]+1)
        v[j,:]      +=  f3.V.data[0,:]/(year_range[1]-year_range[0]+1)
        z3[j,:]      +=  f3.Z3.data[0,:]/(year_range[1]-year_range[0]+1)

        j +=1

    end = time.time()
    print("Finish "+str(yyyy)+" running time: %s second"%(end-start))


# 生成文件
pnew     = np.array([1000, 975, 950, 925, 900, 875, 850, 825, 800, 775, 750, 700, 650, 600, 550, 500, 450, 400, 350, 300, 250, 225, 200, 175, 150, 125, 100, 70, 50, 30, 20, 10, 7, 5, 3, 2, 1])
ds    = xr.Dataset(
    {
        "LHFLX":(["time","lat","lon"],np.float32(lhflx)),
        "OMEGA":(["time","lev","lat","lon"],np.float32(omega)),
        "PRECT":(["time","lat","lon"],np.float32(prect)),
        "Q":(["time","lev","lat","lon"],np.float32(q)),
        "SHFLX":(["time","lat","lon"],np.float32(shflx)),
        "T":(["time","lev","lat","lon"],np.float32(t)),
        "U":(["time","lev","lat","lon"],np.float32(u)),
        "V":(["time","lev","lat","lon"],np.float32(v)),
        "Z3":(["time","lev","lat","lon"],np.float32(z3)),
        "PS":(["time","lat","lon"],np.float32(ps)),
        "TS":(["time","lat","lon"],np.float32(ts)),
    },
    coords={
        "lon":(["lon"],f0.lon.data),
        "lat":(["lat"],f0.lat.data),
        "time":(["time"],np.linspace(1,365,365)),
        "lev":(["lev"],pnew)
    },
)
ds.LHFLX.attrs     =      f0.LHFLX.attrs
ds.OMEGA.attrs     =      f0.OMEGA.attrs
ds.PRECT.attrs     =      f0.PRECT.attrs
ds.Q.attrs         =      f0.Q.attrs
ds.SHFLX.attrs     =      f0.SHFLX.attrs
ds.T.attrs         =      f0.T.attrs
ds.U.attrs         =      f0.U.attrs
ds.V.attrs         =      f0.V.attrs
ds.Z3.attrs        =      f0.Z3.attrs
ds.PS.attrs        =      f0.PS.attrs
ds.TS.attrs        =      f0.TS.attrs
ds.lon.attrs       =      f0.lon.attrs
ds.lat.attrs       =      f0.lat.attrs
ds.time.attrs      =      f0.time.attrs
ds.lev.attrs["units"]    =      "hPa"




ds.to_netcdf(path_out+"f2000_replace_inch_climate.nc")

