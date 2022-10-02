'''
2022-9-24
本代码绘制论文version3.0中的fig7
内容为对涡度收支方程的分解
出版标准

审稿人意见：图太脏了不清晰，所以我想办法让它清晰一点
'''
import sys
import xarray as xr
import numpy as np
module_path = ["/home/sun/mycode/module/","/data5/2019swh/mycode/module/"]
sys.path.append(module_path[0])
from module_sun import *
import cartopy.crs as ccrs
import matplotlib.pyplot as plt


sys.path.append("/home/sun/mycode/paint/")
from paint_lunwen_version3_0_fig2b_2m_tem_wind_20220426 import set_cartopy_tick,save_fig
from paint_lunwen_version3_0_fig2a_tem_gradient_20220426 import add_text
from paint_lunwen_version3_0_fig6_2mwind_sshf_vorticity import cal_vorticity

class number_date:
    '''定义一个日期序号类'''
    dates  =  [-2,0]
    date   =  [28,30]
    number1 =  ["a","b"]
    number2 =  ["c","d","e",'f','g','h']

class location:
    loc_a  =  0.018
    loc_b  =  0.89

    height = 0.9

def data_handle():
    
    # 读取数据
    f1   =  xr.open_dataset("/home/sun/qomo-data/composite-single_merra2_stream_vp_function.nc")
    f2   =  xr.open_dataset("/home/sun/qomo-data/composite-merra2-single.nc")

    disy,disx,location = cal_xydistance(f1.lat,f1.lon)

    # 计算涡度
    vorticity  =  cal_vorticity(time=f2.time.data,lat=f2.lat.data,lon=f2.lon.data,u=f2.U2M.data,v=f2.V2M.data)

    # 计算旋转风
    u_vor  =  np.gradient(f1.stream_function,location,axis=1)*-1
    v_vor  =  np.zeros(f1.stream_function.shape)
    for i in range(1,len(f1.lat)-1):
        v_vor[:,i,:]  =  np.gradient(f1.stream_function[:,i,:],disx[i],axis=1)

    # 计算f
    sinlat = np.array([]) #生成科里奥利力数组
    for ll in f1.lat:
        sinlat = np.append(sinlat,math.sin(math.radians(ll)))
    omega = 7.29e-5
    ff = 2*omega*sinlat

    # 计算涡度拉普拉斯项

    absolute_vorticity  =  vorticity.vorticity.data.copy()
    for i in range(absolute_vorticity.shape[0]):
        for j in range(absolute_vorticity.shape[2]):
            absolute_vorticity[i,:,j]  =  absolute_vorticity[i,:,j] + ff

    d_abs_vor_x  =  np.zeros(f1.stream_function.shape)
    for i in range(1,len(f1.lat)-1):
        d_abs_vor_x[:,i,:]  =  np.gradient(absolute_vorticity[:,i,:],disx[i],axis = 1)
    d_abs_vor_y  =  np.gradient(absolute_vorticity,location,axis=1)


    # 计算散度风
    u_div  =  np.zeros(f1.stream_function.shape)
    v_div  =  np.gradient(f1.velocity_potential_function,location,axis=1)
    for i in range(1,len(f1.lat)-1):
        u_div[:,i,:]  =  np.gradient(f1.velocity_potential_function[:,i,:],disx[i],axis=1)

    # 计算beta项
    beta  =  np.zeros(f1.stream_function.shape)
    for i in range(beta.shape[0]):
        for j in range(beta.shape[2]):
            beta[i,:,j]  =  np.gradient(ff,location)

    # 计算散度
    v_div_y  =  np.gradient(v_div,location,axis=1)
    u_div_x  =  np.zeros(f1.stream_function.shape)
    for i in range(1,len(f1.lat)-1):
        u_div_x[:,i,:]  =  np.gradient(u_div[:,i,:],disx[i],axis=1)

    div  =  v_div_y  +  u_div_x

    dates  =  np.linspace(1,35,35)

    # term1
    d_vor_d_t  =  np.gradient(vorticity.vorticity.data,dates,axis=0)

    # term2
    v_vor_m_abs_vor_gradient  =  d_abs_vor_x * u_vor + d_abs_vor_y * v_vor

    # term2 decompose
    ## 相对涡度laplace项
    d_relative_vor_y  =  np.gradient(vorticity.vorticity.data,location,axis=1)
    d_relative_vor_x  =  np.zeros(f1.stream_function.shape)
    for i in range(1,len(f1.lat)-1):
        d_relative_vor_x[:,i,:]  =  np.gradient(vorticity.vorticity.data[:,i,:],disx[i],axis = 1)
    ## 流函数对相对涡度的平流
    stream_velocity_laplace_relative_vorticity  =  u_vor * d_relative_vor_x  +  v_vor * d_relative_vor_y

    ## 流函数对地转涡度的平流
    stream_velocity_laplace_geostropic_velocity =  v_vor * beta



    # term3
    v_div_m_beta  =  v_div * beta


    # term3 decompose
    ## 辐散风对相对涡度的平流
    divergent_velocity_laplace_relative_vorticity  =  u_div * d_relative_vor_x  +  v_div * d_relative_vor_y

    ## 辐散风对地转涡度的平流
    divergent_velocity_laplace_geostropic_velocity =  v_div * beta

    # term4
    f_div  =  np.zeros(f1.stream_function.shape)
    for i in range(f_div.shape[0]):
        for j in range(f_div.shape[2]):
            f_div[i,:,j]  =  ff * div[i,:,j]
      

    # term5
    v_div_m_abs_vor_gradient  =  d_abs_vor_x * u_div + d_abs_vor_y * v_div


    # 打包
    ncfile   =  xr.Dataset(
        { 
            "absolute_vorticity": (["time","lat", "lon"], absolute_vorticity),
            "vorticity": (["time","lat", "lon"], vorticity.vorticity.data),
            "d_vor_dt": (["time","lat", "lon"], d_vor_d_t),
            "v_vor_m_abs_vor_gradient": (["time","lat","lon"], v_vor_m_abs_vor_gradient*86400),
            "divergent_velocity_laplace_relative_vorticity": (["time","lat","lon"], divergent_velocity_laplace_relative_vorticity*86400),
            "divergent_velocity_laplace_relative_vorticity_x": (["time","lat","lon"],  u_div * d_relative_vor_x*86400),
            "divergent_velocity_laplace_relative_vorticity_y": (["time","lat","lon"],  v_div * d_relative_vor_y*86400),
            "divergent_velocity_laplace_geostropic_vorticity": (["time","lat","lon"], divergent_velocity_laplace_geostropic_velocity*86400),
            "stream_velocity_laplace_geostropic_vorticity": (["time","lat","lon"], stream_velocity_laplace_geostropic_velocity*86400),
            "stream_velocity_laplace_relative_vorticity": (["time","lat","lon"], stream_velocity_laplace_relative_vorticity*86400),
            "stream_velocity_laplace_relative_vorticity_x": (["time","lat","lon"],  u_vor * d_relative_vor_x*86400),
            "stream_velocity_laplace_relative_vorticity_y": (["time","lat","lon"],  v_vor * d_relative_vor_y*86400),
            "f_div": (["time","lat","lon"], f_div*86400),
            "v_div_m_abs_vor_gradient": (["time","lat","lon"], v_div_m_abs_vor_gradient*86400),
        },
        coords={
            "lon": (["lon"], f1.lon.data),
            "lat": (["lat"], f1.lat.data),
            "time": (["time"], f1.time.data),
        },
    )

    return ncfile
    

