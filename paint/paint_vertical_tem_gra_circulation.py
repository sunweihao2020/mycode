'''
20220630
This code paint meridional-vertical temperature gradient and circulation between 90 - 100E
using composite3.nc file, which is composite monsoon onset process
'''

import os
import numpy as np
import sys
import xarray as xr
sys.path.append("/home/sun/mycode/module/")
sys.path.append("/home/sun/mycode/paint/")
from module_sun import *
from paint_lunwen_version3_0_fig2a_tem_gradient_20220426 import create_label_lat
import matplotlib.pyplot as plt

lon_average  =  slice(90,100)

def zonal_avg():
    '''calculate variables for paint and write to ncfile'''
    path0  =  "/home/sun/qomo-data/"
    file0  =  xr.open_dataset(path0+"composite3.nc").sel(lon=lon_average)

    # calculate zonal average of variables
    avg_omega  =    np.nanmean(file0.OMEGA,axis=3) * -100
    avg_u      =    np.nanmean(file0.uwind,axis=3)
    avg_v      =    np.nanmean(file0.vwind,axis=3)
    avg_t      =    np.nanmean(file0.T,axis=3)

    # calculate meridional gradient of T
    disy, disx, location =    cal_xydistance(file0.lat, file0.lon)
    avg_t_gradient       =    np.gradient(avg_t,location,axis=2)

    # write into nc file
    ncfile = xr.Dataset(
        {
            "avg_u": (["time", "level", "lat"], avg_u),
            "avg_v": (["time", "level", "lat"], avg_v),
            "avg_t": (["time", "level", "lat"], avg_t),
            "avg_omega": (["time", "level", "lat"], avg_omega),
            "avg_t_gradient": (["time", "level", "lat"], avg_t_gradient),
        },
        coords={
            "level": (["level"], file0.level.data),
            "lat": (["lat"], file0.lat.data),
            "time": (["time"], np.linspace(1, len(file0.time.data), len(file0.time.data))),
        },
    )
    ncfile["level"].attrs = file0.level.attrs
    ncfile["lat"].attrs   = file0.lat.attrs
    ncfile.attrs["description"]  =  "created in 220630, zonal averaged between 90 to 100E. Based on composite3.nc"

    ncfile.to_netcdf("/home/sun/data/monsoon_onset/composite_zonal_average.nc")

    print("success write into")

def paint_meridional_variables():
    from paint_lunwen_version3_0_fig2a_tem_gradient_20220426 import add_text
    import paint_lunwen_version3_0_fig1_bob_onset_seris as plv3
    '''paint meridional variables daily -9 1 9. Total 3 figs'''
    fig1    =  plt.figure(figsize=(26,26))
    spec1   =  fig1.add_gridspec(nrows=3,ncols=3)

    f0      =  xr.open_dataset("/home/sun/data/monsoon_onset/composite_zonal_average.nc").sel(lat=slice(-10,45),level=slice(1000,200))
    # interpolate values to spaced y axs
    avg_v  =  np.zeros((f0.time.shape[0],len(np.linspace(1000,200,33)),f0.lat.shape[0]))  ;  avg_omega  =  avg_v.copy()
    for latt in range(0,f0.lat.shape[0]):
        for tt in range(0,f0.time.shape[0]):
            avg_v[tt,:,latt]   =   np.interp(np.linspace(1000,200,33),f0.level.data,f0.avg_v.data[tt,:,latt])
            avg_omega[tt, :, latt] = np.interp(np.linspace(1000, 200, 33), f0.level.data, f0.avg_omega.data[tt, :, latt])
    # colorbar is from ncl
    cmap = create_ncl_colormap("/home/sun/data/color_rgb/BlueDarkRed18.txt", 16)

    start1  =  22
    j  =  0
    for col in range(3):
        for row in range(3):
            ax  =  fig1.add_subplot(spec1[row,col])

            im  =  ax.contourf(f0.lat,f0.level,f0.avg_t_gradient.data[start1+j]*1E5,np.linspace(-2,2,11),cmap=cmap,extend='both')
            im2 =  ax.contour(f0.lat,f0.level,f0.avg_t_gradient.data[start1+j]*1E5,[0],linewidths=3)
            # set x-axis
            # ax.set_xticks(np.arange(-10, 50, 5))
            # ax.set_xticklabels(create_label_lat(np.arange(-10, 50, 5)))

            plv3.set_pic_ticks(ax, xticks=np.arange(-10, 50, 10, dtype=int),
                               yticks=np.linspace(1000, 200, 5, dtype=int),
                               xlabels=create_label_lat(np.arange(-10, 50, 10, dtype=int)),
                               ylabels=np.linspace(1000, 200, 5, dtype=int),
                               x_minorspace=5, y_minorspace=50, labelsize=23
                               , axis_labelsize=20
                               )
            add_text(ax=ax, string="D" + str(j+start1-31), location=(0.05, 0.91), fontsize=30)


            #q = ax.quiver(f0.lat, np.linspace(200,1000,33), avg_v[start1+j], avg_omega[start1+j],
            #              angles='uv',  # regrid_shape这个参数越小，是两门就越稀疏
            #              scale_units='xy', scale=0.5,  # scale是参考矢量，所以取得越大画出来的箭头就越短
            #              units='xy', width=2.2,
            #              color='k', zorder=2)
            #print(f0.avg_omega.shape)
            #print(avg_v.shape)
            ax.streamplot(f0.lat.data, np.linspace(200,1000,33), avg_v[start1+j], avg_omega[start1+j], linewidth=3, color='k',
                          density=[1, 1.15], arrowsize=2.75, arrowstyle='->')

            plt.gca().invert_yaxis()
            plt.gca().set_facecolor("black")
            fig1.subplots_adjust(top=0.8)
            cbar_ax = fig1.add_axes([0.2, 0.05, 0.6, 0.03])
            cb = fig1.colorbar(im, cax=cbar_ax, shrink=0.1, pad=0.01, orientation='horizontal')
            cb.ax.tick_params(labelsize=20)
            j += 1

    plt.savefig("/home/sun/paint/meridional_tem_gradient_circulation/d-9tod-1.pdf", dpi=350)
    plt.show()

def main():
    #zonal_avg()
    paint_meridional_variables()


if __name__ == "__main__":
    main()