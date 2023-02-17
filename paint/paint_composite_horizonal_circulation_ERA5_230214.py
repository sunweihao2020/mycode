'''
2023-2-13
This script plot the horizonal circulation at selected level

python paint_composite_horizonal_circulation_ERA5_230214.py -uf u_component_of_wind_composite.nc -vf v_component_of_wind_composite.nc -un u -vn v -pf tp_composite.nc -pn tp -l 925 -n composite_925_streamline_prect.pdf
'''
import xarray as xr
import argparse
from matplotlib import projections
import xarray as xr
import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import sys

sys.path.append("/home/sun/mycode/module/")
from module_sun import *

sys.path.append("/home/sun/mycode/paint/")
from paint_lunwen_version3_0_fig2b_2m_tem_wind_20220426 import set_cartopy_tick,save_fig

# -------------- Define a Class for input value -----------------------------
input_list  =  argparse.ArgumentParser(description='input ncfiles')
input_list.add_argument('--ufile', '-uf', help='input file (absolute path)')
input_list.add_argument('--vfile', '-vf', help='input file (absolute path)')
input_list.add_argument('--uname', '-un', help='variable name for ufile')
input_list.add_argument('--vname', '-vn', help='variable name for vfile')
input_list.add_argument('--precipitation', '-pf', help='precipitation file')
input_list.add_argument('--precipitation_v', '-pn', help='variable name for pfile')
input_list.add_argument('--level', '-l', help='level for sel')
input_list.add_argument('--figname', '-n', help='name of the picture')
input_list.add_argument('--title', '-t', help='title', default=[])
args        =  input_list.parse_args()

# -------------- Read the datasets ------------------------------------------
path0    =  '/home/sun/data/ERA5_data_monsoon_onset/composite_ERA5/'
path1    =  '/home/sun/data/ERA5_data_monsoon_onset/composite_ERA5/single/'

select_time  =  [-6, -2, 0, 2]
number   =  ["a","b","c","d"]
file_u   =  xr.open_dataset(path0 + args.ufile).sel(lev=args.level, time=select_time)
file_v   =  xr.open_dataset(path0 + args.vfile).sel(lev=args.level, time=select_time)
file_p   =  xr.open_dataset(path0 + 'single/' +args.precipitation).sel(time = select_time)
#file_in  =  xr.open_dataset(path0 + 'temperature_composite_abnormal.nc')

# -------------- Paint the Pic -----------------------------------------------
def paint_pic(extent, lat, lon, prect, u, v, paint_name):
    # 设置画布
    proj    =  ccrs.PlateCarree()
    fig1    =  plt.figure(figsize=(26,17))
    spec1   =  fig1.add_gridspec(nrows=2,ncols=2)

    j  =  0
    for col in range(2):
        for row in range(2):
            ax = fig1.add_subplot(spec1[row,col],projection=proj)

            # 设置刻度
            set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(50,110,4,dtype=int),yticks=np.linspace(-10,30,5,dtype=int),nx=1,ny=1,labelsize=25)

            # 赤道线
            ax.plot([40,120],[0,0],'k--')

            # 等值线
            im2  =  ax.contourf(lon, lat, prect[j, :] * 1000 * 24, levels=np.arange(3, 28, 3), cmap='Blues', extend='both', zorder=0)

            # 海岸线
            ax.coastlines(resolution='110m',lw=1)

            # 流线
            q   =   ax.streamplot(lon, lat, u[j, :], v[j, :], linewidth=3, color = 'k',density=[1.25, 1.15], arrowsize=2.75, arrowstyle='->')

            # 加日期
            if select_time[j]<0:
                ax.set_title("D"+str(select_time[j]),loc='right',fontsize=27.5)
            elif select_time[j]>0:
                ax.set_title("D+"+str(select_time[j]),loc='right',fontsize=27.5)
            else:
                ax.set_title("D"+str(select_time[j]),loc='right',fontsize=27.5)
            
            # 加图序号
            ax.set_title("("+number[j]+")",loc='left',fontsize=27.5)

            # Average, early or late
            ax.set_title(args.title, fontsize=27.5)
        
            j += 1

    # 加colorbar
    fig1.subplots_adjust(top=0.8) 
    cbar_ax = fig1.add_axes([0.2, 0.05, 0.6, 0.03]) 
    cb  =  fig1.colorbar(im2, cax=cbar_ax, shrink=0.1, pad=0.01, orientation='horizontal')
    cb.ax.tick_params(labelsize=25)

    # 保存图片
    #plt.tight_layout()
    save_fig(path_out="/home/sun/paint/monsoon_onset_composite_ERA5/",file_out=paint_name)


def main():
    lonmin,lonmax,latmin,latmax  =  45,115,-10,30
    extent     =  [lonmin,lonmax,latmin,latmax]

    print('hello')
    paint_pic(extent=extent, lat=file_u['lat'].data, lon=file_u['lon'].data, prect=file_p['tp'], u=file_u[args.uname], v=file_v[args.vname], paint_name=args.figname)

if __name__ == "__main__":
    main()