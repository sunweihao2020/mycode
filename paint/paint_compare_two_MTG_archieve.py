'''
2022-07-12
This code compare two method of MTG index
1. First method is from Mao, using difference between 5N and 15N
2. Here we check using the dT/dy to calculate meridional temperature index
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

src_path  =  "/home/sun/data/merra2_climate_vars_multi/"

def cal_MTG_1(file):
    f0  =  xr.open_dataset(src_path+file).sel(lat=[5,15],lev=slice(500,200),lon=slice(90,100))

    return np.average(f0.T.data[0,:,1,:]) - np.average(f0.T.data[0,:,0,:])

def cal_MTG_2(file):
    f0 = xr.open_dataset(src_path + file).sel(lev=slice(500, 200), lon=slice(90, 100))

    disy, disx, location = cal_xydistance(f0.lat.data, f0.lon.data)

    #First calculate vertical/zonal average, then meridional gradient
    tem_avg1  =  np.average(np.average(f0.T.data[0],axis=0),axis=1)

    tem_gradient  =  np.gradient(tem_avg1,location)

    return np.average(tem_gradient[190:211]) # we need the location of 5N and 30N, corresponding to 190 211

def main():
    # get files list
    file_name  =  os.listdir(src_path)
    file_name.sort()

    # generate two arrays of length 365 to save the temperature difference
    MTG1 = np.zeros((365))
    MTG2 = MTG1.copy()

    # calculate and save
    j = 0
    for name in file_name:
        MTG1[j] = cal_MTG_1(name)
        MTG2[j] = cal_MTG_2(name)

        j += 1
    
    fig, ax = plt.subplots()
    ax.plot(np.linspace(1,365,365),MTG1,color='red')
    ax2     = ax.twinx()
    ax2.plot(np.linspace(1,365,365),MTG2,color='blue',linestyle='--')


    plt.savefig("/home/sun/paint/two_MTG_index_compare_220720/index_compare_MTG.pdf",dpi=400)
    plt.show()
    

if __name__ == "__main__":
    main()




