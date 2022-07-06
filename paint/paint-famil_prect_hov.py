'''
2021/9/14
这里主要绘制famil实验输出的降水数据，实验为no_land
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

time_slice  =  slice(100,200)
lat_slice   =  slice(10,20)
lon_slice   =  slice(30,140)

prect1      =  control_prect["prect"].sel(time=time_slice,
                                       lat = lat_slice,
                                      lon = lon_slice)
prect2      =  noic_prect["prect"].sel(time=time_slice,
                                       lat = lat_slice,
                                       lon = lon_slice)
prect3      =  noid_prect["prect"].sel(time=time_slice,
                                       lat = lat_slice,
                                       lon = lon_slice)
prect4      =  noicid_prect["prect"].sel(time=time_slice,
                                       lat = lat_slice,
                                       lon = lon_slice)
prect5      =  gpcp_prect["prect"].sel(time=time_slice,
                                       lat = lat_slice,
                                       lon = lon_slice)

np.set_printoptions(suppress=True)
#Compute weights and take weighted average over latitude dimension
def cal_weights_avg(prect):
    weight  =  np.cos(np.deg2rad(prect.lat.values))
    return (prect*weight[None, :, None]).sum(dim='lat')/np.sum(weight)

avg_prect1  =  cal_weights_avg(prect1)
avg_prect2  =  cal_weights_avg(prect2)
avg_prect3  =  cal_weights_avg(prect3)
avg_prect4  =  cal_weights_avg(prect4)
avg_prect5  =  cal_weights_avg(prect5)

#开始绘制
fig = plt.figure(constrained_layout=True,figsize=(20, 16))
widths  = [1, 1]
heights = [1, 3, 3]
spec    = fig.add_gridspec(ncols=2, nrows=3, width_ratios=widths,height_ratios=heights)

#设置坐标
x_tick_labels = []
for xx in range(30, 150, 10):
    x_tick_labels.append(u'' + str(xx) + "\N{DEGREE SIGN}")
y_tick_labels = []
for dddd in range(100, 201, 10):
    y_tick_labels.append(out_date(1981, dddd))

ax1 = fig.add_subplot(spec[0, 0], projection=ccrs.PlateCarree())
ax1.set_extent([25, 145, 5, 25], ccrs.PlateCarree())
ax1.set_yticks([10, 20])
ax1.set_yticklabels([u'10\N{DEGREE SIGN}N', u'20\N{DEGREE SIGN}N'])
ax1.set_xticks(np.linspace(30, 140, 12))
ax1.set_xticklabels(x_tick_labels,fontsize=13)
ax1.grid(linestyle='dotted', linewidth=1)

ax1.add_feature(cfeature.COASTLINE.with_scale('10m'))
ax1.add_feature(cfeature.LAKES.with_scale('50m'), color='black', linewidths=0.05)
ax1.add_feature(cfeature.RIVERS)
ax1.add_feature(cfeature.LAKES)
ax1.stock_img()


ax2 = fig.add_subplot(spec[0, 1], projection=ccrs.PlateCarree())
ax2.set_extent([25, 145, 5, 25], ccrs.PlateCarree())
ax2.set_yticks([10, 20])
ax2.set_yticklabels([u'10\N{DEGREE SIGN}N', u'20\N{DEGREE SIGN}N'])
ax2.set_xticks(np.linspace(30, 140, 12))
ax2.set_xticklabels(x_tick_labels,fontsize=13)
ax2.grid(linestyle='dotted', linewidth=1)

ax2.add_feature(cfeature.COASTLINE.with_scale('10m'))
ax2.add_feature(cfeature.LAKES.with_scale('50m'), color='black', linewidths=0.05)
ax2.add_feature(cfeature.RIVERS)
ax2.add_feature(cfeature.LAKES)
ax2.stock_img()

# Bottom plot for Hovmoller diagram
ax3 = fig.add_subplot(spec[1, 0])
# ax2.invert_yaxis()  # Reverse the time order to do oldest first
# Plot of chosen variable averaged over latitude and slightly smoothed
clevs = np.arange(0, 32, 4)
cf = ax3.contourf(avg_prect1.lon.values,avg_prect1.time.values,avg_prect1.data,  clevs, cmap='Greys', extend='both')
cs = ax3.contour(avg_prect1.lon.values, avg_prect1.time.values, avg_prect1.data,  clevs, colors='k', linewidths=1)
#cbar = plt.colorbar(cf, orientation='horizontal', pad=0.09, aspect=50, extendrect=True)
ax3.set_xticks(np.linspace(30, 140, 12))
ax3.set_xticklabels(x_tick_labels)
ax3.tick_params(labelsize=16)
ax3.set_yticks(np.linspace(100, 200, 11))
ax3.set_yticklabels(y_tick_labels)
ax3.set_title('mm $day^{-1}$',loc='left',fontsize=20);ax3.set_title('Control',loc='right',fontsize=20)
cbar = plt.colorbar(cf, orientation='horizontal', fraction=0.046,pad=0.067, aspect=20, extendrect=True)

# Bottom plot for Hovmoller diagram
ax4 = fig.add_subplot(spec[1, 1])
# ax2.invert_yaxis()  # Reverse the time order to do oldest first
# Plot of chosen variable averaged over latitude and slightly smoothed
clevs = np.arange(0, 32, 4)
cf = ax4.contourf(avg_prect2.lon.values,avg_prect2.time.values, mpcalc.smooth_n_point(
    avg_prect2.data, 9, 2), clevs, cmap='Greys', extend='both')
cs = ax4.contour(avg_prect2.lon.values, avg_prect2.time.values, mpcalc.smooth_n_point(
    avg_prect2.data, 9, 2), clevs, colors='k', linewidths=1)
#cbar = plt.colorbar(cf, orientation='horizontal', pad=0.09, aspect=50, extendrect=True)
ax4.set_xticks(np.linspace(30, 140, 12))
ax4.set_xticklabels(x_tick_labels)
ax4.tick_params(labelsize=16)
ax4.set_yticks(np.linspace(100, 200, 11))
ax4.set_yticklabels(y_tick_labels)
ax4.set_title('mm $day^{-1}$',loc='left',fontsize=20);ax4.set_title('change ICP to sea',loc='right',fontsize=20)
cbar = plt.colorbar(cf, orientation='horizontal', fraction=0.046,pad=0.067, aspect=20, extendrect=True)

# Bottom plot for Hovmoller diagram
ax5 = fig.add_subplot(spec[2, 0])
# ax2.invert_yaxis()  # Reverse the time order to do oldest first
# Plot of chosen variable averaged over latitude and slightly smoothed
clevs = np.arange(0, 32, 4)
cf = ax5.contourf(avg_prect1.lon.values,avg_prect1.time.values, mpcalc.smooth_n_point(
    avg_prect3.data, 9, 2), clevs, cmap='Greys', extend='both')
cs = ax5.contour(avg_prect1.lon.values, avg_prect1.time.values, mpcalc.smooth_n_point(
    avg_prect3.data, 9, 2), clevs, colors='k', linewidths=1)
#cbar = plt.colorbar(cf, orientation='horizontal', pad=0.09, aspect=50, extendrect=True)
ax5.set_xticks(np.linspace(30, 140, 12))
ax5.set_xticklabels(x_tick_labels)
ax5.tick_params(labelsize=16)
ax5.set_yticks(np.linspace(100, 200, 11))
ax5.set_yticklabels(y_tick_labels)
ax5.set_title('mm $day^{-1}$',loc='left',fontsize=20);ax5.set_title('change ID to sea',loc='right',fontsize=20)
cbar = plt.colorbar(cf, orientation='horizontal', fraction=0.046,pad=0.067, aspect=20, extendrect=True)

# Bottom plot for Hovmoller diagram
ax6 = fig.add_subplot(spec[2, 1])
# ax2.invert_yaxis()  # Reverse the time order to do oldest first
# Plot of chosen variable averaged over latitude and slightly smoothed
clevs = np.arange(0, 32, 4)
cf = ax6.contourf(avg_prect1.lon.values,avg_prect1.time.values, mpcalc.smooth_n_point(
    avg_prect4.data, 9, 2), clevs, cmap='Greys', extend='both')
cs = ax6.contour(avg_prect1.lon.values, avg_prect1.time.values, mpcalc.smooth_n_point(
    avg_prect4.data, 9, 2), clevs, colors='k', linewidths=1)
#cbar = plt.colorbar(cf, orientation='horizontal', pad=0.09, aspect=50, extendrect=True)
ax6.set_xticks(np.linspace(30, 140, 12))
ax6.set_xticklabels(x_tick_labels)
ax6.tick_params(labelsize=16)
ax6.set_yticks(np.linspace(100, 200, 11))
ax6.set_yticklabels(y_tick_labels)
ax6.set_title('mm $day^{-1}$',loc='left',fontsize=20);ax6.set_title('change ICP&ID to sea',loc='right',fontsize=20)
cbar = plt.colorbar(cf, orientation='horizontal', fraction=0.046,pad=0.067, aspect=20, extendrect=True)

plt.savefig('/data5/2019swh/paint/day/'+"control_prect.pdf", bbox_inches='tight')
plt.show()


