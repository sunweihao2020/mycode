''''
2022-7-24
This script is new module sun py files
Purpose is to solve some problems in the module_sun.py
'''
def cal_xydistance(lat,lon):
    '''Use lat and lon to calculate distence message'''
    # ---import---
    import numpy as np
    from geopy.distance import distance

    disy = np.array([])
    disx = np.array([])
    for i in range(0, (lat.shape[0]-1)):
        disy = np.append(disy, distance((lat[i], 0), (lat[i + 1], 0)).m)

    for i in range(0, lat.shape[0]):
        disx = np.append(disx, distance((lat[i], lon[0]), (lat[i], lon[1])).m)

    location = np.array([0])
    for dddd in range(0, (lat.shape[0]-1)):
        location = np.append(location, np.sum(disy[:dddd + 1]))

    return disy,disx,location

def set_cartopy_tick(ax, extent, xticks, yticks, nx=0, ny=0,
    xformatter=None, yformatter=None,labelsize=20):
    import matplotlib.ticker as mticker
    from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
    import cartopy.crs as ccrs
    # 本函数设置地图上的刻度 + 地图的范围
    proj = ccrs.PlateCarree()
    ax.set_xticks(xticks, crs=proj)
    ax.set_yticks(yticks, crs=proj)
    # 设置次刻度.
    xlocator = mticker.AutoMinorLocator(nx + 1)
    ylocator = mticker.AutoMinorLocator(ny + 1)
    ax.xaxis.set_minor_locator(xlocator)
    ax.yaxis.set_minor_locator(ylocator)

    # 设置Formatter.
    if xformatter is None:
        xformatter = LongitudeFormatter()
    if yformatter is None:
        yformatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(xformatter)
    ax.yaxis.set_major_formatter(yformatter)

    # 设置axi label_size，这里默认为两个轴
    ax.tick_params(axis='both',labelsize=labelsize)

    # 在最后调用set_extent,防止刻度拓宽显示范围.
    if extent is None:
        ax.set_global()
    else:
        ax.set_extent(extent, crs=proj)

def generate_xlabel(array):
    '''This code generate labels for x axis'''
    labels = []
    for i in array:
        if i<0:
            labels.append(str(abs(i))+"S")
        elif i>0:
            labels.append(str(i)+"N")
        else:
            labels.append("EQ")
    return labels

def add_text(ax,string,props=dict(boxstyle='square', edgecolor='white', facecolor='white', alpha=1),location=(0.05,0.9),fontsize=15):
    
    ax.text(location[0],location[1],string,transform=ax.transAxes,bbox=props,fontsize=fontsize,zorder=5)