'''
2021/4/25
本代码对下载的trmm和merra2再分析资料进行合成平均
资料存储位置：/data5/2019swh/mydown/
'''
import os
import numpy as np
import numpy.ma as ma
import Ngl, Nio
from netCDF4 import Dataset
import json
import sys
import datetime
sys.path.append("/data5/2019swh/mycode/module/")
from module_sun import *
from module_writenc import *
from attribute import *

#获取文件列表
trmm_list = os.listdir("/data5/2019swh/mydown/trmm_precipitation/")
merra_list = os.listdir("/data5/2019swh/mydown/merra2_precipitation/")

#获取时间
with open("/data5/2019swh/data/onsetdate.json",'r') as load_f:
    a = json.load(load_f)
years = np.array(list(a.keys()))
days = np.array(list(a.values()))
years = years.astype(np.int)
days = days.astype(np.int)
days -= 1

def select(start,end,year,name):
    if name[start:end] == str(year):
        return 1
    else:
        return 0

#生成初始数组
f1 =  Nio.open_file("/data5/2019swh/mydown/merra2_precipitation/MERRA2_200.statD_2d_slv_Nx.19991205.nc4.nc4")
merra_p = f1.variables["TPRECMAX"][:]
merra_lon = f1.variables["lon"][:]
merra_lat = f1.variables["lat"][:]
f2 =  Nio.open_file("/data5/2019swh/mydown/trmm_precipitation/3B42_Daily.20070913.7.nc4.nc4")
trmm_p = f2.variables["precipitation"][:]
trmm_lon = f2.variables["lon"][:]
trmm_lat = f2.variables["lat"][:]

merra_p0 = ma.zeros((35,361,576))
trmm_p0  = ma.zeros((35,1440,400))

#先处理trmm的 1998-2019
for yyyy in range(1998,2020):
    #先把这一年的数据给挑出来
    trmm = []
    for nnnn in trmm_list:
        if select(11,15,yyyy,nnnn):
            trmm.append(nnnn)
        else:
            continue
    trmm.sort()
    day0 = int(a[str(yyyy)])-1
    j = 0
    for dddd in range(day0-30,day0+5):
        ff = Nio.open_file("/data5/2019swh/mydown/trmm_precipitation/"+trmm[dddd])
        pre = ff.variables["precipitation"][:]
        trmm_p0[j,:,:] += pre/22
        j += 1

#处理merra2的 1980-2019
for yyyy in range(1980,2020):
    #先把这一年的数据给挑出来
    merra = []
    for nnnn in merra_list:
        if select(27,31,yyyy,nnnn):
            merra.append(nnnn)
        else:
            continue
    merra.sort()
    day0 = int(a[str(yyyy)])-1
    j = 0
    for dddd in range(day0-30,day0+5):
        ff = Nio.open_file("/data5/2019swh/mydown/merra2_precipitation/"+merra[dddd])
        pre = ff.variables["TPRECMAX"][:]
        merra_p0[j,:,:] += pre[0,:,:]/40
        j += 1

merra_p0 *= 86400

time = np.arange(0,35)
fout = create_nc_single('/data5/2019swh/data/','composite-precipitation_merra',time,merra_lon,merra_lat)
add_variables(fout,'precipitation',merra_p0,a_pre,0)
fout.close()

del fout
del add_variables

def add_variables(file,name,variable,attribute,bool):
    if bool == 0:
        var = file.createVariable(name,"f8",("time","lon","lat"),fill_value=1e+15)
    else:
        var = file.createVariable(name,"f8",("time","level","lat","lon"),fill_value=1e+15)

    a = list(attribute.items())
    for i in range(0,3):
        key,value = list(attribute.items())[i]
        exec("var."+key+" = value")

    var[:] = variable

fout = create_nc_single('/data5/2019swh/data/','composite-precipitation_trmm',time,trmm_lon,trmm_lat)
add_variables(fout,'precipitation',trmm_p0,a_pre,0)
fout.close()

