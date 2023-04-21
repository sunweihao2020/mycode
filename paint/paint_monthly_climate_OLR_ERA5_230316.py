'''
This script plot the monthly OLR data over the maritime continent based on ERA5 data
'''
import xarray as xr
import numpy as np
import os
import sys

sys.path.append("/home/sun/mycode/module/")
from module_sun import *

sys.path.append("/home/sun/mycode/paint/")
from paint_lunwen_version3_0_fig2b_2m_tem_wind_20220426 import set_cartopy_tick,save_fig

lon_slice  =  slice(70, 170)
lat_slice  =  slice(30, -30)

path0 = '/home/sun/data/ERA5_data_monsoon_onset/climatic_daily_ERA5/single/'

file  = xr.open_dataset(path0 + 'OLR_climatic_daily.nc').sel(lat=lat_slice, lon=lon_slice)

# Here I plot the 2, 3, 4, 5 month
feb_day = 31 ; mar_day = 60 ; apr_day = 91 ; may_day = 120 ; jun_day = 150

def plot_monthly_olr(data, extent, figname):
    import cartopy.crs as ccrs
    import matplotlib.pyplot as plt

    feb = np.average(data[feb_day : mar_day], axis=0)
    mar = np.average(data[mar_day : apr_day], axis=0)
    apr = np.average(data[apr_day : may_day], axis=0)
    may = np.average(data[may_day : jun_day], axis=0)

    month_avg = [feb, mar, apr, may]
    month_name = ['Feb', 'Mar', 'Apr', 'May']

    # Setting Figure
    proj    =  ccrs.PlateCarree()
    fig1    =  plt.figure(figsize=(26,17))
    spec1   =  fig1.add_gridspec(nrows=2,ncols=2)

    # colorbar使用ncl的
    cmap  =  create_ncl_colormap("/home/sun/data/color_rgb/MPL_coolwarm.txt",32)

    j = 0
    for col in range(2):
        for row in range(2):
            ax = fig1.add_subplot(spec1[row,col],projection=proj)

            # 设置刻度
            set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(70, 170, 6,dtype=int),yticks=np.linspace(30, -30, 5,dtype=int),nx=1,ny=1,labelsize=20)

            # Equator line
            ax.plot([70,170],[0,0],'k--')

            # contour line
            im1  =  ax.contour(file['lon'].data, file['lat'].data, month_avg[j] / -3600, levels=np.arange(170, 300, 5), colors='black', linewidths=1.5, alpha=1, zorder=1)
            im2  =  ax.contourf(file['lon'].data, file['lat'].data, month_avg[j] / -3600, levels=np.arange(170, 300, 5), cmap=cmap, extend='both', zorder=0)

            ax.coastlines(resolution='110m',lw=1)

            # add month name
            ax.set_title(month_name[j], loc='left', fontsize=25)

            j += 1

    # 加colorbar
    fig1.subplots_adjust(top=0.8) 
    cbar_ax = fig1.add_axes([0.2, 0.05, 0.6, 0.03]) 
    cb  =  fig1.colorbar(im2, cax=cbar_ax, shrink=0.1, pad=0.01, orientation='horizontal')
    cb.ax.tick_params(labelsize=25)

    # 保存图片
    #plt.tight_layout()
    save_fig(path_out="/home/sun/paint/monthly_variable/",file_out=figname)

def main():
    lonmin,lonmax,latmin,latmax  =  70, 170, -30, 30
    extent     =  [lonmin,lonmax,latmin,latmax]

    plot_monthly_olr(data=file['ttr_40to80'], extent=extent, figname='ERA5_climate_OLR_maritime_continent.pdf')

if __name__ == '__main__':
    main()

