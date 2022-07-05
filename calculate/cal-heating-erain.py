#!/usr/bin/env python
# coding: utf-8

# ### 2021/3/31
# ### 本代码使用ERAIN的资料来计算视热源

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
#from attribute import *


# In[2]:


f = Nio.open_file("/data/composite-erain.nc")


# In[8]:


lev = f.variables["level"][:]
time = f.variables["time"][:]
t = f.variables["t"][:]
theta = copy.deepcopy(t)


# #### 计算位温

# In[9]:


for i in range(0,len(lev)):
    theta[:,i,:,:] = t[:,i,:,:]*math.pow((1000/lev[i]),0.286)


# ### 获取x，y方向distance

# In[32]:


lat = f.variables["lat"][:]
lon = f.variables["lon"][:]
disy,disx,location = cal_xydistance(lat,lon)
ptheta_px = ma.zeros(theta.shape)
ptheta_py = np.gradient(theta,location,axis = 2)
for tttt in range(0,61):
    for llll in range(0,37):
        for yyyy in range(1,len(lat)-1):
            ptheta_px[tttt,llll,yyyy,:] = np.gradient(theta[tttt,llll,yyyy,:],disx[yyyy])
u = f.variables["u"][:]
v = f.variables["v"][:]

h_advective = u*ptheta_px+v*ptheta_py

p = lev*100
w = f.variables["w"][:]
ptheta_pp = np.gradient(theta,p,axis=1)
w_advective = w*ptheta_pp

advection = (h_advective+w_advective)*60*60*24

time = f.variables["time"][:]
ptheta_pt = np.gradient(theta,axis=0)

dtheta_dt = ptheta_pt+advection


# In[ ]:


q1_cp = ma.zeros(dtheta_dt.shape)
for i in range(0,len(lev)):
    q1_cp[:,i,:,:] = dtheta_dt[:,i,:,:]*math.pow((lev[i]/1000),0.286)


# In[ ]:


a_q = {'longname': 'Q1_heating','units': 'K s-1','valid_range': [-1000000000000000.0, 1000000000000000.0]}
time = np.arange(0,61)
fout = create_nc_multiple('/data/','composite-Q1-erain',time,lev,lon,lat)
add_variables(fout,'Q1',q1_cp,a_q,1)
fout.close()

