'''
2022-4-30
本代码绘制论文version3.0中的fig6
内容为2m风、海表感热、相对涡度
出版标准
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
from paint_lunwen_version3_0_fig2b_2m_tem_wind_20220426 import set_cartopy_tick,save_fig,add_vector_legend
from paint_lunwen_version3_0_fig2a_tem_gradient_20220426 import add_text

class number_date:
    '''定义一个日期序号类'''
    dates  =  [-6,-4,-2,0]
    date   =  [24,26,28,30]
    number =  ["a","b","c","d"]

def paint_pic(extent,f2_lon,f2_lat,sh,f1_lon,f1_lat,vorticity,u,v):
    from matplotlib import cm
    from matplotlib.colors import ListedColormap, LinearSegmentedColormap

    # colormap设置
    viridis = cm.get_cmap('Reds', 22)
    newcolors = viridis(np.linspace(0, 1, 22))
    newcmp = ListedColormap(newcolors)
    newcmp.set_under('white')
    newcmp.set_over('#660036')

    # 设置画布
    proj    =  ccrs.PlateCarree()
    fig1    =  plt.figure(figsize=(26,17))
    spec1   =  fig1.add_gridspec(nrows=2,ncols=2)

    j  =  0
    # 绘画
    for col in range(2):
        for row in range(2):
            ax  =  fig1.add_subplot(spec1[row,col],projection=proj)

            # 设置刻度
            set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(50,110,4,dtype=int),yticks=np.linspace(-10,30,5,dtype=int),nx=1,ny=1,labelsize=25)

            # 赤道线
            ax.plot([40,120],[0,0],'k--')


            # 等值线
            im1  =  ax.contourf(f2_lon,f2_lat,-1*sh[number_date.date[j]]/86400,np.linspace(10,24,15),cmap=newcmp,alpha=1,extend='both')
            im2  =  ax.contour(f1_lon,f1_lat,1e6*(vorticity[number_date.date[j],:]),np.linspace(-10,10,6),colors='#4040ff',linewidths=2)
            im3  =  ax.contour(f1_lon,f1_lat,1e6*(vorticity[number_date.date[j],:]),[0],colors='#3636ff',linewidths=4)
            #ax.clabel(im2, np.linspace(-10,10,6).astype(int), inline=True, fontsize=18)

            # 海岸线
            ax.coastlines(resolution='110m',lw=2)

            # 矢量图
            q  =  ax.quiver(f1_lon, f1_lat, u[number_date.date[j],:], v[number_date.date[j],:], 
                regrid_shape=15, angles='uv',   # regrid_shape这个参数越小，是两门就越稀疏
                scale_units='xy', scale=1,        # scale是参考矢量，所以取得越大画出来的箭头就越短
                units='xy', width=0.25,
                transform=proj,
                color='k',linewidth=1.2,headlength = 5, headaxislength = 4, headwidth = 5,alpha=0.8)

            # 加日期
            if number_date.dates[j]<0:
                ax.set_title("D"+str(number_date.dates[j]),loc='right',fontsize=27.5)
            elif number_date.dates[j]>0:
                ax.set_title("D+"+str(number_date.dates[j]),loc='right',fontsize=27.5)
            else:
                ax.set_title("D"+str(number_date.dates[j]),loc='right',fontsize=27.5)
            # 加序号

            ax.set_title("("+number_date.number[j]+")",loc='left',fontsize=27.5)

            # 加矢量图图例
            add_vector_legend(ax=ax,q=q)
            j+=1

    # 加colorbar
    fig1.subplots_adjust(top=0.8) 
    cbar_ax = fig1.add_axes([0.2, 0.05, 0.6, 0.03]) 
    cb  =  fig1.colorbar(im1, cax=cbar_ax, shrink=0.1, pad=0.01, orientation='horizontal')
    cb.ax.tick_params(labelsize=20)

    save_fig(path_out="/home/sun/paint/lunwen/version5.0/",file_out="lunwen_fig6_v3.0_sshf_vorticity_2mwind.pdf")


def cal_vorticity(time,lat,lon,u,v):
    # 坐标
    disy,disx,location = cal_xydistance(lat,lon)

    vx  =  u.copy() ; uy  =  vx.copy()

    # 计算
    for i in range(1,len(lat)-1):
        vx[:,i,:]  =  np.gradient(v[:,i,:],disx[i],axis=1)

    uy  =  np.gradient(u,location,axis=1)

    vorticity       =  vx - uy

    # 打包
    ncfile   =  xr.Dataset(
        {
            "vorticity": (["time","lat","lon"], vorticity),
        },
        coords={
            "lon": (["lon"], lon),
            "lat": (["lat"], lat),
            "time": (["time"], time),
        },
    )   
    return ncfile

def mask_land_sshf(sh,vorticity,time):
    '''把陆地上的感热和相对涡度给屏蔽掉'''
    # 读取mask文件
    f1  =  xr.open_dataset("/home/sun/data/merra2_mask_1x1.nc")
    f2  =  xr.open_dataset("/home/sun/data/erain_mask_land_sea.nc")
    merra_mask    =  f1.mask_1x1.data
    era_mask      =  f2.lsm.data
    for tt in range(sh.shape[0]):
        for i in range(sh.shape[1]):
            for j in range(sh.shape[2]):
                if merra_mask[i,j] > 0.2:
                    vorticity[tt,i,j]  =  np.nan
                if era_mask[0,i,j] > 0.2:
                    sh[tt,i,j]   =  np.nan

    # 打包
    ncfile_nan   =  xr.Dataset(
        { 
            "sh": (["time","f2_lat", "f2_lon"], sh),
            "vorticity": (["time","f1_lat", "f1_lon"], vorticity),
        },
        coords={
            "f1_lon": (["f1_lon"], f1.lon.data),
            "f1_lat": (["f1_lat"], f1.lat.data),
            "f2_lon": (["f2_lon"], f2.longitude.data),
            "f2_lat": (["f2_lat"], f2.latitude.data),
            "time": (["time"], time),
        },
    )

    return ncfile_nan

def main():
    # 划定范围
    lon_slice  =  slice(40,120)
    lat_slice  =  slice(-10,30)
    time_slice =  slice(1,35)

    # 画图范围
    lonmin,lonmax,latmin,latmax  =  45,115,-10,30
    extent     =  [lonmin,lonmax,latmin,latmax]

    # 读取文件
    path  =  "/home/sun/qomo-data/"
    f1  =  xr.open_dataset(path+"composite-merra2-single.nc").sel(time=time_slice)    
    f2  =  xr.open_dataset(path+"composite_shlh.nc").sel(time=time_slice) 

    # 计算涡度 以及 屏蔽陆地感热
    vorticity  =  cal_vorticity(time=f1.time.data,lat=f1.lat.data,lon=f1.lon.data,u=f1.U2M.data,v=f1.V2M.data)
    sshf       =  mask_land_sshf(sh=f2.SSHF.data,vorticity=vorticity.vorticity.data,time=f2.time.data)

    # 画图
    paint_pic(extent=extent,f2_lat=f2.lat,f2_lon=f2.lon,sh=sshf.sh.data,f1_lat=f1.lat,f1_lon=f1.lon,vorticity=sshf.vorticity.data,u=f1.U2M.data,v=f1.V2M.data)


if __name__ == "__main__":
    main()