def paint_dvdt(extent,lon,lat,d_vor_dt):
    # 绘制涡度的倾向项
    proj    =  ccrs.PlateCarree()
    fig1    =  plt.figure(figsize=(21,6))
    spec1   =  fig1.add_gridspec(nrows=1,ncols=2)

    j = 0

    # mask the value over land
    mask_file  =  xr.open_dataset('/home/sun/qomo-data/merra2_land_sea_mask_low_resolution.nc')
    mask       =  mask_file["ocean_fraction"].data
    print(mask.shape)
    

    for col in range(2):
        ax  =  fig1.add_subplot(spec1[0,col],projection=proj)

        # data
        dvdt2  =  d_vor_dt[number_date.date[j]].data/86400*1e10
        dvdt2[mask<0.5]  =  np.nan

        # 设置刻度
        set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(50,110,4,dtype=int),yticks=np.linspace(-10,30,5,dtype=int),nx=1,ny=1)

        # 赤道线
        ax.plot([40,120],[0,0],'k--')

        # 等值线
        im1  =  ax.contour(lon,lat,dvdt2,[0],linewidths=1.8,colors='k')  # 这里我除以86400因为原本的是一天的涡度变化量
        im2  =  ax.contourf(lon,lat,dvdt2,np.linspace(-1,1,11),cmap=create_ncl_colormap("/home/sun/data/color_rgb/GMT_polar.txt",20),alpha=1,extend='both')
        ax.coastlines(resolution='110m',lw=1.1)

        # 加日期
        # add_text(ax,string="D"+str(number_date.dates[j]),location=(location.loc_b,location.height),fontsize=25)
        ax.set_title("D"+str(number_date.dates[j]),loc='right',fontsize=20)
        # 加序号
        #add_text(ax=ax,string="("+number_date.number1[j]+")",location=(location.loc_a,location.height),fontsize=25)
        ax.set_title("("+number_date.number1[j]+")",loc='left',fontsize=20)

        j += 1

    # 加colorbar
    fig1.subplots_adjust(left=0.2) 
    cbar_ax = fig1.add_axes([0.93, 0.2, 0.01, 0.6]) 
    cb  =  fig1.colorbar(im2, cax=cbar_ax, shrink=0.1, pad=0.01)
    cb.ax.tick_params(labelsize=20)

    save_fig(path_out="/home/sun/paint/lunwen/version4.0/",file_out="lunwen_fig7_v4.0_dv_dt_1.pdf")


