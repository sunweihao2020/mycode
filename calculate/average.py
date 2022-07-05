#!/usr/bin/env python
# coding: utf-8

# #### 本代码对下载的资料进行求均值处理
# #### 处理资料：/data1/merra/single
# 

# In[19]:


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


# In[20]:


path = "/data1/merra/single/"


# In[21]:


file_list = os.listdir(path)
file_list.sort()
for file in file_list:
    f0 = Nio.open_file(path+file)

    varNames = f0.variables.keys()
    vars = list(varNames)
    time = f0.variables[vars[0]][:]
    lon = f0.variables[vars[1]][:]
    lat = f0.variables[vars[2]][:]
    del vars[0:3]
    for vvvv in vars:
        exec(vvvv+"=f0.variables['"+vvvv+"'][:]")
        exec(vvvv+"1=np.average("+vvvv+",axis=0)")
        
    time = np.array([1])
    fout = create_nc_single('/data1/merra/single_daily/',file[0:37]+'_daily',time,lon,lat)
    add_variables(fout,'PS',PS1,a_ps,0)
    a_qv2m = {'longname': '2-meter_specific_humidity', 'units': 'kg kg-1', 'valid_range': [-1000000000000000.0, 1000000000000000.0]}
    add_variables(fout,'QV2M',QV2M1,a_qv2m,0)
    add_variables(fout,'SLP',SLP1,a_ps,0)
    add_variables(fout,'T2M',T2M1,a_T,0)
    add_variables(fout,'TS',TS1,a_T,0)
    add_variables(fout,'V2M',V2M1,a_vwind,0)
    add_variables(fout,'U2M',U2M1,a_uwind,0)


    fout.close()

