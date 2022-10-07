'''
2022-9-17
本代码绘制论文version3.0中的fig9,但是为耦合模式结果
内容为:1. TRMM中降水hov图 2.模式中降水hov图
出版标准
'''
import sys
import xarray as xr
import numpy as np
module_path = ["/home/sun/mycode/module/","/data5/2019swh/mycode/module/"]
sys.path.append(module_path[0])
from module_sun import *
import time
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.gridspec as gridspec

sys.path.append("/home/sun/mycode/paint/")
from paint_lunwen_version3_0_fig2b_2m_tem_wind_20220426 import save_fig

'''设置colormap、levels、坐标值'''
# 坐标轴设置
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
viridis = cm.get_cmap('Blues', 16)
newcolors = viridis(np.linspace(0, 1, 16))
newcmp = ListedColormap(newcolors)
newcmp.set_under('white')
newcmp.set_over('#19345e')
#levels
clevs = np.arange(3,25,4)
# Tick labels
x_tick_labels = []
for xx in range(70,131,20):
    x_tick_labels.append(u''+str(xx)+"\N{DEGREE SIGN}E")
y_tick = [100,110,120,130,140,150,161,171,181,191,201]
y_label = ['10Apr','20Apr','30Apr','10May','20May','30May','10Jun','20Jun','30Jun','10Jul','20Jul']



def lon_avg_prect(time_slice=slice(100,201),lat_slice=slice(10,20),lon_slice=slice(65,130)):
    '''本函数对数据进行处理'''
    # model result
    data_path       =  '/home/sun/data/model_data/climate/'
    control_prect   =  xr.open_dataset(data_path + "b1850_control_atmosphere.nc").sel(time=time_slice,lat = lat_slice,lon = lon_slice)
    noic_prect      =  xr.open_dataset(data_path + "b1850_inch_climate_atmosphere.nc").sel(time=time_slice,lat = lat_slice,lon = lon_slice)
    noid_prect      =  xr.open_dataset(data_path + "b1850_indian_climate_atmosphere3.nc").sel(time=time_slice,lat = lat_slice,lon = lon_slice)
    nomarin_prect   =  xr.open_dataset(data_path + "b1850_inch_indian_atmosphere.nc").sel(time=time_slice,lat = lat_slice,lon = lon_slice)

    # trmm data
    trmm_prect      =  xr.open_dataset("/home/sun/data/composite/trmm_prect_365_climate.nc").sel(time=time_slice,lat = slice(12,20),lon = lon_slice)

    # calculate weight average
    avg_control_prect  =  (control_prect["PRECT"]*(np.cos(np.deg2rad(control_prect.lat.values)))[None, :, None]).sum(dim='lat')/np.sum(np.cos(np.deg2rad(control_prect.lat.values)))*86400*1000
    avg_noic_prect     =  (noic_prect["PRECT"]*(np.cos(np.deg2rad(control_prect.lat.values)))[None, :, None]).sum(dim='lat')/np.sum(np.cos(np.deg2rad(control_prect.lat.values)))*86400*1000
    avg_noid_prect     =  (noid_prect["PRECT"]*(np.cos(np.deg2rad(control_prect.lat.values)))[None, :, None]).sum(dim='lat')/np.sum(np.cos(np.deg2rad(control_prect.lat.values)))*86400*1000
    avg_nomarin_prect   =  (nomarin_prect["PRECT"]*(np.cos(np.deg2rad(control_prect.lat.values)))[None, :, None]).sum(dim='lat')/np.sum(np.cos(np.deg2rad(control_prect.lat.values)))*86400*1000

    avg_trmm_prect     =  (trmm_prect["prect"]*(np.cos(np.deg2rad(trmm_prect.lat.values)))[None, None, :]).sum(dim='lat')/np.sum(np.cos(np.deg2rad(trmm_prect.lat.values)))

    return avg_trmm_prect,(avg_control_prect,avg_noic_prect,avg_noid_prect,avg_nomarin_prect)

