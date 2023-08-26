'''
2023-8-6
This script plot the regression wind field on pentad
This script is for check, I want to paint pentad original wind field to see whether the raw data is error
'''
import xarray as xr
import numpy as np
import os
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import sys
import matplotlib as mpl

sys.path.append("/home/sun/mycode/module/")
from module_sun import *

sys.path.append("/home/sun/mycode/paint/")
from paint_lunwen_version3_0_fig2b_2m_tem_wind_20220426 import set_cartopy_tick,save_fig
from paint_lunwen_version3_0_fig2a_tem_gradient_20220426 import add_text

def add_vector_legend(ax,q,location=(0.825, 0),length=0.175,wide=0.2,fc='white',ec='k',lw=0.5,order=1,quiver_x=0.915,quiver_y=0.125,speed=10,fontsize=18):
    '''
    句柄 矢量 位置 图例框长宽 表面颜色 边框颜色  参考箭头的位置 参考箭头大小 参考label字体大小
    '''
    rect = mpl.patches.Rectangle((location[0], location[1]), length, wide, transform=ax.transAxes,    # 这个能辟出来一块区域，第一个参数是最左下角点的坐标，后面是矩形的长和宽
                            fc=fc, ec=ec, lw=lw, zorder=order
                            )
    ax.add_patch(rect)

    ax.quiverkey(q, X=quiver_x, Y=quiver_y, U=speed,
                    label=f'{speed} m/s', labelpos='S', labelsep=0.1,fontproperties={'size':fontsize})

def save_fig(path_out,file_out,dpi=450):
    plv3_1.check_path(path_out)
    plt.savefig(path_out+file_out,dpi=450)

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

f0 = xr.open_dataset('/home/sun/data/ERA5_data_monsoon_onset/regression/regression_uv_to_OLR_to_LSTC_remove_each_other.nc')
corre_file = xr.open_dataset('/home/sun/data/ERA5_data_monsoon_onset/correlation/correlation_LSTC_OLR_10wind_pentad_remove_each_other.nc')
print(corre_file)

#def paint_picture(lon, lat, u, v, msl, u_correlation, v_correlation, scale, speed, pic_name, title_name):
def paint_picture(lon, lat, u, v, slp, scale, speed, pic_name, title_name, std, correlation_u, correlation_v):
    # 绘制图像
    proj    =  ccrs.PlateCarree()
    fig1    =  plt.figure(figsize=(20,8))
    spec1   =  fig1.add_gridspec(nrows=2,ncols=3)

    j = 0
    for row in range(2):
        for col in range(3):
            ax = fig1.add_subplot(spec1[row,col],projection=proj)

            # 范围设置
            lonmin,lonmax,latmin,latmax  =  45,150,-10,30
            extent     =  [lonmin,lonmax,latmin,latmax]

            # 刻度设置
            set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(50,150,6,dtype=int),yticks=np.linspace(-10,30,5,dtype=int),nx=1,ny=1,labelsize=19)

            # 绘制填色图 —— 回归海平面气压场
            im  =  ax.contourf(lon,lat,slp[j] * -1 * std[j], np.linspace(-75, 75, 11), cmap='coolwarm', alpha=1,extend='both')
    
            # 绘制赤道线
            ax.plot([40,150],[0,0],'--',color='k')

            # 绘制海岸线
            ax.coastlines(resolution='110m',lw=1)

            # 绘制矢量图
            q  =  ax.quiver(lon, lat, u[j], v[j], 
                regrid_shape=15, angles='uv',   # regrid_shape这个参数越小，是两门就越稀疏
                scale_units='xy', scale=scale,        # scale是参考矢量，所以取得越大画出来的箭头就越短 LSTC:0.0075
                units='xy', width=0.25,
                transform=proj,
                color='k',linewidth=1.2,headlength = 5, headaxislength = 4, headwidth = 5)
    
            # 加序号
            #plv3_2a.add_text(ax=ax,string="(b)",fontsize=27.5,location=(0.015,0.91))

            ax.set_title('Pentad '+str(j + 20))

            # 加矢量图图例
            add_vector_legend(ax=ax,q=q, speed=speed)

            # add title
            #ax.set_title(title_name, fontsize=20)
            j += 1

    # 保存图片
    plt.savefig("/home/sun/paint/pentad_variable/regression/"+pic_name)
    
    plt.show()

std_lstc = np.array([])
std_olr  = np.array([])
for i in range(6):
    std_lstc = np.append(std_lstc, np.std(f0['lstc_remove_olr'][i]))
    std_olr  = np.append(std_olr,  np.std(f0['olr_remove_lstc'][i]))
paint_picture(lon=f0.lon.data, lat=f0.lat.data, u=f0['u_detrend'].data[60], v=f0['v_detrend'].data[10], slp=f0['rc_slp_olr'], scale=0.7, speed=1, pic_name='Pentad_20-25_UV_regression_to_OLR.pdf', title_name='10m wind regression to uv', std=std_olr)
#paint_picture(lon=f0.lon.data, lat=f0.lat.data, u=f0['rc_u_lstc'].data, v=f0['rc_v_lstc'].data, slp=f0['rc_slp_lstc'], scale=0.6, speed=1, pic_name='Pentad_20-25_UV_regression_to_LSTC.pdf', title_name='10m wind regression to uv', std=std_lstc)
#print(np.std(f0['lstc_remove_olr']))
#print()
#print(np.std(f0['olr_remove_lstc'][:, 2]))

#fig, ax = plt.subplots()
#plt.plot(f0['lstc_remove_olr'][:, 3])
#plt.savefig("/home/sun/paint/pentad_variable/regression/test1.png")
#plt.show()