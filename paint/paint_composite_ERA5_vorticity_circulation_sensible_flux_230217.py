'''
2023-2-17
This script was to see whether the process of low-level circulation transition in abnormal years is similar to the climate average

python paint_composite_ERA5_vorticity_circulation_sensible_flux_230217.py -uf u_component_of_wind_composite.nc -vf v_component_of_wind_composite.nc -un u -vn v -sf sshf_composite.nc -sn sshf -l 925 -n climate_925wind_vorticity_sshf.pdf -t Climate_Average
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
from paint_lunwen_version3_0_fig2b_2m_tem_wind_20220426 import set_cartopy_tick,save_fig,add_vector_legend

# -------------- Define a Class for input value -----------------------------
input_list  =  argparse.ArgumentParser(description='input ncfiles')
input_list.add_argument('--ufile', '-uf', help='input file (absolute path)')
input_list.add_argument('--vfile', '-vf', help='input file (absolute path)')
input_list.add_argument('--uname', '-un', help='variable name for ufile')
input_list.add_argument('--vname', '-vn', help='variable name for vfile')
input_list.add_argument('--sensiblefile', '-sf', help='sensible heat flux file')
input_list.add_argument('--sensible_v', '-sn', help='variable name of sensible flux')
input_list.add_argument('--level', '-l', help='level for sel')
input_list.add_argument('--figname', '-n', help='name of the picture')
input_list.add_argument('--title', '-t', help='title', default='')
args        =  input_list.parse_args()

ref_file0  =  xr.open_dataset('/home/sun/data/ERA5_data_monsoon_onset/composite_ERA5/single/sst_composite.nc')
mask_file  =  xr.open_dataset('/home/sun/data/mask/ERA5_land_sea_mask_1x1.nc')

path0      =  '/home/sun/data/ERA5_data_monsoon_onset/composite_ERA5/'
path1      =  '/home/sun/data/ERA5_data_monsoon_onset/composite_ERA5/single/'

select_time = [-6, -4, -2, 0]
number =  ["a","b","c","d"]

# --------------- Create geo-distance information ----------------------------
disy, disx, location = cal_xydistance(ref_file0['lat'].data[::-1], ref_file0['lon'].data)

# --------------- Calculate the vorticity for the input data -----------------
def calculate_vorticity(u, v):
    '''
    This function calculate the vorticity for the ERA5 data, notice that the latitude if 90 to -90
    The input variable should be 2d dimension
    '''
    u_reverse  =  u[::-1, :] ; v_reverse  =  v[::-1, :]

    uy = np.gradient(u_reverse, location, axis=0)
    vx = uy.copy()
    for i in range(1, uy.shape[0]):
        vx[i, :] = np.gradient(v_reverse[i, :], disx[i], axis=0)

    vorticity  =  vx - uy

    return vorticity[::-1, :] # Return to the ERA5 latitude

# ---------------- Mask the value on the land -----------------------------------
def land_sea_mask(var, mask):
    '''This function mask the variable on the land'''
    var[ mask[0] > 0.5] = np.nan

    return var

# ---------------- Paint the Pic - vorticity, wind, sensible_flux ----------------
def paint_composite_vorticity_wind_sensible(lat, lon, extent):
    # ---------- 1. Data Preparation ---------------------
    # 1.1 Read u and v wind data
    u_file = xr.open_dataset(path0 + args.ufile).sel(lev=args.level, time=select_time)
    v_file = xr.open_dataset(path0 + args.vfile).sel(lev=args.level, time=select_time)

    # 1.2 Calculate vorticity
    vorticity = u_file[args.uname].data.copy()
    for tttt in range(len(select_time)):
        vorticity[tttt] = calculate_vorticity(u_file[args.uname].data[tttt], v_file[args.vname].data[tttt])

    # 1.3 Read sensible heat flux data
    sshf = xr.open_dataset(path1 + args.sensiblefile).sel(time=select_time)

    # 1.4 Mask the land value
    u_mask = u_file[args.uname].data.copy() ; v_mask = v_file[args.vname].data.copy()
    sshf_mask = sshf[args.sensible_v].data.copy()
    for tttt in range(len(select_time)):
        u_mask[tttt][ mask_file.lsm.data[0] > 0.4] = np.nan
        v_mask[tttt][ mask_file.lsm.data[0] > 0.4] = np.nan
        sshf_mask[tttt][ mask_file.lsm.data[0] > 0.4] = np.nan
        vorticity[tttt][ mask_file.lsm.data[0] > 0.4] = np.nan

    # ------------ 2. Paint the Pic --------------------------
    from matplotlib import cm
    from matplotlib.colors import ListedColormap

    # 2.1 Set the colormap
    viridis = cm.get_cmap('Reds', 22)
    newcolors = viridis(np.linspace(0, 1, 22))
    newcmp = ListedColormap(newcolors)
    newcmp.set_under('white')
    newcmp.set_over('#660036')

    # 2.2 Set the figure
    proj    =  ccrs.PlateCarree()
    fig1    =  plt.figure(figsize=(26,17))
    spec1   =  fig1.add_gridspec(nrows=2,ncols=2)

    j = 0
    # 2.3 Plot
    for col in range(2):
        for row in range(2):
            ax = fig1.add_subplot(spec1[row, col], projection=proj)

            # Tick setting
            set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(50,110,4,dtype=int),yticks=np.linspace(-10,30,5,dtype=int),nx=1,ny=1,labelsize=25)

            # Equator line
            ax.plot([40,120],[0,0],'k--')

            # Shading for sshf
            im1  =  ax.contourf(lon, lat, -1 * sshf_mask[j] / 86400 * 24, np.linspace(10,24,15), cmap=newcmp, alpha=1, extend='both')

            # Contours for vorticity
            im2  =  ax.contour(lon, lat, 1e6 * (vorticity[j]), np.linspace(-10,10,6), colors='#4040ff', linewidths=2)
            im3  =  ax.contour(lon, lat, 1e6 * (vorticity[j]), [0], colors='#3636ff', linewidths=3)

            # Coast Line
            ax.coastlines(resolution='110m', lw=2)

            # Vector Map
            q  =  ax.quiver(lon, lat, u_mask[j], v_mask[j], 
                regrid_shape=15, angles='uv',   # regrid_shape这个参数越小，是两门就越稀疏
                scale_units='xy', scale=1.1,        # scale是参考矢量，所以取得越大画出来的箭头就越短
                units='xy', width=0.25,
                transform=proj,
                color='k',linewidth=1.2,headlength = 5, headaxislength = 4, headwidth = 5,alpha=0.8)

            # Add title of day
            if select_time[j] < 0:
                ax.set_title("D"+str(select_time[j]), loc='right', fontsize=27.5)
            elif select_time[j] > 0:
                ax.set_title("D+"+str(select_time[j]), loc='right',fontsize=27.5)
            else:
                ax.set_title("D"+str(select_time[j]),loc='right',fontsize=27.5)
            
            # Add the Figure number
            ax.set_title("("+number[j]+")",loc='left',fontsize=27.5)

            # Add middle title
            ax.set_title(args.title, fontsize=27.5)

            # Add legend of the vector
            add_vector_legend(ax=ax,q=q, speed=5)

            j+=1

    # Add Colorbar
    fig1.subplots_adjust(top=0.8) 
    cbar_ax = fig1.add_axes([0.2, 0.05, 0.6, 0.03]) 
    cb  =  fig1.colorbar(im1, cax=cbar_ax, shrink=0.1, pad=0.01, orientation='horizontal')
    cb.ax.tick_params(labelsize=20)

    save_fig(path_out="/home/sun/paint/monsoon_onset_composite_ERA5/",file_out=args.figname)

def main():
    # Set range
    lonmin,lonmax,latmin,latmax  =  45,115,-10,30
    extent     =  [lonmin,lonmax,latmin,latmax]

    # Paint Pic
    paint_composite_vorticity_wind_sensible(lat=ref_file0['lat'].data, lon=ref_file0['lon'].data, extent=extent)


if __name__ == "__main__":
    main()   