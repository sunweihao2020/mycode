'''
2021/9/29
本代码绘制famil实验中四月份的daily环流叠加降水图
多层次
'''
import os
import sys
import xarray as xr
import numpy as np
module_path = ["/home/sun/mycode/module/","/data5/2019swh/mycode/module/"]
sys.path.append(module_path[0])
from module_sun import *
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
from metpy.units import units
from matplotlib.path import Path
import matplotlib.patches as patches

path  =  "/home/sun/qomo-data/zhuang_plev/"
file  =  ["plev_con_U.nc","plev_con_V.nc"]
exp   =  ["ic","id"]

'''设置绘图区域'''
lonmin,lonmax,latmin,latmax  =  30,120,-10,30
extent     =  [lonmin,lonmax,latmin,latmax]
tmin,tmax  =  120,150 
#level      =  925
levels     =  [925,850,700,500,200]
dens       =  [2,1.5,1.5,1.25,1]

#绘制长方形
verts = [[(90., 8.),(110.,8.), (110.,21.),(90., 21.),(0., 0.),],[(67., 4.),(90.,4.), (90.,25.),(67., 25.),(0., 0.),]]

codes = [Path.MOVETO,Path.LINETO,Path.LINETO,Path.LINETO,Path.CLOSEPOLY,]

#path_m     =  Path(verts,codes)

dates1   =  []
for dd in range(0,15):
    dates1.append("5-"+str(dd+1))
dates2   =  []
for dd in range(15,30):
    dates2.append("5-"+str(dd+1))
props = dict(boxstyle='Round', facecolor='white', alpha=1)

