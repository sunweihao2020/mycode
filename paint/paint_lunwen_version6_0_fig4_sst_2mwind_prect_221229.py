'''
2022-12-29
本代码绘制论文version6.0中的fig4
version6 新增:修改降水颜色
'''
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
from paint_lunwen_version3_0_fig2a_tem_gradient_20220426 import add_text

def interp_precip(precip,lon,lat,newlon,newlat):
    '''给输入的降水数据进行插值'''
    in_prect1  =  np.zeros((precip.shape[0],len(lat),len(newlon)))
    in_prect2  =  np.zeros((precip.shape[0],len(newlat),len(newlon)))

    for tt in range(precip.shape[0]):
        for latt in range(len(lat)):
            in_prect1[tt,latt,:]  =  np.interp(newlon,lon,precip[tt,latt,:])
    
    for tt in range(precip.shape[0]):
        for lonn in range(len(newlon)):
            in_prect2[tt,:,lonn]  =  np.interp(newlat,lat,in_prect1[tt,:,lonn])

    print('successfully interp precipitation')
    return in_prect2

def interp_precip_onsetday(precip,lon,lat,newlon,newlat):
    '''给输入的降水数据进行插值,仅爆发当日时次'''
    in_prect1  =  np.zeros((len(lat),len(newlon)))
    in_prect2  =  np.zeros((len(newlat),len(newlon)))

    for latt in range(len(lat)):
        in_prect1[latt,:]  =  np.interp(newlon,lon,precip[latt,:])
    
    for lonn in range(len(newlon)):
        in_prect2[:,lonn]  =  np.interp(newlat,lat,in_prect1[:,lonn])

    print('successfully interp onset day precipitation')
    return in_prect2
    
