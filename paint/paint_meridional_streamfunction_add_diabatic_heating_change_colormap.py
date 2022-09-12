'''
2022-9-12
This code is to paint meridional streamfunction add diabatic heating
zonal range is 90 to 100
Dr Wu say my color map is bad, this script is in order to change colormap
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
            print(j)
            ax  =  fig.add_subplot(spec[row,col])

            # set axis ticks and label
            ax.set_xticks(np.linspace(-10, 40, 11, dtype=int))
            ax.set_yticks(np.linspace(1000, 100, 10))

            ax.set_xticklabels(generate_xlabel(np.linspace(-10, 40, 11, dtype=int)))
            ax.tick_params(axis='both', labelsize=22.5)

            # set axis limit
            ax.set_xlim((-10, 40))

            # plot streamfunction contourf
            cf  =  ax.contourf(file1.lat.data ,file1.lev.data ,file1.meridional_streamfunction.data[dates[j]+30]/1e11, levels = np.linspace(-3,3,13),cmap=cmap,extend='both')

            # add zeros line for streamfunction
            cr  =  ax.contour(file1.lat.data ,file1.lev.data ,file1.meridional_streamfunction.data[dates[j]+30]/1e11, levels = [0], colors = "darkgray", linestyles = "--", linewidths = 4)

            # add diabatic heating contour
            cr1 =  ax.contour(file0.lat.data ,file0.level.data ,latent[dates[j]+30], levels = np.linspace(2,10,5), colors = "blue", linewidths = 3)
            cr2 =  ax.contour(file0.lat.data ,file0.level.data ,sensible[dates[j]+30], levels = np.linspace(2,10,5), colors = "red", linewidths = 3)

            # clabel
            ax.clabel(cr1, fontsize=20)
            ax.clabel(cr2, fontsize=20)

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

            # add colorbar
            fig.subplots_adjust(top=0.9)
            cbar_ax = fig.add_axes([0.2, 0.05, 0.6, 0.03])
            cb = fig.colorbar(cf, cax=cbar_ax, shrink=0.1, pad=0.01, orientation='horizontal')
            cb.ax.tick_params(labelsize=25)

            j += 1

    plt.savefig("/Users/sunweihao/paint/circulation_based_on_composite_result/meridional_streamfunction_diabatic_heating_90to100E.png",dpi=500)
    plt.show()

def paint_zonal_field():
    '''This'''
    import xarray as xr
    import numpy as np
    import matplotlib.pyplot as plt
    import cmasher as cmr

    import sys
    sys.path.append("/Users/sunweihao/mycode/module")
    from module_sun_new import generate_xlabel

    # set meridional range for diabatic heating
    lat_slice  =  slice(10,20)

    file0 = xr.open_dataset(src_path + f0).sel(lat=lat_slice)
    file1 = xr.open_dataset(src_path + f1)

    topo_file = xr.open_dataset("/Users/sunweihao/data/topography/bathymetric.nc").sel(lat=lat_slice)
    topo = np.average(topo_file.elevation, axis=0)

    latent = np.nanmean(file0.moist, axis=2)
    sensible = np.nanmean(file0.turbulence, axis=2)

    # ----------Now paint---------------------
    # set dates
    dates = [-30, -20, -10, -5, -3, -1, 0, 2, 4]

    # set figure
    fig = plt.figure(figsize=(34, 30))
    spec = fig.add_gridspec(nrows=3, ncols=3)

    # set cmap
    cmap = cmr.waterlily

    j = 0

    for col in range(3):
        for row in range(3):
            print(j)
            ax  =  fig.add_subplot(spec[row,col])

            # set axis ticks and label
            ax.set_xticks(np.linspace(50, 120, 8, dtype=int))
            ax.set_yticks(np.linspace(1000, 100, 10))

            ax.set_xticklabels(generate_xlabel_lon(np.linspace(50, 120, 8, dtype=int)))
            ax.tick_params(axis='both', labelsize=22.5)

            # set axis limit
            ax.set_xlim((50, 120))

            # plot streamfunction contourf
            cf  =  ax.contourf(file1.lon.data ,file1.lev.data ,file1.zonal_streamfunction.data[dates[j]+30]/1e11, levels = np.linspace(-4,4,17),cmap=cmap,extend='both')

            # add zeros line for streamfunction
            cr  =  ax.contour(file1.lon.data ,file1.lev.data ,file1.zonal_streamfunction.data[dates[j]+30]/1e11, levels = [0], colors = "darkgray", linestyles = "--", linewidths = 4)

            # add diabatic heating contour
            cr1 =  ax.contour(file0.lon.data ,file0.level.data ,latent[dates[j]+30], levels = np.linspace(2,10,5), colors = "blue", linewidths = 3)
            cr2 =  ax.contour(file0.lon.data ,file0.level.data ,sensible[dates[j]+30], levels = np.linspace(2,10,5), colors = "red", linewidths = 3)

            # clabel
            ax.clabel(cr1, fontsize=20)
            ax.clabel(cr2, fontsize=20)

            # set title
            ax.set_title("D"+str(dates[j]),loc="left",fontsize = 25)
            # add topography
            ax2  =  ax.twinx()
            ax2.set_ylim((0, 11))

            ax2.set_yticks([])
            ax2.tick_params(axis='both', labelsize=20.5)

            ax2.plot(topo_file.lon.data, topo / 1000, color='k')
            ax2.fill_between(topo_file.lon.data, 0, topo / 1000, where=topo > 0, color='k')

            ax.invert_yaxis()

            # add colorbar
            fig.subplots_adjust(top=0.9)
            cbar_ax = fig.add_axes([0.2, 0.05, 0.6, 0.03])
            cb = fig.colorbar(cf, cax=cbar_ax, shrink=0.1, pad=0.01, orientation='horizontal')
            cb.ax.tick_params(labelsize=25)

            j += 1

    plt.savefig("/Users/sunweihao/paint/circulation_based_on_composite_result/zonal_streamfunction_diabatic_heating_10to20E.png",dpi=500)


def generate_xlabel_lon(array):
    '''This code generate labels for x axis'''
    labels = []
    for i in array:
        labels.append(str(abs(i))+"E")

    return labels

def main():
    import warnings
    warnings.filterwarnings("ignore")  # close warning message
    paint_zonal_field()
    paint_meridional_field()

if __name__ == "__main__":
    main()