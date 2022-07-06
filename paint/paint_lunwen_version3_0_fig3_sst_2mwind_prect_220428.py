'''
2022-4-28
本代码绘制论文version3.0中的fig3
出版标准
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

def interp_precip(precip,lon,lat,newlon,newlat):
    '''给输入的降水数据进行插值'''
    in_prect1  =  np.zeros((precip.shape[0],len(lat),len(newlon)))
    in_prect2  =  np.zeros((precip.shape[0],len(newlat),len(newlon)))

    for tt in range(precip.shape[0]):
        for latt in range(len(lat)):
            in_prect1[tt,latt,:]  =  np.interp(newlon,lon,precip[tt,latt,:])
    
    for tt in range(precip.shape[0]):
        for lonn in range(len(newlon)):
            in_prect2[tt,:,lonn]  =  np.interp(newlat,lat,in_prect1[tt,:,lonn])

    print('successfully interp precipitation')
    return in_prect2

    
def paint_pic(extent,sst_lon,sst_lat,wind_lon,wind_lat,prect_lat,prect,sst,U2M,V2M,date,dates,number):
    # 设置画布
    proj    =  ccrs.PlateCarree()
    fig1    =  plt.figure(figsize=(26,17))
    spec1   =  fig1.add_gridspec(nrows=2,ncols=2)

    # colorbar使用ncl的
    cmap  =  create_ncl_colormap("/home/sun/data/color_rgb/MPL_coolwarm.txt",32)

    j  =  0
    for col in range(2):
        for row in range(2):
            ax = fig1.add_subplot(spec1[row,col],projection=proj)

            # 设置刻度
            set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(50,110,4,dtype=int),yticks=np.linspace(-10,30,5,dtype=int),nx=1,ny=1,labelsize=25)

            # 赤道线
            ax.plot([40,120],[0,0],'k--')

            # 等值线
            im1  =  ax.contour(sst_lon,prect_lat,prect[date[j],:],levels=np.arange(12,25,12),colors='#59A95A',linewidths=3.5,alpha=1,zorder=1)
            im2  =  ax.contourf(sst_lon,sst_lat,sst[date[j],:],levels=np.arange(26.5,31,0.25),cmap=cmap,extend='both',zorder=0)
            ax.clabel(im1, inline=True, fontsize=13)

            # 海岸线
            ax.coastlines(resolution='110m',lw=1)

            # 流线
            q   =   ax.streamplot(wind_lon, wind_lat, U2M[date[j],:], V2M[date[j],:],linewidth=3, color = 'k',density=[1, 1.15], arrowsize=2.75, arrowstyle='->')

            # 加日期
            if dates[j]<0:
                add_text(ax=ax,string="D"+str(dates[j]),location=(0.87,0.91),fontsize=30)
            elif dates[j]>0:
                 add_text(ax=ax,string="D+"+str(dates[j]),location=(0.87,0.91),fontsize=30)
            else:
                 add_text(ax=ax,string="D"+str(dates[j]),location=(0.87,0.91),fontsize=30)
            
            # 加图序号
            add_text(ax=ax,string="("+number[j]+")",location=(0.015,0.91),fontsize=30)
        
            j += 1

    # 加colorbar
    fig1.subplots_adjust(top=0.8) 
    cbar_ax = fig1.add_axes([0.2, 0.05, 0.6, 0.03]) 
    cb  =  fig1.colorbar(im2, cax=cbar_ax, shrink=0.1, pad=0.01, orientation='horizontal')
    cb.ax.tick_params(labelsize=25)

    # 保存图片
    #plt.tight_layout()
    save_fig(path_out="/home/sun/paint/lunwen/version3.0/",file_out="lunwen_fig3_v3.0_prect_sst_2mwind.pdf")

def main():
    # 划定空间范围
    lon_slice  =  slice(40,120)
    lat_slice  =  slice(-15,40)

    lonmin,lonmax,latmin,latmax  =  45,115,-10,30
    extent     =  [lonmin,lonmax,latmin,latmax]

    # 选取时间
    dates  =  [-12,-6,-2,0]  #总共4张图
    date   =  [18,24,28,30]

    # 图片序号
    number =  ["a","b","c","d"]

    # 读取文件
    path  =  "/home/sun/qomo-data/"
    f1    =  xr.open_dataset(path+"composite_OISST_trans.nc").sel(lon=lon_slice,lat=lat_slice)
    f2    =  xr.open_dataset(path+"composite-precipitation_trmm.nc")
    f3    =  xr.open_dataset(path+"composite-merra2-single.nc").sel(lon=lon_slice,lat=lat_slice)

    # TRMM降水数据需要插值 这里调用swapaxes调换一下trmm的轴
    trmm_prect  =  interp_precip(f2.precipitation.data.swapaxes(2,1),lon=f2.lon,lat=f2.lat,newlat=np.linspace(-50,50,101),newlon=f1.lon)

    #  下面开始绘图
    paint_pic(extent=extent,sst_lon=f1.lon,sst_lat=f1.lat,wind_lon=f3.lon,wind_lat=f3.lat,prect=trmm_prect,sst=f1.sst.data,U2M=f3.U2M.data,V2M=f3.V2M.data,date=date,dates=dates,number=number,prect_lat=np.linspace(-50,50,101))

if __name__ == "__main__":
    main()