'''
2022-9-17
本代码绘制论文version3.0中的fig8
内容为:1. 三种越赤道气流的全年变化 2.模式与观测的对比
出版标准

数据替换为耦合实验b1850
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
import os
import math

sys.path.append("/home/sun/mycode/paint/")
from paint_lunwen_version3_0_fig2b_2m_tem_wind_20220426 import save_fig,set_cartopy_tick


class data_resolve:
    '''数据处理方面函数,最终结果是生成了nc文件'''
    end_path   =  '/home/sun/data/composite/' 
    file_name  =  'pentad_cross_jet_bobprect_filted.nc'

    def year_composite(lat,lon,path,var,time=365,lev=None):
        '''
            由于数据量过大,气候态的数据是按照一天一天存储的,这里设置一个函数可以组成时间维度为365的
            这里只针对多层数据
        '''
        if lev != None:
            if len(lev)==1:
                var_out  =  np.zeros((time,len(lat),len(lon)),dtype=np.float32)
            else:
                var_out  =  np.zeros((time,len(lev),len(lat),len(lon)),dtype=np.float32)

            # 获取文件列表
            files   =   os.listdir(path) ; files.sort()

            # 存入数据
            for i in range(len(files)):
                f0  =  xr.open_dataset(path+files[i]).sel(lev=lev)
                var_out[i]  =  f0[var].data[0,:]

            return var_out
        else:
            '''针对单层数据'''
            var_out  =  np.zeros((time,len(lat),len(lon)),dtype=np.float32)
            # 获取文件列表
            files   =   os.listdir(path) ; files.sort()

            # 存入数据
            for i in range(len(files)):
                f0  =  xr.open_dataset(path+files[i])
                var_out[i]  =  f0[var].data[0,:]
            return var_out

    def cal_pentad(var):
        '''本代码计算变量的候平均'''
        pentad  =  math.floor(var.shape[0]/5)
        if len(var.shape) == 4:
            var_pentad  =  np.zeros((pentad,var.shape[1],var.shape[2],var.shape[3]),dtype=np.float32)
        else:
            var_pentad  =  np.zeros((pentad,var.shape[1],var.shape[2]),dtype=np.float32)

        for i in range(pentad):
            var_pentad[i]  =  np.average(var[i*5:(i*5+5)],axis=0)

        return var_pentad

    def cal_regional_average(var):
        '''calculate regional average of variables.
        note: variable has been select before transmit'''
        import warnings
        warnings.filterwarnings("ignore")

        average_data  =  np.zeros((var.shape[0]))

        for i in range(0,var.shape[0]):
            average_data[i]  =  np.nanmean(var.data[i,:])

        return average_data

    def deal_data_average_climate(cv1=5,prect_lat=(10,25),level=[925]):
        '''deal with climate average data for wind and precipitation
        cv1:filter index
        '''
        path  =  "/home/sun/wd_disk/merra2_multi_climate/"
        f0    =  xr.open_dataset(path+"0707.climate.nc")

        # joint wind data
        u  =  data_resolve.year_composite(f0.lat.data,f0.lon.data,path,var="U",lev=level)
        v  =  data_resolve.year_composite(f0.lat.data,f0.lon.data,path,var="V",lev=level)

        # read precpitation
        path1  =  '/home/sun/data/composite/'
        f2 =  xr.open_dataset(path1 + "gpcp_prect_365_climate.nc")

        # calculate pentad average
        u_pentad      =  data_resolve.cal_pentad(u)
        v_pentad      =  data_resolve.cal_pentad(v)
        prect_pentad  =  data_resolve.cal_pentad(f2.prect.data) # interchange the axes

        # data integration
        ncfile     =xr.Dataset(
            {
                "u": (["time", "wind_lat", "wind_lon"], u_pentad),
                "v": (["time", "wind_lat", "wind_lon"], v_pentad),
                "prect": (["time", "prect_lat", "prect_lon"], prect_pentad),
            },
            coords={
                "wind_lon": (["wind_lon"], f0.lon.data),
                "wind_lat": (["wind_lat"], f0.lat.data),
                "prect_lon": (["prect_lon"], f2.lon.data),
                "prect_lat": (["prect_lat"], f2.lat.data),
                "time": (["time"], np.linspace(1,73,73)),
            },
        )

        # calculate regional average cross jet
        cross_equator  =  np.zeros((2,73))
        cross_equator[0]  =  data_resolve.cal_regional_average(ncfile.v.sel(wind_lat=slice(-5,5),wind_lon=slice(50,60)))
        cross_equator[1]  =  data_resolve.cal_regional_average(ncfile.v.sel(wind_lat=slice(-5,5),wind_lon=slice(80,90)))

        # calculate regional average precipitation in BOB
        ncfile.prect.data[ncfile.prect.data>100]  =  0  # ignore nan
        bob_prect  =  data_resolve.cal_regional_average(ncfile.prect.sel(prect_lat=slice(prect_lat[0],prect_lat[1]),prect_lon=slice(90,100)))

        # filter data
        filter_data  =  np.zeros((3,73),dtype=np.float32) # first two is cross eq index, third is precipitation
        filter_data[0]  =  np.convolve(cross_equator[0],np.ones(cv1)/cv1,mode='same')
        filter_data[1]  =  np.convolve(cross_equator[1],np.ones(cv1)/cv1,mode='same')
        filter_data[2]  =  np.convolve(bob_prect,np.ones(cv1)/cv1,mode='same')

        return filter_data

    def joint_anomaly_prect():
        '''早晚年的降水数据都是按日排列的，这里给组装起来'''
        import os.path
        if os.path.isfile("/home/sun/data/composite/gpcp_anomaly_prect_365_times.nc") == False:
            path1  =  "/home/sun/qomo-data/year_mean/gpcp_97_19_early/"
            path2  =  "/home/sun/qomo-data/year_mean/gpcp_97_19_late/"
            f      =  xr.open_dataset(path1+"early_gpcp_0722.climate.nc")
            # 连接
            prect_early  =  data_resolve.year_composite(f.lat.data,f.lon.data,path1,var="precip")
            prect_late   =  data_resolve.year_composite(f.lat.data,f.lon.data,path2,var="precip")

            # 存储
            ncfile     =xr.Dataset(
            {
                "prect_early": (["time", "lat", "lon"], prect_early),
                "prect_late": (["time", "lat", "lon"], prect_late),
            },
            coords={
                "lon": (["lon"], f.lon.data),
                "lat": (["lat"], f.lat.data),
                "time": (["time"], np.linspace(1,365,365)),
            },
            )
            ncfile.attrs['description']  =  'Combine the 365 files to one file includes anamoly years precipitation'
            ncfile.to_netcdf("/home/sun/data/composite/gpcp_anomaly_prect_365_times.nc")

            file  =  xr.open_dataset("/home/sun/data/composite/gpcp_anomaly_prect_365_times.nc")
        else:
            file  =  xr.open_dataset("/home/sun/data/composite/gpcp_anomaly_prect_365_times.nc")

        return file

    def deal_data_average_anamoly(cv1=5,prect_lat=(10,25)):
        '''处理异常年份的数据'''
        path1  =  "/home/sun/qomo-data/year_mean/multi_early/"
        path2  =  "/home/sun/qomo-data/year_mean/multi_late/"
        path3  =  "/home/sun/qomo-data/year_mean/gpcp_97_19_early/"
        f0    =  xr.open_dataset(path1+"early_multi_0915.climate.nc")
        f1    =  xr.open_dataset(path3+"early_gpcp_0722.climate.nc")

        # joint wind and precipitation data
        u_early  =  data_resolve.year_composite(f0.lat.data,f0.lon.data,path1,var="U",lev=[925])
        u_late   =  data_resolve.year_composite(f0.lat.data,f0.lon.data,path2,var="U",lev=[925])
        v_early  =  data_resolve.year_composite(f0.lat.data,f0.lon.data,path1,var="V",lev=[925])
        v_late   =  data_resolve.year_composite(f0.lat.data,f0.lon.data,path2,var="V",lev=[925])
        prect    =  data_resolve.joint_anomaly_prect()  # get the 365 seris anomaly precipitation in early and late year

        # calculate pentad average
        u_pentad_early  =  data_resolve.cal_pentad(u_early)
        v_pentad_early  =  data_resolve.cal_pentad(v_early)
        u_pentad_late   =  data_resolve.cal_pentad(u_late)
        v_pentad_late   =  data_resolve.cal_pentad(v_late)
        prect_pentad_early   =  data_resolve.cal_pentad(prect.prect_early.data)
        prect_pentad_late    =  data_resolve.cal_pentad(prect.prect_late.data)

        # data integration
        ncfile     =xr.Dataset(
            {
                "u_early": (["time", "wind_lat", "wind_lon"], u_pentad_early),
                "v_early": (["time", "wind_lat", "wind_lon"], v_pentad_early),
                "prect_early": (["time", "prect_lat", "prect_lon"], prect_pentad_early),
                "u_late": (["time", "wind_lat", "wind_lon"], u_pentad_late),
                "v_late": (["time", "wind_lat", "wind_lon"], v_pentad_late),
                "prect_late": (["time", "prect_lat", "prect_lon"], prect_pentad_late),
            },
            coords={
                "wind_lon": (["wind_lon"], f0.lon.data),
                "wind_lat": (["wind_lat"], f0.lat.data),
                "prect_lon": (["prect_lon"], f1.lon.data),
                "prect_lat": (["prect_lat"], f1.lat.data),
                "time": (["time"], np.linspace(1,73,73)),
            },
        )

        # calculate regional average cross jet
        cross_equator_early  =  np.zeros((2,73))
        cross_equator_early[0]  =  data_resolve.cal_regional_average(ncfile.v_early.sel(wind_lat=slice(-5,5),wind_lon=slice(50,60)))
        cross_equator_early[1]  =  data_resolve.cal_regional_average(ncfile.v_early.sel(wind_lat=slice(-5,5),wind_lon=slice(80,90)))

        cross_equator_late   =  np.zeros((2,73))
        cross_equator_late[0]  =  data_resolve.cal_regional_average(ncfile.v_late.sel(wind_lat=slice(-5,5),wind_lon=slice(50,60)))
        cross_equator_late[1]  =  data_resolve.cal_regional_average(ncfile.v_late.sel(wind_lat=slice(-5,5),wind_lon=slice(80,90)))

        # calculate regional average precipitation in BOB
        ncfile.prect_early.data[ncfile.prect_early.data>100]  =  0  # ignore nan
        bob_prect_early  =  data_resolve.cal_regional_average(ncfile.prect_early.sel(prect_lat=slice(prect_lat[0],prect_lat[1]),prect_lon=slice(90,100)))
        ncfile.prect_late.data[ncfile.prect_late.data>100]    =  0  # ignore nan
        bob_prect_late   =  data_resolve.cal_regional_average(ncfile.prect_late.sel(prect_lat=slice(prect_lat[0],prect_lat[1]),prect_lon=slice(90,100)))

        # filter data
        filter_data_early     =  np.zeros((3,73),dtype=np.float32) # first two is cross eq index, third is precipitation
        filter_data_early[0]  =  np.convolve(cross_equator_early[0],np.ones(cv1)/cv1,mode='same')
        filter_data_early[1]  =  np.convolve(cross_equator_early[1],np.ones(cv1)/cv1,mode='same')
        filter_data_early[2]  =  np.convolve(bob_prect_early,np.ones(cv1)/cv1,mode='same')
        filter_data_late     =  np.zeros((3,73),dtype=np.float32) # first two is cross eq index, third is precipitation
        filter_data_late[0]  =  np.convolve(cross_equator_late[0],np.ones(cv1)/cv1,mode='same')
        filter_data_late[1]  =  np.convolve(cross_equator_late[1],np.ones(cv1)/cv1,mode='same')
        filter_data_late[2]  =  np.convolve(bob_prect_late,np.ones(cv1)/cv1,mode='same')

        return filter_data_early,filter_data_late

    def integration_result():
        '''这里将生成的文件进行汇总
        内容为，气候态及早晚年的两股越赤道气流 + bob地区降水
        数据进行了5点滑动平均
        '''
        average_data         =  data_resolve.deal_data_average_climate()
        early_data,late_data =  data_resolve.deal_data_average_anamoly()

        # data integration
        ncfile     =xr.Dataset(
            {
                "climate": (["seris", "time"], average_data),
                "early": (["seris", "time"], early_data),
                "late":  (["seris", "time"], late_data),    
            },
            coords={
                "seris": (["seris"], ["somali","bob","bob_prect"]),
                "time": (["time"], np.linspace(1,73,73)),
            },
        )
        ncfile.attrs["description"]  =  "this file is calculated for lunwen, which is two cross equator stream and bob regional precipitation. all data has been moving average using 5 points"
        ncfile.attrs["date"]  =  "2022-9-18"

        ncfile.to_netcdf("/home/sun/data/composite/pentad_cross_jet_bobprect_filted.nc")

    def cal_geo_force(path,filename):
        '''本代码计算cesm2实验中的气压梯度力'''
        f0  =  xr.open_dataset(path+filename)

        z3  =  f0["Z3"].data * 9.8

        # 计算y方向气压梯度力
        '''获取地理坐标'''
        disy,disx,location =   cal_xydistance(f0.lat,f0.lon)

        '''计算梯度'''
        gradient_y         =   np.gradient(z3,location,axis=2)

        return gradient_y

    def save_and_read_geo_force_ncfile():
        '''本代码保存控制实验及无印度大陆实验中的气压梯度力数据'''
        # 判断文件是否存在
        from pathlib import Path

        result_file  =  "/home/sun/data/model_data/process/geopotential_height_gradient_con_id_b1850.nc"
        check_name   =  Path(result_file)
        if check_name.is_file() == False:
            # 指定的文件存在
            geo_force_con = data_resolve.cal_geo_force(path="/home/sun/data/model_data/climate/",filename="b1850_control_atmosphere.nc")
            geo_force_id  = data_resolve.cal_geo_force(path="/home/sun/data/model_data/climate/",filename="b1850_indian_climate_atmosphere3.nc")

            # 存储数据
            f0      =  xr.open_dataset("/home/sun/data/model_data/climate/b1850_control_atmosphere.nc")
            ncfile  =  xr.Dataset(
                {
                    "gradient_y_con": (["time", "lev", "lat", "lon"], geo_force_con),
                    "gradient_y_id": (["time", "lev", "lat", "lon"], geo_force_id),
                },
                coords={
                    "lon": (["lon"], f0.lon.data),
                    "lat": (["lat"], f0.lat.data),
                    "lev": (["lev"], f0.lev.data),
                    "time": (["time"], np.linspace(1,365,365)),
                },
            )
            ncfile["lat"].attrs  =  f0["lat"].attrs
            ncfile["lon"].attrs  =  f0["lon"].attrs
            ncfile["lev"].attrs  =  f0["lev"].attrs
            ncfile.attrs["description"]  =  "this file is calculated by only y axis gradient, and multiply 9.8"
            ncfile.to_netcdf(result_file)

            #file  =  xr.open_dataset(result_file).sel(lev=925,time=slice(90,120),lat=slice(-10,30),lon=slice(40,120))  # 这里提前选好范围了

    def model_cross_index(prect_lat=(10,20)):
        '''处理模式控制实验和敏感性实验的越赤道气流对比数据'''
        lev  =  925
        f1   =  xr.open_dataset("/home/sun/data/model_data/climate/b1850_control_atmosphere.nc").sel(lev=lev)
        f2   =  xr.open_dataset("/home/sun/data/model_data/climate/b1850_indian_climate_atmosphere3.nc").sel(lev=lev)

        # 计算区域平均
        prect_con  =  data_resolve.cal_regional_average(f1.sel(lat=slice(prect_lat[0],prect_lat[1]),lon=slice(90,100)).PRECT)
        prect_id   =  data_resolve.cal_regional_average(f2.sel(lat=slice(prect_lat[0],prect_lat[1]),lon=slice(90,100)).PRECT)
        v_con      =  data_resolve.cal_regional_average(f1.sel(lat=slice(-5,5),lon=slice(80,90)).V)
        v_id       =  data_resolve.cal_regional_average(f2.sel(lat=slice(-5,5),lon=slice(80,90)).V)

        # 计算侯平均
        pentad_avg  =  np.zeros((4,73),dtype=np.float32)
        for i in range(73):
            pentad_avg[0,i]  =  np.average(prect_con[i*5:(i*5+5)],axis=0)
            pentad_avg[1,i]  =  np.average(prect_id[i*5:(i*5+5)],axis=0)
            pentad_avg[2,i]  =  np.average(v_con[i*5:(i*5+5)],axis=0)
            pentad_avg[3,i]  =  np.average(v_id[i*5:(i*5+5)],axis=0)

        return pentad_avg
    

def set_pic_ticks(
    ax,xticks,yticks,
    xlabels,ylabels,
    xlim,ylim,
    x_minorspace=5,y_minorspace=5,
    labelsize=20,axis='both',
    ):
    from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,AutoMinorLocator)
    # 设置tick
    ax.set_xticks(xticks)
    ax.set_yticks(yticks)
    # 设置tick_label
    ax.set_xticklabels(xlabels)
    ax.set_yticklabels(ylabels)
    # 设置最小刻度 默认为1
    ax.xaxis.set_minor_locator(MultipleLocator(x_minorspace))
    ax.yaxis.set_minor_locator(MultipleLocator(y_minorspace))

    # 设置labelsize大小
    ax.tick_params(axis=axis,labelsize=labelsize)

    # 设置范围
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)

def paint_pic_cross(somali,bob,prect,path_out,filename,date):
    '''绘制图片，这里不同年份的分开画'''
    fig, ax = plt.subplots(figsize=(13,10))
    xticks = [1,10,20,30,40,50,60,70]
    set_pic_ticks(ax=ax,xticks=xticks,yticks=np.linspace(-6,10,9,dtype=int),xlabels=xticks,ylabels=np.linspace(-6,10,9,dtype=int),xlim=(1,73),ylim=(-6,11),labelsize=25)


    ax.plot(np.linspace(1,73,73,dtype=int),somali,label="Somali jet",color='#c0504d',linewidth=4.5)
    ax.plot(np.linspace(1,73,73,dtype=int),bob,label="BOB jet",color='#8064a2',linewidth=4.5)

    # 参考线
    ax.plot([1,73],[0,0],'k--')
    ax.plot([1,73],[2,2],'r--')
    ax.plot([date,date],[-6,14],'k--')

    # 图例
    ax.legend(loc='upper left',prop={'size': 25},labelcolor='linecolor')

    # 绘制降水
    ax2  =  ax.twinx()

    ax2.set_ylim((0,19))

    ax2.set_yticks(np.arange(0,19,3))
    ax2.set_yticklabels(np.arange(0,19,3),fontsize=25)

    ax2.yaxis.label.set_color('#9bbb59')
    ax2.tick_params(axis='y', colors='#9bbb59')
    ax2.spines['right'].set_color('#9bbb59')
    ax2.spines['right'].set_lw(2)

    ax2.plot(np.linspace(1,73,73),prect,color='#9bbb59',alpha=1,linewidth=4.5)

    save_fig(path_out=path_out,file_out=filename)

def paint_geo_force():
    '''本函数绘制一张图，即控制实验和敏感性实验之间的气压梯度力差值，这里选用四月的平均'''
    # 读取文件
    result_file  =  "/home/sun/data/model_data/process/geopotential_height_gradient_con_id_b1850.nc"
    f0  =  xr.open_dataset(result_file).sel(lev=925,time=slice(90,120),lat=slice(-10,35),lon=slice(40,120))

    # 绘制图像
    proj    =  ccrs.PlateCarree()
    fig,ax   =  plt.subplots(figsize=(13,10),subplot_kw=dict(projection=ccrs.PlateCarree()))
    
    # 范围设置
    lonmin,lonmax,latmin,latmax  =  45,115,-10,30
    extent     =  [lonmin,lonmax,latmin,latmax]
    # 刻度设置
    set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(50,110,4,dtype=int),yticks=np.linspace(-10,30,5,dtype=int),nx=1,ny=1,labelsize=25)

    # 绘制赤道线
    ax.plot([40,120],[0,0],'--',color='k')

    # 绘制气温等值线
    im  =  ax.contourf(f0.lon,f0.lat,-1e6*(np.average(f0.gradient_y_id,axis=0)-np.average(f0.gradient_y_con,axis=0)),np.linspace(-300,300,21),cmap=create_ncl_colormap("/home/sun/data/color_rgb/GMT_polar.txt",20),alpha=1,extend='both')
    # 绘制海岸线
    ax.coastlines(resolution='110m',lw=1)


    # 加序号
    #add_text(ax=ax,string="(d)",fontsize=20)
    # colorbar
    a = fig.colorbar(im,shrink=0.6, pad=0.05,orientation='horizontal')
    a.ax.tick_params(labelsize=15)
    # 保存图片
    save_fig(path_out="/home/sun/paint/lunwen/version4.0/",file_out="lunwen_fig10_v4.0_geo_deff.pdf")
    
def paint_cross_model(con_cross,noid_cross,con_prect,noid_prect,path_out,filename,cv1=5,date1=15,date2=30):
    '''绘制图片，这里不同年份的分开画'''
    fig, ax = plt.subplots(figsize=(13,10))
    xticks = [1,10,20,30,40,50,60,70]
    set_pic_ticks(ax=ax,xticks=xticks,yticks=np.linspace(-6,10,9,dtype=int),xlabels=xticks,ylabels=np.linspace(-6,10,9,dtype=int),xlim=(1,73),ylim=(-6,11),labelsize=30)
    ax.plot(np.linspace(1,73,73,dtype=int),np.convolve(con_cross,np.ones(cv1)/cv1,mode='same'),label="CTRL",color='#c0504d',linewidth=2.5)
    ax.plot(np.linspace(1,73,73,dtype=int),np.convolve(noid_cross,np.ones(cv1)/cv1,mode='same'),label="NO_INDO",color='#c0504d',linewidth=2.5,ls='--')
    # 参考线
    ax.plot([1,73],[0,0],'k--')
    ax.plot([date1,date1],[-6,14],'k--')
    ax.plot([date2,date2],[-6,14],'k--')
    # 图例
    ax.legend(loc='upper right',prop={'size': 25},labelcolor='k')
    # 绘制降水
    ax2  =  ax.twinx()
    ax2.set_ylim((0,19))
    ax2.set_yticks(np.arange(0,19,3))
    ax2.set_yticklabels(np.arange(0,19,3),fontsize=30)
    ax2.yaxis.label.set_color('#9bbb59')
    ax2.tick_params(axis='y', colors='#9bbb59')
    ax2.spines['right'].set_color('#9bbb59')
    ax2.spines['right'].set_lw(2)
    ax2.plot(np.linspace(1,73,73),np.convolve(con_prect*86400*1000,np.ones(cv1)/cv1,mode='same'),color='#9bbb59',alpha=1,linewidth=2.5)
    ax2.plot(np.linspace(1,73,73),np.convolve(noid_prect*86400*1000,np.ones(cv1)/cv1,mode='same'),color='#9bbb59',alpha=1,linewidth=2.5,ls='--')
    save_fig(path_out=path_out,file_out=filename)

                                                                

def main():
    start = time.time()

    #data_resolve.integration_result()
    ## 读取文件
    #file  =  xr.open_dataset(data_resolve.end_path + data_resolve.file_name)
#
    #paint_pic_cross(somali=file.climate.data[0],bob=file.climate.data[1],prect=file.climate.data[2],path_out="/home/sun/paint/lunwen/version4.0/",filename="lunwen_fig8_v4.0_climate_cross_prect_pentad.pdf",date=25)
    #paint_pic_cross(somali=file.early.data[0],bob=file.early.data[1],prect=file.early.data[2],path_out="/home/sun/paint/lunwen/version4.0/",filename="lunwen_fig8_v4.0_early_cross_prect_pentad.pdf",date=21)
    #paint_pic_cross(somali=file.late.data[0],bob=file.late.data[1],prect=file.late.data[2],path_out="/home/sun/paint/lunwen/version4.0/",filename="lunwen_fig8_v4.0_late_cross_prect_pentad.pdf",date=26)
    
    data_resolve.save_and_read_geo_force_ncfile()
    paint_geo_force()
    model_index  =  data_resolve.model_cross_index()

    paint_cross_model(con_cross=model_index[2],noid_cross=model_index[3],con_prect=model_index[0],noid_prect=model_index[1],path_out="/home/sun/paint/lunwen/version4.0/",filename="lunwen_fig10_v4.0_model_cross_prect_pentad.pdf",date1=10,date2=35)






    end = time.time()
    print('\n')
    print('Running time: %s Seconds'%(end-start))


if __name__ == "__main__":
    main()