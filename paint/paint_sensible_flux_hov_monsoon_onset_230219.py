'''
2023-2-19
This script plot the hov diagram of the sensible heating over the Indian Peninsula

Departure value in abnormal years is also plotted
python paint_sensible_flux_hov_monsoon_onset_230219.py -sf_a surface_sensible_heat_flux_climatic_daily.nc -sf_e surface_sensible_heat_flux_climatic_daily_year_early.nc -sf_l surface_sensible_heat_flux_climatic_daily_year_late.nc -sn sshf -l0 20 -l1 10 -n1 daily_sensible_heating_10_20.pdf -n2 daily_sensible_heating_late_deviation_10_20.pdf
'''
import xarray as xr
import numpy as np
import argparse
import sys
from matplotlib import projections
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

sys.path.append("/home/sun/mycode/module/")
from module_sun import *

sys.path.append("/home/sun/mycode/paint/")
from paint_lunwen_version3_0_fig2b_2m_tem_wind_20220426 import save_fig

# -------------- Define a Class for input value -----------------------------
input_list  =  argparse.ArgumentParser(description='input ncfiles')
input_list.add_argument('--sensible_avg', '-sf_a', help='sensible heat flux file for climate average')
input_list.add_argument('--sensible_early', '-sf_e', help='sensible heat flux file for early onset year')
input_list.add_argument('--sensible_late',  '-sf_l', help='sensible heat flux file for late onset year')
input_list.add_argument('--sensible_v', '-sn', help='variable name of sensible flux')
input_list.add_argument('--lat0', '-l0', help='start latitude')
input_list.add_argument('--lat1', '-l1', help='end latitude')
input_list.add_argument('--figname1', '-n1', help='name of the picture1')
input_list.add_argument('--figname2', '-n2', help='name of the picture2')
input_list.add_argument('--title', '-t', help='title', default='')
args        =  input_list.parse_args()

path0       =  '/home/sun/data/ERA5_data_monsoon_onset/climatic_daily_ERA5/single/'
end_path    =  '/home/sun/paint/monsoon_onset_composite_ERA5/'
ref_file0   =  xr.open_dataset(path0 + args.sensible_avg)
mask_file   =  xr.open_dataset('/home/sun/data/mask/ERA5_land_sea_mask_1x1.nc').sel(latitude=slice(args.lat0, args.lat1))

def calculate_meridional_avg(variable):
    '''Return the meridional average, the input should be cut for the requisite lat range and has been masked'''
    for tttt in range(variable.shape[0]):
        variable[tttt][ mask_file['lsm'][0].data < 0.5] = np.nan

    return np.nanmean(variable, axis=1) # (365, longitude)

def paint_hov_sensible_climate(sensible,):
    from matplotlib import cm
    from matplotlib.colors import ListedColormap
    import matplotlib.gridspec as gridspec

    # ------------ 1. Paint Setting --------------------------------------------
    # 1.1 Colormap
    viridis = cm.get_cmap('Reds', 20)
    newcolors = viridis(np.linspace(0, 1, 20))
    newcmp = ListedColormap(newcolors)
    newcmp.set_under('white')
    #newcmp.set_over('brown')

    # 1.2 levels
    clevs = np.linspace(50, 110, 7, dtype=int)

    # 1.3 Tick labels
    # Tick labels
    x_tick_labels = []
    for xx in range(50, 131, 20):
        x_tick_labels.append(u''+str(xx)+"\N{DEGREE SIGN}E")

    # time range from 1 March to 1 Jun
    y_tick = [59, 68, 78, 90, 99, 109, 120, 129, 139, 151]
    y_label = ['1 Mar', '10 Mar', '20 Mar', '1 Apr', '10 Apr', '20 Apr', '1 May', '10 May', '20 May', '1 Jun']

    # ------------ 2. Paint ------------------------------------------------------
    fig, ax = plt.subplots(figsize=(13, 15))

    # 2.1 contours
    #print(np.nanmin(sensible / 86400 * 24))
    #print(np.nanmax(sensible / 86400 * 24))
    im1 = ax.contour(ref_file0['lon'].data, ref_file0['time'].data, -1 * sensible / 86400 * 24, clevs, colors='k', linewidths=1)

    # 2.2 Shading
    im2 = ax.contourf(ref_file0['lon'].data, ref_file0['time'].data, -1 * sensible / 86400 * 24, clevs, cmap=newcmp, extend='both')

    # 2.3 Other setting
    ax.set_xticks(np.arange(50, 131, 20))
    ax.set_xticklabels(x_tick_labels,fontsize=25)

    ax.set_yticks(y_tick)
    ax.set_yticklabels(y_label,fontsize=25)

    # 2.4 Time limitation
    ax.set_ylim((50, 160))
    ax.set_xlim((45, 135))

    # ------------- 3. Colorbar -------------------------------------------------------
    fig.subplots_adjust(top=0.8) 
    cbar_ax = fig.add_axes([0.2, 0.05, 0.6, 0.03]) 
    cb  =  fig.colorbar(im2, cax=cbar_ax, shrink=0.1, pad=0.01, orientation='horizontal')
    cb.ax.tick_params(labelsize=20)

    # ------------- 4. Save the Pic -----------------------------------------------
    save_fig(path_out=end_path, file_out=args.figname1)

