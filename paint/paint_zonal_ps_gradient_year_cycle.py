'''
2022-5-31
本代码绘制气压差的全年cycle
'''
import sys
import xarray as xr
import numpy as np
module_path = ["/home/sun/mycode/module/","/data5/2019swh/mycode/module/"]
sys.path.append(module_path[0])
from module_sun import *
import time
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import os
import math
#from paint_lunwen_version3_0_fig8_cross_jet_prect_model_compare import data_resolve

def year_composite_ps(lat_slice,lon_slice,path="/home/sun/qomo-data/year_mean/multi/",var="PS",time=365,lev=None):
    #f0  =  xr.open_dataset("/home/sun/qomo-data/year_mean/multi/").sel(lat=lat_slice,lon=lon_slice)
    #var_out  =  np.zeros((time,len(f0.lat),len(f0.lon)),dtype=np.float32)
    var_out  =  np.zeros((time),dtype=np.float32)

    # 获取文件列表
    files   =   os.listdir(path) ; files.sort()

    # 存入数据
    for i in range(len(files)):
        f1  =  xr.open_dataset(path+files[i]).sel(lat=lat_slice,lon=lon_slice)
        var_out[i]  =  np.average(f1[var].data[0,:])

    return var_out
    


def main():

    ps_indian  =  year_composite_ps(lat_slice=slice(15,20),lon_slice=slice(75,80))
    ps_bob  =  year_composite_ps(lat_slice=slice(15,20),lon_slice=slice(90,92))
    np.save("/home/sun/data/ps_cycle.npy",ps_indian-ps_bob)

if __name__ == "__main__":
    main() 