def paint_pic(extent,sst_lon,sst_lat,wind_lon,wind_lat,prect_lat,prect,sst,U2M,V2M,prect_early, prect_late, sst_early, sst_late, U2M_early, U2M_late, V2M_early, V2M_late, date,dates,number):
    # 设置画布
    proj    =  ccrs.PlateCarree()
    fig1    =  plt.figure(figsize=(26, 25.5))
    spec1   =  fig1.add_gridspec(nrows=3, ncols=2)

    # colorbar使用ncl的
    cmap  =  create_ncl_colormap("/home/sun/data/color_rgb/MPL_coolwarm.txt",32)

    j  =  0
    for row in range(2):
        for col in range(2):
            ax = fig1.add_subplot(spec1[row,col],projection=proj)

            # 设置刻度
            set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(50,110,4,dtype=int),yticks=np.linspace(-10,30,5,dtype=int),nx=1,ny=1,labelsize=25)

            # 赤道线
            ax.plot([40,120],[0,0],'k--')

            # 等值线
            im1  =  ax.contour(sst_lon,prect_lat,prect[date[j],:],levels=np.arange(6,31,12),colors='blue',linewidths=3.1,alpha=1,zorder=1)
            im2  =  ax.contourf(sst_lon,sst_lat,sst[date[j],:],levels=np.arange(26.5,31,0.25),cmap=cmap,extend='both',zorder=0)
            ax.clabel(im1, inline=True, fontsize=13)

            # 海岸线
            ax.coastlines(resolution='110m',lw=1)

            # 流线
            print(U2M.shape)
            q   =   ax.streamplot(wind_lon, wind_lat, U2M[date[j],:], V2M[date[j],:],linewidth=2.5, color = '#6D6D6D',density=[1, 1.15], arrowsize=3.5, arrowstyle='->',)

            # 加日期
            if dates[j]<0:
                ax.set_title("D"+str(dates[j]),loc='right',fontsize=27.5)
            elif dates[j]>0:
                ax.set_title("D+"+str(dates[j]),loc='right',fontsize=27.5)
            else:
                ax.set_title("D"+str(dates[j]),loc='right',fontsize=27.5)
            
            # 加图序号
            ax.set_title("("+number[j]+")",loc='left',fontsize=27.5)
        
            j += 1

    # -----------------paint the early year-------------------------
    ax = fig1.add_subplot(spec1[2, 0],projection=proj)

    # 设置刻度
    set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(50,110,4,dtype=int),yticks=np.linspace(-10,30,5,dtype=int),nx=1,ny=1,labelsize=25)

    # 赤道线
    ax.plot([40,120],[0,0],'k--')

    # 等值线
    im1  =  ax.contour(sst_lon,prect_lat,prect_early,levels=np.arange(6,31,12),colors='blue',linewidths=3.1,alpha=1,zorder=1)
    im2  =  ax.contourf(sst_lon,sst_lat,sst_early,levels=np.arange(26.5,31,0.25),cmap=cmap,extend='both',zorder=0)
    ax.clabel(im1, inline=True, fontsize=13)

    # 海岸线
    ax.coastlines(resolution='110m',lw=1)

    # 流线
    print(U2M_early.shape)
    q   =   ax.streamplot(wind_lon, wind_lat, U2M_early, V2M_early,linewidth=2.5, color = '#6D6D6D',density=[1, 1.15], arrowsize=3.5, arrowstyle='->',)

    # set title
    ax.set_title("D0 (Early Onset Year)", loc='right', fontsize=27.5)

    # 加图序号
    ax.set_title("(e)",loc='left',fontsize=27.5)

    # paint the late year
    ax = fig1.add_subplot(spec1[2, 1],projection=proj)

    # 设置刻度
    set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(50,110,4,dtype=int),yticks=np.linspace(-10,30,5,dtype=int),nx=1,ny=1,labelsize=25)

    # 赤道线
    ax.plot([40,120],[0,0],'k--')

    # 等值线
    im1  =  ax.contour(sst_lon,prect_lat,prect_late,levels=np.arange(6,31,12),colors='blue',linewidths=3.1,alpha=1,zorder=1)
    im2  =  ax.contourf(sst_lon,sst_lat,sst_late,levels=np.arange(26.5,31,0.25),cmap=cmap,extend='both',zorder=0)
    ax.clabel(im1, inline=True, fontsize=13)

    # 海岸线
    ax.coastlines(resolution='110m',lw=1)

    # 流线
    q   =   ax.streamplot(wind_lon, wind_lat, U2M_late, V2M_late,linewidth=2.5, color = '#6D6D6D',density=[1, 1.15], arrowsize=3.5, arrowstyle='->',)

    # set title
    ax.set_title("D0 (Late Onset Year)", loc='right', fontsize=27.5)

    # 加图序号
    ax.set_title("(f)",loc='left',fontsize=27.5)

    # 加colorbar
    fig1.subplots_adjust(top=0.8) 
    cbar_ax = fig1.add_axes([0.2, 0.05, 0.6, 0.03]) 
    cb  =  fig1.colorbar(im2, cax=cbar_ax, shrink=0.1, pad=0.01, orientation='horizontal')
    cb.ax.tick_params(labelsize=25)

    # 保存图片
    #plt.tight_layout()
    save_fig(path_out="/home/sun/paint/lunwen/version6.0/",file_out="color7.pdf")

