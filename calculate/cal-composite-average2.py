'''2020/11/5
所用资料：merra2
要素 ：计算合成平均的PS
level ：单层
'''
import os
import numpy as np
import numpy.ma as ma
import Ngl, Nio
from netCDF4 import Dataset
import json
import sys
os.system("rm -rf /data5/2019swh/data/composite_PS.nc")
sys.path.append("/data5/2019swh/mycode/module/")
from module_composite_average import *
from module_writenc import *
from attribute import *

with open("/data5/2019swh/data/onsetdate.json",'r') as load_f:
    a = json.load(load_f)

dimension = np.load('/data5/2019swh/data/dimension.npz')
lon = dimension['lon']
lat = dimension['lat']
time = np.arange(0,61)
time += 1
level = np.array([1000])

year = np.array(list(a.keys()))
day = np.array(list(a.values()))
years = year.astype(int)
day = day.astype(np.int)
day -= 1
location = [str(x) for x in day]  #从日期回归文件位置
path='/data1/MERRA2/daily/plev/'

ps = np.zeros((61,361,576))
variables=['PS']
end = 40
first = 0
for yyyy in range(0,40):
    path1 = path+year[yyyy]+"/"
    file_list = os.listdir(path1)
    file_list.sort()
    day0 = day[yyyy]
    j = 0
    for dddd in np.arange(day0-30,day0+31):
        ff = Nio.open_file(path1 + file_list[dddd])
        ps1 = ff.variables["PS"][:]
        ps[j,:,:] += ps1[0,:,:]/(end-first)
        j += 1

fout = create_nc_single('/data5/2019swh/data/','composite_PS',time,lon,lat)
add_variables(fout,'PS',ps,a_ps,0)

fout.close()


