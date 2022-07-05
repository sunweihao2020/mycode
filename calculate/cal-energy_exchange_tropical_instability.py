'''
2021/5/12
本代码计算正压不稳定过程中的能量转化关系
公式出自关月博士论文
'''
import os
import numpy as np
import Ngl, Nio
import json
from geopy.distance import distance
import numpy.ma as ma
import sys
import math
import xarray as xr
from netCDF4 import Dataset
sys.path.append("/data5/2019swh/mycode/module/")
from module_cal_heating import *
from module_writenc import *

data = xr.open_dataset("/data5/2019swh/data/composite3.nc")

u    = data["uwind"]
v    = data["vwind"]

u1 = u.sel(lon=slice(80,100),lat=slice(-10,30),level=850)
v1 =