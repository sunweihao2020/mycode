'''
2022/5/13
本代码对于模式输出进行插值
实验为replace_inch
'''
import os
import numpy as np
import numpy.ma as ma
import xarray as xr
import math
import copy
import sys
import Ngl
import netCDF4

def cesm_vin2p(path,file,pnew):
    vars  =  ["KVH","DTV","LHFLX","OMEGA","OMEGAT","PRECT","PS","Q","SHFLX","T","TS","U","V","Z3"]
    files = xr.open_dataset(path+file,engine='netcdf4')
    ds    = xr.Dataset(
        {
            "LHFLX":(["time","lat","lon"],np.float32(files.LHFLX.data)),
            "OMEGA":(["time","lev","lat","lon"],np.float32(Ngl.vinth2p(files.OMEGA.data,files.hyam.data,files.hybm.data,pnew,files.PS.data,1,files.P0.data/100,1,True))),
            "PRECT":(["time","lat","lon"],np.float32(files.PRECT.data)),
            "Q":(["time","lev","lat","lon"],np.float32(Ngl.vinth2p(files.Q.data,files.hyam.data,files.hybm.data,pnew,files.PS.data,1,files.P0.data/100,1,True))),
            "SHFLX":(["time","lat","lon"],np.float32(files.SHFLX.data)),
            "T":(["time","lev","lat","lon"],np.float32(Ngl.vinth2p(files.T.data,files.hyam.data,files.hybm.data,pnew,files.PS.data,1,files.P0.data/100,1,True))),
            "U":(["time","lev","lat","lon"],np.float32(Ngl.vinth2p(files.U.data,files.hyam.data,files.hybm.data,pnew,files.PS.data,1,files.P0.data/100,1,True))),
            "V":(["time","lev","lat","lon"],np.float32(Ngl.vinth2p(files.V.data,files.hyam.data,files.hybm.data,pnew,files.PS.data,1,files.P0.data/100,1,True))),
            "Z3":(["time","lev","lat","lon"],np.float32(Ngl.vinth2p(files.Z3.data,files.hyam.data,files.hybm.data,pnew,files.PS.data,1,files.P0.data/100,1,True))),
            "PS":(["time","lat","lon"],np.float32(files.PS.data)),
            "TS":(["time","lat","lon"],np.float32(files.TS.data)),
        },
        coords={
            "lon":(["lon"],files.lon.data),
            "lat":(["lat"],files.lat.data),
            "time":(["time"],files.time.data),
            "lev":(["lev"],pnew)
        },
    )
    ds.LHFLX.attrs     =      files.LHFLX.attrs
    ds.OMEGA.attrs     =      files.OMEGA.attrs
    ds.PRECT.attrs     =      files.PRECT.attrs
    ds.Q.attrs         =      files.Q.attrs
    ds.SHFLX.attrs     =      files.SHFLX.attrs
    ds.T.attrs         =      files.T.attrs
    ds.U.attrs         =      files.U.attrs
    ds.V.attrs         =      files.V.attrs
    ds.Z3.attrs        =      files.Z3.attrs
    ds.PS.attrs        =      files.PS.attrs
    ds.TS.attrs        =      files.TS.attrs
    ds.lon.attrs       =      files.lon.attrs
    ds.lat.attrs       =      files.lat.attrs
    ds.time.attrs      =      files.time.attrs
    ds.lev.attrs["units"]    =      "hPa"

    return ds


path       =     '/home/sun/model_output/replace_sealand_indian/atm/hist/'
path_out   =     '/home/sun/model_output/replace_sealand_indian_vin2p/vin2p/'
file_list  =     os.listdir(path)
file_list.sort()

pnew     = np.array([1000, 975, 950, 925, 900, 875, 850, 825, 800, 775, 750, 700, 650, 600, 550, 500, 450, 400, 350, 300, 250, 225, 200, 175, 150, 125, 100, 70, 50, 30, 20, 10, 7, 5, 3, 2, 1])
for name in file_list:
    if ".cam.h1." in name:
        out_ds  =  cesm_vin2p(path,name,pnew)
        out_ds.attrs["description"]  =  "after vin2p"
        out_ds.to_netcdf(path_out+name)

        del out_ds
        print("successfully transform "+name)
    else:
        continue
