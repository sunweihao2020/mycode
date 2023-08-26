'''孙同学的模块合集奥里给'''
import matplotlib
import matplotlib.pyplot as plt
import os
import numpy as np
from geopy.distance import distance
import numpy.ma as ma
import math
import json
import copy
import sys
from netCDF4 import Dataset
import datetime
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
from metpy.units import units
from cartopy.io.shapereader import Reader
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

'''
这里记录一些量，省去手打的麻烦
'''
month_name  =  ["Jan","Feb","Mar","April","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

def initial_mask(var,shape,mask_path):
    masked = np.load(mask_path)
    var_m = masked[var]
    var1 = ma.zeros(shape)
    for t in range(0,shape[0]):
        #var1[t,:,:,:] = ma.array(var1[t,:,:,:],mask=var_m[0,:,:,:])
        var1[t, :,:] = ma.array(var1[t, :,:], mask=var_m[:,:])
    return var1

def origin_day(y1,m1,d1,y2,m2,d2):
    date1 = datetime.datetime(y1,m1,d1)
    date2 = datetime.datetime(y2,m2,d2)
    delta = date2 - date1
    interval = delta.days
    return interval

def cal_gepstrophic_wind(h,lat,lon):
    '''此方程专杀地转风'''
    #计算f
    sinlat = np.array([])
    for ll in lat:
        sinlat = np.append(sinlat,math.sin(math.radians(ll)))
    omega = 7.29e-5
    f  =  2*omega*sinlat

    disy = np.array([])
    disx = np.array([])
    for i in range(0,len(lat)-1):
        disy = np.append(disy,distance((lat[i],0),(lat[i+1],0)).m)

    for i in range(0,180):
        disx = np.append(disx, distance((lat[i], lon[0]), (lat[i], lon[1])).m)

    location = np.array([0])
    for dddd in range(0,len(lat)-1):
        location = np.append(location,np.sum(disy[:dddd+1]))

    ug = np.zeros((61,42,181,288))
    ug = ma.array(h,mask=h.mask)
    vg = copy.deepcopy(ug)

    for t in range(0,h.shape[0]):
        for lev in range(0,h.shape[1]):
            ug[t,lev,:,:] = -1*np.gradient(h[t,lev,:,:],location,axis=0)
            for latt in range(1,len(lat)-1):
                vg[t,lev,latt,:] = 9.8*np.gradient(h[t,lev,latt,:],disx[latt],axis=0)/f[latt]
                ug[t,lev,latt,:] = ug[t,lev,latt,:]/f[latt]

    return ug,vg

def cal_xydistance(lat,lon):
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

def out_date(year,day):

    fir_day = datetime.datetime(year,1,1)
    zone    = datetime.timedelta(days=day-1)
    #return datetime.datetime.strftime(fir_day + zone, "%Y-%m-%d")
    #return datetime.datetime.strftime(fir_day + zone, "%m-%d")
    return datetime.datetime.strftime(fir_day + zone, "%m%d")

def dew_point(T,RH):
    RH = RH*100
    TD =243.04*(math.log(RH/100)+((17.625*T)/(243.04+T)))/(17.625-math.log(RH/100)-((17.625*T)/(243.04+T)))

    return TD

def model_theta(T,P):
    #2020/12/22
    #此方程旨在计算模式层上的位温
    theta = copy.deepcopy(T)
    for z in range(0,T.shape[1]):
        for y in range(0,T.shape[2]):
            for x in range(0,T.shape[3]):
                theta[0,z,y,x] = T[0,z,y,x]*math.pow((100000/P[0,z,y,x]),0.286)

    return theta

def leap_year(year):
    #判断是不是闰年，是就返回1，不是就返回0
    if (year % 4) == 0:
        if (year % 100) == 0:
            if (year % 400) == 0:
                return 1  # 整百年能被400整除的是闰年
            else:
                return 0
        else:
            return 1  # 非整百年能被4整除的为闰年
    else:
        return 0

def omega_to_w(omega,p,t):
    rgas = 287.058
    g = 9.80665
    rho = p/(rgas*t)
    w = -omega/(rho*g)

    return w

def conform(p,shape,axis1,axis2,axis3):
    conformx  =  np.zeros(shape)
    for t in range(0,shape[axis1]):
        for y in range(0,shape[axis2]):
            for x in range(0,shape[axis3]):
                conformx[t,:,y,x] = p
    return conformx

def daily_mean(var,alltime,times):
    days = alltime//times
    mean = ma.zeros((days,int(var.shape[1]),int(var.shape[2]),int(var.shape[3])))
    mean = ma.array(mean,mask = var.mask)
    for tttt in range(0,var.shape[0],times):
        mean[tttt//times,:,:,:] =  np.sum(var[tttt:tttt+times,:,:,:],axis=0)/times

    return mean

def short2flt(var):
    scale_factor = var.scale_factor[0]
    add_offset = var.add_offset[0]
    v1  =  var[:]
    v2  =  v1*scale_factor + add_offset
    return v2

#def pinjie(year,path):
    #本函数解决的痛点：对于以月为分割的文件，这里给它整成

def cesm_vin2p(path,file,pnew):
    vars  =  ["KVH","DTV","LHFLX","OMEGA","OMEGAT","PRECT","PS","Q","SHFLX","T","TS","U","V","Z3"]
    files = xr.open_dataset(path+file,engine='netcdf4')
    ds    = xr.Dataset(
        {
            "LHFLX":(["time","lat","lon"],files.LHFLX.data),
            "OMEGA":(["time","lev","lat","lon"],Ngl.vinth2p(files.OMEGA.data,files.hyam.data,files.hybm.data,pnew,files.PS.data,1,files.P0.data/100,1,True)),
            "PRECT":(["time","lat","lon"],files.PRECT.data),
            "Q":(["time","lev","lat","lon"],Ngl.vinth2p(files.Q.data,files.hyam.data,files.hybm.data,pnew,files.PS.data,1,files.P0.data/100,1,True)),
            "SHFLX":(["time","lat","lon"],files.SHFLX.data),
            "T":(["time","lev","lat","lon"],Ngl.vinth2p(files.T.data,files.hyam.data,files.hybm.data,pnew,files.PS.data,1,files.P0.data/100,1,True)),
            "U":(["time","lev","lat","lon"],Ngl.vinth2p(files.U.data,files.hyam.data,files.hybm.data,pnew,files.PS.data,1,files.P0.data/100,1,True)),
            "V":(["time","lev","lat","lon"],Ngl.vinth2p(files.V.data,files.hyam.data,files.hybm.data,pnew,files.PS.data,1,files.P0.data/100,1,True)),
            "Z3":(["time","lev","lat","lon"],Ngl.vinth2p(files.Z3.data,files.hyam.data,files.hybm.data,pnew,files.PS.data,1,files.P0.data/100,1,True)),
            "PS":(["time","lat","lon"],files.PS.data),
            "TS":(["time","lat","lon"],files.TS.data),
        },
        coords={
            "lon":(["lon"],files.lon.data),
            "lat":(["lat"],files.lat.data),
            "time":(["time"],files.time.data),
            "lev":(["lev"],pnew)
        },
    )
    ds.LHFLX.attrs     =      files.LHFLX.attrs
    ds.OMEGA.attrs     =      files.OMEGA.attrs
    ds.PRECT.attrs     =      files.PRECT.attrs
    ds.Q.attrs         =      files.Q.attrs
    ds.SHFLX.attrs     =      files.SHFLX.attrs
    ds.T.attrs         =      files.T.attrs
    ds.U.attrs         =      files.U.attrs
    ds.V.attrs         =      files.V.attrs
    ds.Z3.attrs        =      files.Z3.attrs
    ds.PS.attrs        =      files.PS.attrs
    ds.TS.attrs        =      files.TS.attrs
    ds.lon.attrs       =      files.lon.attrs
    ds.lat.attrs       =      files.lat.attrs
    ds.time.attrs      =      files.time.attrs
    ds.lev.attrs["units"]    =      "hPa"

    return ds

def cal_monthly_average_daily(array):
    #本函数通过daily的资料来计算monthly数据
    day  =  [31,28,31,30,31,30,31,31,30,31,30,31]
    if len(array.shape) == 4:
        month_avg = np.zeros((12,array.shape[1],array.shape[2],array.shape[3]))
    else:
        month_avg = np.zeros((12, array.shape[1], array.shape[2]))
    start  =  0
    for mm in range(0,12):
        month_avg[mm,:]  =  np.average(array[start:(start+day[mm]),:],axis=0)
        start += day[mm]

    return month_avg

def cal_pentad_average_daily(array):
    #本函数通过daily的资料来计算pentad数据
    if len(array.shape) == 4:
        pentad_avg = np.zeros((73,array.shape[1],array.shape[2],array.shape[3]))
    else:
        pentad_avg = np.zeros((73, array.shape[1], array.shape[2]))
    for mm in range(0,73):
        pentad_avg[mm,:]  =  np.average(array[mm*5:(mm*5+5),:],axis=0)

    return pentad_avg

def set_map_ticks(ax, dx=60, dy=30, nx=0, ny=0, labelsize=15):
    '''
    为PlateCarree投影的GeoAxes设置tick和tick label.
    需要注意,set_extent应该在该函数之后使用.

    Parameters
    ----------
    ax : GeoAxes
        需要被设置的GeoAxes,要求投影必须为PlateCarree.

    dx : float, default: 60
        经度的major ticks的间距,从-180度开始算起.默认值为10.

    dy : float, default: 30
        纬度的major ticks,从-90度开始算起,间距由dy指定.默认值为10.

    nx : float, default: 0
        经度的minor ticks的个数.默认值为0.

    ny : float, default: 0
        纬度的minor ticks的个数.默认值为0.

    labelsize : str or float, default: 'medium'
        tick label的大小.默认为'medium'.

    Returns
    -------
    None
    '''
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


def generate_lat_lon_label(left,right,space1,bottom,top,space2):
    x_tick_labels=[]
    for xx in range(left,right,space1):
        x_tick_labels.append(u''+str(xx)+"\N{DEGREE SIGN}E")
    y_tick_labels=[]
    for yy in range(bottom,top,space2):
        y_tick_labels.append(u''+str(yy)+"\N{DEGREE SIGN}N")

def generate_lon_label(left,right,space1):
    x_tick_labels=[]
    for xx in range(left,right+1,space1):
        x_tick_labels.append(u''+str(xx)+"\N{DEGREE SIGN}E")
    return x_tick_labels

def create_ncl_colormap(file,bin):
    import numpy as np
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap

    rgb  =  []
    with open(file,"r") as f:
        for line in f.readlines():
            line = line.strip('\n')
            line1  =  line.split()
            rgb.append(tuple(np.array(line.split()).astype(float))/max(tuple(np.array(line.split()).astype(float))))
    cmap = LinearSegmentedColormap.from_list('newcmp', rgb, N=bin)

    return cmap

def cal_partial_correlation(rab, rac, rbc):
    '''
    This function calculate the partial correlation, c is variable to be removed
    '''
    top = rab - (rac * rab)
    bottom = math.sqrt((1-rac**2) * (1-rbc**2))

    return top/bottom