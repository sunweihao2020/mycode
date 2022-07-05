'''
2021/5/6
本代码计算视水汽汇
使用数据包含：比湿 基础要素场
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
f2 = Nio.open_file("/data5/2019swh/data/composite_specific_humidity.nc")

#L= 2.5×10^6J/kg 定义凝结潜热


u = f1.variables["uwind"][:]
v = f1.variables["vwind"][:]
omega = f1.variables["OMEGA"][:]
q = f2.variables["q"][:]

time = np.arange(0,61)+1
lat  = f1.variables["lat"][:]
lon  = f1.variables["lon"][:]
lev  = f1.variables["level"][:]
p    = lev * 100

disy = np.array([])
disx = np.array([])
q_t = np.gradient(q, time, axis=0)
#处理坐标信息
for i in range(0,len(lat)-1):
    disy    =   np.append(disy,distance((lat[i],0),(lat[i+1],0)).m)
for i in range(0,len(lat)):
    disx    =   np.append(disx,distance((lat[i],lon[0]),(lat[i],lon[1])).m)
location = np.array([0])
for dddd in range(0, len(lat)-1):
    location = np.append(location, np.sum(disy[:dddd + 1]))
q_x = ma.array(ma.zeros(q.shape), mask=q.mask)
q_y = np.gradient(q,location,axis = 2)
for latt in range(0,len(lat)):
    q_x[:,:,latt,:] = np.gradient(q[:,:,latt,:],disx[latt],axis = 2)
term2 = u*q_x+v*q_y
q_p = np.gradient(q,p,axis = 1)
term3 = q_p*omega
term3 = term3 * (60 * 60 * 24)
term2 = term2 * (60 * 60 * 24)
#q2 = 2.5e6*(q_t+term2+term3)/1004      #kJ/(kg K)
q2 = 2.5e6*(term3)/1004



fout = create_nc_multiple('/data5/2019swh/data/heating/','composite_Q2',time,lev,lon,lat)
a_q={'longname': 'water_heating','units': 'K day-1','valid_range': [-1000000000000000.0, 1000000000000000.0]}
add_variables(fout,'Q2',q2,a_q,1)

fout.close()