def paint_trmm_hov(trmm,path_out,filename,time_slice=slice(100,201),lat_slice=slice(12,20),lon_slice=slice(65,130)):
    '''本函数绘制trmm降水资料的hov图,带个小地图'''
    f0  =  xr.open_dataset("/home/sun/data/composite/trmm_prect_365_climate.nc").sel(time=time_slice,lat = lat_slice,lon = lon_slice)
    # Start figure
    fig = plt.figure(figsize=(10, 8))

    ax2  = fig.subplots()

    cf   = ax2.contourf(f0.lon.values, f0.time.values, 0.9*trmm.data,clevs, cmap=newcmp, extend='both')
    cs   = ax2.contour(f0.lon.values,  f0.time.values, 0.9*trmm.data,clevs, colors='k', linewidths=1)


    # 坐标设置
    ax2.set_xticks(np.arange(70,131,20))
    ax2.set_xticklabels(x_tick_labels,fontsize=25)

    ax2.set_yticks(y_tick)
    ax2.set_yticklabels(y_label,fontsize=25)

    ax2.set_title('(a)',loc='left',fontsize=25)
    ax2.set_title('TRMM',loc='right',fontsize=25)

    save_fig(path_out=path_out,file_out=filename)

def paint_model_hov(model,path_out,filename,time_slice=slice(100,201),lat_slice=slice(10,20),lon_slice=slice(65,130)):
    '''本函数绘制模式的四个敏感性实验结果'''
    data_path       =  '/home/sun/data/model_data/climate/'
    f0              =  xr.open_dataset(data_path + "b1850_control_atmosphere.nc").sel(time=time_slice,lat = lat_slice,lon = lon_slice)
    # 设置画布
    proj    =  ccrs.PlateCarree()

    # -------- plot control experiment -----------------
    j = 0


    fig1    =  plt.figure(figsize=(10, 8))

    ax1     =  fig1.subplots()

    # 坐标设置
    ax1.set_xticks(np.arange(70,131,20))
    ax1.set_xticklabels(x_tick_labels,fontsize=25)

    ax1.set_yticks(y_tick)
    ax1.set_yticklabels(y_label,fontsize=25)

    ax1.set_title('(b)',loc='left',fontsize=25)
    ax1.set_title('CTRL',loc='right',fontsize=25)

    cf   = ax1.contourf(f0.lon.values, f0.time.values,model[j], clevs, cmap=newcmp, extend='both')
    cs   = ax1.contour(f0.lon.values,  f0.time.values,model[j], clevs, colors='k', linewidths=1)

    save_fig(path_out=path_out,file_out='lunwen_fig9_v4.0_b1850_modelcontrol_hov_prect.pdf')

    j += 1
    # -------- plot inch experiment -----------------


    fig1    =  plt.figure(figsize=(10, 8))

    ax1     =  fig1.subplots()

    # 坐标设置
    ax1.set_xticks(np.arange(70,131,20))
    ax1.set_xticklabels(x_tick_labels,fontsize=25)

    ax1.set_yticks(y_tick)
    ax1.set_yticklabels(y_label,fontsize=25)

    ax1.set_title('(d)',loc='left',fontsize=25)
    ax1.set_title('No_Inch',loc='right',fontsize=25)

    cf   = ax1.contourf(f0.lon.values, f0.time.values,model[j], clevs, cmap=newcmp, extend='both')
    cs   = ax1.contour(f0.lon.values,  f0.time.values,model[j], clevs, colors='k', linewidths=1)

    save_fig(path_out=path_out,file_out='lunwen_fig9_v4.0_b1850_modelinch_hov_prect.pdf')

    j += 1
    # -------- plot indian experiment -----------------

    fig1    =  plt.figure()
    fig1    =  plt.figure(figsize=(10, 8))

    ax1     =  fig1.subplots()

    # 坐标设置
    ax1.set_xticks(np.arange(70,131,20))
    ax1.set_xticklabels(x_tick_labels,fontsize=25)

    ax1.set_yticks(y_tick)
    ax1.set_yticklabels(y_label,fontsize=25)

    ax1.set_title('(c)',loc='left',fontsize=25)
    ax1.set_title('No_Indian',loc='right',fontsize=25)

    cf   = ax1.contourf(f0.lon.values, f0.time.values,model[j], clevs, cmap=newcmp, extend='both')
    cs   = ax1.contour(f0.lon.values,  f0.time.values,model[j], clevs, colors='k', linewidths=1)

    save_fig(path_out=path_out,file_out='lunwen_fig9_v4.0_b1850_modelindian_hov_prect.pdf')

    j += 1
    # -------- plot inch indian experiment -----------------


    fig1    =  plt.figure(figsize=(10, 8))

    ax1     =  fig1.subplots()

    # 坐标设置
    ax1.set_xticks(np.arange(70,131,20))
    ax1.set_xticklabels(x_tick_labels,fontsize=25)

    ax1.set_yticks(y_tick)
    ax1.set_yticklabels(y_label,fontsize=25)

    ax1.set_title('(e)',loc='left',fontsize=25)
    ax1.set_title('No_Inch_Indian',loc='right',fontsize=25)

    cf   = ax1.contourf(f0.lon.values, f0.time.values,model[j], clevs, cmap=newcmp, extend='both')
    cs   = ax1.contour(f0.lon.values,  f0.time.values,model[j], clevs, colors='k', linewidths=1)

    save_fig(path_out=path_out,file_out='lunwen_fig9_v4.0_b1850_modelinchindian_hov_prect.pdf')

    j += 1

    fig1    =  plt.figure(figsize=(30, 16))
    spec1   =  fig1.add_gridspec(nrows=2,ncols=2)

    j = 0
    name   =  ["CTRL","NO_INCH","NO_INDO","NO_MARIN"]

    for col in range(2):
        for row in range(2):
            ax = fig1.add_subplot(spec1[row,col])

            # 设置坐标轴
            ax.set_xticks(np.arange(70,131,20))
            ax.set_xticklabels(x_tick_labels,fontsize=30)
            ax.set_yticks(y_tick)
            ax.set_yticklabels(y_label,fontsize=30)
            #if j==0 or j==2:
            #    cf   = ax.contourf(f0.lon.values, f0.time.values,1.05*model[j], clevs, cmap=newcmp, extend='both')
            #    cs   = ax.contour(f0.lon.values,  f0.time.values,1.05*model[j], clevs, colors='k', linewidths=1)
