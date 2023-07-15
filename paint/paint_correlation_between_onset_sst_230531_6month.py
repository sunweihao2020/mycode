'''
2023-3-6
This script paint the correlation between monsoon onset dates and the other indexes

Reference:

'''
from matplotlib import projections
import xarray as xr
import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import sys
import cartopy

sys.path.append("/home/sun/mycode/module/")
from module_sun import *

sys.path.append("/home/sun/mycode/paint/")
from paint_lunwen_version3_0_fig2b_2m_tem_wind_20220426 import set_cartopy_tick,save_fig
from paint_lunwen_version3_0_fig2a_tem_gradient_20220426 import add_text

def calculate_threshold_correlation(n=63):
    '''This function calculate the threshold for the given sample number
    list is here: https://wenku.baidu.com/view/fdfece05a6c30c2259019eed.html?_wkts_=1678086714615
    '''
    return 0.20912, 0.24803, 0.32227 # 0.1, 0.05, 0.01

corr_file = xr.open_dataset('/home/sun/data/ERA5_data_monsoon_onset/index/correlation/many_index_corr_with_onset_dates.nc')

def paint_12month_correlation(correlation, extent, lon, lat, title):
    '''This function plot the correlation among the 12 months'''
    from cartopy.util import add_cyclic_point
    # Figure Setting
    proj    =  ccrs.PlateCarree(central_longitude=180)
    fig1    =  plt.figure(figsize=(17.5,12))
    spec1   =  fig1.add_gridspec(nrows=3,ncols=2)

    # colorbar使用ncl的
    cmap  =  create_ncl_colormap("/home/sun/data/color_rgb/MPL_coolwarm.txt",22)

    j = 0
    for col in range(2):
        for row in range(3):
            ax = fig1.add_subplot(spec1[row,col],projection=proj)

            # Set the tick and tick-label
            set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(30,330,6,dtype=int),yticks=np.linspace(60,-60,7,dtype=int),nx=1,ny=1,labelsize=17)

            # contourf
            #im = ax.contourf(lon, lat, correlation[j], [0, 0.24, 1], hatches=[None, '.'])
            #print(np.nanmax(correlation[j]))
            data = correlation[j]
            data, lons = add_cyclic_point(correlation[j], coord=lon)
            im = ax.contourf(lons, lat, data, np.linspace(-0.8, 0.8, 9), cmap=cmap, transform = ccrs.PlateCarree(), extend='both')
            #im = ax.contourf(lon, lat, data, np.linspace(-0.8, 0.8, 9), cmap=cmap,)
            im2 = ax.contourf(lons, lat, data, [-1, -0.248, 0, 0.248, 1], hatches=['.', None, None, '.'], colors="none", transform=ccrs.PlateCarree())
            ax.coastlines()
            

            ax.plot([0,360],[0,0],'k--',transform = ccrs.PlateCarree())
           # ax.plot([30,330],[10,10],'r--',transform = ccrs.PlateCarree())

            ax.set_title('Month '+str(j+1), loc='left', fontsize=22.5)
            ax.set_title(title, loc='right', fontsize=22.5)


            j+=1

    # 加colorbar
    fig1.subplots_adjust(top=0.8) 
    cbar_ax = fig1.add_axes([0.2, 0.05, 0.6, 0.03]) 
    cb  =  fig1.colorbar(im, cax=cbar_ax, shrink=0.1, pad=0.01, orientation='horizontal')
    cb.ax.tick_params(labelsize=25)

    save_fig(path_out="/home/sun/paint/index_correlation_with_onsetdate/",file_out=title+"6month.pdf")

def main():
    lonmin,lonmax,latmin,latmax  =  30,360,60,-60
    extent     =  [lonmin,lonmax,latmin,latmax]
    paint_12month_correlation(corr_file['onset_with_sst'], extent, corr_file['lon'], corr_file['lat'], "SST (95%)")

if __name__ == '__main__':
    main()