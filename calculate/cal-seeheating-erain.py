'''
2021/3/14
本代码使用ERAIN来计算视热源用以比较
'''
import os
import numpy as np
import numpy.ma as ma
import Ngl, Nio
from netCDF4 import Dataset
import json
import sys
import math
import copy
sys.path.append("/data5/2019swh/mycode/module/")
from module_writenc import *
from module_sun import *
from attribute import *
with open("/data5/2019swh/data/onsetdate.json",'r') as load_f:
    a = json.load(load_f)
var = ['t','w','vo','d','u','v','r']
path = '/data1/other_data/DataUpdate/ERA5/new-erain/6hourly/'
mm1 = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
mm2 = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
month = ['01','02','03','04','05','06','07','08','09','10','11','12']

#获取维度信息
ff = Nio.open_file('/data1/other_data/DataUpdate/ERA5/new-erain/6hourly/2018/2018-03-6hourly.nc')
level = ff.variables["level"][:]
lat = ff.variables["latitude"][:]
lon = ff.variables["longitude"][:]

for yyyy in range(1980,2019):
    path1 = path+str(yyyy)+"/"
    if leap_year(yyyy):
        var1 = ma.zeros((366,37,121,240))
        mm = mm2
    else:
        var1 = ma.zeros((365, 37, 121, 240))
        mm = mm1
    t0 = copy.deepcopy(var1)
    w0 = copy.deepcopy(var1)
    vo0 = copy.deepcopy(var1)
    d0 = copy.deepcopy(var1)
    u0 = copy.deepcopy(var1)
    v0 = copy.deepcopy(var1)
    r0 = copy.deepcopy(var1)

    for mmmm in range(1,13):
        f = Nio.open_file(path1+str(yyyy)+'-'+month[mmmm-1]+'-6hourly.nc')
        t1 = f.variables["t"]
        t1 = short2flt(t1)
        w1 = f.variables["w"]
        w1 = short2flt(w1)
        vo1= f.variables["vo"]
        vo1 = short2flt(vo1)
        d1 = f.variables["d"]
        d1 = short2flt(d1)
        u1 = f.variables["u"]
        u1 = short2flt(u1)
        v1 = f.variables["v"]
        v1 = short2flt(v1)
        r1 = f.variables["r"]
        r1 = short2flt(r1)
        days = return_month(mmmm-1,yyyy)
        start = int(np.sum(mm[0:mmmm-1]))
        for vvvv in var:
            command = 'var0[start:(start+days),:,:,:] = daily_mean(var1,var1.shape[0],4)'
            command1 = command.replace('var',vvvv)
            exec(command1)
    time = np.arange(0, u0.shape[0])
    fout = create_nc_multiple('/data5/2019swh/data/erain_mean/', 'erain-daymean-'+str(yyyy), time, level, lon, lat)
    add_variables(fout, 't', t0, a_T, 1)
    add_variables(fout, 'w',w0,a_omega,1)
    a_vo = {'longname': 'vorticity', 'units': 's-1', 'valid_range': [-1000000000000000.0, 1000000000000000.0]}
    add_variables(fout, 'vo', vo0, a_vo, 1)
    add_variables(fout, 'd', d0, a_vo, 1)
    add_variables(fout, 'u', u0, a_uwind, 1)
    add_variables(fout, 'v', v0, a_vwind, 1)
    a_rh = {'longname': 'relative humidity', 'units': '1', 'valid_range': [-1000000000000000.0, 1000000000000000.0]}
    add_variables(fout, 'rh', r0, a_rh, 1)
    fout.close()