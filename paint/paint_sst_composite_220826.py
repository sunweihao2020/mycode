'''
2022-8-26
This code use composite sst to paint sea surface temperature
time resolution is pentad
'''
src_path  =  "/Users/sunweihao/data/composite/"

file0     =  "composite_OISST.nc"

def cal_pentad_sst():
    '''This function calculate pentad average for sea surface temperature'''
    import xarray as xr
    import numpy as np

    f0    =  xr.open_dataset(src_path + file0) #(61,720,1440)

    sst     =  f0.SST.data
    avg_sst =  np.zeros((6,720,1440))

    '''
    Here I define the -2 -1 0 1 2 as the onset pentad
    '''
    date0 =  8  # correspond to d -22

    for pp in range(6):
        start_date  =  date0 + pp*5
        end_date    =  date0 + (pp+1)*5

        avg_sst[pp]  =  np.nanmean(sst[start_date:end_date],axis=0)


    return avg_sst

def paint_pentad_sst():
    '''This function paint pentad sst'''
    import xarray as xr
    import numpy as np
    import matplotlib.pyplot as plt
    import cmasher as cmr
    import cartopy.crs as ccrs

    import sys
    sys.path.append("/Users/sunweihao/mycode/module")
    from module_sun_new import set_cartopy_tick

    # get pentad average SST
    sst   =   cal_pentad_sst()


    # reference dimension message
    f0 = xr.open_dataset(src_path + file0)

    # ---------- start paint -----------------
    # set paint range
    lonmin, lonmax, latmin, latmax = 45, 115, - 10, 30
    extent = [lonmin, lonmax, latmin, latmax]

    # set figure
    proj      =     ccrs.PlateCarree()
    fig       =     plt.figure(figsize=(34, 15))
    spec1     =     fig.add_gridspec(nrows=2, ncols=3)

    # set colormap
    cmap      =     cmr.prinsenvlag

    # set pentad label
    pentads   =     ["P-4","P-3","P-2","P-1","P0","P+1"]

    j         =     0

    for row in range(2):
        for col in range(3):
            ax  =  fig.add_subplot(spec1[row,col],projection=proj)

            # set tick and ticklabel
            set_cartopy_tick(ax=ax, extent=extent, xticks=np.linspace(50, 110, 4, dtype=int),
                             yticks=np.linspace(-10, 30, 5, dtype=int), nx=1, ny=1, labelsize=25)

            # add equatorial line
            ax.plot([40, 120], [0, 0], 'k--')

            # paint sst
            im1 = ax.contour(f0.lon, f0.lat, sst[j, :], levels = np.linspace(26, 30.5, 19), colors='k',
                             linewidths=1.5, alpha=1, zorder=1)
            im2 = ax.contourf(f0.lon, f0.lat, sst[j, :],levels=np.linspace(26, 30.5, 19), cmap='coolwarm',
                              extend='both', zorder=0)

            ax.coastlines(resolution='110m', lw=1)

            # set title
            ax.set_title(pentads[j],loc="left",fontsize=25)

            j += 1

    # add colorbar
    fig.subplots_adjust(top=0.9)
    cbar_ax = fig.add_axes([0.2, 0.05, 0.6, 0.03])
    cb = fig.colorbar(im2, cax=cbar_ax, shrink=0.1, pad=0.01, orientation='horizontal')
    cb.ax.tick_params(labelsize=25)

    plt.savefig("/Users/sunweihao/paint/circulation_based_on_composite_result/pentad_avg_sst.png",dpi=500)


def main():
    import warnings
    warnings.filterwarnings("ignore")  # close warning message

    paint_pentad_sst()


if __name__ ==  "__main__":
    main()