import os
import numpy as np
import numpy.ma as ma
import Ngl, Nio
from netCDF4 import Dataset
import json
import sys
import metpy.calc as mc
from metpy.units import units
sys.path.append("/data5/2019swh/mycode/module/")
from module_sun import *
from module_writenc import *
from attribute import *

f = Nio.open_file("/data5/2019swh/data/composite_rh.nc")
f2 = Nio.open_file("/data5/2019swh/data/composite3.nc")
rh = f.variables["RH"][:]
t  = f2.variables["T"][:]
lat = f.variables["lat"][:]
lon = f.variables["lon"][:]
time = f.variables["time"][:]
level = f.variables["level"][:]
tm = t * units.kelvin
td = mc.dewpoint_from_relative_humidity(tm,rh).to('kelvin').m

file = create_nc("/data5/2019swh/data/","dewpoint",time,level,lon,lat)
add_variables(file,"td",ug,a_T)

file.close()
