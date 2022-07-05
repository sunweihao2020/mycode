'''
2021/8/24
写一个插值的module
'''
import os
import numpy as np
from geopy.distance import distance
import numpy.ma as ma
import xarray as xr
import math
import json
import copy
import sys
from netCDF4 import Dataset
import datetime
import Ngl

def cesm_vin2p(path,file,pnew):
    vars  =  ["KVH","DTV","LHFLX","OMEGA","OMEGAT","PRECT","PS","Q","SHFLX","T","TS","U","V","Z3"]
    files = xr.open_dataset(path+file,engine='netcdf4')
    ds    = xr.Dataset(
        {
            "OMEGA":(["time","lev","lat","lon"],Ngl.vinth2p(files.OMEGA.data,files.hyam.data,files.hybm.data,pnew,files.PS.data,1,files.P0.data,1,True),
            "Q":(["time","lev","lat","lon"],Ngl.vinth2p(files.Q.data,files.hyam.data,files.hybm.data,pnew,files.PS.data,1,files.P0.data,1,True),
            "T":(["time","lev","lat","lon"],Ngl.vinth2p(files.KVH.data,files.hyam.data,files.hybm.data,pnew,files.PS.data,1,files.P0.data,1,True),
            "U":(["time","lev","lat","lon"],Ngl.vinth2p(files.KVH.data,files.hyam.data,files.hybm.data,pnew,files.PS.data,1,files.P0.data,1,True),
            "V":(["time","lev","lat","lon"],Ngl.vinth2p(files.KVH.data,files.hyam.data,files.hybm.data,pnew,files.PS.data,1,files.P0.data,1,True),
            "Z3":(["time","lev","lat","lon"],Ngl.vinth2p(files.KVH.data,files.hyam.data,files.hybm.data,pnew,files.PS.data,1,files.P0.data,1,True),
            "PS":(["time","lat","lon"],files.PS.data),
            "TS":(["time","lat","lon"],files.TS.data),
            "LHFLX":(["time","lat","lon"],files.LHFLX.data),
            "PRECT":(["time","lat","lon"],files.PRECT.data,
            "SHFLX":(["time","lat","lon"],files.SHFLX.data),
        },
        coords={
            "lon":(["lon"],files.lon),
            "lat":(["lat"],files.lat),
            "time":(["time"],files.time),
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

    return ds
