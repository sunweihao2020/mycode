'''
2022-9-13
This code paint b1850 exp output
includes: 4 5 6 7 month
'''
import os
src_path  =  '/home/sun/data/model_data/climate/'
file_name =  ['b1850_control_atmospheric_monthly_average.nc','b1850_indian_atmospheric_monthly_average.nc','b1850_inch_atmospheric_monthly_average.nc','b1850_maritime_atmospheric_monthly_average.nc']
exp_names =  ['control','indian','inch','maritime']
date   =  [3,4,5,6]

def paint_monthly_925_wind(path,file,extent,expname):
    from matplotlib import projections
    import xarray as xr
    import numpy as np
    import cartopy.crs as ccrs
    import matplotlib.pyplot as plt
    import sys
    import cartopy.crs as ccrs

    #sys.path.append("/home/sun/mycode/module/")
    #from module_sun import *    

    sys.path.append("/home/sun/mycode/paint/")
    from paint_lunwen_version3_0_fig2b_2m_tem_wind_20220426 import set_cartopy_tick,save_fig
    from paint_lunwen_version3_0_fig2a_tem_gradient_20220426 import add_text

    # source file
    f0     =   xr.open_dataset(path + file)
    # 设置画布
    proj    =  ccrs.PlateCarree()
    fig1    =  plt.figure(figsize=(26,17))
    spec1   =  fig1.add_gridspec(nrows=2,ncols=2)

    # colorbar使用ncl的

    j  =  0
    for col in range(2):
        for row in range(2):
            ax = fig1.add_subplot(spec1[row,col],projection=proj)

            # 设置刻度
            set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(50,110,4,dtype=int),yticks=np.linspace(-10,30,5,dtype=int),nx=1,ny=1,labelsize=25)

            # 赤道线
            ax.plot([40,120],[0,0],'k--')

            # 等值线
            im1  =  ax.contour(f0.lon,f0.lat,f0['PRECT'][date[j],:]*86400*1000,levels=np.linspace(3,33,7),colors='#59A95A',linewidths=3.5,alpha=1,zorder=1)

            ax.clabel(im1, inline=True, fontsize=13)

            # 海岸线
            ax.coastlines(resolution='110m',lw=1)

            # 流线
            #q  =  ax.quiver(f0.lon.data, f0.lat.data, (f0["U"].data[date[j],3]), (f0["V"].data[date[j],3]), 
            #    regrid_shape=15, angles='uv',       # regrid_shape这个参数越小，是两门就越稀疏
            #    scale_units='xy', scale=1.,        # scale是参考矢量，所以取得越大画出来的箭头就越短
            #    units='xy', width=0.35,
            #    transform=proj,
            #    color='k',linewidth=1,headlength = 4, headaxislength = 3, headwidth = 5,alpha=1)
            ax.streamplot(f0.lon, f0.lat, f0.U.data[date[j],3,], f0.V.data[date[j],3], color='k',linewidth=2.5,density=1.2,arrowsize=2.75, arrowstyle='->')

            # 加日期
            add_text(ax=ax,string="Month"+str(date[j]+1),location=(0.7,0.91),fontsize=30)
            
        
            j += 1


    # 保存图片
    #plt.tight_layout()
    save_fig(path_out="/home/sun/paint/b1850_exp/monthly/",file_out=expname + "925_4567_month.pdf")

def main():
    # 划定空间范围
    lon_slice  =  slice(40,120)
    lat_slice  =  slice(-15,40)

    lonmin,lonmax,latmin,latmax  =  45,115,-10,30
    extent     =  [lonmin,lonmax,latmin,latmax]

    for i in range(4):
        paint_monthly_925_wind(src_path,file_name[i],extent,exp_names[i])

if __name__ == "__main__":
    main()