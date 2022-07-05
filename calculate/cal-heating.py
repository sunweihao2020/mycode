'''
2020/12/2
调用module cal_heating 模块
计算merra2合成分析后的潜热感热加热情况
'''
import os
import numpy as np
import Ngl, Nio
import json
from geopy.distance import distance
import numpy.ma as ma
import sys
import math
from netCDF4 import Dataset
sys.path.append("/data5/2019swh/mycode/module/")
from module_cal_heating import *
from module_writenc import *

f1 = Nio.open_file("/data5/2019swh/data/composite3.nc")
f2 = Nio.open_file("/data5/2019swh/data/potential_temperature.nc")

pt = f2.variables["pt"][:]
u  = f1.variables["uwind"][:]
v  = f1.variables["vwind"][:]
omega = f1.variables["OMEGA"][:]
t  = f1.variables["T"][:]
time = f1.variables["time"][:]
lon  = f1.variables["lon"][:]
lat  = f1.variables["lat"][:]
level = f1.variables["level"][:]
dimension = [time,level,lat,lon]

heating,t1,t2,t3 = all_heating(t,u,v,pt,omega,dimension)

fout = create_nc_multiple('/data5/2019swh/data/','composite_Q1',time,level,lon,lat)
a_q={'longname': 'all_heating','units': 'K day-1','valid_range': [-1000000000000000.0, 1000000000000000.0]}
add_variables(fout,'all_heating',heating,a_q,1)

fout.close()