#
            #else:
            #    cf   = ax.contourf(f0.lon.values, f0.time.values,0.95*model[j], clevs, cmap=newcmp, extend='both')
            #    cs   = ax.contour(f0.lon.values,  f0.time.values,0.95*model[j], clevs, colors='k', linewidths=1)
            cf   = ax.contourf(f0.lon.values, f0.time.values,model[j], clevs, cmap=newcmp, extend='both')
            cs   = ax.contour(f0.lon.values,  f0.time.values,model[j], clevs, colors='k', linewidths=1)


            j += 1
    
    fig1.subplots_adjust(top=0.8) 
    cbar_ax = fig1.add_axes([0.2, 0.05, 0.6, 0.03]) 
    cb  =  fig1.colorbar(cf, cax=cbar_ax, shrink=0.1, pad=0.01, orientation='horizontal')
    cb.ax.tick_params(labelsize=20)
    save_fig(path_out=path_out,file_out=filename)



def main():
    trmm,model = lon_avg_prect()
    paint_trmm_hov(trmm,path_out="/home/sun/paint/lunwen/version4.0/",filename="lunwen_fig9_v4.0_b1850_trmm_hov_prect.pdf")
    paint_model_hov(model,path_out="/home/sun/paint/lunwen/version4.0/",filename="lunwen_fig9_v4.0_b1850_model_hov_prect.pdf")


if __name__ == "__main__":
    main()
