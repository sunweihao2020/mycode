'''
2021/1/3
本代码旨在将模式层数据以季风爆发当日为D0前后进行合成以待后续使用
数据地址：/data1/MERRA2/daily/modellev/
合成的变量：H OMEGA QV RH T U V
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
from attribute import *
with open("/data5/2019swh/data/onsetdate.json",'r') as load_f:
    a = json.load(load_f)


a_pv   = {"longname":"pv","units":"K m+2 kg-1 s-1","valid_range":[-1e+15,1e+15]}
years = np.array(list(a.keys()))
days  = np.array(list(a.values()))
years = years.astype(np.int)
days = days.astype(np.int)
days -= 1
path0 = "/data1/MERRA2/daily/modellev/"

#读取基础信息
f0 = Nio.open_file("/data1/MERRA2/daily/modellev/2006/MERRA2_300.inst3_3d_asm_Nv.20060411.SUB.nc")
level = f0.variables["lev"][:]
lat   = f0.variables["lat"][:]
lon   = f0.variables["lon"][:]

#σ-p坐标没有缺测值不需要额外设置mask，nice
h0  =   ma.zeros((61,33,361,576))
omega0  =   ma.zeros((61,33,361,576))
qv0 =   ma.zeros((61,33,361,576))
rh0 =   ma.zeros((61,33,361,576))
t0  =   ma.zeros((61,33,361,576))
u0  =   ma.zeros((61,33,361,576))
v0  =   ma.zeros((61,33,361,576))

def composite(var,varname,years,days,path0):
    for i in range(0,40):
        path1 = path0+str(years[i])+"/"
        file  = os.listdir(path1)
        file.sort()
        stat = days[i]

        j = 0
        for dddd in range(stat-30,stat+31):
            f1 = Nio.open_file(path1+file[dddd])
            var1 = f1.variables[varname][:]
            var[j,:,:,:] += var1[0,:,:,:]/40
            j+=1

vars = [h0,omega0,qv0,rh0,t0,u0,v0]
varnames = ["H", "OMEGA", "QV", "RH", "T", "U", "V"]
for j in range(0,7):
    vars[j] = composite(vars[j],varnames[j],years,days,path0)

time = np.arange(0,61)
fout = create_nc_multiple('/data5/2019swh/data/','composite-model',time,level,lon,lat)
add_variables(fout,'H',h0,a_h,1)
add_variables(fout,'OMEGA',omega0,a_omega,1)
a_qv = {'longname': 'specific_humidity','units': 'kg kg-1','valid_range': [-1000000000000000.0, 1000000000000000.0]}
add_variables(fout,'QV',qv0,a_qv,1)
add_variables(fout,'T',t0,a_T,1)
a_rh = {'longname': 'relative_humidity_after_moist','units': '1','valid_range': [-1000000000000000.0, 1000000000000000.0]}
add_variables(fout,'RH',rh0,a_rh,1)
add_variables(fout,'U',u0,a_uwind,1)
add_variables(fout,'V',v0,a_vwind,1)

fout.close()
