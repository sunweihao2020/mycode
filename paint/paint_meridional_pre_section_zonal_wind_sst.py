'''
created at 2022-7-4
This code is to draw meri-pre section of: zonal wind and SST
Objective is to see the relationship between SST and zonal wind
'''

import os
import numpy as np
import sys
import xarray as xr
import matplotlib.pyplot as plt
sys.path.append("/home/sun/mycode/module/")
sys.path.append("/home/sun/mycode/paint/")
from module_sun import *
import sys
sys.path.append("/home/sun/mycode/paint/")
from paint_lunwen_version3_0_fig2a_tem_gradient_20220426 import add_text
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

path0  =  "/home/sun/qomo-data/"

file1  =  xr.open_dataset('/home/sun/data/composite3.nc').sel(lon=slice(90,100),level=slice(1000,100))
file2  =  xr.open_dataset(path0+"composite_OISST.nc").sel(lon=slice(90,100))

avg_u   =  np.nanmean(file1.uwind,axis=3)
avg_sst =  np.nanmean(file2.SST,axis=2)

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

viridis = cm.get_cmap('coolwarm', 22)
newcolors = viridis(np.linspace(0, 1, 22))
newcmp = ListedColormap(newcolors)
newcmp.set_under('blue')
newcmp.set_over('brown')

def meridional_sst():
    '''This function paint meridional sst from -10 to 40. The purpose is to see the maximum sea temperature'''
    # set figure
    fig1  =  plt.figure(figsize=(34,26))
    spec1 =  fig1.add_gridspec(nrows=3,ncols=3)

    j = 0 ; start = 30
    #start = 21
    for col in range(3):
        for row in range(3):
            ax  =  fig1.add_subplot(spec1[row,col])

            # set axis ticks and label
            ax.set_xticks(np.linspace(-10,30,9,dtype=int))
            ax.set_yticks(np.linspace(28,31,7))

            ax.set_xticklabels(generate_xlabel(np.linspace(-10,30,9,dtype=int)))
            ax.tick_params(axis='both',labelsize=22.5)

            # plot sst
            ax.plot(file2.lat.data,avg_sst[start],linewidth=3,color='red',label="SST")

            # set range
            ax.set_xlim((-10,30))
            ax.set_ylim((28,31))

            # set axis label
            ax.set_xlabel("Latitude",fontsize=18)
            ax.set_ylabel("SST(90-100E average)",fontsize=18)

            # add date
            add_text(ax=ax, string="D" + str(start-30), location=(0.05, 0.91), fontsize=30)

            # add legend
            plt.legend(loc='lower right', prop={'size': 20})
            # plot air temperature at 925 850 700hPa
            # second axis
            ax2  =  ax.twinx()

            ax2.plot(file1.lat.data,avg_u[start,0],linewidth=3,label="925hpa")
            ax2.plot(file1.lat.data, avg_u[start, 1],linewidth=2.5,label="850hpa")
            ax2.plot(file1.lat.data, avg_u[start, 2],linewidth=3,label="700hpa")

            ax2.tick_params(axis='both', labelsize=22.5)

            plt.legend(loc='upper right',prop={'size': 20})

            start += 1


    plt.savefig('/home/sun/paint/meridional_tem_gradient_circulation/meridional_sst_0to+8.pdf', dpi=400)
    plt.show()
    #plt.plot(file2.lat.data,avg_sst[15])
    #plt.xlim([-10,30])
    #plt.ylim([27,31])
    #plt.show()

def meridional_section_uwind():
    # set figure
    fig1 = plt.figure(figsize=(30, 26))
    spec1 = fig1.add_gridspec(nrows=3, ncols=3)
    j = 0;
    start = 21
    for col in range(3):
        for row in range(3):
            ax = fig1.add_subplot(spec1[row, col])
            # set axis ticks and label
            ax.set_xticks(np.linspace(-10, 30, 9, dtype=int))
            ax.set_yticks(np.linspace(1000, 100, 10))
            ax.set_xticklabels(generate_xlabel(np.linspace(-10, 30, 9, dtype=int)))
            ax.tick_params(axis='both', labelsize=22.5)
            # plot sst
            im = ax.contourf(file1.lat.data, file1.level.data,avg_u[start],np.linspace(-15,15,21),cmap=newcmp,extend='both')
            # set range
            ax.set_xlim((-10, 30))
            #ax.set_ylim((28, 31))
            # set axis label
            ax.set_xlabel("Latitude", fontsize=18)
            ax.set_ylabel("uwind (90-100E average)", fontsize=18)
            # add date
            add_text(ax=ax, string="D" + str(start - 30), location=(0.05, 0.91), fontsize=30)
            # plot air temperature at 925 850 700hPa
            # second axis
            ax.invert_yaxis()

            start += 1
            plt.gca().set_facecolor("black")

    fig1.subplots_adjust(top=0.8)
    cbar_ax = fig1.add_axes([0.2, 0.05, 0.6, 0.03])
    cb = fig1.colorbar(im, cax=cbar_ax, shrink=0.1, pad=0.01, orientation='horizontal')
    cb.ax.tick_params(labelsize=25)

    plt.savefig('/home/sun/paint/meridional_tem_gradient_circulation/meridional_uwind_90to100_-9to-1.pdf', dpi=400)
    plt.show()

def main():
    meridional_section_uwind()
    #meridional_sst()

if __name__ == "__main__":
    main()