def paint_other_term(extent,ncfile):
    # 绘制涡度的倾向项
    proj    =  ccrs.PlateCarree()
    fig1    =  plt.figure(figsize=(21,17.3))
    spec1   =  fig1.add_gridspec(nrows=3,ncols=2)

    # mask the value over land
    mask_file  =  xr.open_dataset('/home/sun/qomo-data/merra2_land_sea_mask_low_resolution.nc')
    mask       =  mask_file["ocean_fraction"].data
    print(mask.shape)

    clev = np.linspace(-2,2,11)

    j = 0
    for col in range(2):
        # data
        fdiv  =  ncfile.f_div[number_date.date[j]].data*-1e5
        fdiv[mask<0.5]  =  np.nan

        ax  =  fig1.add_subplot(spec1[0,col],projection=proj)
        # 设置刻度
        set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(50,110,4,dtype=int),yticks=np.linspace(-10,30,5,dtype=int),nx=1,ny=1)
        # 赤道线
        ax.plot([40,120],[0,0],'k--')
        # 等值线
        im1  =  ax.contour(ncfile.lon,ncfile.lat,fdiv,[0],linewidths=1.8,colors='k')
        im2  =  ax.contourf(ncfile.lon,ncfile.lat,fdiv,clev,cmap=create_ncl_colormap("/home/sun/data/color_rgb/GMT_polar.txt",23),alpha=1,extend='both')
        ax.coastlines(resolution='110m',lw=1.35)
        # 加日期
        # add_text(ax,string="D"+str(number_date.dates[j]),location=(location.loc_b,location.height),fontsize=25)
        ax.set_title("D"+str(number_date.dates[j]),loc='right',fontsize=20)
        # 加序号
        #add_text(ax=ax,string="("+number_date.number1[j]+")",location=(location.loc_a,location.height),fontsize=25)
        ax.set_title("("+number_date.number2[j]+")",loc='left',fontsize=20)

        j += 1


    j = 0
    for col in range(2):
        # data
        vor_gradient  =  ncfile.v_vor_m_abs_vor_gradient[number_date.date[j]].data*-1e5
        vor_gradient[mask<0.5]  =  np.nan

        ax  =  fig1.add_subplot(spec1[1,col],projection=proj)
        # 设置刻度
        set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(50,110,4,dtype=int),yticks=np.linspace(-10,30,5,dtype=int),nx=1,ny=1)
        # 赤道线
        ax.plot([40,120],[0,0],'k--')
        # 等值线
        im1  =  ax.contour(ncfile.lon,ncfile.lat,vor_gradient,[0],linewidths=1.8,colors='k')
        im2  =  ax.contourf(ncfile.lon,ncfile.lat,vor_gradient,clev,cmap=create_ncl_colormap("/home/sun/data/color_rgb/GMT_polar.txt",23),alpha=1,extend='both')
        ax.coastlines(resolution='110m',lw=1.35)
        # 加日期
        # add_text(ax,string="D"+str(number_date.dates[j]),location=(location.loc_b,location.height),fontsize=25)
        ax.set_title("D"+str(number_date.dates[j]),loc='right',fontsize=20)
        # 加序号
        #add_text(ax=ax,string="("+number_date.number1[j]+")",location=(location.loc_a,location.height),fontsize=25)
        ax.set_title("("+number_date.number2[j+2]+")",loc='left',fontsize=20)

        j+= 1

    j = 0
    for col in range(2):
        # data
        div_gradient  =  ncfile.v_div_m_abs_vor_gradient[number_date.date[j]].data*-1e5
        div_gradient[mask<0.5] = np.nan

        ax  =  fig1.add_subplot(spec1[2,col],projection=proj)
        # 设置刻度
        set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(50,110,4,dtype=int),yticks=np.linspace(-10,30,5,dtype=int),nx=1,ny=1)
        # 赤道线
        ax.plot([40,120],[0,0],'k--')
        # 等值线
        im1  =  ax.contour(ncfile.lon,ncfile.lat,div_gradient,[0],linewidths=1.8,colors='k')
        im2  =  ax.contourf(ncfile.lon,ncfile.lat,div_gradient,clev,cmap=create_ncl_colormap("/home/sun/data/color_rgb/GMT_polar.txt",23),alpha=1,extend='both')
        ax.coastlines(resolution='110m',lw=1.35)
        # 加日期
        # add_text(ax,string="D"+str(number_date.dates[j]),location=(location.loc_b,location.height),fontsize=25)
        ax.set_title("D"+str(number_date.dates[j]),loc='right',fontsize=20)
        # 加序号
        #add_text(ax=ax,string="("+number_date.number1[j]+")",location=(location.loc_a,location.height),fontsize=25)
        ax.set_title("("+number_date.number2[j+4]+")",loc='left',fontsize=20)

        j += 1

    # 加colorbar
    fig1.subplots_adjust(left=0.2) 
    cbar_ax = fig1.add_axes([0.93, 0.25, 0.01, 0.5]) 
    cb  =  fig1.colorbar(im2, cax=cbar_ax, shrink=0.1, pad=0.01)
    cb.ax.tick_params(labelsize=20)

    save_fig(path_out="/home/sun/paint/lunwen/version4.0/",file_out="lunwen_fig7_v4.0_dv_dt_2.pdf")






def main():
    path = "/home/sun/qomo-data/"
    f1   =  xr.open_dataset("/home/sun/qomo-data/composite-single_merra2_stream_vp_function.nc")
    f2   =  xr.open_dataset("/home/sun/qomo-data/composite-merra2-single.nc")

    ncfile  =  data_handle()

    # extent
    lonmin,lonmax,latmin,latmax  =  45,115,-10,30
    extent     =  [lonmin,lonmax,latmin,latmax]

    # 绘图
    paint_dvdt(extent=extent,lon=f1.lon.data,lat=f1.lat.data,d_vor_dt=ncfile.d_vor_dt)
    paint_other_term(extent=extent,ncfile=ncfile)


if __name__ == "__main__":
    main()