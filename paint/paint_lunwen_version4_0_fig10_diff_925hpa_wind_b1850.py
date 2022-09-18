'''
2022-9-17
本代码绘制论文version3.0中的fig10
内容为模式控制实验与敏感性实验之间的差值风
出版标准

数据替换为耦合模式结果
'''
import sys
import xarray as xr
import numpy as np
module_path = ["/home/sun/mycode/module/","/data5/2019swh/mycode/module/"]
sys.path.append(module_path[0])
from module_sun import *
import time
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import os
import math

sys.path.append("/home/sun/mycode/paint/")
from paint_lunwen_version3_0_fig2b_2m_tem_wind_20220426 import save_fig,set_cartopy_tick,add_vector_legend
from paint_lunwen_version3_0_fig2a_tem_gradient_20220426 import add_text
import paint_lunwen_version3_0_fig8_cross_jet_prect_model_compare as fig8


class number_date:
    '''定义一个日期序号类'''
    dates  =  np.array([22,23,24,25],dtype=int)
    date   =  np.array([21,22,23,24],dtype=int)
    number =  ["a","b","c","d"]

def cal_diff_wind(lev=925,lat_slice=slice(-10,30),lon_slice=slice(45,115)):

    # model data
    data_path       =  '/home/sun/data/model_data/climate/'
    f1  =  xr.open_dataset(data_path + "b1850_control_atmosphere.nc").sel(lev=lev,lat=lat_slice,lon=lon_slice)
    f2  =  xr.open_dataset(data_path + "b1850_indian_climate_atmosphere3.nc").sel(lev=lev,lat=lat_slice,lon=lon_slice)

    diff_u  =  f1.U.data - f2.U.data
    diff_v  =  f1.V.data - f2.V.data

    return (fig8.data_resolve.cal_pentad(diff_u), fig8.data_resolve.cal_pentad(diff_v))

def paint_wind(wind,extent=[45,115,-10,30],lev=925,lat_slice=slice(-10,30),lon_slice=slice(45,115)):
    '''本函数绘制22-25侯差值风'''
    data_path   =  '/home/sun/data/model_data/climate/'
    f0          =  xr.open_dataset(data_path + "b1850_control_atmosphere.nc").sel(lev=lev,lat=lat_slice,lon=lon_slice)
    # 设置画布
    proj    =  ccrs.PlateCarree()
    fig1    =  plt.figure(figsize=(20,14))
    spec1   =  fig1.add_gridspec(nrows=2,ncols=2)

    j = 0
    for row in range(2):
        for col in range(2):
            ax  =  fig1.add_subplot(spec1[row,col],projection=proj)

            # 设置刻度
            set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(50,110,4,dtype=int),yticks=np.linspace(-10,30,5,dtype=int),nx=1,ny=1,labelsize=25)

            # 赤道线
            ax.plot([40,120],[0,0],'k--')


            # 海岸线
            ax.coastlines(resolution='110m',lw=2)

            # 矢量图
            q  =  ax.quiver(f0.lon, f0.lat, wind[0][number_date.date[j],:], wind[1][number_date.date[j],:], 
                regrid_shape=15, angles='uv',   # regrid_shape这个参数越小，是两门就越稀疏
                scale_units='xy', scale=1.2,        # scale是参考矢量，所以取得越大画出来的箭头就越短
                units='xy', width=0.25,
                transform=proj,
                color='k',linewidth=1.2,headlength = 5, headaxislength = 4, headwidth = 5,alpha=1)

            # 加日期
            if number_date.dates[j]<0:
                add_text(ax=ax,string="Pentad "+str(number_date.dates[j]),location=(0.68,0.88),fontsize=30)
            elif number_date.dates[j]>0:
                 add_text(ax=ax,string="Pentad "+str(number_date.dates[j]),location=(0.68,0.88),fontsize=30)
            else:
                 add_text(ax=ax,string="Pentad "+str(number_date.dates[j]),location=(0.68,0.88),fontsize=30)
            # 加序号
            #add_text(ax=ax,string="("+number_date.number[j]+")",location=(0.02,0.88),fontsize=30)

            # 加矢量图图例
            add_vector_legend(ax=ax,q=q)

            
            j += 1
    

    save_fig(path_out="/home/sun/paint/lunwen/version4.0/",file_out="lunwen_fig10_v4.0_diff_925_wind_b1850.pdf")


def main():
    paint_wind(wind=cal_diff_wind())

if __name__ == "__main__":
    main()
