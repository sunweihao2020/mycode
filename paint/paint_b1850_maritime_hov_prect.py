'''
2022-8-10
This script paint hov for experiment: b1850 global1m
'''
import sys
import xarray as xr
import numpy as np
module_path = ["/home/sun/mycode/module/","/data5/2019swh/mycode/module/"]
sys.path.append(module_path[0])
from module_sun import *
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.gridspec as gridspec
import matplotlib
matplotlib.use('Agg')

sys.path.append("/home/sun/mycode/paint/")
from paint_lunwen_version3_0_fig2b_2m_tem_wind_20220426 import save_fig


'''设置colormap、levels、坐标值'''
# 坐标轴设置
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
viridis = cm.get_cmap('Blues', 16)
newcolors = viridis(np.linspace(0, 1, 16))
newcmp = ListedColormap(newcolors)
newcmp.set_under('white')
newcmp.set_over('#19345e')
#levels
clevs = np.arange(3,26,2)
# Tick labels
x_tick_labels = []
for xx in range(70,131,20):
    x_tick_labels.append(u''+str(xx)+"\N{DEGREE SIGN}E")
y_tick = [100,110,120,130,140,150,161,171,181,191,201]
y_label = ['10Apr','20Apr','30Apr','10May','20May','30May','10Jun','20Jun','30Jun','10Jul','20Jul']



def lon_avg_prect(time_slice=slice(100,201),lat_slice=slice(10,20),lon_slice=slice(65,130)):
    '''This function deal with precipitation data'''
    # model result
    control_prect   =  xr.open_dataset("/home/sun/data/model_data/climate/b1850_maritime_climate_atmosphere.nc").sel(time=time_slice,lev=925,lat = lat_slice,lon = lon_slice)

    # calculate weight average
    avg_control_prect  =  (control_prect["PRECT"]*(np.cos(np.deg2rad(control_prect.lat.values)))[None, :, None]).sum(dim='lat')/np.sum(np.cos(np.deg2rad(control_prect.lat.values)))*86400*1000

    #avg_control_prect  =  (control_prect["U"]*(np.cos(np.deg2rad(control_prect.lat.values)))[None, :, None]).sum(dim='lat')/np.sum(np.cos(np.deg2rad(control_prect.lat.values)))
    return avg_control_prect

def paint_trmm_hov(control,path_out,filename,time_slice=slice(100,201),lat_slice=slice(10,20),lon_slice=slice(65,130)):
    '''This function paint control prect with map'''
    f0  =  xr.open_dataset("/home/sun/data/model_data/climate/b1850_maritime_climate_atmosphere.nc").sel(time=time_slice,lat = lat_slice,lon = lon_slice)
    # Start figure
    fig = plt.figure(figsize=(13, 15))
    gs = gridspec.GridSpec(nrows=2, ncols=1, height_ratios=[2, 6], hspace=0.03)


    # Top plot for geographic reference (makes small map)
    ax1 = fig.add_subplot(gs[0, 0], projection=ccrs.PlateCarree())
    ax1.set_extent([65, 130, 10, 20], ccrs.PlateCarree())
    # 设置y轴刻度
    ax1.set_yticks([10, 20])
    ax1.set_yticklabels([u'10\N{DEGREE SIGN}N', u'20\N{DEGREE SIGN}N'],fontsize=25)
    # 设置x轴刻度
    ax1.set_xticks(np.arange(70,131,20))
    ax1.set_xticklabels(x_tick_labels,fontsize=25)
    ax1.grid(linestyle='dotted', linewidth=2)

    ax1.add_feature(cfeature.COASTLINE.with_scale('10m'))
    ax1.add_feature(cfeature.LAKES.with_scale('50m'), color='black', linewidths=0.05)
    ax1.add_feature(cfeature.RIVERS)
    ax1.add_feature(cfeature.LAKES)
    ax1.stock_img()

    ax2 = fig.add_subplot(gs[1, 0])

    cf   = ax2.contourf(f0.lon.values, f0.time.values, control.data,clevs, cmap=newcmp, extend='both')
    cs   = ax2.contour(f0.lon.values,  f0.time.values, control.data,clevs, colors='k', linewidths=1)


    # 坐标设置
    ax2.set_xticks(np.arange(70,131,20))
    ax2.set_xticklabels(x_tick_labels,fontsize=25)

    ax2.set_yticks(y_tick)
    ax2.set_yticklabels(y_label,fontsize=25)

    save_fig(path_out=path_out,file_out=filename)


def main():
    control = lon_avg_prect()
    paint_trmm_hov(control,path_out="/home/sun/paint/b1850_exp/",filename="maritime_hov_prect.pdf")


if __name__ == "__main__":
    main()
