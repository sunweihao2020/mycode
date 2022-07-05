'''
2021/9/12
本代码计算cesm2的输出文件的气候态平均
由于内存限制，目前的策略是一次针对一个变量计算并生成气候态文件
'''
import Ngl
import xarray as xr
import os
import numpy as np
import math

experiment  =  ["close_all_intel","control_intel","topo_all_1m_intel2","topo_indo_1m_intel","topo_indo_no_plateau"]
var         =  ["DTV","KVH","LHFLX","OMEGA","PRECT","PS","Q","SHFLX","T","TS","U","V","Z3"]

path        =  "/home/sun/cesm_output/"
exp         =  experiment[0]
reference   =  xr.open_dataset("/home/sun/cesm_output/close_all_intel/atm/hist/close_all_intel.cam.h1.1986-04-04-00000.nc")

def get_filelist(path,exp):
    '''生成该试验下所有h1文件，
    这里舍掉前两年'''
    list1  =  os.listdir(path+exp+"/atm/hist")
    list2  =  [x for x in list1 if (".cam.h1." in x)] ; list2.sort()
    del list2[0:(365*2)] #去除spin-up的两年,这之后第一个文件从1981-01-01开始
    return list2

def create_basearray(var,reference):
    #本代码生成base数组
    pnew = np.array(
        [1000, 975, 950, 925, 900, 875, 850, 825, 800, 775, 750, 700, 650, 600, 550, 500, 450, 400, 350, 300, 250, 225,
         200, 175, 150, 125, 100, 70, 50, 30, 20, 10, 7, 5, 3, 2, 1]
    )
    if len(reference[var].data.shape) == 3:
        return np.zeros((365,reference[var].data.shape[1],reference[var].data.shape[2]))
    else:
        return np.zeros((365,len(pnew),reference[var].data.shape[2],reference[var].data.shape[3]))

def add_climate(var,base,path,list):
    #把一个变量逐日的气候态加起来
    pnew = np.array(
        [1000, 975, 950, 925, 900, 875, 850, 825, 800, 775, 750, 700, 650, 600, 550, 500, 450, 400, 350, 300, 250, 225,
         200, 175, 150, 125, 100, 70, 50, 30, 20, 10, 7, 5, 3, 2, 1]
    )
    for yyyy in range(0,math.floor(len(list)/365)):
        for dddd in range(0,365):
            f0          =    xr.open_dataset(path+list[(yyyy*365)+dddd])
            if len(base.shape)==4:
                array0   =    Ngl.vinth2p(f0[var].data,f0.hyam.data,f0.hybm.data,pnew,f0.PS.data,1,f0.P0.data/100,1,True)
                array    =    array0[0,:,:,:].copy()
                base[dddd,:,:,:]   +=  array
            else:
                array   =    f0[var].data[0,:,:]
                base[dddd,:,:]     +=  array

    return (base/math.floor(len(list)/365))

def create_ncfile(var,out,ref,path,name):
    time    =  np.arange(0,365,1)
    pnew = np.array(
        [1000, 975, 950, 925, 900, 875, 850, 825, 800, 775, 750, 700, 650, 600, 550, 500, 450, 400, 350, 300, 250, 225,
         200, 175, 150, 125, 100, 70, 50, 30, 20, 10, 7, 5, 3, 2, 1]
    )
    if len(out.shape) == 4:
        ncfile  =  xr.Dataset(
            {
                var: (["time", "lev","lat", "lon"], out),
            },
            coords={
                "lon": (["lon"], ref.lon.data),
                "lat": (["lat"], ref.lat.data),
                "time": (["time"], time),
                "lev":(["lev"],pnew),
            },
        )
        ncfile["lev"].attrs["units"] = "hPa"
    else:
        ncfile = xr.Dataset(
            {
                var: (["time","lat", "lon"], out),
            },
            coords={
                "lon": (["lon"], ref.lon.data),
                "lat": (["lat"], ref.lat.data),
                "time": (["time"], time),
            },
        )

    ncfile[var].attrs   =  ref[var].attrs
    ncfile["lon"].attrs = ref["lon"].attrs
    ncfile["lat"].attrs = ref["lat"].attrs
    ncfile.to_netcdf(path+name)

#test  =  add_climate(var[1],create_basearray(var[1],reference),path+experiment[1]+"/atm/hist/",get_filelist(path,experiment[1]))

path_out  =  "/home/sun/data/"

for eeee in experiment:
    for vvvv in var:
        base1        =  create_basearray(vvvv,reference)
        path1        =  path+eeee+"/atm/hist/"
        list1        =  get_filelist(path,eeee)
        avg_climate  =  add_climate(vvvv,base1,path1,list1)
        name1        =  "year_mean_cesm2_"+eeee+"_"+vvvv+".nc"
        create_ncfile(vvvv,
                      avg_climate,
                      reference,
                      path_out,
                      name1,
                      )






