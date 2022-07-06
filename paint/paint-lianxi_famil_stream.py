'''
2021/9/22
练习绘制流场图、叠加降水
'''
import numpy as np
import xarray as xr

import matplotlib as mpl
import matplotlib.pyplot as plt

import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.io.shapereader import Reader
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

f1  =  xr.open_dataset("/data5/2019swh/data/zhuang_plev/famil_zhuang_con_prect.nc")
f2  =  xr.open_dataset("/data5/2019swh/data/zhuang_plev/plev_con_U.nc")
f3  =  xr.open_dataset("/data5/2019swh/data/zhuang_plev/plev_con_V.nc")

def set_map_ticks(ax, dx=60, dy=30, nx=0, ny=0, labelsize='medium'):
    if not isinstance(ax.projection, ccrs.PlateCarree):
        raise ValueError('Projection of ax should be PlateCarree!')
    proj = ccrs.PlateCarree()   # 专门给ticks用的crs.

    # 设置x轴.
    major_xticks = np.arange(-180, 180 + 0.9 * dx, dx)
    ax.set_xticks(major_xticks, crs=proj)
    if nx > 0:
        ddx = dx / (nx + 1)
        minor_xticks = np.arange(-180, 180 + 0.9 * ddx, ddx)
        ax.set_xticks(minor_xticks, minor=True, crs=proj)

    # 设置y轴.
    major_yticks = np.arange(-90, 90 + 0.9 * dy, dy)
    ax.set_yticks(major_yticks, crs=proj)
    if ny > 0:
        ddy = dy / (ny + 1)
        minor_yticks = np.arange(-90, 90 + 0.9 * ddy, ddy)
        ax.set_yticks(minor_yticks, minor=True, crs=proj)

    # 为tick label增添度数标识.
    ax.xaxis.set_major_formatter(LongitudeFormatter())
    ax.yaxis.set_major_formatter(LatitudeFormatter())
    ax.tick_params(labelsize=labelsize)

lonmin,lonmax,latmin,latmax = 30,120,-10,30
extent = [lonmin, lonmax, latmin, latmax]
pre =  f1.prect
u   =  f2.sel(
    lon=slice(lonmin,lonmax),
    lat=slice(latmin,latmax),
    lev=925
).U
v   =  f3.sel(
    lon=slice(lonmin,lonmax),
    lat=slice(latmin,latmax),
    lev=925
).V

proj = ccrs.PlateCarree()
fig = plt.figure()
ax = fig.add_subplot(111, projection=proj)
ax.coastlines(resolution='10m', lw=0.3)
# 设置经纬度刻度.
set_map_ticks(ax, dx=15, dy=15, nx=1, ny=1, labelsize='small')
ax.set_extent(extent, crs=proj)