def early_late_onsetday_data_sst():
    '''准备在季风爆发早年和晚年的变量
    '''
    # ---------------- 1. get the early and late onset day ----------------------------
    import json
    with open("/home/sun/qomo-data/early_date.json",'r') as load_f:
        early_date = json.load(load_f)

    early_years = np.array(list(early_date.keys()))
    early_days  = np.array(list(early_date.values()))
    early_years = early_years.astype(int)
    early_days  = early_days.astype(int)

    with open("/home/sun/qomo-data/late_date.json", 'r') as load_f2:
        b = json.load(load_f2)

    years = np.array(list(b.keys()))
    days  = np.array(list(b.values()))
    late_years = years.astype(int)
    late_days  = days.astype(int)

    # ------------- 2. Calculate the early and late year average SST ----------------
    sst_file  =  xr.open_dataset('/home/sun/qomo-data/burst_seris/composite_sst.nc')
    year_range  =  [1982, 2016]

    # 2.1 claim the base array
    early_sst  =  np.zeros((720, 1440))
    late_sst   =  np.zeros((720, 1440))

    # 2.2 calculate the average
    year0  =  1982
    early_n = 0 ; late_n = 0 # save the early and late year number
    for yyyy in range(35):
        year1  =  year0 + yyyy
        if year1 in early_years:
            early_n += 1
            early_sst += sst_file['sea_surface_temperature'].data[yyyy, 30]
        elif year1 in late_years:
            late_n  += 1
            late_sst  += sst_file['sea_surface_temperature'].data[yyyy, 30]
        else:
            continue
    
    # 2.2.1 divide the years number
    early_sst /= early_n ; late_sst /= late_n
    # up to this step, the longitude is 0 - 360

    # -------------- 3. Intepolate the new SST data ---------------------------------
    early_sst_in1  =  np.zeros((720, 360)) ; late_sst_in1  =  early_sst_in1.copy()
    early_sst_in2  =  np.zeros((181, 360)) ; late_sst_in2  =  early_sst_in2.copy()

    ref_sst_file   =  xr.open_dataset("/home/sun/qomo-data/" + "composite_OISST_trans2.nc")

    for y in range(720):
        early_sst_in1[y, :]  =  np.interp(ref_sst_file.lon.data, sst_file.lon.data, early_sst[y, :])
        late_sst_in1[y, :]   =  np.interp(ref_sst_file.lon.data, sst_file.lon.data, late_sst[y, :])

    for x in range(360):
        early_sst_in2[:, x]  =  np.interp(ref_sst_file.lat.data, sst_file.lat.data, early_sst_in1[:, x])
        late_sst_in2[:, x]   =  np.interp(ref_sst_file.lat.data, sst_file.lat.data, late_sst_in1[:, x])
    
    # ------------- 4. wite intepolated sst to ncfile --------------------------------
    ncfile  =  xr.Dataset(
    {
        "early_d0_sst": (["lat", "lon"], early_sst_in2),
        "late_d0_sst":  (["lat", "lon"], late_sst_in2),
    },
    coords={
        "lon": (["lon"], ref_sst_file.lon.data),
        "lat": (["lat"], ref_sst_file.lat.data),
    },
    )
    ncfile.early_d0_sst.attrs  =  sst_file['sea_surface_temperature'].attrs
    ncfile.late_d0_sst.attrs   =  sst_file['sea_surface_temperature'].attrs

    ncfile["lon"].attrs  =  ref_sst_file["lon"].attrs
    ncfile["lat"].attrs  =  ref_sst_file["lat"].attrs

    ncfile.attrs['description'] = 'Created in 2022-12-31. This file include the onset day SST data averaged from early and late years.'

    ncfile.to_netcdf("/home/sun/data/onset_day_sst_early_late_years.nc")

