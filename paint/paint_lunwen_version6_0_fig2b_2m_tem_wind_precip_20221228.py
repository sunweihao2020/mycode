'''
2022-12-28
本代码绘制论文version6.0中的fig2b
内容为2m温度+2m风
version6新增: 4月降水
'''
import sys
sys.path.append("/home/sun/mycode/paint")
import paint_lunwen_version3_0_fig1_bob_onset_seris as plv3_1
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
import paint_lunwen_version3_0_fig2a_tem_gradient_20220426 as plv3_2a
from matplotlib.colors import ListedColormap,LinearSegmentedColormap
import matplotlib as mpl
module_path = ["/home/sun/mycode/module/","/data5/2019swh/mycode/module/"]
sys.path.append(module_path[0])
from module_sun import *

def colormap_from_list_color(list):
    # 本函数读取颜色列表然后制作出来colormap
    return LinearSegmentedColormap.from_list('chaos',list)

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

def paint_picture(lon,lat,avg_t2m,avg_u,avg_v,precip):
    # 绘制图像
    proj    =  ccrs.PlateCarree()
    fig,ax   =  plt.subplots(figsize=(13,10),subplot_kw=dict(projection=ccrs.PlateCarree()))



    # 范围设置
    lonmin,lonmax,latmin,latmax  =  45,115,-10,30
    extent     =  [lonmin,lonmax,latmin,latmax]

    # 刻度设置
    set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(50,110,4,dtype=int),yticks=np.linspace(-10,30,5,dtype=int),nx=1,ny=1,labelsize=19)
    
    # 绘制赤道线
    ax.plot([40,120],[0,0],'--',color='k')

    # 获取colorbar
    clist=['#0394f7','#6df279','#f9f980','#ff0000']
    cmp  =  colormap_from_list_color(clist)


    # 绘制气温填色图
    im  =  ax.contourf(lon,lat,avg_t2m-273.15,np.linspace(10,34,13),cmap=cmp,alpha=1,extend='both')

    # 绘制海岸线
    ax.coastlines(resolution='110m',lw=1)

    # 绘制降水等值线
    im1  =  ax.contour(lon, lat, precip, levels=np.arange(5,31,5), colors='white', linewidths=2.75, alpha=1, zorder=1)
    ax.clabel(im1, levels=np.arange(5,31,5), inline=True, fontsize=12)

    # 绘制矢量图
    q  =  ax.quiver(lon, lat, avg_u, avg_v, 
                regrid_shape=15, angles='uv',   # regrid_shape这个参数越小，是两门就越稀疏
                scale_units='xy', scale=1,        # scale是参考矢量，所以取得越大画出来的箭头就越短
                units='xy', width=0.25,
                transform=proj,
                color='k',linewidth=1.2,headlength = 5, headaxislength = 4, headwidth = 5)
    
    # 加序号
    #plv3_2a.add_text(ax=ax,string="(b)",fontsize=27.5,location=(0.015,0.91))

    # 加矢量图图例
    add_vector_legend(ax=ax,q=q, speed=5)

    # colorbar
    a = fig.colorbar(im,shrink=0.6, pad=0.05,orientation='horizontal')
    a.ax.tick_params(labelsize=15)

    # 保存图片
    save_fig(path_out="/home/sun/paint/lunwen/version6.0/",file_out="lunwen_fig2b_v6.0_2m_tem_wind_precip.pdf")

def main():
    from paint_lunwen_version5_0_fig3_sst_2mwind_prect_220428 import interp_precip
    path = "/home/sun/qomo-data/"
    
    f1   =  plv3_2a.xarray_read_file(path=path,file="composite_u10v10.nc",range_lat=slice(-10,30),range_lon=slice(30,120))
    f2   =  plv3_2a.xarray_read_file(path=path,file="composite-merra2-single.nc",range_lat=slice(-10,30),range_lon=slice(30,120))
    f3   =  plv3_2a.xarray_read_file(path=path,file="composite-precipitation_trmm.nc",range_lat=slice(-10,30),range_lon=slice(30,120))

    avg_u  =  np.average(f1.u10m.data[0:30,:],axis=0)
    avg_v  =  np.average(f1.v10m.data[0:30,:],axis=0)

    avg_t2m = np.average(f2.T2M.data[0:30,:],axis=0)

    # 这里我需要对precipitation进行插值，使用的是以前编写的函数
    trmm_prect  =  interp_precip(f3.precipitation.data.swapaxes(2,1),lon=f3.lon,lat=f3.lat,newlat=f2.lat,newlon=f1.lon)
    avg_precip  =  np.average(trmm_prect[0:30], axis=0)

    paint_picture(lon=f1.lon,lat=f1.lat,avg_t2m=avg_t2m,avg_u=avg_u,avg_v=avg_v, precip=avg_precip)



if __name__ == "__main__":
    main()
