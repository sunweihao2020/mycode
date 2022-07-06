'''
2022/4/26
本代码绘制论文version3.0的图2a
内容为温度的lat-pressure剖面
'''

from matplotlib.pyplot import xlabel


def xarray_read_file(path,file,range_lat=None,range_lon=None,range_lev=None):
    # 读取nc文件，同时划定范围
    import xarray as xr
    if range_lev == None:
        f0  =  xr.open_dataset(path+file).sel(lat=range_lat,lon=range_lon)
    else:
        f0  =  xr.open_dataset(path+file).sel(lat=range_lat,lon=range_lon,level=range_lev)

    return f0

def create_label_lat(array):
    lat_label = []
    for llat in array:
        if llat < 0:
            lat_label.append(u''+str(llat)+"\N{DEGREE SIGN}S")
        elif llat > 0:
            lat_label.append(u''+str(llat)+"\N{DEGREE SIGN}N")
        else:
            lat_label.append("EQ")
    
    return lat_label

def add_text(ax,string,props=dict(boxstyle='square', edgecolor='white', facecolor='white', alpha=1),location=(0.05,0.9),fontsize=15):
    
    ax.text(location[0],location[1],string,transform=ax.transAxes,bbox=props,fontsize=fontsize)


def paint_gradient(f0,tem_avg):
    import matplotlib.pyplot as plt
    import numpy as np
    import sys

    sys.path.append("/home/sun/mycode/module/paint")
    import paint_lunwen_version3_0_fig1_bob_onset_seris as plv3

    fig, axs = plt.subplots(figsize=(13,10))

    im  =  axs.contour(f0.lat,f0.level,tem_avg,levels=np.linspace(220,300,17),colors='k',linewidths=2.34)
    axs.clabel(im, inline=1, fontsize=20,inline_spacing=20)
    
    axs.set_xticks(np.linspace(-10,30,5))
    axs.set_xticklabels(create_label_lat(np.linspace(-10,30,5)))

    plv3.set_pic_ticks(axs,xticks=np.linspace(-10,30,5,dtype=int),yticks=np.linspace(1000,200,5,dtype=int),
    xlabels=create_label_lat(np.linspace(-10,30,5,dtype=int)),ylabels=np.linspace(1000,200,5,dtype=int),
    x_minorspace=5,y_minorspace=40,labelsize=23
    ,axis_labelsize=20
    )
    

    #add_text(axs,location=(0.015,0.945),string='(a)',fontsize=27.5)

    plt.gca().invert_yaxis()
    path_out = "/home/sun/paint/lunwen/version3.0/" ; plv3.check_path(path_out)
    file_out = "lunwen_fig2a_v3.0_tem_gradient_220426.pdf"
    plt.savefig(path_out+file_out,dpi=450)


def main():
    import numpy as np
    import matplotlib.pyplot as plt


    path = '/home/sun/qomo-data/'
    file = 'composite3.nc'

    f0      = xarray_read_file(path,file,range_lat=slice(-10,30),range_lev=slice(1000,200),range_lon=slice(80,100))
    tem_avg =  np.average(np.nanmean(f0.T.data[0:30,:],axis=3),axis=0)

    paint_gradient(f0,tem_avg)





if __name__ == "__main__":
    main()