def early_late_onsetday_data_trmm():
    '''准备在季风爆发早年和晚年的变量
    '''
    # ---------------- 1. get the early and late onset day ----------------------------
    import json
    import os
    with open("/home/sun/qomo-data/early_date.json",'r') as load_f:
        early_date = json.load(load_f)

    early_years = np.array(list(early_date.keys()))
    early_days  = np.array(list(early_date.values()))
    early_years = early_years.astype(int)
    early_days  = early_days.astype(int)

    with open("/home/sun/qomo-data/late_date.json", 'r') as load_f2:
        late_date = json.load(load_f2)

    #print(late_date)
    years = np.array(list(late_date.keys()))
    #print(years)
    days  = np.array(list(late_date.values()))
    late_years = years.astype(int)
    late_days  = days.astype(int)

    # ------------- 2. Calculate the early and late year average TRMM precipitation ----------------
    trmm_file0 =  xr.open_dataset('/home/sun/mydown/trmm_precipitation/3B42_Daily.20110227.7.nc4.nc4')
    trmm_path  =  '/home/sun/mydown/trmm_precipitation/'
    year_range  =  [1998, 2019]

    # 2.1 claim the base array
    early_trmm  =  np.zeros((1440, 400))
    late_trmm   =  np.zeros((1440, 400))

    # calculate the average
    year0 = 1998
    early_n = 0 ; late_n = 0 # save the early and late year number
    list_trmm = os.listdir('/home/sun/mydown/trmm_precipitation')
    for yyyy in range(22):
        year1  =  year0 + yyyy
        if year1 in early_years:
            early_n += 1
            # get this year file list
            list_trmm2  =  [x for x in list_trmm if str(year1) in x]
            list_trmm2.sort() 
            #print(b[str(year1)])
            day0        =  int(early_date[str(year1)])
            #print(day0)
            print('This year is early year {}, onsetday is {}'.format(year1, day0))
            trmm_file   =  xr.open_dataset(trmm_path + list_trmm2[day0])
            early_trmm  += trmm_file['precipitation'].data
        elif year1 in late_years:
            #print(late_date[str(year1)])
            late_n  += 1
            # get this year file list
            list_trmm2  =  [x for x in list_trmm if str(year1) in x]
            list_trmm2.sort() 
            day0        =  int(late_date[str(year1)])
            #print(day0)
            print('This year is late year {}, onsetday is {}'.format(year1, day0))
            trmm_file   =  xr.open_dataset(trmm_path + list_trmm2[day0])
            late_trmm  += trmm_file['precipitation'].data
        else:
            continue

    # 2.2.1 divide the years number
    early_trmm /= early_n ; late_trmm /= late_n

    # ------------- 4. wite TRMM to ncfile --------------------------------
    ncfile  =  xr.Dataset(
    {
        "early_d0_trmm": (["lon", "lat"], early_trmm),
        "late_d0_trmm":  (["lon", "lat"], late_trmm),
    },
    coords={
        "lon": (["lon"], trmm_file0.lon.data),
        "lat": (["lat"], trmm_file0.lat.data),
    },
    )
    ncfile.early_d0_trmm.attrs  =  trmm_file0['precipitation'].attrs
    ncfile.late_d0_trmm.attrs   =  trmm_file0['precipitation'].attrs

    ncfile["lon"].attrs  =  trmm_file0["lon"].attrs
    ncfile["lat"].attrs  =  trmm_file0["lat"].attrs

    ncfile.attrs['description'] = 'Created in 2023-1-1. This file include the onset day TRMM data averaged from early and late years.'

    os.system('rm -rf /home/sun/data/composite/early_late_composite/onset_day_trmm_early_late_years.nc')
    ncfile.to_netcdf("/home/sun/data/composite/early_late_composite/onset_day_trmm_early_late_years.nc")

