'''
2020/12/27
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
from attribute import *
with open("/data5/2019swh/data/onsetdate.json",'r') as load_f:
    a = json.load(load_f)
#合成计算modelpv
'''
a_pv   = {"longname":"pv","units":"K m+2 kg-1 s-1","valid_range":[-1e+15,1e+15]}
years = np.array(list(a.keys()))
days  = np.array(list(a.values()))
years = years.astype(np.int)
days = days.astype(np.int)

path = "/data1/other_data/DataUpdate/ERA5/merra2/modelpv/"
files = os.listdir(path)
files.sort()

#获取基础信息
f0 = Nio.open_file(path+files[0])
level = f0.variables["level"][:]
lat   = f0.variables["lat"][:]
lon   = f0.variables["lon"][:]
level2 = [level[10],level[16],level[23],level[32]]
lev2   = [10,16,23,32]

pvh0 = ma.zeros((61,4,361,576)) #合成后的pv
pvv0 = ma.zeros((61,4,361,576))
all_pv0 = ma.zeros((61,4,361,576))

#定位每年的头一日
for i in range(0,36):
    stat = i*153
    #定位文件位置
    if leap_year(years[i]):
        location = stat+days[i]-60
    else:
        location = stat+days[i]-59

    j = 0
    for dddd in range(location-30,location+31):
        f1 = Nio.open_file(path+files[dddd])
        pvh = f1.variables["pvh"][:]
        pvv = f1.variables["pvv"][:]
        all_pv = f1.variables["all_pv"][:]
        for ll in range(0,4):
            pvh0[j,ll,:,:] += pvh[0,lev2[ll],:,:]/36
            pvv0[j,ll,:,:] += pvv[0,lev2[ll],:,:]/36
            all_pv0[j,ll,:,:] += all_pv[0,lev2[ll],:,:]/36
        j += 1


time = np.arange(0,61)
fout = create_nc_multiple('/data5/2019swh/data/','composite-modelpv',time,level2,lon,lat)
add_variables(fout,'pvh',pvh0,a_pv,1)
add_variables(fout,'pvv',pvv0,a_pv,1)
add_variables(fout,'all_pv',all_pv0,a_pv,1)

fout.close()
'''

#合成计算model-theta
years = np.array(list(a.keys()))
days  = np.array(list(a.values()))
years = years.astype(np.int)
days = days.astype(np.int)
days -= 1

path = "/data1/other_data/DataUpdate/ERA5/merra2/model_theta/"
files = os.listdir(path)
files.sort()

#获取基础信息
f0 = Nio.open_file(path+files[0])
level = f0.variables["level"][:]
lat   = f0.variables["lat"][:]
lon   = f0.variables["lon"][:]


theta0 = ma.zeros((61,33,361,576)) #合成后的pv
pl0 = ma.zeros((61,33,361,576))


#定位每年的头一日
for i in range(0,40):
    stat = i*153
    #定位文件位置
    if leap_year(years[i]):
        location = stat+days[i]-60
    else:
        location = stat+days[i]-59

    j = 0
    for dddd in range(location-30,location+31):
        f1 = Nio.open_file(path+files[dddd])
        theta = f1.variables["theta"][:]
        pl = f1.variables["PL"][:]
        theta0[j,:,:,:] += theta[0,:,:,:]/40
        pl0[j,:,:,:] += pl[0,:,:,:]/40
        j += 1

a_pl = {'longname': 'pressure_level','units': 'Pa','valid_range': [-1000000000000000.0, 1000000000000000.0]}
time = np.arange(0,61)
fout = create_nc_multiple('/data5/2019swh/data/','composite-modeltheta',time,level,lon,lat)
add_variables(fout,'theta',theta0,a_T,1)
add_variables(fout,'pl',pl0,a_pl,1)


fout.close()