'''
2022-7-23
This script paint b1850 control experiment circulation and precipitation
The daily resolution is pentad.Thus, in this script I need to calculate pentad average
'''
import os
import sys
import xarray as xr
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
from metpy.units import units
from matplotlib.path import Path
import matplotlib.patches as patches


    
def paint_pentad_circulation():
    '''This function paint pentad circulation based on b1850 experiment'''
    #  ----- import  ----------
    from matplotlib import cm
    from matplotlib.colors import ListedColormap

    import sys
    sys.path.append("/home/sun/mycode/paint/")
    from paint_lunwen_version3_0_fig2b_2m_tem_wind_20220426 import set_cartopy_tick,save_fig
    from paint_lunwen_version3_0_fig2a_tem_gradient_20220426 import add_text

    import matplotlib
    matplotlib.use('Agg')
    ## ------------------------

    path_out  =  "/home/sun/data/model_data/climate/"
    file_out  =  "b1850_maritime_atmospheric_monthly_average.nc"
    f0        =  xr.open_dataset(path_out+file_out)
    ## -------------------------------------------------


    # ------  time period  -----------
    pentads   =  [0,3,6,9]
    date      =  [1,4,7,10]

    # -------  color bar   -----------
    viridis = cm.get_cmap('Blues', 16)
    newcolors = viridis(np.linspace(0, 1, 16))
    newcmp = ListedColormap(newcolors)
    newcmp.set_under('white')
    newcmp.set_over('#004080')

    # -------   cartopy extent  -----
    lonmin,lonmax,latmin,latmax  =  45,150,-10,50
    extent     =  [lonmin,lonmax,latmin,latmax]

    # -------     figure    -----------
    proj  =  ccrs.PlateCarree()
    fig1    =  plt.figure(figsize=(32,24))
    spec1   =  fig1.add_gridspec(nrows=2,ncols=2)

    j  =  0

    # ------       paint    ------------
    for col in range(2):
        for row in range(2):
            ax = fig1.add_subplot(spec1[row,col],projection=proj)

            # 设置刻度
            set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(50,150,6,dtype=int),yticks=np.linspace(-10,50,7,dtype=int),nx=1,ny=1,labelsize=25)

            # 添加赤道线
            ax.plot([40,120],[0,0],'k--')

            im  =  ax.contourf(f0.lon,f0.lat,f0["PRECT"].data[pentads[j]]*86400*1000,np.linspace(3,24,8),cmap=newcmp,alpha=1,extend='both')

            # 海岸线
            ax.coastlines(resolution='50m',lw=2)


            ax.streamplot(f0.lon, f0.lat, f0.sel(lev=925)["U"].data[pentads[j]], f0.sel(lev=925)["V"].data[pentads[j]], color='k',linewidth=2.5,density=1.2,arrowsize=2.75, arrowstyle='->')

            # 加日期
            add_text(ax=ax,string="month"+str(date[j]),location=(0.80,0.91),fontsize=25)
        
            j += 1
    
    # 加colorbar
    fig1.subplots_adjust(top=0.8) 
    cbar_ax = fig1.add_axes([0.2, 0.05, 0.6, 0.03]) 
    cb  =  fig1.colorbar(im, cax=cbar_ax, shrink=0.1, pad=0.01, orientation='horizontal')
    cb.ax.tick_params(labelsize=20)

    save_fig(path_out="/home/sun/paint/b1850_exp/",file_out="b1850_mari_monthly_925_circulation_with_prect.pdf")



def main():
    paint_pentad_circulation()
    





if __name__  ==  "__main__":
    main()