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
from paint_meridional_pre_section_zonal_wind_sst import generate_xlabel
from matplotlib import cm
from matplotlib.colors import ListedColormap


path0  =  "/home/sun/data/"

file0  =  xr.open_dataset(path0+'zonal_meridional_streamfunction_90to100_2.nc') #The dimension is (61,31,361)
print(file0)

viridis = cm.get_cmap('coolwarm', 22)
newcolors = viridis(np.linspace(0, 1, 22))
newcmp = ListedColormap(newcolors)
newcmp.set_under('blue')
newcmp.set_over('brown')

def paint_meridional_stream():
    # set figure
    fig1 = plt.figure(figsize=(32, 26))
    spec1 = fig1.add_gridspec(nrows=3, ncols=3)
    j = 0
    start = 21

    for col in range(3):
        for row in range(3):
            ax  =  fig1.add_subplot(spec1[row, col])

            # set axis ticks and label
            ax.set_xticks(np.linspace(-10, 30, 9, dtype=int))
            ax.set_yticks(np.linspace(1000, 100, 10))
            ax.set_xticklabels(generate_xlabel(np.linspace(-10, 30, 9, dtype=int)))
            ax.tick_params(axis='both', labelsize=22.5)

            # plot streamfunction
            im = ax.contourf(file0.lat.data, file0.level.data,[start],np.linspace(-15,15,21),cmap=newcmp,extend='both')