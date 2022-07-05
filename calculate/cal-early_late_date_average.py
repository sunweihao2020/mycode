'''
2021/8/13
计算看看早年晚年的平均日期
'''
import os
import numpy as np
import numpy.ma as ma
import Ngl, Nio
from netCDF4 import Dataset
import json
import sys
import time
sys.path.append("/data5/2019swh/mycode/module/")
from module_sun import *
from module_writenc import *
#from attribute import *

with open("/data5/2019swh/data/early_date.json",'r') as load_f:
    early = json.load(load_f)

with open("/data5/2019swh/data/late_date.json",'r') as load_f:
    late = json.load(load_f)

years  =  np.array(list(early.keys()))
days   =  np.array(list(early.values()))
years  =  years.astype(np.int)
days   =  days.astype(np.int)

early_average = np.average(days)

years  =  np.array(list(late.keys()))
days   =  np.array(list(late.values()))
years  =  years.astype(np.int)
days   =  days.astype(np.int)

late_average = np.average(days)

print(out_date(1993,round(early_average)))
print(out_date(1993,round(late_average)))
print(early)
print(late)