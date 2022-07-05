#!/usr/bin/env python
# coding: utf-8

# #### 2021/4/3
# #### 本代码使用已经求过日平均的资料
# #### 资料路径：/data1/merra/single_daily

# In[1]:


import os
import numpy as np
import numpy.ma as ma
import Ngl, Nio
from netCDF4 import Dataset
import json
import sys
import math
sys.path.append("/mycode/module/")
from module_sun import *
from module_writenc import *
from attribute import *


# In[19]:


with open("/data/onsetdate.json",'r') as load_f:
    a = json.load(load_f)
years = np.array(list(a.keys()))
days  = np.array(list(a.values()))
years = years.astype(int)
days = days.astype(int)
days -= 1

path = "/data1/merra/single_daily/"
ps0 = ma.zeros((35,181,360))
file_list = os.listdir(path)

vars = ['PS','QV2M','SLP','T2M','TS','V2M','U2M']
cmd0 = 'var0 = ma.zeros((35,181,360))'
for vvvv in vars:
    exec(cmd0.replace('var',vvvv))


# In[22]:


for yyyy in range(0,40):
    file_list2 = []
    for ffff in file_list:
        if ffff[27:31] == str(years[yyyy]):
            file_list2.append(ffff)
            file_list2.sort()
        else:
            continue
    location = days[yyyy]
    j = 0
    for dddd in range(location-30,location+5):
        ff = Nio.open_file(path+file_list2[dddd])
        cmd0 = 'vvv = ff.variables["vvv"][:]'
        cmd1 = 'vvv0[j,:,:] += vvv[0,:,:]/40'
        for vvvv in vars:
            exec(cmd0.replace('vvv',vvvv))
            exec(cmd1.replace('vvv',vvvv))
        j += 1


# In[21]:


time = np.arange(0,35)
lon = ff.variables["lon"][:]
lat = ff.variables["lat"][:]
fout = create_nc_single('/data/','composite-merra2-single',time,lon,lat)
add_variables(fout,'PS',PS0,a_ps,0)
a_qv2m = {'longname': '2-meter_specific_humidity', 'units': 'kg kg-1', 'valid_range': [-1000000000000000.0, 1000000000000000.0]}
add_variables(fout,'QV2M',QV2M0,a_qv2m,0)
add_variables(fout,'SLP',SLP0,a_ps,0)
add_variables(fout,'T2M',T2M0,a_T,0)
add_variables(fout,'TS',TS0,a_T,0)
add_variables(fout,'V2M',V2M0,a_vwind,0)
add_variables(fout,'U2M',U2M0,a_uwind,0)
fout.close()


# In[ ]:




