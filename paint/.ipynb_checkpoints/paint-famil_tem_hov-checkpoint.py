'''
2021/9/16
本代码计算并绘制上层温度的经向-纬度图，对应数据为庄的三个实验及控制实验
'''
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import metpy.calc as mpcalc
import numpy as np
import xarray as xr
import sys
import pdb

sys.path.append("/data5/2019swh/mycode/module/")
from module_sun import *

time_slice = slice(80,170)
lon_slice = slice(85, 100)
lev_slice = slice(500, 200)
lat_slice = slice(5, 15)

basecon   =  xr.open_dataset("/data5/2019swh/data/plev_con_T.nc").sel(lev=lev_slice,lat=lat_slice,lon=lon_slice,time=time_slice)
#baseicid  =  xr.open_dataset("/data5/2019swh/data/zhuang_plev/plev_icid_T.nc").sel(lev=lev_slice,lat=lat_slice,lon=lon_slice,time=time_slice)
baseicid  =  xr.open_dataset("/data5/2019swh/data/plev_icid_T.nc").sel(lev=lev_slice,lat=lat_slice,lon=lon_slice,time=time_slice)
baseic    =  xr.open_dataset("/data5/2019swh/data/zhuang_plev/plev_ic_T.nc").sel(lev=lev_slice,lat=lat_slice,lon=lon_slice,time=time_slice)
baseid    =  xr.open_dataset("/data5/2019swh/data/zhuang_plev/plev_id_T.nc").sel(lev=lev_slice,lat=lat_slice,lon=lon_slice,time=time_slice)


lat_data  =  np.array([5.15625,6.09375,7.03125,7.96875,8.90625,9.84375,10.78125,11.71875,12.65625,13.59375,14.53125])
def cal_upper_average(array):
    #本代码计算上层的温度
    tem1     = array["T"]
    tem_avg1 = np.average(tem1,axis=1)

    return tem_avg1

avg_con   =  cal_upper_average(basecon)
avg_icid  =  cal_upper_average(baseicid)
avg_ic    =  cal_upper_average(baseic)
avg_id    =  cal_upper_average(baseid)

def cal_gradient(array,lat_data):
    a2  =  np.zeros((91,16))
    for dd in range(0,array.shape[0]):
        for ll in range(0,array.shape[2]):
            a2[dd,ll]  =  np.polyfit(lat_data,array[dd,:,ll],1)[0]

    return a2

gradient_con   =  cal_gradient(avg_con,lat_data)
gradient_icid  =  cal_gradient(avg_icid,lat_data)
gradient_ic    =  cal_gradient(avg_ic,lat_data)
gradient_id    =  cal_gradient(avg_id,lat_data)

#开始绘制
fig = plt.figure(constrained_layout=True,figsize=(20, 16))
spec    = fig.add_gridspec(ncols=2, nrows=2)

#设置坐标
x_tick_labels = []
for xx in range(85, 105, 5):
    x_tick_labels.append(u'' + str(xx) + "\N{DEGREE SIGN}")
y_tick_labels = []
for dddd in range(80, 171, 10):
    y_tick_labels.append(out_date(1981, dddd))


# Bottom plot for Hovmoller diagram
ax3 = fig.add_subplot(spec[0, 0])
# ax2.invert_yaxis()  # Reverse the time order to do oldest first
# Plot of chosen variable averaged over latitude and slightly smoothed
clevs = np.arange(-1, 2, 1)
cf = ax3.contourf(baseid.lon.values,baseid.time.values,gradient_con.data,  clevs, cmap='RdBu')
cs = ax3.contour(baseid.lon.values,baseid.time.values,gradient_con.data,  clevs, colors='k', linewidths=1)
ax3.set_xticks(range(85, 105, 5))
ax3.set_xticklabels(x_tick_labels)
ax3.tick_params(labelsize=16)
ax3.set_yticks(range(80, 171, 10))
ax3.set_yticklabels(y_tick_labels)
ax3.set_title('Control',loc='right',fontsize=20)
cbar = plt.colorbar(cf, orientation='horizontal', fraction=0.046,pad=0.067, aspect=20, extendrect=True)

ax4 = fig.add_subplot(spec[0, 1])
# ax2.invert_yaxis()  # Reverse the time order to do oldest first
# Plot of chosen variable averaged over latitude and slightly smoothed
clevs = np.arange(-1, 2, 1)
cf = ax4.contourf(baseid.lon.values,baseid.time.values,gradient_ic.data,  clevs, cmap='RdBu')
cs = ax4.contour(baseid.lon.values,baseid.time.values,gradient_ic.data,  clevs, colors='k', linewidths=1)
ax4.set_xticks(range(85, 105, 5))
ax4.set_xticklabels(x_tick_labels)
ax4.tick_params(labelsize=16)
ax4.set_yticks(range(80, 171, 10))
ax4.set_yticklabels(y_tick_labels)
ax4.set_title('IC to sea',loc='right',fontsize=20)
cbar = plt.colorbar(cf, orientation='horizontal', fraction=0.046,pad=0.067, aspect=20, extendrect=True)

ax5 = fig.add_subplot(spec[1, 0])
# ax2.invert_yaxis()  # Reverse the time order to do oldest first
# Plot of chosen variable averaged over latitude and slightly smoothed
clevs = np.arange(-1, 2, 1)
cf = ax5.contourf(baseid.lon.values,baseid.time.values,gradient_id.data,  clevs, cmap='RdBu')
cs = ax5.contour(baseid.lon.values,baseid.time.values,gradient_id.data,  clevs, colors='k', linewidths=1)
ax5.set_xticks(range(85, 105, 5))
ax5.set_xticklabels(x_tick_labels)
ax5.tick_params(labelsize=16)
ax5.set_yticks(range(80, 171, 10))
ax5.set_yticklabels(y_tick_labels)
ax5.set_title('India to sea',loc='right',fontsize=20)
cbar = plt.colorbar(cf, orientation='horizontal', fraction=0.046,pad=0.067, aspect=20, extendrect=True)

ax6 = fig.add_subplot(spec[1, 1])
# ax2.invert_yaxis()  # Reverse the time order to do oldest first
# Plot of chosen variable averaged over latitude and slightly smoothed
clevs = np.arange(-1, 2, 1)
cf = ax6.contourf(baseid.lon.values,baseid.time.values,gradient_icid.data,  clevs, cmap='RdBu')
cs = ax6.contour(baseid.lon.values,baseid.time.values,gradient_icid.data,  clevs, colors='k', linewidths=1)
ax6.set_xticks(range(85, 105, 5))
ax6.set_xticklabels(x_tick_labels)
ax6.tick_params(labelsize=16)
ax6.set_yticks(range(80, 171, 10))
ax6.set_yticklabels(y_tick_labels)
ax6.set_title('IC and ID to ocean',loc='right',fontsize=20)
cbar = plt.colorbar(cf, orientation='horizontal', fraction=0.046,pad=0.067, aspect=20, extendrect=True)

plt.savefig('/data5/2019swh/paint/day/'+"famil-tem_gradient.pdf", bbox_inches='tight')
plt.show()
