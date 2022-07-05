'''
2021/1/3
使用倒算法计算model层上的加热率
公式：来自生宸
使用资料：合成分析的模式层资料 /data5/2019swh/data/composite-model.nc /data5/2019swh/data/composite-modeltheta.nc
'''
import os
import numpy as np
import Ngl, Nio
import numpy.ma as ma
from geopy.distance import distance
import sys
from netCDF4 import Dataset
import math
import copy
sys.path.append("/data5/2019swh/mycode/module/")
from module_sun import *
from module_writenc import *
from attribute import *

f1 = Nio.open_file("/data5/2019swh/data/composite-model.nc")
f2 = Nio.open_file("/data5/2019swh/data/composite-modeltheta.nc")
level = f1.variables["level"][:]
lat   = f1.variables["lat"][:]
lon   = f1.variables["lon"][:]
time  = f1.variables["time"][:]

theta = f2.variables["theta"][:]
pl    = f2.variables["pl"][:]
u     = f1.variables["U"][:]
v     = f1.variables["V"][:]
omega = f1.variables["OMEGA"][:]

#计算偏θ偏t
theta_t = np.gradient(theta,time,axis=0)

#计算平流项
disy,disx,location  =  cal_xydistance(lat,lon)
theta_y = np.gradient(theta,location,axis=2)

theta_x = copy.deepcopy(theta_y)
for i in range(1,len(lat)-1):
    theta_x[:,:,i,:] = np.gradient(theta[:,:,i,:],disx[i],axis=2)

term1 = theta_y * v
term2 = theta_x * u

advective_term = term1 + term2

#计算偏θ偏p
theta_p = copy.deepcopy(theta_y)
for t in range(0,61):
    for i in range(0,361):
        for j in range(0,576):
            theta_p[t,:,i,j] = np.gradient(theta[t,:,i,j],pl[t,:,i,j],axis=0)

#计算omega_h
p_y = np.gradient(pl,location,axis=2)
p_x = copy.deepcopy(p_y)
for i in range(1,len(lat)-1):
    p_x[:,:,i,:] = np.gradient(pl[:,:,i,:],disx[i],axis=2)

p_t = np.gradient(pl,time,axis=0)

term1 = u*p_x
term2 = v*p_y

omega_h = omega-p_t-term1-term2

#计算垂直项
term3 = omega_h * theta_p

final = theta_t + advective_term + term3

fout = create_nc_multiple('/data5/2019swh/data/','composite-model_heating',time,level,lon,lat)
a_final = {'longname': 'model heating','units': 'T day-1','valid_range': [-1000000000000000.0, 1000000000000000.0]}
add_variables(fout,'heating',final,a_final,1)
fout.close()