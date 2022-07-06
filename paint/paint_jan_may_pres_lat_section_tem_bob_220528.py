'''
2022-5-28
本代码绘制一月至五月的BOB地区气温的垂直-经向剖面图
'''
import os
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt


def cal_monthly_lat_pres_avg(lon_slice=slice(80,100),lat_slice=slice(-10,30),lev_slice=slice(1000,200)):
    '''计算1-5月的月平均'''

    # 获取列表信息
    path       =  "/home/sun/qomo-data/year_mean/multi/"
    file_list  =  os.listdir(path) ; file_list.sort() 
    months     =  [1,2,3,4,5]
    f0         =  xr.open_dataset(path+file_list[5]).isel(time=0).sel(lon=lon_slice,lat=lat_slice,lev=lev_slice).T.mean(dim='lon')

    # base array
    base_array =  np.zeros((len(months)*30,len(f0.lev),len(f0.lat)),dtype=np.float32)
    for i in range(len(months)*30):
        base_array[i]  =  xr.open_dataset(path+file_list[i]).sel(lon=lon_slice,lat=lat_slice,lev=lev_slice).isel(time=0).T.mean(dim='lon')
    #print(base_array.shape)

    # monthly average
    month_average  =  np.zeros((5,len(f0.lev),len(f0.lat)),dtype=np.float32)
    for i in range(5):
        month_average[i]  =  np.average(base_array[i*30:i*30+30],axis=0)

    return month_average,f0

def paint_gradient(f0,tem_avg,pathout,fileout):
    import matplotlib.pyplot as plt
    import numpy as np
    import sys

    sys.path.append("/home/sun/mycode/module/paint")
    import paint_lunwen_version3_0_fig1_bob_onset_seris as plv3
    from paint_lunwen_version3_0_fig2a_tem_gradient_20220426 import create_label_lat

    fig, axs = plt.subplots(figsize=(13,10))

    im  =  axs.contour(f0.lat,f0.lev,tem_avg,levels=np.linspace(220,300,17),colors='k',linewidths=2.34)
    axs.clabel(im, inline=1, fontsize=20,inline_spacing=20)
    
    axs.set_xticks(np.linspace(-10,30,5))
    axs.set_xticklabels(create_label_lat(np.linspace(-10,30,5)))

    plv3.set_pic_ticks(axs,xticks=np.linspace(-10,30,5,dtype=int),yticks=np.linspace(1000,200,5,dtype=int),
    xlabels=create_label_lat(np.linspace(-10,30,5,dtype=int)),ylabels=np.linspace(1000,200,5,dtype=int),
    x_minorspace=5,y_minorspace=40,labelsize=23
    ,axis_labelsize=20
    )
    

    plt.gca().invert_yaxis()
    path_out = pathout ; plv3.check_path(path_out)
    file_out = fileout
    plt.savefig(path_out+file_out,dpi=450)

def main():
    month_average,f0  =  cal_monthly_lat_pres_avg()
    paint_gradient(f0,month_average[0],pathout="/home/sun/paint/monthly_tem_pres_lat_section/",fileout="jan_tem_cross_section.pdf")
    paint_gradient(f0,month_average[1],pathout="/home/sun/paint/monthly_tem_pres_lat_section/",fileout="feb_tem_cross_section.pdf")
    paint_gradient(f0,month_average[2],pathout="/home/sun/paint/monthly_tem_pres_lat_section/",fileout="mar_tem_cross_section.pdf")
    paint_gradient(f0,month_average[3],pathout="/home/sun/paint/monthly_tem_pres_lat_section/",fileout="apr_tem_cross_section.pdf")
    paint_gradient(f0,month_average[4],pathout="/home/sun/paint/monthly_tem_pres_lat_section/",fileout="may_tem_cross_section.pdf")


if __name__ == "__main__":
    main()   

    