'''
2022-12-16
This code paint the variables in the docn input file
The main purpose is to see the characteristic of the _preddile
'''
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import matplotlib as mpl


f0  =  xr.open_dataset('/home/sun/data/model_data/input/sst_HadOIBl_bc_1x1_2000climo_c221112.nc')

def paint_ice(var_name,month):
    '''1. set Figure'''
    proj  =  ccrs.PlateCarree()
    fig,ax  =  plt.subplots(figsize=(13,10),subplot_kw=dict(projection=ccrs.PlateCarree()))

    print("max value of {} is {}".format(var_name, np.nanmax(f0[var_name].data[month])))
    print("min value of {} is {}".format(var_name, np.nanmin(f0[var_name].data[month])))

    # contourf
    im1 =  ax.contourf(f0.lon.data, f0.lat.data, f0[var_name].data[month], levels = 11, cmap='coolwarm', alpha=1, extend='both')

    # contour 
    im2 = ax.contour(f0.lon.data, f0.lat.data, f0[var_name].data[month], levels=11, colors='gray', linewidths=1.5, linestyles='--')

    # coastline
    #ax.coastlines()

    # colorbar
    a = fig.colorbar(im1,shrink=0.6, pad=0.05,orientation='horizontal')
    a.ax.tick_params(labelsize=15)

    # save figure
    plt.savefig('/home/sun/paint/b1850_exp/f2000_ensemble/diagnose_input_sstfile/sst_.pdf', dpi=500)

def main():
    paint_ice('SST_cpl', 5)

if __name__ == '__main__':
    main()