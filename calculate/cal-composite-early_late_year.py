'''
2021/3/26
本代码根据早年晚年分别进行合成
日期资料
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

#先处理早年的
with open("/data5/2019swh/data/early_date.json",'r') as load_f:
    a = json.load(load_f)

years = np.array(list(a.keys()))
days  = np.array(list(a.values()))
years = years.astype(np.int)
days = days.astype(np.int)
days -= 1

path='/data1/MERRA2/daily/plev/'
dimension = np.load('/data5/2019swh/data/dimension.npz')
lon = dimension['lon']
lat = dimension['lat']
lev = dimension['lev']
time = dimension['time']

vars = ['H','OMEGA','RH','T','U','V']
#初始化
for vvvv in vars:
    exec(vvvv+"0 = ma.zeros((35,42,361,576))")

first = 0
end = len(years)
for yyyy in range(0,end):
    path1 = path+str(years[yyyy])+"/"
    file_list = os.listdir(path1)
    file_list.sort()
    day0 = days[yyyy]
    j = 0
    for dddd in np.arange(day0-30,day0+5):
        ff = Nio.open_file(path1+file_list[dddd])
        for vvvv in vars:
            cmd = 'xyz1 = ff.variables["xyz"][:]'
            exec(cmd.replace('xyz',vvvv))
            cmd2 = 'xyz0[j,:,:,:] += xyz1[0,:,:,:]'
            exec(cmd2.replace('xyz',vvvv))
    j += 1

fout = create_nc_multiple('/data5/2019swh/data/','composite-early',time,level,lon,lat)
time = np.arange(0,35)
add_variables(fout,'H',H0,a_h,1)
add_variables(fout,'OMEGA',OMEGA0,a_omega,1)
a_rh = {'longname': 'relative_humidity','units': '1','valid_range': [-1000000000000000.0, 1000000000000000.0]}
add_variables(fout,'RH',RH0,a_rh,1)
add_variables(fout,'T',T0,a_T,1)
add_variables(fout,'uwind',U0,a_uwind,1)
add_variables(fout,'vwind',V0,a_vwind,1)

fout.close()


#先处理早年的
del a
with open("/data5/2019swh/data/early_late_date.json",'r') as load_f:
    a = json.load(load_f)

years = np.array(list(a.keys()))
days  = np.array(list(a.values()))
years = years.astype(np.int)
days = days.astype(np.int)
days -= 1

path='/data1/MERRA2/daily/plev/'
dimension = np.load('/data5/2019swh/data/dimension.npz')
lon = dimension['lon']
lat = dimension['lat']
lev = dimension['lev']
time = dimension['time']

vars = ['H','OMEGA','RH','T','U','V']
#初始化
for vvvv in vars:
    exec(vvvv+"0 = ma.zeros((35,42,361,576))")

first = 0
end = len(years)
for yyyy in range(0,end):
    path1 = path+str(years[yyyy])+"/"
    file_list = os.listdir(path1)
    file_list.sort()
    day0 = days[yyyy]
    j = 0
    for dddd in np.arange(day0-30,day0+5):
        ff = Nio.open_file(path1+file_list[dddd])
        for vvvv in vars:
            cmd = 'xyz1 = ff.variables["xyz"][:]'
            exec(cmd.replace('xyz',vvvv))
            cmd2 = 'xyz0[j,:,:,:] += xyz1[0,:,:,:]'
            exec(cmd2.replace('xyz',vvvv))
    j += 1

fout = create_nc_multiple('/data5/2019swh/data/','composite-early',time,level,lon,lat)
time = np.arange(0,35)
add_variables(fout,'H',H0,a_h,1)
add_variables(fout,'OMEGA',OMEGA0,a_omega,1)
a_rh = {'longname': 'relative_humidity','units': '1','valid_range': [-1000000000000000.0, 1000000000000000.0]}
add_variables(fout,'RH',RH0,a_rh,1)
add_variables(fout,'T',T0,a_T,1)
add_variables(fout,'uwind',U0,a_uwind,1)
add_variables(fout,'vwind',V0,a_vwind,1)

fout.close()