'''
2021/2/28
本代码验证一下cdo求的日平均是否正确
'''

import os
import numpy as np
import numpy.ma as ma
import Ngl, Nio
from netCDF4 import Dataset
import json
import sys
path = "/data5/2019swh/mydown/jra55/"
f1 = Nio.open_file(path+"fcst_phy3m125.222_adhr.1980030100_1980033118.nc")
f2 = Nio.open_file(path+"test.nc")
var1 = f1.variables["ADHR_GDS0_ISBL_ave6h"][:]
var2 = f2.variables["ADHR_GDS0_ISBL_ave6h"][:]
#选定（70，80）
a = np.sum(var1[0:4,:,70,80],axis=0)/4
b = var2[0,:,70,80]

'''验证结果：great！'''