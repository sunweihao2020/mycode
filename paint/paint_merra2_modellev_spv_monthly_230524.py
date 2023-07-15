'''
2023-5-24
This script plot climatological monthly mean of the spv
'''
from matplotlib import projections
import xarray as xr
import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import sys

sys.path.append("/home/sun/mycode/module/")
from module_sun import *

sys.path.append("/home/sun/mycode/paint/")
from paint_lunwen_version3_0_fig2b_2m_tem_wind_20220426 import set_cartopy_tick,save_fig
from paint_lunwen_version3_0_fig2a_tem_gradient_20220426 import add_text

f0 = xr.open_dataset('/home/sun/wd_disk/merra2_modellev/spv/cdo/spv_monthly_1980_2019_multi_year_monthly.nc').sel(lev=72)

def paint_pic(extent,lon,lat,spv,date,number):
    # 设置画布
    proj    =  ccrs.PlateCarree()
    fig1    =  plt.figure(figsize=(26,13.5))
    spec1   =  fig1.add_gridspec(nrows=2,ncols=3)


    # colorbar使用ncl的
    cmap  =  create_ncl_colormap("/home/sun/data/color_rgb/MPL_coolwarm.txt",32)

    j  =  0
    for row in range(2):
        for col in range(3):
            # Data calculation
            lat_avg = np.average(spv[j], axis=1)
            lat_avg_2 = lat_avg.reshape((181, 1))

            ax = fig1.add_subplot(spec1[row,col],projection=proj)

            # 设置刻度
            set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(50,110,4,dtype=int),yticks=np.linspace(-10,30,5,dtype=int),nx=1,ny=1,labelsize=25)

            # 赤道线
            ax.plot([40,120],[0,0],'k--')

            # 等值线
            im1  =  ax.contour(lon,lat,spv[j], levels=np.linspace(-0.02, 0.02, 21),colors='k',linestyles='solid',linewidths=2,alpha=1,zorder=1)
            im2  =  ax.contourf(lon,lat,spv[j],levels=np.linspace(-0.02, 0.02, 21),cmap=cmap,extend='both',zorder=0)

            #im1  =  ax.contour(lon,lat,spv[j] - lat_avg_2,levels=np.linspace(-0.02, 0.02, 21),colors='k',linestyles='solid',linewidths=2,alpha=1,zorder=1)
            #im2  =  ax.contourf(lon,lat,spv[j] - lat_avg_2,levels=np.linspace(-0.02, 0.02, 21),cmap=cmap,extend='both',zorder=0)

            # 海岸线
            ax.coastlines(resolution='110m',lw=1)

            

            # 加日期
            ax.set_title(date[j], loc='right', fontsize=22.5)
            
            # 加图序号
            ax.set_title(number[j], loc='left', fontsize=22.5)
        
            j += 1

    # 加colorbar
    fig1.subplots_adjust(top=0.8) 
    cbar_ax = fig1.add_axes([0.2, 0.05, 0.6, 0.03]) 
    cb  =  fig1.colorbar(im2, cax=cbar_ax, shrink=0.1, pad=0.01, orientation='horizontal')
    cb.ax.tick_params(labelsize=25)

    # 保存图片
    #plt.tight_layout()
    save_fig(path_out="/home/sun/paint/monthly_variable/spv/",file_out="merra2_modellev_spv_monthly_1_6.pdf")


def main():
    lonmin,lonmax,latmin,latmax  =  45,115,-10,30
    extent     =  [lonmin,lonmax,latmin,latmax]

    # month name
    date   =  ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]

    # 图片序号
    number =  ["(a)","(b)","(c)","(d)","(e)","(f)"]


    #  下面开始绘图
    paint_pic(extent=extent,lat=f0.lat,lon=f0.lon,spv=f0['__xarray_dataarray_variable__'].data,date=date,number=number)

if __name__ == "__main__":
    main()