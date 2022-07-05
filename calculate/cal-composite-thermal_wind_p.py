'''
2021/5/28
使用资料：/data1/other_data/DataUpdate/ERA5/merra2/modelpv/  下计算的模式层pv
计算层次：地表-72 850-63 700-56 500-(50+51)/2
所以合成后只存在该四层的资料：垂直PV 水平PV 总PV
原资料为1980-2015年 共36年 每年里是3.1-7.31 每年是153个文件
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
with open("/data5/2019swh/data/onsetdate.json",'r') as load_f:
    a = json.load(load_f)


#合成计算model-theta
years = np.array(list(a.keys()))
days  = np.array(list(a.values()))
years = years.astype(np.int)
days = days.astype(np.int)
days -= 1

path = "/data5/2019swh/data/cal_thermal_p/"
files = os.listdir(path)
files.sort()

#获取基础信息
f0 = Nio.open_file(path+files[0])
level = f0.variables["level"][:]
lat   = f0.variables["lat"][:]
lon   = f0.variables["lon"][:]


uti0 = ma.zeros((41,42,41,97))
vti0 = ma.zeros((41,42,41,97))


#定位每年的头一日
for i in range(0,40):
    stat = i*122
    #定位文件位置
    if leap_year(years[i]):
        location = stat+days[i]-60
    else:
        location = stat+days[i]-59

    j = 0
    for dddd in range(location-30,location+11):
        f1 = Nio.open_file(path+files[dddd])
        uti = f1.variables["uti"][:]
        vti = f1.variables["vti"][:]
        uti0[j,:,:,:] += uti[:,:,:]/40
        vti0[j,:,:,:] += vti[:,:,:]/40
        j += 1

a_v = {'longname': 'thermal_wind','units': 'm s-1','valid_range': [-1000000000000000.0, 1000000000000000.0]}
time = np.arange(0,41)
fout = create_nc_multiple('/data5/2019swh/data/','composite-thermal_wind',time,level,lon,lat)
add_variables(fout,'vti',vti0,a_v,1)
add_variables(fout,'uti',uti0,a_v,1)


fout.close()