def early_late_onsetday_data_singlelayer():
    '''This function calculate the early and late year U2M V2M'''
    import os

    path0  =  '/home/sun/mydown/merra2_u2v2/'
    file_list0  =  os.listdir(path0)
    # ---------------- 1. get the early and late onset day ----------------------------
    import json
    import os
    with open("/home/sun/qomo-data/early_date.json",'r') as load_f:
        early_date = json.load(load_f)

    early_years = np.array(list(early_date.keys()))
    early_days  = np.array(list(early_date.values()))
    early_years = early_years.astype(int)
    early_days  = early_days.astype(int)

    with open("/home/sun/qomo-data/late_date.json", 'r') as load_f2:
        late_date = json.load(load_f2)

    years = np.array(list(late_date.keys()))
    days  = np.array(list(late_date.values()))
    late_years = years.astype(int)
    late_days  = days.astype(int)

    # ------------- 2. Calculate the early and late year average TRMM precipitation ----------------
    year_range  =  [1980, 2019]

    # 2.1 claim the base array
    early_u2    =  np.zeros((361, 576)) ; late_u2  =  early_u2.copy()
    early_v2    =  np.zeros((361, 576)) ; late_v2  =  early_u2.copy()

    # calculate the average
    year0 = 1980
    early_n = 0 ; late_n = 0 # save the early and late year number
    for yyyy in range(40):
        year1  =  year0 + yyyy
        if year1 in early_years:
            early_n += 1
            # get this year file list
            list_single2  =  [x for x in file_list0 if str(year1) in x]
            list_single2.sort() 
            day0        =  int(early_date[str(year1)])
            print('This year is early year {}, onsetday is {}'.format(year1, day0))
            single_file   =  xr.open_dataset(path0 + list_single2[day0])
            early_u2      += np.average(single_file['U2M'].data, axis=0)
            early_v2      += np.average(single_file['V2M'].data, axis=0)

        elif year1 in late_years:
            late_n  += 1
            # get this year file list
            list_single2  =  [x for x in file_list0 if str(year1) in x]
            list_single2.sort() 
            day0        =  int(late_date[str(year1)])
            print('This year is late year {}, onsetday is {}'.format(year1, day0))
            single_file   =  xr.open_dataset(path0 + list_single2[day0])
            late_u2     += np.average(single_file['U2M'].data, axis=0)
            late_v2     += np.average(single_file['V2M'].data, axis=0)
        else:
            continue

    # 2.2.1 divide the years number
    early_u2 /= early_n ; late_u2 /= late_n
    early_v2 /= early_n ; late_v2 /= late_n

    # 2.2.3 intepolate to the 1 x 1 resolution
    ref_file  =  xr.open_dataset('/home/sun/qomo-data/composite-merra2-single.nc')
    early_d0_u2_interp  =  np.zeros((181, 360))
    early_d0_v2_interp  =  np.zeros((181, 360))
    late_d0_u2_interp   =  np.zeros((181, 360))
    late_d0_v2_interp   =  np.zeros((181, 360))

    #interim array
    early_d0_u2_interp_in1  =  np.zeros((361, 360))
    early_d0_v2_interp_in1  =  np.zeros((361, 360))
    late_d0_u2_interp_in1   =  np.zeros((361, 360))
    late_d0_v2_interp_in1   =  np.zeros((361, 360))

    for i in range(361):
        early_d0_u2_interp_in1[i, :]  =  np.interp(ref_file.lon.data, single_file.lon.data, early_u2[i, :])
        early_d0_v2_interp_in1[i, :]  =  np.interp(ref_file.lon.data, single_file.lon.data, early_v2[i, :])
        late_d0_u2_interp_in1[i, :]   =  np.interp(ref_file.lon.data, single_file.lon.data, late_u2[i, :])
        late_d0_v2_interp_in1[i, :]   =  np.interp(ref_file.lon.data, single_file.lon.data, late_v2[i, :])

    for j in range(360):
        early_d0_u2_interp[:, j]      =  np.interp(ref_file.lat.data, single_file.lat.data, early_d0_u2_interp_in1[:, j])
        early_d0_v2_interp[:, j]      =  np.interp(ref_file.lat.data, single_file.lat.data, early_d0_v2_interp_in1[:, j])
        late_d0_u2_interp[:, j]       =  np.interp(ref_file.lat.data, single_file.lat.data, late_d0_u2_interp_in1[:, j])
        late_d0_v2_interp[:, j]       =  np.interp(ref_file.lat.data, single_file.lat.data, late_d0_v2_interp_in1[:, j])


    # ------------- 4. wite single vars to ncfile --------------------------------
    ncfile  =  xr.Dataset(
    {
        "early_d0_u2": (["lat", "lon"], early_d0_u2_interp),
        "late_d0_u2":  (["lat", "lon"], late_d0_u2_interp),
        "early_d0_v2": (["lat", "lon"], early_d0_v2_interp),
        "late_d0_v2":  (["lat", "lon"], late_d0_v2_interp),
    },
    coords={
        "lon": (["lon"], ref_file.lon.data),
        "lat": (["lat"], ref_file.lat.data),
    },
    )
    ncfile.early_d0_u2.attrs  =  single_file['U2M'].attrs
    ncfile.late_d0_u2.attrs   =  single_file['U2M'].attrs
    ncfile.early_d0_v2.attrs  =  single_file['V2M'].attrs
    ncfile.late_d0_v2.attrs   =  single_file['V2M'].attrs

    ncfile["lon"].attrs  =  single_file["lon"].attrs
    ncfile["lat"].attrs  =  single_file["lat"].attrs

    ncfile.attrs['description'] = 'Created in 2023-1-13. This file include the onset day single data U2M V2M averaged from early and late years. and interpolate to the 1x1 resolution'

    os.system('rm -rf /home/sun/data/composite/early_late_composite/onset_day_u2v2_early_late_years_1x1.nc')
    ncfile.to_netcdf("/home/sun/data/composite/early_late_composite/onset_day_u2v2_early_late_years_1x1.nc")


