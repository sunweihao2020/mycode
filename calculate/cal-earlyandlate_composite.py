'''
2021/2/16
本代码旨在就季风爆发的早年和晚年分别进行合成
日期资料:early_late_date.json
'''
import matplotlib
import matplotlib.pyplot as plt
import os
import numpy as np
import numpy.ma as ma
import Ngl, Nio
from netCDF4 import Dataset
import json
import sys
sys.path.append("/data5/2019swh/mycode/module/")
from module_sun import *
from module_writenc import *
from attribute import *

with open("/data5/2019swh/data/early_date.json",'r') as load_f1:
    a = json.load(load_f1)

with open("/data5/2019swh/data/late_date.json",'r') as load_f2:
    b = json.load(load_f2)

dimension = np.load('/data5/2019swh/data/dimension.npz')
lon = dimension['lon']
lat = dimension['lat']
lev = dimension['lev']


data_path = "/data1/MERRA2/daily/plev/"
def cal_composite(yearday,name):
    year = np.array(list(yearday.keys()))

    h     = ma.zeros((91, 42, 361, 576))
    u     = ma.zeros((91, 42, 361, 576))
    v     = ma.zeros((91, 42, 361, 576))
    t     = ma.zeros((91, 42, 361, 576))
    omega = ma.zeros((91, 42, 361, 576))

    end = len(year)
    first = 0
    for yyyy in year:
        path1 = data_path + yyyy +"/"
        file_list = os.listdir(path1)
        file_list.sort()
        day0 = yearday[yyyy]
        day0 = int(day0)
        day0 -= 1
        j = 0
        for dddd in range(day0-60,day0+31):
            ff = Nio.open_file(path1+file_list[dddd])
            h1 = ff.variables["H"][:]
            omega1 = ff.variables["OMEGA"][:]
            t1 = ff.variables["T"][:]
            u1 = ff.variables["U"][:]
            v1 = ff.variables["V"][:]
            h[j, :, :, :] += h1[0, :, :, :] / (end - first)
            omega[j, :, :, :] += omega1[0, :, :, :] / (end - first)
            t[j, :, :, :] += t1[0, :, :, :] / (end - first)
            u[j, :, :, :] += u1[0, :, :, :] / (end - first)
            v[j, :, :, :] += v1[0, :, :, :] / (end - first)
            j += 1

    time = np.arange(0,91)
    fout = create_nc_multiple('/data5/2019swh/data/',name,time,lev,lon,lat)
    add_variables(fout, 'u', u, a_uwind, 1)
    add_variables(fout, 'v', v, a_vwind, 1)
    add_variables(fout, 'h', h, a_h, 1)
    add_variables(fout, 't', t, a_T, 1)
    fout.close()

cal_composite(a,"early-year-composite2")
cal_composite(b,"late-year-composite2")