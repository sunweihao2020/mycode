import os
import sys
import xarray as xr
import numpy as np
module_path = ["/home/sun/mycode/module/","/data5/2019swh/mycode/module/"]
sys.path.append(module_path[0])
from module_sun import *

path   =   "/home/sun/qomo-data/zhuang_plev/pentad_average/"
prect_con     =   xr.open_dataset(path+"plev_pentad_con_prect.nc").prect_pen
prect_id      =   xr.open_dataset(path+"plev_pentad_id_prect.nc").prect_pen

'''设置绘图区域'''
lonmin,lonmax,latmin,latmax  =  30,120,-10,30
extent     =  [lonmin,lonmax,latmin,latmax]
tmin,tmax  =  90,120
level      =  925

props = dict(boxstyle='Round', facecolor='wheat', alpha=1)

proj    =  ccrs.PlateCarree()
fig1    =  plt.figure(figsize=(34,10))
spec1   =  fig1.add_gridspec(nrows=3,ncols=5)

tmin    =  20 ; j = 0

for row in range(0,3):
    for col in range(0,5):
        ax = fig1.add_subplot(spec1[row,col],projection=proj)
        ax.coastlines(resolution='110m',lw=1)
        # 设置经纬度刻度.
        set_map_ticks(ax, dx=10, dy=10, nx=1, ny=1, labelsize='small')
        ax.set_extent(extent, crs=proj)

        im  =  ax.contourf(prect_con.lon,prect_con.lat,prect_con.data[j+20,:],levels=np.linspace(2,20,10),cmap='Blues',alpha=1,extend='both')
        ax.plot([30,120],[0,0],color='k')
        ax.text(0.02,0.85,str(j+20+1),transform=ax.transAxes,bbox=props,fontsize=24)
        j += 1

os.system("mkdir -p /home/sun/paint/famil_exp_pentad_prect_for_check")
plt.savefig('/home/sun/paint/famil_exp_pentad_prect_for_check/con_prect.pdf', bbox_inches='tight')
plt.show()

'''设置绘图区域'''
lonmin,lonmax,latmin,latmax  =  30,120,-10,30
extent     =  [lonmin,lonmax,latmin,latmax]
tmin,tmax  =  90,120
level      =  925

props = dict(boxstyle='Round', facecolor='wheat', alpha=1)

proj    =  ccrs.PlateCarree()
fig1    =  plt.figure(figsize=(34,10))
spec1   =  fig1.add_gridspec(nrows=3,ncols=5)

tmin    =  20 ; j = 0

for row in range(0,3):
    for col in range(0,5):
        ax = fig1.add_subplot(spec1[row,col],projection=proj)
        ax.coastlines(resolution='110m',lw=1)
        # 设置经纬度刻度.
        set_map_ticks(ax, dx=10, dy=10, nx=1, ny=1, labelsize='small')
        ax.set_extent(extent, crs=proj)

        im  =  ax.contourf(prect_con.lon,prect_con.lat,prect_id[j+20,:],levels=np.linspace(2,20,10),cmap='Blues',alpha=1,extend='both')
        ax.plot([30,120],[0,0],color='k')
        ax.text(0.02,0.85,str(j+20+1),transform=ax.transAxes,bbox=props,fontsize=24)
        j += 1

plt.savefig('/home/sun/paint/famil_exp_pentad_prect_for_check/id_prect.pdf', bbox_inches='tight')
plt.show()