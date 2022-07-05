import os
import numpy as np
import numpy.ma as ma
from netCDF4 import Dataset
import json
import sys
import time
import math
import xarray as xr
import copy
import pandas as pd
sys.path.append("/home/sun/mycode/module/")
from module_sun import *
from module_writenc import *
import metpy

path = "/home/sun/data1/beifen/data/burst_seris/"
with open("/home/sun/data1/beifen/data/early_date.json", 'r') as load_f1:
    a = json.load(load_f1)
with open("/home/sun/data1/beifen/data/late_date.json", 'r') as load_f2:
    b = json.load(load_f2)

years = np.array(list(a.keys()))
days = np.array(list(a.values()))
early_years = years.astype(np.int32)
early_days = days.astype(np.int32)
early_days -= 1

years = np.array(list(b.keys()))
days  = np.array(list(b.values()))
late_years = years.astype(np.int32)
late_days  = days.astype(np.int32)
late_days -= 1

early = xr.open_dataset("/home/sun/data1/beifen/data/early-year-composite.nc")
late  = xr.open_dataset("/home/sun/data1/beifen/data/late-year-composite.nc")
early_u  =  early["u"].data
late_u   =  late["u"].data
early_v  =  early["v"].data
late_v   =  late["v"].data

diff_u   =  late_u - early_u
diff_v   =  late_v - early_v

lon      =  early.lon.data
lat      =  early.lat.data
level    =  early.level.data

ds = xr.Dataset(
    {"diff_u": (["time","level", "lat", "lon"], diff_u),
    "diff_v": (["time", "level", "lat","lon"], diff_v),
     },
     coords={"lon": (["lon"],lon),"lat": (["lat"], lat),
             "time": pd.date_range(start='1/1/1980', periods=61),
             "level":(["level"],level),
             },
     )

ds.diff_u["units"] = "m s-1"
