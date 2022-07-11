'''
2022/5/25
将json格式的bob onset date转化为nc格式
'''
import numpy as np
from netCDF4 import Dataset
import json
import xarray as xr
with open("/home/sun/data/onsetdate.json",'r') as load_f:
    a = json.load(load_f)


years = np.array(list(a.keys()))
days  = np.array(list(a.values()))
years = years.astype(int)
days = days.astype(int)

ncfile  =  xr.Dataset(
    {
        "bob_onset_date": (["year"], days),
    },
    coords={
        "year": (["year"], years),
    },
)
ncfile.attrs["description"]  =  "this file record the BOBSM onset date from 1980-2019"
ncfile.to_netcdf("/home/sun/data/onsetdate.nc")