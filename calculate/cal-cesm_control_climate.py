'''
2021/8/23
本代码使用cesm输出数据来计算气候态平均
变量名有：DTV KVH...
'''
import os
import numpy as np
import numpy.ma as ma
import json
import xarray as xr
import sys
sys.path.append("/home/sun/mycode/module/")
from module_writenc import *
from attribute import *

path  =  "/home/sun/cesm_output/control_intel/atm/hist/"

#test  =  xr.open_dataset(path+"control_intel.cam.h1.1983-05-12-00000.nc")
#总共有这些变量
vars  =  ["KVH","DTV","LHFLX","OMEGA","OMEGAT","PRECT","PS","Q","SHFLX","T","TS","U","V","Z3"]
