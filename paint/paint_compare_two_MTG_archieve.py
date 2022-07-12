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

src_path  =  "/home/sun/qomo-data/year_mean/multi/"

def cal_MTG_1(file):
    f0  =  xr.open_dataset(src_path+file).sel(lat=[5,15],level=slice(500,200),lon=slice(90,100))

    return np.average(f0.T.data[0,:,1,:]) - np.average(f0.T.data[0,:,0,:])

def cal_MTG_2(file):
    f0 = xr.open_dataset(src_path + file).sel(level=slice(500, 200), lon=slice(90, 100))

    disy, disx, location = cal_xydistance(f0.lat.data, f0.lon.data)

    #First calculate vertical/zonal average, then meridional gradient
    tem_avg1  =  np.average(np.average(f0.T.data[0],axis=0),axis=1)

    tem_gradient  =  np.gradient(tem_avg1,location)

    return tem_gradient

def main()





