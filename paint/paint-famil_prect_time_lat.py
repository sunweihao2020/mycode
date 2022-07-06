'''
2021/9/14
本代码绘制孟加拉湾地区的降水的“时间-经度”图，来看不同海陆分布配置下，降水集中带的经向移动可能到达的区域
模式为famil
'''
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import metpy.calc as mpcalc
import numpy as np
import xarray as xr
import sys

sys.path.append("/data5/2019swh/mycode/module/")
from module_sun import *

path            =  "/data5/2019swh/data/"
control_prect   =  xr.open_dataset(path+"famil_zhuang_climate_prect.nc")
noic_prect      =  xr.open_dataset(path+"famil_zhuang_ic_prect.nc")
noid_prect      =  xr.open_dataset(path+"famil_zhuang_id_prect.nc")
noicid_prect    =  xr.open_dataset(path+"famil_zhuang_icid_prect.nc")
gpcp_prect      =  xr.open_dataset("/data5/2019swh/data/gpcp_prect_365_climate.nc")

lon_slice   =  slice(90,100)
lat_slice   =  slice(-45,45)

prect1      =  control_prect["prect"].sel(lon = lon_slice,lat = lat_slice)
prect2      =  noic_prect["prect"].sel(lon = lon_slice,lat = lat_slice)
prect3      =  noid_prect["prect"].sel(lon = lon_slice,lat = lat_slice)
prect4      =  noicid_prect["prect"].sel(lon = lon_slice,lat = lat_slice)

avg_pre1    =  np.average(prect1,axis=2)
avg_pre2    =  np.average(prect2,axis=2)
avg_pre3    =  np.average(prect3,axis=2)
avg_pre4    =  np.average(prect4,axis=2)

prect       =  [avg_pre1,avg_pre2,avg_pre3,avg_pre4]
#开始绘制
fig     = plt.figure(constrained_layout=True,figsize=(20, 16))
fig, axes = plt.subplots(nrows=4, ncols=1)
#fig     = plt.figure(constrained_layout=True,figsize=(20, 20))
#设置坐标
x_tick_labels = []
for dddd in range(1, 362, 30):
    x_tick_labels.append(out_date(1981, dddd))
y_tick_labels = []
for xxxx in range(-40, 41, 20):
    y_tick_labels.append(u'' + str(xxxx) + "\N{DEGREE SIGN}")

for i,ax in enumerate(axes.flat):
    clevs = np.arange(0, 32, 4)
    cf = ax.contourf(prect1.time.data,prect1.lat.data,mpcalc.smooth_n_point(np.swapaxes(prect[i],0,1),9,2), clevs, cmap='Blues',extend='both')
    cs = ax.contour(prect1.time.data,prect1.lat.data,mpcalc.smooth_n_point(np.swapaxes(prect[i],0,1),9,2), clevs, colors='k', linewidths=1)
    ax.set_xticks(np.linspace(0, 360, 13))
    ax.set_xticklabels(x_tick_labels)
    ax.tick_params(labelsize=8)
    ax.set_yticks(np.linspace(-40, 40, 5))
    ax.set_yticklabels(y_tick_labels)
    ax.tick_params(pad=0.2)
    #ax.set_title('mm $day^{-1}$', loc='left', fontsize=8);
    #ax.set_title('Control', loc='right', fontsize=8)
    #cbar = plt.colorbar(cf, orientation='horizontal', fraction=0.046, pad=0.067, aspect=20, extendrect=True)

fig.subplots_adjust(bottom=0.2)
cbar_ax = fig.add_axes([0.1, 0.1, 0.8, 0.05])
fig.colorbar(cf, cax=cbar_ax,orientation= 'horizontal')
plt.show()
fig.savefig('/data5/2019swh/paint/day/'+"famil_prect_time_lat.pdf", bbox_inches='tight')