def paint_hov_sensible_deviation(sensible_deviation,):
    from matplotlib import cm
    from matplotlib.colors import ListedColormap
    import matplotlib.gridspec as gridspec

    # ------------ 1. Paint Setting --------------------------------------------
    # 1.1 Colormap
    viridis = cm.get_cmap('Reds', 20)
    newcolors = viridis(np.linspace(0, 1, 20))
    newcmp = ListedColormap(newcolors)
    newcmp.set_under('white')
    #newcmp.set_over('brown')

    # 1.2 levels
    clevs = np.linspace(-15, 15, 13, dtype=int)

    # 1.3 Tick labels
    # Tick labels
    x_tick_labels = []
    for xx in range(50, 131, 20):
        x_tick_labels.append(u''+str(xx)+"\N{DEGREE SIGN}E")

    # time range from 1 March to 1 Jun
    y_tick = [59, 68, 78, 90, 99, 109, 120, 129, 139, 151]
    y_label = ['1 Mar', '10 Mar', '20 Mar', '1 Apr', '10 Apr', '20 Apr', '1 May', '10 May', '20 May', '1 Jun']

    # ------------ 2. Paint ------------------------------------------------------
    fig, ax = plt.subplots(figsize=(13, 15))

    # 2.1 contours
    #print(np.nanmin(sensible / 86400 * 24))
    #print(np.nanmax(sensible / 86400 * 24))
    im1 = ax.contour(ref_file0['lon'].data, ref_file0['time'].data, -1 * sensible_deviation / 86400 * 24, clevs, colors='k', linewidths=1)

    # 2.2 Shading
    im2 = ax.contourf(ref_file0['lon'].data, ref_file0['time'].data, -1 * sensible_deviation / 86400 * 24, clevs, cmap='coolwarm', extend='both')

    # 2.3 Other setting
    ax.set_xticks(np.arange(50, 131, 20))
    ax.set_xticklabels(x_tick_labels,fontsize=25)

    ax.set_yticks(y_tick)
    ax.set_yticklabels(y_label,fontsize=25)

    # 2.4 Time limitation
    ax.set_ylim((50, 160))
    ax.set_xlim((45, 135))

    # ------------- 3. Colorbar -------------------------------------------------------
    fig.subplots_adjust(top=0.8) 
    cbar_ax = fig.add_axes([0.2, 0.05, 0.6, 0.03]) 
    cb  =  fig.colorbar(im2, cax=cbar_ax, shrink=0.1, pad=0.01, orientation='horizontal')
    cb.ax.tick_params(labelsize=20)

    # ------------- 4. Save the Pic -----------------------------------------------
    save_fig(path_out=end_path, file_out=args.figname2)


def main():
    # ----------- 1. Calculate the meridional average ---------------------------
    sfile0  =  xr.open_dataset(path0 + args.sensible_avg).sel(lat=slice(args.lat0, args.lat1))
    sfile1  =  xr.open_dataset(path0 + args.sensible_early).sel(lat=slice(args.lat0, args.lat1))
    sfile2  =  xr.open_dataset(path0 + args.sensible_late).sel(lat=slice(args.lat0, args.lat1))

    sen_avg   =  calculate_meridional_avg(sfile0[args.sensible_v].data)
    sen_early =  calculate_meridional_avg(sfile1[args.sensible_v].data)
    sen_late  =  calculate_meridional_avg(sfile2[args.sensible_v].data)

    # ------------ 2. Paint the pic -----------------------------------------------
    paint_hov_sensible_climate(sensible=sen_avg)
    paint_hov_sensible_deviation(
        sensible_deviation=(sen_late - sen_avg)
    )
    

if __name__ == '__main__':
    main()