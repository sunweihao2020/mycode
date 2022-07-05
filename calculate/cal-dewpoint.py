'''
2020/12/13
merra2合成分析资料
手动计算相当位温
多层次

formula:
TD: =243.04*(LN(RH/100)+((17.625*T)/(243.04+T)))/(17.625-LN(RH/100)-((17.625*T)/(243.04+T)))
'''
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

f1   = Nio.open_file("/data5/2019swh/data/composite3.nc")
f2   = Nio.open_file("/data5/2019swh/data/composite_rh.nc")
lat = f1.variables["lat"][:]
lon = f1.variables["lon"][:]
level = f1.variables["level"][:]
t   = f1.variables["T"][:]
rh  = f2.variables["RH"][:]

td  =   ma.array(ma.zeros((61,42,361,576)),mask=t.mask)
for yyyy in range(0,361):
    for xxxx in range(0,576):
        for zzzz in range(0,42):
            for tttt in range(0,61):
                if td[tttt,zzzz,yyyy,xxxx] is ma.masked:
                    continue
                else:
                    td[tttt,zzzz,yyyy,xxxx] = dew_point((t[tttt,zzzz,yyyy,xxxx]-273.15),rh[tttt,zzzz,yyyy,xxxx])

time = np.arange(0,61)+1
file = create_nc_multiple("/data5/2019swh/data/","composite_dewpoint",time,level,lon,lat)
add_variables(file,"td",td,a_T,1)

file.close()