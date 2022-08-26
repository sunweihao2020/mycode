'''
2022-8-25
This code is to paint meridional streamfunction add diabatic heating
zonal range is 90 to 100
'''
src_path  =  "/Users/sunweihao/data/composite/"

f0        =  "composite-heating-merra.nc"
f1        =  "composite_calculate_regional_streamfunction_zonal10to20_meridional_220825.nc"

def paint_meridional_field():
    import xarray as xr
    import numpy as np
    import matplotlib.pyplot as plt
    import cmasher as cmr

    import sys
    sys.path.append("/Users/sunweihao/mycode/module")
    from module_sun_new import generate_xlabel

    # calculate zonal average for the diabatic heating
    lon_slice = slice(90, 100)
    file0  =  xr.open_dataset(src_path + f0).sel(lon=lon_slice)
    file1  =  xr.open_dataset(src_path + f1)

    topo_file  =  xr.open_dataset("/Users/sunweihao/data/topography/bathymetric.nc").sel(lon=lon_slice)
    topo       =  np.average(topo_file.elevation,axis=1)



    latent    =  np.nanmean(file0.moist,axis=3)
    sensible  =  np.nanmean(file0.turbulence,axis=3)

    # ----------Now paint---------------------
    # set dates
    dates     =  [-30,-20,-10,-5,-3,-1,0,2,4]

    # set figure
    fig       =  plt.figure(figsize=(34,30))
    spec      =  fig.add_gridspec(nrows=3, ncols=3)

    # set cmap
    cmap      =  cmr.waterlily

    j         =  0

    for col in range(3):
        for row in range(3):
            ax  =  fig.add_subplot(spec[row,col])

            # set axis ticks and label
            ax.set_xticks(np.linspace(-10, 40, 11, dtype=int))
            ax.set_yticks(np.linspace(1000, 100, 10))

            ax.set_xticklabels(generate_xlabel(np.linspace(-10, 40, 11, dtype=int)))
            ax.tick_params(axis='both', labelsize=22.5)

            # set axis limit
            ax.set_xlim((-10, 40))

            # plot streamfunction contourf
            cf  =  ax.contourf(file1.lat.data ,file1.lev.data ,file1.meridional_streamfunction.data[dates[j]+30]/1e11, levels = np.linspace(-4,4,33),cmap=cmap,extend='both')

            # add zeros line for streamfunction
            cr  =  ax.contour(file1.lat.data ,file1.lev.data ,file1.meridional_streamfunction.data[dates[j]+30]/1e11, levels = [0], colors = "darkgray", linestyles = "--", linewidths = 4)

            # add diabatic heating contour
            cr1 =  ax.contour(file0.lat.data ,file0.level.data ,latent[dates[j]+30], levels = np.linspace(2,10,5), colors = "blue", linewidths = 3)
            cr2 =  ax.contour(file0.lat.data ,file0.level.data ,sensible[dates[j]+30], levels = np.linspace(2,10,5), colors = "red", linewidths = 3)

            # set title
            ax.set_title("D"+str(dates[j]),loc="left",fontsize = 25)
            # add topography
            ax2  =  ax.twinx()
            ax2.set_ylim((0, 11))

            ax2.set_yticks([])
            ax2.tick_params(axis='both', labelsize=20.5)

            ax2.plot(topo_file.lat.data, topo / 1000, color='k')
            ax2.fill_between(topo_file.lat.data, 0, topo / 1000, where=topo > 0, color='k')



            ax.invert_yaxis()
            j += 1

    plt.savefig("/Users/sunweihao/paint/circulation_based_on_composite_result/meridional_streamfunction_diabatic_heating_90to100E.png",dpi=500)
    plt.show()




def main():
    paint_meridional_field()

if __name__ == "__main__":
    main()