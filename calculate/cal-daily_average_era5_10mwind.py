'''
2021/10/12
本代码计算下载的era5的10m风的气候态侯平均
'''
import numpy as np
import xarray as xr

f0  =  xr.open_dataset("/home/sun/data/out/1993_10m_u_component_of_wind.nc")
u_climate_average  =  np.zeros((73,f0.u10.data.shape[1],f0.u10.data.shape[2]))
v_climate_average  =  u_climate_average.copy()
path = "/home/sun/data/out/"
vars  =  ["u","v"]

start =  1980 ; end  =  2004

for yyyy in range(start,end):
    f1  =  xr.open_dataset(path+str(yyyy)+"_10m_u_component_of_wind.nc")
    f2  =  xr.open_dataset(path+str(yyyy)+"_10m_v_component_of_wind.nc")

    u1  =  f1.u10.data[:,::-1,:]
    v1  =  f2.v10.data[:,::-1,:]

    u1_pen  =  np.zeros((73,f0.u10.data.shape[1],f0.u10.data.shape[2]))
    v1_pen  =  np.zeros((73,f0.u10.data.shape[1],f0.u10.data.shape[2]))

    for i in range(0,73):
        u1_pen[i, :] =  np.average(u1[i * 5:i * 5 + 5, :], axis=0)
        v1_pen[i, :] =  np.average(v1[i * 5:i * 5 + 5, :], axis=0)

    u_climate_average += u1_pen / (end - start)
    v_climate_average += v1_pen / (end - start)

time  =  np.linspace(1,73,73)

ncfile1  =  xr.Dataset(
    {
        "u10": (["time","lat", "lon"], u_climate_average),
    },
    coords={
        "lon": (["lon"], f0.longitude.data),
        "lat": (["lat"], f0.latitude.data[::-1]),
        "time": (["time"], time),
    },
)
ncfile1["lat"].attrs  =  f0["latitude"].attrs
ncfile1["lon"].attrs  =  f0["longitude"].attrs
ncfile1["u10"].attrs  =  f0["u10"].attrs
ncfile1.to_netcdf("/home/sun/data/pentad_average/era5_u10_pentad_climate.nc")

f0  =  xr.open_dataset("/home/sun/data/out/1993_10m_v_component_of_wind.nc")
ncfile2  =  xr.Dataset(
    {
        "v10": (["time","lat", "lon"], v_climate_average),
    },
    coords={
        "lon": (["lon"], f0.longitude.data),
        "lat": (["lat"], f0.latitude.data[::-1]),
        "time": (["time"], time),
    },
)
ncfile2["lat"].attrs  =  f0["latitude"].attrs
ncfile2["lon"].attrs  =  f0["longitude"].attrs
ncfile2["v10"].attrs  =  f0["v10"].attrs
ncfile2.to_netcdf("/home/sun/data/pentad_average/era5_v10_pentad_climate.nc")
