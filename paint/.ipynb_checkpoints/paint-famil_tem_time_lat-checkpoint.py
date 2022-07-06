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

sys.path.append("/data5/2019swh/mycode/module/")
from module_sun import *

baseicid  =  xr.open_dataset("/data5/2019swh/data/zhuang_plev/plev_icid_T.nc")
baseic    =  xr.open_dataset("/data5/2019swh/data/zhuang_plev/plev_ic_T.nc")
baseid    =  xr.open_dataset("/data5/2019swh/data/zhuang_plev/plev_id_T.nc")

def cal_upper_average(array):
    #本代码计算上层的温度
    lon_slice  =  slice(90,100)
    lev_slice  =  slice(500,200)
    lat_slice  =  slice(-42,42)
    tem1     = array["T"].sel(lev=lev_slice,lon=lon_slice,lat=lat_slice)
    tem_avg1 = np.average(tem1,axis=3)
    tem_avg2 = np.average(tem_avg1,axis=1)

    return tem_avg2

avg_icid  =  cal_upper_average(baseicid)
avg_ic    =  cal_upper_average(baseic)
avg_id    =  cal_upper_average(baseid)

temp       =  [avg_icid,avg_ic,avg_id]
#开始绘制
fig     = plt.figure(constrained_layout=True,figsize=(20, 16))
fig, axes = plt.subplots(nrows=3, ncols=1)
#fig     = plt.figure(constrained_layout=True,figsize=(20, 20))
#设置坐标
x_tick_labels = []
for dddd in range(1, 362, 30):
    x_tick_labels.append(out_date(1981, dddd))
y_tick_labels = []
for xxxx in range(-40, 41, 20):
    y_tick_labels.append(u'' + str(xxxx) + "\N{DEGREE SIGN}")

for i,ax in enumerate(axes.flat):
    clevs = np.arange(240, 252, 0.5)
    cf = ax.contourf(baseid.sel(lat=slice(-42,42)).time.data,baseid.sel(lat=slice(-42,42)).lat.data,mpcalc.smooth_n_point(np.swapaxes(temp[i],0,1),9,2), clevs, cmap='coolwarm',extend='both')
    cs = ax.contour(baseid.sel(lat=slice(-42,42)).time.data,baseid.sel(lat=slice(-42,42)).lat.data,mpcalc.smooth_n_point(np.swapaxes(temp[i],0,1),9,2), clevs, colors='k', linewidths=1)
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
fig.savefig('/data5/2019swh/paint/day/'+"famil_temp_time_lat.pdf", bbox_inches='tight')