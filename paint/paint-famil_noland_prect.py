'''
2021/9/12
本代码绘制去除了印度、中南半岛、印度和中南半岛后的实验结果
hovmoller图
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

def paint_hov(data,title,name):
    # Start figure
    fig = plt.figure(figsize=(10, 14))
    # Use gridspec to help size elements of plot; small top plot and big bottom plot
    gs = gridspec.GridSpec(nrows=2, ncols=1, height_ratios=[1, 6], hspace=0.03)

    # Tick labels
    x_tick_labels = []
    for xx in range(30, 150, 10):
        x_tick_labels.append(u'' + str(xx) + "\N{DEGREE SIGN}E")

    y_tick_labels = []
    for dddd in range(100, 201, 4):
        y_tick_labels.append(out_date(1981, dddd))

    # Top plot for geographic reference (makes small map)
    ax1 = fig.add_subplot(gs[0, 0], projection=ccrs.PlateCarree())
    ax1.set_extent([25, 145, 5, 25], ccrs.PlateCarree())
    ax1.set_yticks([10, 20])
    ax1.set_yticklabels([u'10\N{DEGREE SIGN}N', u'20\N{DEGREE SIGN}N'])
    ax1.set_xticks(np.linspace(30, 140, 12))
    ax1.set_xticklabels(x_tick_labels)
    ax1.grid(linestyle='dotted', linewidth=2)

    # Add geopolitical boundaries for map reference
    ax1.add_feature(cfeature.COASTLINE.with_scale('10m'))
    ax1.add_feature(cfeature.LAKES.with_scale('50m'), color='black', linewidths=0.05)
    ax1.add_feature(cfeature.RIVERS)
    ax1.add_feature(cfeature.LAKES)
    ax1.stock_img()

    # Set some titles
    plt.title('Hovmoller Diagram', loc='left')
    plt.title(title, loc='right')

    # Bottom plot for Hovmoller diagram
    ax2 = fig.add_subplot(gs[1, 0])
    # ax2.invert_yaxis()  # Reverse the time order to do oldest first

    # Plot of chosen variable averaged over latitude and slightly smoothed
    clevs = np.arange(0, 32, 4)
    cf = ax2.contourf(data.lon.values, data.time.values, mpcalc.smooth_n_point(
        data, 9, 2), clevs, cmap='Greys', extend='both')
    cs = ax2.contour(data.lon.values, data.time.values, mpcalc.smooth_n_point(
        data, 9, 2), clevs, colors='k', linewidths=1)
    cbar = plt.colorbar(cf, orientation='horizontal', pad=0.09, aspect=50, extendrect=True)
    cbar.set_label('mm $day^{-1}$')

    ax2.set_xticks(np.linspace(30, 140, 12))
    ax2.set_xticklabels(x_tick_labels)
    ax2.tick_params(labelsize=16)
    ax2.set_yticks(np.linspace(100, 200, 26))
    ax2.set_yticklabels(y_tick_labels)
    plt.savefig('/data5/2019swh/paint/day/'+name, bbox_inches='tight')
    plt.show()

paint_hov(avg_prect1,"control","control_prect.pdf")
paint_hov(avg_prect2,"no_ic","noic_prect.pdf")
paint_hov(avg_prect3,"no_id","noid_prect.pdf")
paint_hov(avg_prect4,"no_icid","noicid_prect.pdf")
paint_hov(avg_prect5,"GPCP","GPCP_prect.pdf")