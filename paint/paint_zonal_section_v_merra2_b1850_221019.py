'''
2022-10-19
This code paint the zonal-pressure section for the cross-equator flow
data is from climatology merra-2 and b1850 output
latitude scope is -5 to 5
'''
import os

'''This file has been intepolated into the same resolution'''
data_path   =  '/home/sun/data/model_assessment/'
data_file   =  'low-resolution-merra2_b1850_control_wind.nc'

# function of data-processing
def average_latitude_month(lat_slice,time_slice,lon_slice,f,varname):
    '''This function calculate time average and meridional average for the xarray-file's varname '''
    import numpy as np

    f0  =  f.sel(month=time_slice,lat=lat_slice, lon=lon_slice)


    return np.nanmean(np.nanmean(f0[varname],axis=0),axis=1)

def paint_zonal_section(merra,control):
    '''This function plot the zonal section for the cross-equator'''
    import sys
    import numpy as np
    import matplotlib.pyplot as plt
    sys.path.append("/Users/sunweihao/mycode/paint")
    from cartopy.mpl.ticker import LongitudeFormatter
    import xarray as xr
    from matplotlib import cm
    from matplotlib.colors import ListedColormap
    from paint_lunwen_version3_0_fig2a_tem_gradient_20220426 import add_text

    '''reference file'''
    file = xr.open_dataset(data_path + data_file).sel(lon=slice(30,165))

    '''Figure set'''
    fig     =  plt.figure(figsize=(28,14))
    spec1   =  fig.add_gridspec(nrows=1, ncols=2)

    '''Plot Merra-2 CEF'''
    ax  =  fig.add_subplot(spec1[0,0])

    # set axis ticks and label
    ax.set_xticks(np.linspace(30,150,7))
    ax.set_yticks(np.linspace(1000,200,5))
    ax.set_xticklabels(np.linspace(30,150,7,dtype=int))
    ax.set_yticklabels(np.linspace(1000,200,5,dtype=int))
    ax.tick_params(axis='both',labelsize=22.5)

    # set range
    ax.set_xlim((30,165))
    ax.set_ylim((200,1000))

    # plot vwind
    im  =  ax.contourf(file.lon.data,file.lev.data,merra,levels = np.linspace(-10,10,21),cmap='coolwarm',extend='both')

    # title
    ax.set_title('MERRA-2', loc='left', fontsize=25)
    ax.set_title('5S~5N', loc='right', fontsize=25)

    ax.invert_yaxis()

    # fill nan value
    plt.gca().set_facecolor("black")

    '''Plot Control CEF'''
    ax = fig.add_subplot(spec1[0, 1])

    # set axis ticks and label
    ax.set_xticks(np.linspace(30, 150, 7))
    ax.set_yticks(np.linspace(1000, 200, 5))
    ax.set_xticklabels(np.linspace(30, 150, 7, dtype=int))
    ax.set_yticklabels(np.linspace(1000, 200, 5, dtype=int))
    ax.tick_params(axis='both', labelsize=25)

    # set range
    ax.set_xlim((30, 165))
    ax.set_ylim((200, 1000))

    # plot vwind
    im = ax.contourf(file.lon.data, file.lev.data, control, levels=np.linspace(-10, 10, 21), cmap='coolwarm',
                     extend='both')

    # title
    ax.set_title('CESM2',loc='left',fontsize=25)
    ax.set_title('5S~5N',loc='right',fontsize=25)

    ax.invert_yaxis()

    # fill nan value
    plt.gca().set_facecolor("black")

    fig.subplots_adjust(top=0.8)
    cbar_ax = fig.add_axes([0.2, 0.05, 0.6, 0.03])
    cb = fig.colorbar(im, cax=cbar_ax, shrink=0.1, pad=0.01, orientation='horizontal')
    cb.ax.tick_params(labelsize=25)

    plt.savefig('/home/sun/paint/b1850_exp/assessment/MERRA2_B1850_JJACEF.pdf', dpi=400)
    plt.show()

def main():
    import xarray as xr

    file  =  xr.open_dataset(data_path + data_file)
    merra_v   =  average_latitude_month(f=file,lat_slice=slice(-5,5),time_slice=slice(6,8),lon_slice=slice(30,165),varname='merra_v')
    control_v = average_latitude_month(f=file, lat_slice=slice(-5, 5), time_slice=slice(6,8),lon_slice=slice(30,165), varname='control_v')

    paint_zonal_section(merra_v,control_v)



if __name__ == '__main__':
    main()