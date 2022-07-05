'''
2021/6/9
本代码使用最基础的方程对温度以及风矢量来进行诊断
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
#from attribute import *


f0 = Nio.open_file("/data5/2019swh/data/composite3.nc")
u  = f0.variables['uwind'][:]
v  = f0.variables['vwind'][:]
t  = f0.variables['T'][:]
w  = f0.variables['OMEGA'][:]
lon  =  f0.variables["lon"][:]
lat  =  f0.variables["lat"][:]

f1 = Nio.open_file("/data5/2019swh/data/composite_equivalent_tem.nc")
theta = f1.variables["theate_e"][:]
level = f1.variables["level"][:]

#f2 = Nio.open_file("/data/heating/composite-heating-merra.nc")
#q  =  f2.variables["physics"][:]

disy,disx,location = cal_xydistance(lat,lon)

dd = np.arange(1,62)
#把时间变化项求出来
def cal_dt(dd,a,b,c):
    d = np.gradient(a,dd,axis=0)
    e = np.gradient(b,dd,axis=0)
    f = np.gradient(c,dd,axis=0)
    return d,e,f

du_dt,dv_dt,dt_dt = cal_dt(dd,u,v,t)

def cal_dx(disx,var):
    var_x  =  copy.deepcopy(var)
    for tt in range(0,var.shape[0]):
        for ll in range(0,var.shape[1]):
            for yy in range(1,var.shape[2]-1):
                var_x[tt,ll,yy,:] = np.gradient(var[tt,ll,yy,:],disx[yy])
    return var_x

#计算水平平流项
du_dx = cal_dx(disx,u)
du_dy = np.gradient(u,location,axis=2)
dv_dx = cal_dx(disx,v)
dv_dy = np.gradient(v,location,axis=2)
dt_dx = cal_dx(disx,t)
dt_dy = np.gradient(t,location,axis=2)

#计算温度的垂直平流项
dtheta_dp = np.gradient(theta,level*100,axis=1)

#开始计算方程中各项
t_advection_x = u*dt_dx*60*60*24
t_advection_y = v*dt_dy*60*60*24

p_p0 = level/1000
p_p0 = pow(p_p0,0.286)

p_p0_k = conform(p_p0,u.shape,0,2,3)

t_advection_z = p_p0_k*w*dtheta_dp*60*60*24

#至此温度平流各项计算完毕
fout = create_nc_multiple('/data5/2019swh/data/','composite-tem_advection',np.arange(1,62),level,lon,lat)
a_k = {'longname': 'temperature_tendency','units': 'K day-1','valid_range': [-1000000000000000.0, 1000000000000000.0]}
add_variables(fout,'tt',dt_dt,a_k,1)
a_k = {'longname': 'temperature_tendency_due_to_x_advection','units': 'K day-1','valid_range': [-1000000000000000.0, 1000000000000000.0]}
add_variables(fout,'t_x_advection',t_advection_x,a_k,1)
a_k = {'longname': 'temperature_tendency_due_to_y_advection','units': 'K day-1','valid_range': [-1000000000000000.0, 1000000000000000.0]}
add_variables(fout,'t_y_advection',t_advection_y,a_k,1)
a_k = {'longname': 'temperature_tendency_due_to_z_advection','units': 'K day-1','valid_range': [-1000000000000000.0, 1000000000000000.0]}
add_variables(fout,'t_z_advection',t_advection_z,a_k,1)
a_k = {'longname': 'temperature_gradient_y','units': 'K m-1','valid_range': [-1000000000000000.0, 1000000000000000.0]}
add_variables(fout,'dt_dy',dt_dy,a_k,1)
fout.close()