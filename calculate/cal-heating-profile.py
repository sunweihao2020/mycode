'''
2021/1/28
利用merra2资料计算加热廓线
所用资料路径：/data/tdt-merra
'''
#先计算合成平均 每一年从3.1—6.30是122天
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

start = datetime.datetime.now()
#获取维度信息
file1 = os.listdir("/data5/2019swh/mydown/merra-tdt/daymean")
file1.sort()
f1 = Nio.open_file("/data5/2019swh/mydown/merra-tdt/daymean/"+file1[0])
lon = f1.variables["lon"][:]
lat = f1.variables["lat"][:]
lev = f1.variables["lev"][:]

#原数据是一天八个时次，这里计算日平均
'''
file1 = os.listdir("/data5/2019swh/mydown/merra-tdt")
file1.sort()
for file in file1:
    name_out = file[27:35]+".nc"
    os.system("cdo daymean /data5/2019swh/mydown/merra-tdt/"+file+" /data5/2019swh/mydown/merra-tdt/daymean/"+name_out)
'''
#计算合成平均
total = ma.zeros((61,26,121,91))
dynamic = ma.zeros((61,26,121,91))
moist = ma.zeros((61,26,121,91))
radiation = ma.zeros((61,26,121,91))
physics = ma.zeros((61,26,121,91))
turbulence = ma.zeros((61,26,121,91))

#获取时间变量
with open("/data5/2019swh/data/onsetdate.json",'r') as load_f:
    a = json.load(load_f)
years = np.array(list(a.keys()))
days = np.array(list(a.values()))
years = years.astype(np.int)
days = days.astype(np.int)

for i in range(0,40):
    stat = i*122
    #定位
    if leap_year(years[i]):
        location = stat+days[i]-60
    else:
        location = stat+days[i]-59

    j = 0
    for dddd in range(location-30,location+31):
        f2 = Nio.open_file("/data5/2019swh/mydown/merra-tdt/daymean/"+file1[dddd])
        total2 = f2.variables["DTDTANA"][0,:,:,:]
        dynamic2 = f2.variables["DTDTDYN"][0,:,:,:]
        moist2 = f2.variables["DTDTMST"][0,:,:,:]
        radiation2 = f2.variables["DTDTRAD"][0,:,:,:]
        physics2 = f2.variables["DTDTTOT"][0,:,:,:]
        turbulence2 = f2.variables["DTDTTRB"][0,:,:,:]

        total[j,:,:,:] += total2/40
        dynamic[j,:,:,:] += dynamic2/40
        moist[j,:,:,:] += moist2/40
        radiation[j,:,:,:] += radiation2/40
        physics[j,:,:,:] += physics2/40
        turbulence[j,:,:,:] += turbulence2/40

        j += 1

time = np.arange(0,61)
a_tdt = {'longname': 'temperature tendency', 'units': 'K s-1', 'valid_range': [-1000000000000000.0, 1000000000000000.0]}
fout = create_nc_multiple('/data5/2019swh/data/','composite-heating-merra',time,lev,lon,lat)
add_variables(fout,'total',total*60*60*24,a_tdt,1)
add_variables(fout,'dynamic',dynamic*60*60*24,a_tdt,1)
add_variables(fout,'moist',moist*60*60*24,a_tdt,1)
add_variables(fout,'radiation',radiation*60*60*24,a_tdt,1)
add_variables(fout,'physics',physics*60*60*24,a_tdt,1)
add_variables(fout,'turbulence',turbulence*60*60*24,a_tdt,1)

fout.close()

end = datetime.datetime.now()
print('Running time: %s Seconds'%(end-start))
