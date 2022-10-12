'''
2022-4-28
本代码绘制论文version3.0中的fig4
Q1 流线
出版标准
'''
import xarray as xr
import numpy as np

from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import matplotlib.pyplot as plt

import cartopy.crs as ccrs

import sys
sys.path.append("/home/sun/mycode/paint/")
from paint_lunwen_version3_0_fig2b_2m_tem_wind_20220426 import set_cartopy_tick,save_fig
from paint_lunwen_version3_0_fig2a_tem_gradient_20220426 import add_text

class number_date:
    '''定义一个日期序号类'''
    dates  =  [-6,-2,0,2]
    date   =  [24,28,30,32]
    number =  ["a","b","c","d"]

def paint_pic(extent,lon,lat,q1_avg,uwind,vwind):
    # 获取colormap
    viridis = cm.get_cmap('Reds', 16)
    newcolors = viridis(np.linspace(0, 1, 16))
    newcmp = ListedColormap(newcolors)
    newcmp.set_under('white')
    newcmp.set_over('brown')

    # 设置画布
    proj  =  ccrs.PlateCarree()
    fig1    =  plt.figure(figsize=(26,17))
    spec1   =  fig1.add_gridspec(nrows=2,ncols=2)

    j  =  0

    for col in range(2):
        for row in range(2):
            ax = fig1.add_subplot(spec1[row,col],projection=proj)

            # 设置刻度
            set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(50,110,4,dtype=int),yticks=np.linspace(-10,30,5,dtype=int),nx=1,ny=1,labelsize=25)

            # 添加赤道线
            ax.plot([40,120],[0,0],'k--')

            im  =  ax.contourf(lon,lat,q1_avg[number_date.date[j]],np.linspace(0,6,7),cmap=newcmp,alpha=1,extend='both')

            # 海岸线
            ax.coastlines(resolution='110m',lw=2)


            ax.streamplot(lon, lat, uwind[number_date.date[j]], vwind[number_date.date[j]], color='k',linewidth=2.5,density=1.2,arrowsize=2.75, arrowstyle='->')

            # 加日期
            if number_date.dates[j]<0:
                ax.set_title("D"+str(number_date.dates[j]),loc='right',fontsize=27.5)
            elif number_date.dates[j]>0:
                 ax.set_title("D+"+str(number_date.dates[j]),loc='right',fontsize=27.5)
            else:
                 ax.set_title("D"+str(number_date.dates[j]),loc='right',fontsize=27.5)
            # 加序号
            ax.set_title("("+number_date.number[j]+")",loc='left',fontsize=27.5)
        
            j += 1

    
    # 加colorbar
    fig1.subplots_adjust(top=0.8) 
    cbar_ax = fig1.add_axes([0.2, 0.05, 0.6, 0.03]) 
    cb  =  fig1.colorbar(im, cax=cbar_ax, shrink=0.1, pad=0.01, orientation='horizontal')
    cb.ax.tick_params(labelsize=20)

    save_fig(path_out="/home/sun/paint/lunwen/version5.0/",file_out="lunwen_fig4_v5.0_q1_700_stream.pdf")

def generate_cmap():
    viridis = cm.get_cmap('Reds', 16)
    newcolors = viridis(np.linspace(0, 1, 16))
    newcmp = ListedColormap(newcolors)
    newcmp.set_under('white')
    newcmp.set_over('brown')

    return newcmp


def main():
    # 划定范围
    level1  =  700
    level2  =  slice(850,500)
    lon_slice  =  slice(40,120)
    lat_slice  =  slice(-10,40)

    lonmin,lonmax,latmin,latmax  =  45,115,-10,30
    extent     =  [lonmin,lonmax,latmin,latmax]


    # 读取数据
    path  =  "/home/sun/qomo-data/"
    f1  =  xr.open_dataset(path+"composite3.nc").sel(level=level1,lon=lon_slice,lat=lat_slice)   
    f2  =  xr.open_dataset(path+"composite-Q1-merra2.nc").sel(level=level2,lon=lon_slice,lat=lat_slice)  

    # 计算Q1的z方向平均
    q1_avg  =  np.average(f2.Q1,axis=1)

    # 绘图
    paint_pic(extent=extent,lon=f1.lon.data,lat=f1.lat.data,q1_avg=q1_avg,uwind=f1.uwind.data,vwind=f1.vwind.data)

if __name__ == "__main__":
    main()