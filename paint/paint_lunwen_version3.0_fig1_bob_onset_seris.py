# 2022/4/25
# 本代码绘制BOB的时间


import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import metpy.calc as mpcalc
import numpy as np
import xarray as xr
import sys
from matplotlib.ticker import MultipleLocator, FormatStrFormatter


sys.path.append("/home/sun/mycode/module/")
from module_sun import *

def open_onsetdate(file):
    with open(file,'r') as load_f:
        a = json.load(load_f)

    year = np.array(list(a.keys()))    ;  year  =  year.astype(int)
    day  = np.array(list(a.values()))  ;  day   =  day.astype(int)

    return year,day


def select_anomaly_year(day):
    # 筛选 晚年用红色，早年用蓝色
    a  =  np.zeros(40,dtype=int).astype(dtype=str) ; a[:]  =  'grey'
    color_list  =  a.tolist()#  ;  color_list[:]  =  'grey'

    for i in range(0,40):
        if day[i] < np.mean(day) - np.std(day):
            color_list[i]  =  'blue'
        if day[i] > np.mean(day) + np.std(day)-1:
            color_list[i]  =  'red'

    return color_list
        


def set_pic_ticks(
    ax,xticks,yticks,
    xlabels,ylabels,
    x_minorspace=1,y_minorspace=1,
    labelsize='medium',axis='both',
    xaxis_label=None,yaxis_label=None
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

    # 设置坐标轴标签
    ax.set_xlabel(xaxis_label)
    ax.set_ylabel(yaxis_label)


def plot_baseline(axs,day):
    axs.plot([1979,2020],[0,0],color='black')
    axs.plot([1979,2020],[np.ceil(np.mean(day)-np.std(day))-120-1,np.ceil(np.mean(day)-np.std(day))-120-1],color='k',linestyle='dashed')
    axs.plot([1979,2020],[np.floor(np.mean(day)+np.std(day))-120-1,np.floor(np.mean(day)+np.std(day))-120-1],color='k',linestyle='dashed')

def check_path(path):
    # 检查生成的路径是否存在，如果不存在则创建之
    from pathlib import Path
    import os
    path1 = Path(path)
    if path1.exists():
        print("generation path is exists")
    else:
        os.mkdir(path)

def add_legend():
    # 添加legend
    from matplotlib.patches import Patch
    import matplotlib.pyplot as plt

    legend_elements = [
                        Patch(color='grey',label='normal'),
                        Patch(color='blue',label='early'),
                        Patch(color='red',label='late')]
    plt.legend(handles=legend_elements, loc=3,edgecolor='white',facecolor='white',bbox_to_anchor=(0.2, 0.05))                              
    # Patch这个函数我不是很明白，只调用这个函数不会生成什么
    # 得配合legend一起用，可能就是用来生成legend样式的吧？



def main():
    year,day = open_onsetdate("/home/sun/data/onsetdate.json")
    colorlist = select_anomaly_year(day)

    fig,axs  =  plt.subplots(tight_layout=True)

    y_label  =  ['10Apr','20Apr','1May','10May','20May']
    x_label  =  np.arange(1980,2021,10)

    ytick    =  np.arange(-20,25,10)
    xtick    =  np.arange(1980,2021,10)

    set_pic_ticks(axs,xtick,ytick,x_label,y_label,x_minorspace=5,y_minorspace=5,xaxis_label="Year",yaxis_label="BOBSM Onset Date")
    axs.set_xlim(1979,2020)

    axs.bar(year,day-120,width=1,color=colorlist,edgecolor='black')
    plot_baseline(axs,day)
    add_legend()
    plt.show()

    path_out = "/home/sun/paint/lunwen/version3.0/" ; check_path(path_out)
    file_out = "lunwen_fig1_v3.0_bob_time_seris_220425.pdf"
    plt.savefig(path_out+file_out,dpi=450)

if __name__ == "__main__":
    main()