def main():
    # 划定空间范围
    lon_slice  =  slice(40,120)
    lat_slice  =  slice(-15,40)

    lonmin,lonmax,latmin,latmax  =  45,115,-10,30
    extent     =  [lonmin,lonmax,latmin,latmax]

    # 选取时间
    dates  =  [-12,-6,-2,0]  #总共4张图
    date   =  [18,24,28,30]

    # 图片序号
    number =  ["a","b","c","d"]

    # 读取文件
    path  =  "/home/sun/qomo-data/"
    f1    =  xr.open_dataset(path+"composite_OISST_trans.nc").sel(lon=lon_slice,lat=lat_slice)
    f2    =  xr.open_dataset(path+"composite-precipitation_trmm.nc")
    f3    =  xr.open_dataset(path+"composite-merra2-single.nc").sel(lon=lon_slice,lat=lat_slice)
    f4    =  xr.open_dataset('/home/sun/data/composite/early_late_composite/onset_day_trmm_early_late_years.nc')
    f5    =  xr.open_dataset('/home/sun/data/composite/early_late_composite/onset_day_sst_early_late_years_lonflip.nc').sel(lon=lon_slice,lat=lat_slice)
    f6    =  xr.open_dataset('/home/sun/data/composite/early_late_composite/onset_day_u2v2_early_late_years_1x1.nc').sel(lon=lon_slice,lat=lat_slice)


    # 处理早晚年的爆发当日数据
    #early_late_onsetday_data_sst()
    #early_late_onsetday_data_trmm()
    #early_late_onsetday_data_singlelayer()

    # TRMM降水数据需要插值 这里调用swapaxes调换一下trmm的轴
    trmm_prect    =  interp_precip(f2.precipitation.data.swapaxes(2,1),lon=f2.lon,lat=f2.lat,newlat=np.linspace(-50,50,101),newlon=f1.lon)
    trmm_prect_e  =  interp_precip_onsetday(f4.early_d0_trmm.data.swapaxes(1,0),lon=f2.lon,lat=f2.lat,newlat=np.linspace(-50,50,101),newlon=f1.lon)
    trmm_prect_l  =  interp_precip_onsetday(f4.late_d0_trmm.data.swapaxes(1,0),lon=f2.lon,lat=f2.lat,newlat=np.linspace(-50,50,101),newlon=f1.lon)

    #  下面开始绘图
    paint_pic(extent=extent,sst_lon=f1.lon,sst_lat=f1.lat,wind_lon=f3.lon,wind_lat=f3.lat,prect=trmm_prect,sst=f1.sst.data,U2M=f3.U2M.data,V2M=f3.V2M.data,prect_early = trmm_prect_e, prect_late = trmm_prect_l, sst_early=f5['early_d0_sst'].data, sst_late=f5['late_d0_sst'].data, U2M_early=f6['early_d0_u2'].data, U2M_late=f6['late_d0_u2'].data, V2M_early=f6['early_d0_v2'].data, V2M_late=f6['late_d0_v2'].data, date=date,dates=dates,number=number,prect_lat=np.linspace(-50,50,101))

if __name__ == "__main__":
    main()