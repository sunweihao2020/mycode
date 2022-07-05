'''
2021/8/17
本代码根据年份对早年晚年的海温分别进行合成分析
注意海温的年份：1982-2016
'''
import os
import numpy as np
import numpy.ma as ma
import Ngl, Nio
from netCDF4 import Dataset
import json
import sys
import time
sys.path.append("/data5/2019swh/mycode/module/")
from module_sun import *
from module_writenc import *
#from attribute import *

with open("/data5/2019swh/data/early_date.json",'r') as load_f:
    early = json.load(load_f)

with open("/data5/2019swh/data/late_date.json",'r') as load_f:
    late = json.load(load_f)

f         =  Nio.open_file('/data5/2019swh/data/burst_seris/composite_sst.nc')
sst       =  f.variables["sea_surface_temperature"][:]
lon       =  f.variables["lon"][:]
lat       =  f.variables["lat"][:]

early_sst =  ma.array(ma.zeros(sst[0,:,:,:].shape),mask=sst[0,:,:,:].mask)
late_sst  =  ma.array(ma.zeros(sst[0,:,:,:].shape),mask=sst[0,:,:,:].mask)
#先计算早年的
years     =  np.array(list(early.keys()))
days      =  np.array(list(early.values()))
years     =  years.astype(np.int)
days      =  days.astype(np.int)

for yyyy in years[:-1]:
    early_sst +=  sst[yyyy-1982,:,:,:]/(len(years)-1)

years  =  np.array(list(late.keys()))
days   =  np.array(list(late.values()))
years  =  years.astype(np.int)
days   =  days.astype(np.int)

for yyyy in years[1:]:
    late_sst +=  sst[yyyy-1982,:,:,:]/(len(years)-1)

time = np.arange(0,40)
fout = create_nc_single('/data5/2019swh/data/','ear_late_oisst',time,lon,lat)
a_t={'longname': 'sst','units': 'degC','valid_range': [-1000000000000000.0, 1000000000000000.0]}
add_variables(fout,'early_sst',early_sst,a_t,0)
add_variables(fout,'late_sst',late_sst,a_t,0)
fout.close()
