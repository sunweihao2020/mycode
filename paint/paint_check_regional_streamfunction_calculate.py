'''
2022-8-3
This script is used to check regional meridional stream function I calculated
'''
import os
import numpy as np
import sys
import xarray as xr
import matplotlib.pyplot as plt
sys.path.append("/Users/sunweihao/mycode/paint")
from matplotlib import cm
from matplotlib.colors import ListedColormap
from paint_lunwen_version3_0_fig2a_tem_gradient_20220426 import add_text


src_path   =  '/Users/sunweihao/ubuntu-server-data/composite/'

src_file   =  'composite_calculate_regional_streamfunction_zonal_meridional_220804.nc'

file0  =  xr.open_dataset(src_path + src_file) #The dimension is (61,42,361)
print(file0)

viridis = cm.get_cmap('coolwarm', 30)
newcolors = viridis(np.linspace(0, 1, 30))
newcmp = ListedColormap(newcolors)
newcmp.set_under('blue')
newcmp.set_over('brown')

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

def generate_lonlabel(array):
    '''this function generate labels for lon direction'''
    labels = []
    for i in array:
        if i<0:
            labels.append(str(abs(i))+"W")
        elif i>0:
            labels.append(str(i)+"E")
        else:
            labels.append("0")
    return labels


def paint_meridional_stream():
    # set figure
    fig1 = plt.figure(figsize=(32, 26))
    spec1 = fig1.add_gridspec(nrows=3, ncols=3)
    j = 0
    start = 15

    for col in range(3):
        for row in range(3):
            ax  =  fig1.add_subplot(spec1[row, col])

            # set axis ticks and label
            ax.set_xticks(np.linspace(-10, 30, 9, dtype=int))
            ax.set_yticks(np.linspace(1000, 100, 10))
            ax.set_xticklabels(generate_xlabel(np.linspace(-10, 30, 9, dtype=int)))
            ax.tick_params(axis='both', labelsize=22.5)

            # plot streamfunction
            im    = ax.contourf(file0.lat.data, file0.lev.data,file0.meridional_streamfunction.data[start]/1e11,levels = np.linspace(-3,3,25),cmap=newcmp,extend='both')

            # set range
            ax.set_xlim((-10,30))

            # set axis label
            ax.set_xlabel("Latitude", fontsize=18)
            ax.set_ylabel("MPSI (90-100E average)", fontsize=18)

            # add date
            add_text(ax=ax, string="D" + str(start - 30), location=(0.05, 0.91), fontsize=30)

            # invert y axis
            ax.invert_yaxis()

            # fill nan value
            plt.gca().set_facecolor("black")

            start += 1

            print(start)
    
    fig1.subplots_adjust(top=0.8)
    cbar_ax = fig1.add_axes([0.2, 0.05, 0.6, 0.03])
    cb = fig1.colorbar(im, cax=cbar_ax, shrink=0.1, pad=0.01, orientation='horizontal')
    cb.ax.tick_params(labelsize=25)

    plt.savefig('/Users/sunweihao/paint/circulation_based_on_composite_result/meridional_st_90to100_check.pdf', dpi=400)
    plt.show()

def paint_zonal_stream():
    # set figure
    fig1 = plt.figure(figsize=(32, 26))
    spec1 = fig1.add_gridspec(nrows=3, ncols=3)
    j = 0
    start = 25

    for col in range(3):
        for row in range(3):
            ax  =  fig1.add_subplot(spec1[row, col])

            # set axis ticks and label
            ax.set_xticks(np.linspace(30, 120, 10, dtype=int))
            ax.set_yticks(np.linspace(1000, 100, 10))
            ax.set_xticklabels(generate_lonlabel(np.linspace(30, 120, 10, dtype=int)))
            ax.tick_params(axis='both', labelsize=22.5)

            # plot streamfunction
            im    = ax.contourf(file0.lon.data, file0.lev.data,file0.zonal_streamfunction.data[start]/1e11,np.linspace(-4,4,33),cmap=newcmp,extend='both')

            # set range
            ax.set_xlim((30,120))

            # set axis label
            ax.set_xlabel("Longitude", fontsize=18)
            ax.set_ylabel("MPSI (10-15N average)", fontsize=18)

            # add date
            add_text(ax=ax, string="D" + str(start - 30), location=(0.05, 0.91), fontsize=30)

            # invert y axis
            ax.invert_yaxis()

            # fill nan value
            plt.gca().set_facecolor("black")

            start += 1

            print(start)
    
    fig1.subplots_adjust(top=0.8)
    cbar_ax = fig1.add_axes([0.2, 0.05, 0.6, 0.03])
    cb = fig1.colorbar(im, cax=cbar_ax, shrink=0.1, pad=0.01, orientation='horizontal')
    cb.ax.tick_params(labelsize=25)

    plt.savefig('/Users/sunweihao/paint/circulation_based_on_composite_result/zonal_st_10to15_check.pdf', dpi=400)
    plt.show()


def main():
    paint_zonal_stream()


if __name__ == "__main__":
    main()
