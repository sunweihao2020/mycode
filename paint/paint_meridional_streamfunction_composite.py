'''
2022-7-6
This code paint regional streamfunction between 90 and 100E. Based on composite ncfile
'''
import os
import numpy as np
import sys
import xarray as xr
import matplotlib.pyplot as plt
sys.path.append("/home/sun/mycode/module/")
sys.path.append("/home/sun/mycode_git/paint/")
from module_sun import *
import sys
from matplotlib import cm
from matplotlib.colors import ListedColormap
from paint_lunwen_version3_0_fig2a_tem_gradient_20220426 import add_text


path0  =  "/home/sun/data/composite/"

file0  =  xr.open_dataset(path0+'zonal_meridional_streamfunction_90to100.nc') #The dimension is (61,31,361)
file1  =  xr.open_dataset(path0+'composite3.nc').sel(level=slice(1000,100))
file2  =  xr.open_dataset(path0+'zonal_meridional_streamfunction_90to100_2.nc')
#print(file0)

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

def interp_mpsi():
    '''The regional meridional stream function does not has 1000hpa, so I need to interp it to 1000'''
    old_lev   =  file2.lev.data/100
    new_level =  file1.level.data[::-1]
    #print(new_level)
    #print(old_lev)
    mpsi_new  =  np.zeros((61,len(new_level),361))
    for dd in range(61):
        for yy in range(361):
            mpsi_new[dd,:,yy]  =  np.interp(new_level,old_lev,file0.MPSI.data[dd,:,yy])

    return mpsi_new



def paint_meridional_stream():
    # set figure
    fig1 = plt.figure(figsize=(32, 26))
    spec1 = fig1.add_gridspec(nrows=3, ncols=3)
    j = 0
    start = 30

    for col in range(3):
        for row in range(3):
            ax  =  fig1.add_subplot(spec1[row, col])

            # set axis ticks and label
            ax.set_xticks(np.linspace(-10, 30, 9, dtype=int))
            ax.set_yticks(np.linspace(1000, 100, 10))
            ax.set_xticklabels(generate_xlabel(np.linspace(-10, 30, 9, dtype=int)))
            ax.tick_params(axis='both', labelsize=22.5)

            # plot streamfunction
            im    = ax.contourf(file0.lat.data, file0.lev.data,file0.meridional_streamfunction.data[j]/1e11,np.linspace(-2.8,2.8,29),cmap=newcmp,extend='both')

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
    
    fig1.subplots_adjust(top=0.8)
    cbar_ax = fig1.add_axes([0.2, 0.05, 0.6, 0.03])
    cb = fig1.colorbar(im, cax=cbar_ax, shrink=0.1, pad=0.01, orientation='horizontal')
    cb.ax.tick_params(labelsize=25)

    plt.savefig('/home/sun/paint/meridional_tem_gradient_circulation/meridional_st_90to100_check.pdf', dpi=400)
    plt.show()

def main():
    paint_meridional_stream()


if __name__ == "__main__":
    main()