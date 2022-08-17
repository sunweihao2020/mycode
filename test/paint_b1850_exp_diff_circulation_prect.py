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
import matplotlib.pyplot as plt


def set_cartopy_tick(ax, extent, xticks, yticks, nx=0, ny=0,
    xformatter=None, yformatter=None,labelsize=20):
    import matplotlib.ticker as mticker
    from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
    # 本函数设置地图上的刻度 + 地图的范围
    proj = ccrs.PlateCarree()
    ax.set_xticks(xticks, crs=proj)
    ax.set_yticks(yticks, crs=proj)
    # 设置次刻度.
    xlocator = mticker.AutoMinorLocator(nx + 1)
    ylocator = mticker.AutoMinorLocator(ny + 1)
    ax.xaxis.set_minor_locator(xlocator)
    ax.yaxis.set_minor_locator(ylocator)

    # 设置Formatter.
    if xformatter is None:
        xformatter = LongitudeFormatter()
    if yformatter is None:
        yformatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(xformatter)
    ax.yaxis.set_major_formatter(yformatter)

    # 设置axi label_size，这里默认为两个轴
    ax.tick_params(axis='both',labelsize=labelsize)

    # 在最后调用set_extent,防止刻度拓宽显示范围.
    if extent is None:
        ax.set_global()
    else:
        ax.set_extent(extent, crs=proj)

def add_vector_legend(ax,q,location=(0.825, 0),length=0.175,wide=0.2,fc='white',ec='k',lw=0.5,order=1,quiver_x=0.915,quiver_y=0.125,speed=5,fontsize=18):
    '''
    句柄 矢量 位置 图例框长宽 表面颜色 边框颜色  参考箭头的位置 参考箭头大小 参考label字体大小
    '''
    import matplotlib as mpl
    rect = mpl.patches.Rectangle((location[0], location[1]), length, wide, transform=ax.transAxes,    # 这个能辟出来一块区域，第一个参数是最左下角点的坐标，后面是矩形的长和宽
                            fc=fc, ec=ec, lw=lw, zorder=order
                            )
    ax.add_patch(rect)

    ax.quiverkey(q, X=quiver_x, Y=quiver_y, U=speed,
                    label=f'{speed} m/s', labelpos='S', labelsep=0.1,fontproperties={'size':fontsize})


def add_text(ax, string, props=dict(boxstyle='square', edgecolor='white', facecolor='white', alpha=1),
             location=(0.05, 0.9), fontsize=15):
    ax.text(location[0], location[1], string, transform=ax.transAxes, bbox=props, fontsize=fontsize)

    
def paint_pentad_circulation():
    '''This function paint pentad circulation based on b1850 experiment'''
    #  ----- import  ----------
    from matplotlib import cm
    from matplotlib.colors import ListedColormap



    import matplotlib
    matplotlib.use('Agg')
    ## ------------------------

    path_out   =  "/Users/sunweihao/ubuntu-server-data/model_data/climate/"
    file_out1  =  "b1850_control_atmospheric_monthly_average.nc"
    file_out2  =  "b1850_maritime_atmospheric_monthly_average.nc"
    f0        =  xr.open_dataset(path_out+file_out1)
    f1        =  xr.open_dataset(path_out+file_out2)
    ## -------------------------------------------------


    # ------  time period  -----------
    pentads   =  [5,6,7,8]
    date      =  [6,7,8,9]

    # -------  color bar   -----------
    viridis = cm.get_cmap('coolwarm', 16)
    newcolors = viridis(np.linspace(0, 1, 16))
    newcmp = ListedColormap(newcolors)
    #newcmp.set_under('white')
    #newcmp.set_over('#004080')

    # -------   cartopy extent  -----
    lonmin,lonmax,latmin,latmax  =  30,150,-10,70
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
            set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(30,150,7,dtype=int),yticks=np.linspace(-10,70,9,dtype=int),nx=1,ny=1,labelsize=25)

            # 添加赤道线
            ax.plot([40,120],[0,0],'k--')

            im  =  ax.contourf(f0.lon,f0.lat,(f0["PRECT"].data[pentads[j]]*86400000 - f1["PRECT"].data[pentads[j]]*86400000)/(f0["PRECT"].data[pentads[j]]*86400000)*100,np.linspace(-100,100,21),cmap=newcmp,alpha=1,extend='both')

            # 海岸线
            ax.coastlines(resolution='50m',lw=2)

            print((f0["U"].data[pentads[j]]-f1["U"].data[pentads[j]]).shape)
            q  =  ax.quiver(f0.lon.data, f0.lat.data, (f0["U"].data[pentads[j],3]-f1["U"].data[pentads[j],3]), (f0["V"].data[pentads[j],3]-f1["V"].data[pentads[j],3]), 
                regrid_shape=20, angles='uv',       # regrid_shape这个参数越小，是两门就越稀疏
                scale_units='xy', scale=0.3,        # scale是参考矢量，所以取得越大画出来的箭头就越短
                units='xy', width=0.35,
                transform=proj,
                color='k',linewidth=1.2,headlength = 5, headaxislength = 4, headwidth = 5,alpha=1)

            # 加日期
            add_text(ax=ax,string="month"+str(date[j]),location=(0.80,0.91),fontsize=25)

            # 加矢量图图例
            add_vector_legend(ax=ax,q=q)
        
            j += 1
    
    # 加colorbar
    fig1.subplots_adjust(top=0.8) 
    cbar_ax = fig1.add_axes([0.2, 0.05, 0.6, 0.03]) 
    cb  =  fig1.colorbar(im, cax=cbar_ax, shrink=0.1, pad=0.01, orientation='horizontal')
    cb.ax.tick_params(labelsize=20)

    plt.savefig("test1.pdf",dpi=300)



def main():
    paint_pentad_circulation()
    


if __name__  ==  "__main__":
    main()