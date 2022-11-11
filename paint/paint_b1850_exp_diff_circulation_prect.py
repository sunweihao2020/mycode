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


def convert_lon(lon):
    '''将经度换算到[-180, 180]范围内.'''
    return (lon + 180) % 360 - 180

def paint_pentad_circulation():
    '''This function paint pentad circulation based on b1850 experiment'''
    #  ----- import  ----------
    from matplotlib import cm
    from matplotlib.colors import ListedColormap

    import sys
    sys.path.append("/home/sun/mycode/paint/")
    from paint_lunwen_version3_0_fig2b_2m_tem_wind_20220426 import set_cartopy_tick,save_fig,add_vector_legend
    from paint_lunwen_version3_0_fig2a_tem_gradient_20220426 import add_text



    import matplotlib
    matplotlib.use('Agg')
    ## ------------------------

    path_out  =  "/home/sun/data/model_data/climate/"
    file_out1  =  "b1850_control_atmospheric_monthly_average_2.nc"
    file_out2  =  "b1850_maritime_atmospheric_monthly_average_2.nc"
    f0        =  xr.open_dataset(path_out+file_out1)
    f1        =  xr.open_dataset(path_out+file_out2)
    ## -------------------------------------------------


    # ------  time period  -----------
    pentads   =  [5,6,7,8]
    date      =  [6,7,8,9]

    # -------  color bar   -----------
    viridis = cm.get_cmap('jet', 22)
    newcolors = viridis(np.linspace(0, 1, 22))
    newcmp = ListedColormap(newcolors)
    #newcmp.set_under('white')
    #newcmp.set_over('#004080')

    # -------   cartopy extent  -----
    #lonmin,lonmax,latmin,latmax  =  50,230,-20,50
    #extent     =  [lonmin,lonmax,latmin,latmax]

    # -------     figure    -----------
    proj  =  ccrs.PlateCarree(central_longitude=180)
    fig1    =  plt.figure(figsize=(35,24))
    spec1   =  fig1.add_gridspec(nrows=2,ncols=2)

    j  =  0

    # ------       paint    ------------
    for col in range(2):
        for row in range(2):
            ax = fig1.add_subplot(spec1[row,col],projection=proj)

            # 设置刻度
            #set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(50,230,10,dtype=int),yticks=np.linspace(-20,50,8,dtype=int),nx=1,ny=1,labelsize=25)
            #print(f0.lon.data[144])
            # 添加赤道线
            ax.plot([50,170],[0,0],'k--')

            im  =  ax.contourf(f0.lon.data,f0.lat,(f0["PRECT"].data[pentads[j]]*86400000 - f1["PRECT"].data[pentads[j]]*86400000)/(f0["PRECT"].data[pentads[j]]*86400000)*100,np.linspace(-100,100,21),cmap=newcmp,alpha=1,extend='both')

            # 海岸线
            ax.coastlines(resolution='50m',lw=2)

            print((f0["U"].data[pentads[j]]-f1["U"].data[pentads[j]]).shape)
            q  =  ax.quiver(f0.lon.data, f0.lat.data, (f0["U"].data[pentads[j],6]-f1["U"].data[pentads[j],6]), (f0["V"].data[pentads[j],6]-f1["V"].data[pentads[j],6]),
                regrid_shape=20, angles='uv',       # regrid_shape这个参数越小，是两门就越稀疏
                scale_units='xy', scale=0.28,        # scale是参考矢量，所以取得越大画出来的箭头就越短
                units='xy', width=0.35,
                transform=proj,
                color='k',linewidth=1.2,headlength = 5, headaxislength = 4, headwidth = 5,alpha=1)

            # 加日期
            add_text(ax=ax,string="month"+str(date[j]),location=(0.80,0.91),fontsize=25)

            # 加矢量图图例
            add_vector_legend(ax=ax,q=q,speed=1)
        
            j += 1
    print(f0["U"].data[6, 6, 50, :])
    # 加colorbar
    fig1.subplots_adjust(top=0.8) 
    cbar_ax = fig1.add_axes([0.2, 0.05, 0.6, 0.03]) 
    cb  =  fig1.colorbar(im, cax=cbar_ax, shrink=0.1, pad=0.01, orientation='horizontal')
    cb.ax.tick_params(labelsize=20)

    save_fig(path_out="/home/sun/paint/b1850_exp/",file_out="b1850_diff_monthly_925_circulation_with_prect.pdf")



def main():
    paint_pentad_circulation()
    


if __name__  ==  "__main__":
    main()