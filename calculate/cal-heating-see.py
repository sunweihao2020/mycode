import os
import numpy as np
import numpy.ma as ma
import Ngl, Nio
from netCDF4 import Dataset
import json
import sys
import math
sys.path.append("/data5/2019swh/mycode/module/")
from module_writenc import *
from module_sun import *
#from attribute import *
with open("/data5/2019swh/data/onsetdate.json",'r') as load_f:
    a = json.load(load_f)

f = Nio.open_file("/data5/2019swh/data/composite3.nc")
f2 = Nio.open_file("/data5/2019swh/data/composite_equivalent_tem.nc")

w = f.variables["OMEGA"][:]
u = f.variables["uwind"][:]
t = f2.variables["theate_e"][:]
v = f.variables["vwind"][:]
lat = f.variables["lat"][:]
lon = f.variables["lon"][:]
lev = f.variables["level"][:]

disy,disx,location = cal_xydistance(lat,lon)
time = np.arange(61)+1
tt = np.gradient(t,time,axis = 0)
ty = ma.zeros((61,42,361,576))
tx = ma.zeros((61,42,361,576))
for dd in range(0, u.shape[0]):
    for z in range(0, u.shape[1]):
        ty[dd, z, :, :] = np.gradient(t[dd, z, :, :], location, axis=0)
        for latt in range(1, u.shape[2]-1):
            tx[dd, z, latt, :] = np.gradient(t[dd, z, latt, :], disx[latt], axis=0)
term2 = u*tx+v*ty

thetap = np.gradient(t,lev,axis=1)
pp = conform(lev,(61,42,361,576),0,2,3)

#term3 = np.power((pp/1000),0.286)*w[:,:,:,:]*thetap[:,:,:,:]

see_heating = 1.004*np.power((pp/1000),0.286)*(tt+term2+w*thetap)

a_pl = {'longname': 'see heating','units': 'K day-1','valid_range': [-1000000000000000.0, 1000000000000000.0]}
time = np.arange(0,61)
fout = create_nc_multiple('/data5/2019swh/data/','composite-see_heating2',time,lev,lon,lat)
add_variables(fout,'see_heating',see_heating,a_pl,1)



fout.close()

