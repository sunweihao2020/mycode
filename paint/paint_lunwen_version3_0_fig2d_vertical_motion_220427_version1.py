'''
2022-4-28
本代码绘制论文version3_0中的fig2d
内容为等熵面 散度 流场
出版标准
有bug不会改 放弃
'''
import os
import sys
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

sys.path.append("/home/sun/mycode/paint")
import paint_lunwen_version3_0_fig2a_tem_gradient_20220426 as plv3_2a


def read_cal_april_mean(path,file,var,range_lat=slice(10,15),range_lon=slice(30,120),range_lev=slice(1000,200)):
    f  =  plv3_2a.xarray_read_file(path=path,file=file,range_lat=range_lat,range_lon=range_lon,range_lev=range_lev)

    return np.nanmean(np.nanmean(f[var].data[0:30],axis=0),axis=1)

def set_lon_pressure_tick(ax, xticks, yticks, nx=0, ny=0,
    xformatter=None, yformatter=None,labelsize=23):
    '''
    这个函数是对纬向-垂直剖面的坐标轴进行设置
    '''
    import matplotlib.ticker as mticker
    from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
    # 本函数设置地图上的刻度 + 地图的范围
    ax.set_xticks(xticks)
    ax.set_yticks(yticks)
    # 设置次刻度.
    xlocator = mticker.AutoMinorLocator(nx + 1)
    ylocator = mticker.AutoMinorLocator(ny + 1)
    ax.xaxis.set_minor_locator(xlocator)
    ax.yaxis.set_minor_locator(ylocator)

    # 设置Formatter.
    if xformatter is None:
        xformatter = LongitudeFormatter()
    ax.xaxis.set_major_formatter(xformatter)

    # 设置axi label_size，这里默认为两个轴
    ax.tick_params(axis='both',labelsize=labelsize)


def add_topo(ax,lon,topo):
    ax2  =  ax.twinx()
    ax2.set_ylim((0,4.5))
    ax2.plot(lon,topo/1000,color='k')
    ax2.fill_between(lon,0,topo/1000,where=topo>0,color='k')

    ax2.set_yticklabels([])
    ax2.set_yticks([])
  

def paint_pic(lon,level,avg_theta,div,uwind,omega,topo_lon,topo):
    # 绘制图像
    fig,ax   =  plt.subplots(figsize=(13,10))
    ax.invert_yaxis()

    # 绘制等值线
    im1   =  ax.contour(lon,level,avg_theta,np.linspace(-2,4,13),linewidth=0.9,colors='grey',negative_linestyle='dashed',zorder=1,alpha=0.9)
    im2   =  ax.contourf(lon,level,div,12,cmap='seismic',extend='both',alpha=0.9,zorder=0)

    # 绘制矢量图
    q  =  ax.quiver(lon[::4], level[::2], uwind[::2,::4], omega[::2,::4], 
                angles='uv',                        # regrid_shape这个参数越小，是两门就越稀疏
                scale_units='xy', scale=1.1,        # scale是参考矢量，所以取得越大画出来的箭头就越短
                units='xy', width=2.2,
                color='k',zorder=2)

    # 设置colorbar
    cb = fig.colorbar(im2,shrink=0.6, pad=0.05,orientation='horizontal')
    cb.ax.tick_params(labelsize=15)
    
    # 设置坐标轴
    set_lon_pressure_tick(ax=ax,xticks=np.linspace(50,110,4,dtype=int),yticks=np.linspace(1000,200,5,dtype=int),nx=1,ny=1,labelsize=23)


    # 添加地形
    #add_topo(ax,lon=topo_lon,topo=topo)


def main():
    path =   "/home/sun/qomo-data/"
    avg_theta = read_cal_april_mean(path=path,file="composite_equivalent_tem.nc",var="theate_e")
    avg_uwind = read_cal_april_mean(path=path,file="composite3.nc",var="uwind")
    avg_omega = read_cal_april_mean(path=path,file="composite3.nc",var="OMEGA") * -60

    # 计算纬向偏差
    f3   =   xr.open_dataset(path+"composite_equivalent_tem.nc").sel(lat=slice(10,15),level=slice(1000,200)).isel(time=slice(0,30))
    avg_theta_all  =  np.nanmean(np.nanmean(np.nanmean(f3.theate_e,axis=0),axis=1),axis=1)

    for i in range(0,113):
        avg_theta[:,i]  =  avg_theta[:,i] - avg_theta_all

    # 计算散度
    f4   =   xr.open_dataset(path+"composite-div_vor.nc").sel(lat=slice(10,15),lon=slice(30,120),level=slice(1000,200))
    div  =   np.nanmean(np.nanmean(f4.div[0:30],axis=0),axis=1)

    # 计算地形
    f5   =   xr.open_dataset("/home/sun/data/gebco/bathymetric.nc").sel(lat=slice(10,15),lon=(30,120))
    dixing  =  f5.elevation.data
    dixing[dixing <= 0]  =  0
    topo    =  np.average(dixing,axis=0)

    # 绘制图片
    paint_pic(f4.lon.data,f4.level,avg_theta=avg_theta,div=div,uwind=avg_uwind,omega=avg_omega,topo_lon=f5.lon.data,topo=topo)