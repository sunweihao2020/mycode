'''
2023-2-19
This script plot the monthly deviation in sensible heat flux between abnormal years and climate average for March April May
'''
import xarray as xr
import numpy as np
import argparse
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import sys

sys.path.append("/home/sun/mycode/module/")
from module_sun import *

sys.path.append("/home/sun/mycode/paint/")
from paint_lunwen_version3_0_fig2b_2m_tem_wind_20220426 import set_cartopy_tick,save_fig
from paint_lunwen_version3_0_fig2a_tem_gradient_20220426 import add_text

# -------------- Define a Class for input value -----------------------------
input_list  =  argparse.ArgumentParser(description='input ncfiles')
input_list.add_argument('--sst_avg', '-sst_a', help='SST file for climate average', default='skin_temperature_climatic_daily.nc')
input_list.add_argument('--sst_early', '-sst_e', help='SST file for early onset year', default='skin_temperature_climatic_daily_year_early.nc')
input_list.add_argument('--sst_late',  '-sst_l', help='SST file for late onset year', default='skin_temperature_climatic_daily_year_late.nc')
input_list.add_argument('--figname', '-n', help='name of the picture1', default='3-5_skt_deviation.pdf')
input_list.add_argument('--title', '-t', help='title', default='')
args        =  input_list.parse_args()

# --------------- Other information ------------------------------------------
month_name  =  ['March', 'April', 'May']
clev        =  np.linspace(-1.5, 1.5, 11)

lonmin,lonmax,latmin,latmax  =  45,115,-10,30
extent     =  [lonmin,lonmax,latmin,latmax]

path0       =  '/home/sun/data/ERA5_data_monsoon_onset/climatic_daily_ERA5/single/'
end_path    =  '/home/sun/paint/monsoon_onset_composite_ERA5/'
ref_file0   =  xr.open_dataset(path0 + args.sst_avg)

# -------------- Calculate Deviation for March April May ----------------------
day_slice   =  [59, 90, 120, 150]
monthly_sst_avg  =  np.zeros((3, 181, 360))
monthly_sst_early=  monthly_sst_avg.copy()
monthly_sst_late =  monthly_sst_early.copy

sst_file1   =  xr.open_dataset(path0 + args.sst_avg)
sst_file2   =  xr.open_dataset(path0 + args.sst_early)
sst_file3   =  xr.open_dataset(path0 + args.sst_late)

#print(np.average(sst_file1['sst'].data[day_slice[0] : day_slice[1]], axis=0))
#
#for i in range(3):
#    monthly_sst_avg[i]   = np.average(sst_file1['sst'].data[day_slice[i] : day_slice[i+1]], axis=0)
#    monthly_sst_early[i] = np.average(sst_file2['sst'].data[day_slice[i] : day_slice[i+1]], axis=0)
#    monthly_sst_late[i]  = np.average(sst_file3['sst'].data[day_slice[i] : day_slice[i+1]], axis=0)

#deviation_early = monthly_sst_early - monthly_sst_avg
#print(deviation_early.shape)
#deviation_late = monthly_sst_late - monthly_sst_avg

# --------------- paint the Pic -------------------------------------------------
# 1. Set the figure
proj    =  ccrs.PlateCarree()
fig1    =  plt.figure(figsize=(36, 17))
spec1   =  fig1.add_gridspec(nrows=2, ncols=3)

# 2. Set the color map
cmap  =  create_ncl_colormap("/home/sun/data/color_rgb/MPL_coolwarm.txt",22)

# 3. First row plot the deviation in Early years
j = 0
for i in range(3):
    deviation = np.average(sst_file2['skt'].data[day_slice[i] : day_slice[i+1]], axis=0) - ( np.average(sst_file1['skt'].data[day_slice[i] : day_slice[i+1]], axis=0))
    ax = fig1.add_subplot(spec1[0, j], projection=proj)

    # Set ticks
    set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(50,110,4,dtype=int),yticks=np.linspace(-10,30,5,dtype=int),nx=1,ny=1,labelsize=25)

    # Equator Line
    ax.plot([40,120],[0,0],'k--')

    # Contour
    im1  =  ax.contour(ref_file0['lon'].data, ref_file0['lat'].data, deviation, levels=clev, colors='black', linewidths=1.5, alpha=1, zorder=1)
    # Contourf
    im2  =  ax.contourf(ref_file0['lon'].data, ref_file0['lat'].data, deviation, levels=clev, cmap=cmap, extend='both', zorder=0)

    # Coast Line
    ax.coastlines(resolution='110m',lw=1)

    # Add month name
    ax.set_title(month_name[j], loc='right', fontsize=25)

    j += 1

# 4. Second row plot the deviation in Late years
j = 0
for i in range(3):
    deviation = np.average(sst_file3['skt'].data[day_slice[i] : day_slice[i+1]], axis=0) - ( np.average(sst_file1['skt'].data[day_slice[i] : day_slice[i+1]], axis=0))
    ax = fig1.add_subplot(spec1[1, j], projection=proj)

    # Set ticks
    set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(50,110,4,dtype=int),yticks=np.linspace(-10,30,5,dtype=int),nx=1,ny=1,labelsize=25)

    # Equator Line
    ax.plot([40,120],[0,0],'k--')

    # Contour
    im1  =  ax.contour(ref_file0['lon'].data, ref_file0['lat'].data, deviation, levels=clev, colors='black', linewidths=1.5, alpha=1, zorder=1)
    # Contourf
    im2  =  ax.contourf(ref_file0['lon'].data, ref_file0['lat'].data, deviation, levels=clev, cmap=cmap, extend='both', zorder=0)

    # Coast Line
    ax.coastlines(resolution='110m',lw=1)

    # Add month name
    ax.set_title(month_name[j], loc='right', fontsize=25)

    j += 1

# Add colorbar
fig1.subplots_adjust(top=0.8) 
cbar_ax = fig1.add_axes([0.2, 0.05, 0.6, 0.03]) 
cb  =  fig1.colorbar(im2, cax=cbar_ax, shrink=0.1, pad=0.01, orientation='horizontal')
cb.ax.tick_params(labelsize=25)

save_fig(path_out=end_path, file_out=args.figname)