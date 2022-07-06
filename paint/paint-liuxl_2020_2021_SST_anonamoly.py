#!/usr/bin/env python
# coding: utf-8

# # 2022/1/24
# # 绘制2020年冬季以及2021年12月份海温距平

# In[5]:


import os
import sys
import xarray as xr
import numpy as np
module_path = ["/home/sun/mycode/module/","/data5/2019swh/mycode/module/"]
sys.path.append(module_path[0])
from module_sun import *
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
from metpy.units import units
from matplotlib.path import Path
import matplotlib.patches as patches


# In[6]:


f0  =  xr.open_dataset("/home/sun/data/sst.mnmean.nc")
# 求取冬季气候态
winter_sst   =  [f0.sst.data[i*12+11:i*12+11+3,:] for i in range(40)]
december_sst =  [f0.sst.data[i*12+11,:] for i in range(40)]
climate_winter_sst    =  np.zeros((180,360))
climate_december_sst  =  np.zeros((180,360))

for i in range(40):
    climate_winter_sst    +=  np.average(winter_sst[i],axis=0)/40
    climate_december_sst  +=  december_sst[i]/40


winter_anomoly    =  np.average(f0.sst[468:471,:],axis=0) - climate_winter_sst
december_anomoly  =  f0.sst[480] - climate_december_sst


# In[7]:



proj    =  ccrs.PlateCarree()
fig1    =  plt.figure(figsize=(12,10))


ax1     = fig1.add_subplot(121,projection=proj)
ax1.coastlines(resolution='110m',lw=1)
# 设置经纬度刻度.
#set_map_ticks(ax1, dx=10, dy=10, nx=1, ny=1, labelsize='small')
#ax.set_extent(extent, crs=proj)
           #
#ax.plot([40,120],[0,0],'k--')
im1  =  ax1.contourf(f0.lon,f0.lat,winter_anomoly,20,cmap='Reds',alpha=1,extend='both')
im1  =  ax1.contourf(f0.lon,f0.lat,winter_anomoly,20,alpha=1,extend='both')

cbar = fig1.colorbar(im1, ax=ax1, shrink=0.9, pad=0.2, orientation='horizontal')

ax2     = fig1.add_subplot(122,projection=proj)
ax2.coastlines(resolution='110m',lw=1)
# 设置经纬度刻度.
#set_map_ticks(ax2, dx=10, dy=10, nx=1, ny=1, labelsize='small')
#ax.set_extent(extent, crs=proj)
           #
#ax.plot([40,120],[0,0],'k--')
im2  =  ax2.contourf(f0.lon,f0.lat,december_anomoly,20,cmap='Reds',alpha=1,extend='both')
im2  =  ax2.contourf(f0.lon,f0.lat,december_anomoly,20,alpha=1,extend='both')

cbar = fig1.colorbar(im2, ax=ax2, shrink=0.9, pad=0.2, orientation='horizontal')


plt.savefig("/home/sun/paint/liuxl/winter_anomoly.pdf",dpi=300)
#plt.tight_layout()


# In[ ]:




