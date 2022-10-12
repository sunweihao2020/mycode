'''
2022-4-28
本代码绘制论文version3.0中的fig2d
出版标准
'''
import os
import sys
from matplotlib import rcParams
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

path =   "/home/sun/qomo-data/"
lon_slice  =  slice(45,120)
lat_slice  =  slice(10,15)
lev_slice  =  slice(1000,200)

f1   =   xr.open_dataset(path+"composite_equivalent_tem.nc").sel(lon=lon_slice,lat=lat_slice,level=lev_slice).isel(time=slice(0,30))

theta1      =  f1.theate_e
avg_theta   =  np.average(np.average(theta1,axis=0),axis=1)

f2     =  xr.open_dataset("/home/sun/qomo-data/composite3.nc").sel(lat=slice(10,15),lon=lon_slice,level=lev_slice)
uwind  =  np.average(np.average(f2.uwind[0:30],axis=0),axis=1)
vwind  =  np.average(np.average(f2.vwind[0:30],axis=0),axis=1)
omega  =  np.average(np.average(f2.OMEGA[0:30],axis=0),axis=1)*-60

# 计算纬向偏差值
f3   =   xr.open_dataset(path+"composite_equivalent_tem.nc").sel(lat=lat_slice,level=lev_slice).isel(time=slice(0,30))

theta3      =  f3.theate_e
avg_theta3  =  np.nanmean(np.nanmean(np.nanmean(theta1,axis=0),axis=1),axis=1)

for i in range(0,113):
    avg_theta[:,i]  =  avg_theta[:,i] - avg_theta3

# 计算散度
f4   =   xr.open_dataset(path+"composite-div_vor.nc").sel(lat=slice(10,15),lon=lon_slice,level=lev_slice)
div  =   np.nanmean(np.nanmean(f4.div[0:30],axis=0),axis=1)

# 计算地形
f5   =   xr.open_dataset("/home/sun/data/topography/bathymetric.nc").sel(lat=slice(10,15),lon=lon_slice)
dixing  =  f5.elevation.data
dixing[dixing <= 0]  =  0
topo    =  np.average(dixing,axis=0)

# 创建画布
fig  =  plt.figure(figsize=(13,10))
ax   =  fig.add_subplot()
ax.invert_yaxis()

# 绘制等值线
im1   =  ax.contour(f1.lon,f1.level,avg_theta,np.linspace(-2,4,13),linewidths=2.5,colors='green',zorder=1,alpha=0.9)
rcParams["contour.negative_linestyle"] = 'dashed'
im2   =  ax.contourf(f4.lon,f4.level,div,12,cmap='seismic',extend='both',alpha=0.9,zorder=0)
q  =  ax.quiver(f2.lon[::4], f2.level[::2], uwind[::2,::4], omega[::2,::4], 
                angles='uv',# regrid_shape这个参数越小，是两门就越稀疏
                scale_units='xy', scale=1.1,        # scale是参考矢量，所以取得越大画出来的箭头就越短
                units='xy', width=2.2,
                color='k',zorder=2)

ax.set_xticks(np.linspace(50,110,4))
ax.set_xticklabels(generate_lon_label(50,120,20))
ax.set_yticks(np.linspace(1000,200,5,dtype=int))
ax.set_yticklabels(np.linspace(1000,200,5,dtype=int))
import matplotlib.ticker as mticker
xlocator = mticker.AutoMinorLocator(2)
ylocator = mticker.AutoMinorLocator(2)
ax.xaxis.set_minor_locator(xlocator)
ax.yaxis.set_minor_locator(ylocator)


ax.set_xlim(45,115)

ax.tick_params(axis='both',labelsize=20.5)

a = fig.colorbar(im2,shrink=0.6, pad=0.05,orientation='horizontal')
a.ax.tick_params(labelsize=15)

# 添加地形
ax2  =  ax.twinx()
ax2.set_ylim((0,4.5))
#ax2.set_yticks(np.arange(0,21,1))
ax2.plot(f5.lon.data,topo/1000,color='k')
ax2.fill_between(f5.lon.data,0,topo/1000,where=topo>0,color='k')

ax2.set_yticklabels([])
ax2.set_yticks([])


plt.savefig("/home/sun/paint/lunwen/version5.0/lunwen_v5.0_fig2d_div_theta_vector.pdf",dpi=350)