# 2021/11/3
# 计算famil实验中的MSE

import os
import sys
import xarray as xr
import numpy as np
module_path = ["/home/sun/mycode/module/","/data5/2019swh/mycode/module/"]
sys.path.append(module_path[1])
from module_sun import *

def cal_mse(T,q,z):
    #模式数据有虚假数据，这里要进行修正，位势高度小于0处都让其等于0
    T[z<0]  =  0
    q[z<0]  =  0
    z[z<0]  =  0
    cp  =  1.004 #kj/kg*K
    lv  =  2.5e3 #kj/kg
    g   =  9.8 #m/s^2

    mse  =  cp*T+lv*q+9.8*z/1000

    return mse,q

path  =  "/data5/2019swh/data/zhuang_plev/"

#控制实验数据
con_t  =  xr.open_dataset(path+"plev_con_T.nc")
con_q  =  xr.open_dataset(path+"plev_con_Q.nc")
con_h  =  xr.open_dataset(path+"plev_con_Z3.nc")
#noid实验数据
id_t  =  xr.open_dataset(path+"plev_id_T.nc")
id_q  =  xr.open_dataset(path+"plev_id_Q.nc")
id_h  =  xr.open_dataset(path+"plev_id_Z3.nc")

con_mse,testq  =  cal_mse(con_t.T.data,con_q.Q.data/100,con_h.Z3.data)
id_mse,testq2  =  cal_mse(id_t.T.data,id_q.Q.data/100,id_h.Z3.data)

from scipy import integrate
integrate_mse_con   =   np.zeros((con_t.T.data.shape[0],con_t.T.data.shape[2],con_t.T.data.shape[3]))
integrate_mse_id    =   np.zeros((con_t.T.data.shape[0],con_t.T.data.shape[2],con_t.T.data.shape[3]))
for dd in range(0,con_t.T.data.shape[0]):
    for lat in range(0,con_t.T.data.shape[2]):
        for lon in range(0,con_t.T.data.shape[3]):
            integrate_mse_con[dd,lat,lon]  =  -1*integrate.trapz(con_mse[dd,:,lat,lon],con_t.lev.data)/9.8
            integrate_mse_id[dd,lat,lon]   =  -1*integrate.trapz(id_mse[dd,:,lat,lon],con_t.lev.data)/9.8

ncfile  =  xr.Dataset(
    {
        "integrated_mse_con": (["time", "lat", "lon"], integrate_mse_con),
        "integrated_mse_id": (["time", "lat", "lon"], integrate_mse_id),
    },
    coords={
        "lon": (["lon"], con_t.lon.data),
        "lat": (["lat"], con_t.lat.data),
        "time": (["time"], np.linspace(1,365,365)),
    },
)
ncfile["lat"].attrs  =  con_t["lat"].attrs
ncfile["lon"].attrs  =  con_t["lon"].attrs
ncfile["integrated_mse_con"].attrs["units"]  =  "kj/kg"
ncfile["integrated_mse_id"].attrs["units"]  =  "kj/kg"

ncfile.to_netcdf("/data5/2019swh/data/famil_con_noid_mse_integrated.nc")

ncfile  =  xr.Dataset(
    {
        "mse_con": (["time", "lat", "lon"], con_mse),
        "mse_id": (["time", "lat", "lon"], id_mse),
    },
    coords={
        "lon": (["lon"], con_t.lon.data),
        "lat": (["lat"], con_t.lat.data),
        "lev": (["lev"], con_t.lev.data),
        "time": (["time"], np.linspace(1,365,365)),
    },
)
ncfile["lat"].attrs  =  con_t["lat"].attrs
ncfile["lon"].attrs  =  con_t["lon"].attrs
ncfile["lev"].attrs  =  con_t["lev"].attrs
ncfile["mse_con"].attrs["units"]  =  "kj/kg"
ncfile["mse_id"].attrs["units"]   =  "kj/kg"

ncfile.to_netcdf("/data5/2019swh/data/famil_con_noid_mse.nc")