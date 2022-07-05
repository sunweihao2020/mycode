'''2020/11/30
所用资料：era-interim
要素 ：计算合成平均的10m风
level ：单层
时间跨度： 1980-2017 38年
'''
import os
import numpy as np
import numpy.ma as ma
import Ngl, Nio
from netCDF4 import Dataset
import json
import sys
#os.system("rm -rf /data5/2019swh/data/composite_erain_shlh.nc")
sys.path.append("/data5/2019swh/mycode/module/")
from module_composite_average import *
from module_writenc import *
from attribute import *

with open("/data5/2019swh/data/onsetdate.json",'r') as load_f:
    a = json.load(load_f)

ff = Nio.open_file("/data5/2019swh/data/erain/shlh/sh_1981_.nc")
lat = ff.variables["latitude"][:]
lon = ff.variables["longitude"][:]

year = np.array(list(a.keys()))
day = np.array(list(a.values()))
years = year.astype(int)
day = day.astype(np.int)
day -= 1
location = [str(x) for x in day]  #从日期回归文件位置
path='/data5/2019swh/data/erain/shlh/'

sh = np.zeros((61,181,360))
lh = np.zeros((61,181,360))

variables=['SH','LH']
end = 38
first = 0

for yyyy in range(0,38):
    day0 = day[yyyy]
    j = 0
    f1 = Nio.open_file(path + "sh_" + year[yyyy] + "_.nc")
    f2 = Nio.open_file(path + "lh_" + year[yyyy] + "_.nc")
    sh_1 = f1.variables["sshf"][:]
    lh_1 = f2.variables["slhf"][:]
    for dddd in np.arange(day0-30,day0+31):
        sh[j, :, :] += sh_1[dddd, :, :] / (end - first)
        lh[j, :, :] += lh_1[dddd, :, :] / (end - first)
        j += 1


a_sh    = {"longname":"Surface sensible heat flux","units":"J m**-2","valid_range":[-1e+15,1e+15]}
a_lh    = {"longname":"Surface latent heat flux","units":"J m**-2","valid_range":[-1e+15,1e+15]}
time = np.arange(0,61)

fout = create_nc_single('/data5/2019swh/data/','composite_shlh',time,lon,lat)
add_variables(fout,'SSHF',sh,a_sh,0)
add_variables(fout,'SLHF',lh,a_lh,0)
fout.close()