ll = 0
for level in levels:
    for name in exp:
        f0    =  xr.open_dataset(path+"plev_"+name+"_U.nc").sel(lon=slice(lonmin,lonmax),lat=slice(latmin,latmax),time=slice(tmin,tmax),lev=level)
        f1    =  xr.open_dataset(path+"plev_"+name+"_V.nc").sel(lon=slice(lonmin,lonmax),lat=slice(latmin,latmax),time=slice(tmin,tmax),lev=level)
        prect =  xr.open_dataset(path+"famil_zhuang_"+name+"_prect.nc").sel(lon=slice(lonmin,lonmax),lat=slice(latmin,latmax),time=slice(tmin,tmax))

        proj    =  ccrs.PlateCarree()
        fig1    =  plt.figure(figsize=(36,10))
        spec1   =  fig1.add_gridspec(nrows=3,ncols=5)
        if name == "ic":
            path_m  =  Path(verts[0],codes)
        elif name == "id":
            path_m  =  Path(verts[1],codes)


        j  =  0 ; middle = 15

        for row in range(3):
            for col in range(5):
                ax = fig1.add_subplot(spec1[row,col],projection=proj)
                ax.coastlines(resolution='110m',lw=1)
                # 设置经纬度刻度.
                set_map_ticks(ax, dx=10, dy=10, nx=1, ny=1, labelsize='small')
                ax.set_extent(extent, crs=proj)

                im  =  ax.contourf(prect.lon,prect.lat,prect.prect.data[j,:],levels=np.linspace(2,20,10),cmap='Blues',alpha=1,extend='both')
                ax.plot([30,120],[0,0],color='k')
                patch = patches.PathPatch(path_m, edgecolor='red', lw=2,linestyle='--',alpha=1,facecolor='None')
                ax.add_patch(patch)
                ax.streamplot(f0.lon.data, f0.lat.data, 
                              f0.U.data[j,:], f1.V.data[j,:], 
                              color='k',linewidth=2,
                             density=dens[ll])
                ax.text(0.02,0.85,dates1[j]+" "+str(level)+"hPa",transform=ax.transAxes,bbox=props,fontsize=24)

                j += 1



        plt.tight_layout()
        plt.savefig('/home/sun/paint/famil_stream_prect/may/may_'+name+"_"+str(level)+"_1.pdf", bbox_inches='tight')
        plt.show()

        fig2    =  plt.figure(figsize=(36,10))
        spec2   =  fig2.add_gridspec(nrows=3,ncols=5)

        j  =  0
        for row in range(3):
            for col in range(5):
                ax = fig2.add_subplot(spec1[row,col],projection=proj)
                ax.coastlines(resolution='110m',lw=1)
                # 设置经纬度刻度.
                set_map_ticks(ax, dx=10, dy=10, nx=1, ny=1, labelsize='small')
                ax.set_extent(extent, crs=proj)

                im  =  ax.contourf(prect.lon,prect.lat,prect.prect.data[j+middle,:],levels=np.linspace(2,20,10),cmap='Blues',alpha=1,extend='both')
                ax.plot([30,120],[0,0],color='k')
                patch = patches.PathPatch(path_m, edgecolor='red', lw=2,linestyle='--',alpha=1,facecolor='None')
                ax.add_patch(patch)
                ax.streamplot(f0.lon.data, f0.lat.data, 
                            f0.U.data[middle+j,:], f1.V.data[middle+j,:], 
                            color='k',linewidth=2,
                            density=dens[ll])
                ax.text(0.02,0.85,dates2[j]+" "+str(level)+"hPa",transform=ax.transAxes,bbox=props,fontsize=24)

                j += 1

        plt.tight_layout()
        plt.savefig('/home/sun/paint/famil_stream_prect/may/may_'+name+"_"+str(level)+"_2.pdf", bbox_inches='tight')
        plt.show()

    f0    =  xr.open_dataset(path+"plev_con_U.nc").sel(lon=slice(lonmin,lonmax),lat=slice(latmin,latmax),time=slice(tmin,tmax),lev=level)
    f1    =  xr.open_dataset(path+"plev_con_V.nc").sel(lon=slice(lonmin,lonmax),lat=slice(latmin,latmax),time=slice(tmin,tmax),lev=level)
    prect =  xr.open_dataset(path+"famil_zhuang_con_prect.nc").sel(lon=slice(lonmin,lonmax),lat=slice(latmin,latmax),time=slice(tmin,tmax))
    proj    =  ccrs.PlateCarree()

    fig1    =  plt.figure(figsize=(36,10))
    spec1   =  fig1.add_gridspec(nrows=3,ncols=5)   
    j  =  0 ; middle = 15

    for row in range(3):
        for col in range(5):
            ax = fig1.add_subplot(spec1[row,col],projection=proj)
            ax.coastlines(resolution='110m',lw=1)
            # 设置经纬度刻度.
            set_map_ticks(ax, dx=10, dy=10, nx=1, ny=1, labelsize='small')
            ax.set_extent(extent, crs=proj)

            im  =  ax.contourf(prect.lon,prect.lat,prect.prect.data[j,:],levels=np.linspace(2,20,10),cmap='Blues',alpha=1,extend='both')
            ax.plot([30,120],[0,0],color='k')
            ax.streamplot(f0.lon.data, f0.lat.data, 
                          f0.U.data[j,:], f1.V.data[j,:], 
                          color='k',linewidth=2,
                         density=dens[ll],arrowstyle='-|>')
            ax.text(0.02,0.85,dates1[j]+" "+str(level)+"hPa",transform=ax.transAxes,bbox=props,fontsize=24)

            j += 1

    plt.tight_layout()
    plt.savefig("/home/sun/paint/famil_stream_prect/may/may_con_"+str(level)+"_1.pdf", bbox_inches='tight')
    plt.show()

    fig2    =  plt.figure(figsize=(36,10))
    spec2   =  fig2.add_gridspec(nrows=3,ncols=5)
    j  =  0

    for row in range(3):
        for col in range(5):
            ax = fig2.add_subplot(spec1[row,col],projection=proj)
            ax.coastlines(resolution='110m',lw=1)
            # 设置经纬度刻度.
            set_map_ticks(ax, dx=10, dy=10, nx=1, ny=1, labelsize='small')
            ax.set_extent(extent, crs=proj)

            im  =  ax.contourf(prect.lon,prect.lat,prect.prect.data[j+middle,:],levels=np.linspace(2,20,10),cmap='Blues',alpha=1,extend='both')
            ax.plot([30,120],[0,0],color='k')
            ax.streamplot(f0.lon.data, f0.lat.data, 
                        f0.U.data[middle+j,:], f1.V.data[middle+j,:], 
                        color='k',linewidth=2,
                        density=dens[ll],arrowstyle='-|>')
            ax.text(0.02,0.85,dates2[j]+" "+str(level)+"hPa",transform=ax.transAxes,bbox=props,fontsize=24)

            j += 1
    plt.tight_layout()
    plt.savefig("/home/sun/paint/famil_stream_prect/may/may_con_"+str(level)+"_2.pdf", bbox_inches='tight')
    plt.show()

    f0    =  xr.open_dataset(path+"plev_icid_U.nc").sel(lon=slice(lonmin,lonmax),lat=slice(latmin,latmax),time=slice(tmin,tmax),lev=level)
    f1    =  xr.open_dataset(path+"plev_icid_V.nc").sel(lon=slice(lonmin,lonmax),lat=slice(latmin,latmax),time=slice(tmin,tmax),lev=level)
    prect =  xr.open_dataset(path+"famil_zhuang_con_prect.nc").sel(lon=slice(lonmin,lonmax),lat=slice(latmin,latmax),time=slice(tmin,tmax))
    proj    =  ccrs.PlateCarree()
    fig1    =  plt.figure(figsize=(36,10))
    spec1   =  fig1.add_gridspec(nrows=3,ncols=5)   
    j  =  0 ; middle = 15

    for row in range(3):
        for col in range(5):
            ax = fig1.add_subplot(spec1[row,col],projection=proj)
            ax.coastlines(resolution='110m',lw=1)
            # 设置经纬度刻度.
            set_map_ticks(ax, dx=10, dy=10, nx=1, ny=1, labelsize='small')
            ax.set_extent(extent, crs=proj)
            im  =  ax.contourf(prect.lon,prect.lat,prect.prect.data[j,:],levels=np.linspace(2,20,10),cmap='Blues',alpha=1,extend='both')
            patch = patches.PathPatch(Path(verts[0],codes),edgecolor='red', lw=2,linestyle='--',alpha=1,facecolor='None')
            ax.add_patch(patch)
            patch = patches.PathPatch(Path(verts[1],codes),edgecolor='red', lw=2,linestyle='--',alpha=1,facecolor='None')
            ax.add_patch(patch) 
            ax.plot([30,120],[0,0],color='k')
            ax.streamplot(f0.lon.data, f0.lat.data, 
                          f0.U.data[j,:], f1.V.data[j,:], 
                          color='k',linewidth=2,
                         density=dens[ll],arrowstyle='-|>')
            ax.text(0.02,0.85,dates1[j]+" "+str(level)+"hPa",transform=ax.transAxes,bbox=props,fontsize=24)

            j += 1

    plt.tight_layout()
    plt.savefig("/home/sun/paint/famil_stream_prect/may/may_icid_"+str(level)+"_1.pdf", bbox_inches='tight')
    plt.show()

    fig2    =  plt.figure(figsize=(36,10))
    spec2   =  fig2.add_gridspec(nrows=3,ncols=5)
    j  =  0
    for row in range(3):
        for col in range(5):
            ax = fig2.add_subplot(spec1[row,col],projection=proj)
            ax.coastlines(resolution='110m',lw=1)
            # 设置经纬度刻度.
            set_map_ticks(ax, dx=10, dy=10, nx=1, ny=1, labelsize='small')
            ax.set_extent(extent, crs=proj)
            im  =  ax.contourf(prect.lon,prect.lat,prect.prect.data[j+middle,:],levels=np.linspace(2,20,10),cmap='Blues',alpha=1,extend='both')
            patch = patches.PathPatch(Path(verts[0],codes),edgecolor='red', lw=2,linestyle='--',alpha=1,facecolor='None')
            ax.add_patch(patch)
            patch = patches.PathPatch(Path(verts[1],codes),edgecolor='red', lw=2,linestyle='--',alpha=1,facecolor='None')
            ax.add_patch(patch) 
            ax.plot([30,120],[0,0],color='k')
            ax.streamplot(f0.lon.data, f0.lat.data, 
                        f0.U.data[middle+j,:], f1.V.data[middle+j,:], 
                        color='k',linewidth=2,
                        density=dens[ll],arrowstyle='-|>')
            ax.text(0.02,0.85,dates2[j]+" "+str(level)+"hPa",transform=ax.transAxes,bbox=props,fontsize=24)

            j += 1

    plt.tight_layout()
    plt.savefig("/home/sun/paint/famil_stream_prect/may/may_icid_"+str(level)+"_2.pdf", bbox_inches='tight')
    plt.show()

    ll += 1