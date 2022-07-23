# # 2022/7/22
# # This script calculate climate for model output
# # exp is b1850_control, vars is ocean variables

# ---------------------------  Metion  ------------------------------
# the ocean has two file type
# 1. mom6.hm_ : hfsso rlntds rsntds hfds        monthly(one month in one file)
# 2. mom6.sfc_: SSH tos sos SSU SSV mlotst      daily(365 days in one file)

import os
import xarray as xr
import numpy as np
import time


start = time.time()
path_in  =  "/home/sun/model_output/b1850_exp/exp_output/"
path_out =  "/home/sun/data/model_data/climate/"

year_range  =  np.array([4,55],dtype=int)

f0  =  xr.open_dataset(path_in+'b1850_control_o1_220703.mom6.sfc_0016.nc')
f1  =  xr.open_dataset(path_in+'b1850_control_o1_220703.mom6.hm_0036_10.nc')
hmvar  =  ["hfsso", "rlntds", "rsntds", "hfds"]
sfvar  =  ["SSH", "tos", "sos", "SSU", "SSV", "mlotst"]

# declare variables
hfsso     =  np.zeros((12,458,540),dtype=np.float32)
rlntds    =  hfsso.copy()
rsntds    =  hfsso.copy()
hfds      =  hfsso.copy()

ssh       =  np.zeros((365,458,540),dtype=np.float32)
tos       =  ssh.copy()
sos       =  ssh.copy()
ssu       =  ssh.copy()
ssv       =  ssh.copy()
mlotst    =  ssh.copy()


for yyyy in range(year_range[0],year_range[1]+1):
    # I need get two file list corresponding to two types, here we deal with two type files respectively

    # --------------------  calculate hm file  -----------------------
    list0  =  []
    for f1 in os.listdir(path_in):
        if yyyy < 10:
            if "control_o1_220703.mom6.hm_000"+str(yyyy) in f1:
                list0.append(f1)
        else:
            if "control_o1_220703.mom6.hm_00"+str(yyyy) in f1:
                list0.append(f1)
    list0.sort()
    print("it is in hm year:"+str(yyyy)+" length is "+str(len(list0)))
    
    j = 0 # j 0->365 account
    for f2 in list0:
        f3  =  xr.open_dataset(path_in+f2,engine='netcdf4')
        hfsso[j,:]   +=  f3.hfsso.data[0,:]/(year_range[1]-year_range[0]+1)
        rlntds[j,:]  +=  f3.rlntds.data[0,:]/(year_range[1]-year_range[0]+1)
        rsntds[j,:]  +=  f3.rsntds.data[0,:]/(year_range[1]-year_range[0]+1)
        hfds[j,:]    +=  f3.hfds.data[0,:]/(year_range[1]-year_range[0]+1)

        j +=1

    end = time.time()
    print("Finish "+str(yyyy)+" running time for hm: %s second"%(end-start))

    # --------------------  calculate sfc file  -----------------------
    list0  =  []
    for f1 in os.listdir(path_in):
        if yyyy < 10:
            if "control_o1_220703.mom6.sfc_000"+str(yyyy) in f1:
                list0.append(f1)
        else:
            if "control_o1_220703.mom6.sfc_00"+str(yyyy) in f1:
                list0.append(f1)
    list0.sort()
    print("it is in sfc year:"+str(yyyy)+" length is "+str(len(list0)))
    
    #j = 0 no need j loop
    for f2 in list0:
        f3  =  xr.open_dataset(path_in+f2,engine='netcdf4')
        ssh      +=  f3.SSH.data[0,:]/(year_range[1]-year_range[0]+1)
        tos      +=  f3.tos.data[0,:]/(year_range[1]-year_range[0]+1)
        sos      +=  f3.sos.data[0,:]/(year_range[1]-year_range[0]+1)
        ssu      +=  f3.SSU.data[0,:]/(year_range[1]-year_range[0]+1)
        ssv      +=  f3.SSV.data[0,:]/(year_range[1]-year_range[0]+1)
        mlotst   +=  f3.mlotst.data[0,:]/(year_range[1]-year_range[0]+1)



    end = time.time()
    print("Finish "+str(yyyy)+" running time for sfc: %s second"%(end-start))
    
f0  =  xr.open_dataset(path_in+'b1850_control_o1_220703.mom6.sfc_0016.nc')
f1  =  xr.open_dataset(path_in+'b1850_control_o1_220703.mom6.hm_0036_10.nc')
# 生成文件
ds    = xr.Dataset(
    {
        "hfsso":(["month","yh","xh"],np.float32(hfsso)),
        "rlntds":(["month","yh","xh"],np.float32(rlntds)),
        "rsntds":(["month","yh","xh"],np.float32(rsntds)),
        "hfds":(["month","yh","xh"],np.float32(hfds)),
        "ssh":(["day","yh","xh"],np.float32(ssh)),
        "tos":(["day","yh","xh"],np.float32(tos)),
        "sos":(["day","yh","xh"],np.float32(sos)),
        "ssu":(["day","yh","xq"],np.float32(ssu)),
        "ssv":(["day","yq","xh"],np.float32(ssv)),
        "mlotst":(["day","yh","xh"],np.float32(mlotst)),
    },
    coords={
        "xh":(["xh"],f0.xh.data),
        "yh":(["yh"],f0.yh.data),
        "month":(["month"],np.linspace(1,12,12)),
        "day":(["day"],np.linspace(1,365,365)),
        "yq":(["yq"],f0.yq.data),
        "xq":(["xq"],f0.xq.data),
    },
)
ds.hfsso.attrs     =      f1.hfsso.attrs
ds.rlntds.attrs    =      f1.rlntds.attrs
ds.rsntds.attrs    =      f1.rsntds.attrs
ds.hfds.attrs      =      f1.hfds.attrs
ds.tos.attrs       =      f0.tos.attrs
ds.ssh.attrs       =      f0.SSH.attrs
ds.sos.attrs       =      f0.sos.attrs
ds.ssu.attrs       =      f0.SSU.attrs
ds.ssv.attrs       =      f0.SSV.attrs
ds.mlotst.attrs    =      f0.mlotst.attrs
ds.xh.attrs        =      f0.xh.attrs
ds.yh.attrs        =      f0.yh.attrs
ds.xq.attrs        =      f0.xq.attrs
ds.yq.attrs        =      f0.yq.attrs




ds.to_netcdf(path_out+"b1850_control_ocean.nc")