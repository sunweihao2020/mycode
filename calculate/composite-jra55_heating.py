'''
2021/2/28
本代码计算jra55的加热资料，时间跨度1980-1985共6年
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

variables = ['adhr','cnvhr','lrghr','lwhr','vdfhr']
def hebing(year):
    path1 = "/data5/2019swh/mydown/jra55_nc/"
    variables = ['adhr', 'cnvhr', 'lrghr', 'lwhr', 'vdfhr']
    number = ['222','242','241','251','246']
    variables_name = ['ADHR_GDS0_ISBL_ave6h','CNVHR_GDS0_ISBL_ave6h','LRGHR_GDS0_ISBL_ave6h','LWHR_GDS0_ISBL_ave6h','VDFHR_GDS0_ISBL_ave6h']
    adhr = ma.zeros((31+30+31,37,145,288))
    cnvhr = ma.zeros((31 + 30 + 31, 37, 145, 288))
    lrghr = ma.zeros((31 + 30 + 31, 37, 145, 288))
    lwhr = ma.zeros((31 + 30 + 31, 37, 145, 288))
    vdfhr = ma.zeros((31 + 30 + 31, 37, 145, 288))
    all_var = [adhr,cnvhr,lrghr,lwhr,vdfhr]
    for var in range(0,len(variables)):
        f1 = Nio.open_file(path1+variables[var]+"."+str(year)+"030100_"+str(year)+"033118.nc")
        f2 = Nio.open_file(path1+variables[var]+"."+str(year) + "040100_" + str(year) + "043018.nc")
        f3 = Nio.open_file(path1+variables[var]+"."+str(year)+"050100_"+str(year)+"053118.nc")
        a = f1.variables[variables_name[var]][:]
        b = f2.variables[variables_name[var]][:]
        c = f3.variables[variables_name[var]][:]
        all_var[var][0:31,:,:,:] = a
        all_var[var][31:61,:,:,:] = b
        all_var[var][61:,:,:,:] =c
    return all_var


with open("/data5/2019swh/data/onsetdate.json",'r') as load_f:
    a = json.load(load_f)
years = np.array(list(a.keys()))
days = np.array(list(a.values()))
years = years.astype(np.int)
days = days.astype(np.int)

#获取维度信息
f1 = Nio.open_file("/data5/2019swh/mydown/jra55_nc/fcst_phy3m125.222_adhr.2001030100_2001033118.nc")
level = f1.variables["lv_ISBL1"][:]
lat = f1.variables["g0_lat_2"][:]
lon = f1.variables["g0_lon_3"][:]

#计算30+1+4共35天
adiabatic_heating_rate = ma.zeros((35,37,145,288))
convective_heating_rate = ma.zeros((35,37,145,288))
condensation_heating_rate = ma.zeros((35,37,145,288))
radiation_heating_rate = ma.zeros((35,37,145,288))
vertical_diffusion_rate = ma.zeros((35,37,145,288))

for i in range(0,29):
    if leap_year(years[i]):
        location = days[i]-30-60
    else:
        location = days[i]-30-61
    j = 0

    vvvv = hebing(years[i])
    for dddd in range(location,location+35):
        adiabatic_heating_rate[j,:,:,:] += vvvv[0][dddd,:,:,:]/34
        convective_heating_rate[j,:,:,:] += vvvv[1][dddd,:,:,:]/34
        condensation_heating_rate[j,:,:,:] += vvvv[2][dddd,:,:,:]/34
        radiation_heating_rate[j,:,:,:] += vvvv[3][dddd,:,:,:]/34
        vertical_diffusion_rate[j,:,:,:] += vvvv[4][dddd,:,:,:]/34
        j += 1

for i in range(30,35):
    if leap_year(years[i]):
        location = days[i]-30-60
    else:
        location = days[i]-30-61
    j = 0

    vvvv = hebing(years[i])
    for dddd in range(location,location+35):
        adiabatic_heating_rate[j,:,:,:] += vvvv[0][dddd,:,:,:]/34
        convective_heating_rate[j,:,:,:] += vvvv[1][dddd,:,:,:]/34
        condensation_heating_rate[j,:,:,:] += vvvv[2][dddd,:,:,:]/34
        radiation_heating_rate[j,:,:,:] += vvvv[3][dddd,:,:,:]/34
        vertical_diffusion_rate[j,:,:,:] += vvvv[4][dddd,:,:,:]/34
        j += 1


time = np.arange(0,35)
a_tdt = {'longname': 'temperature tendency', 'units': 'K day-1', 'valid_range': [-1000000000000000.0, 1000000000000000.0]}
fout = create_nc_multiple('/data5/2019swh/data/','composite-heating-jra55',time,level,lon,lat)
add_variables(fout,'adiabatic',adiabatic_heating_rate,a_tdt,1)
add_variables(fout,'convective',convective_heating_rate,a_tdt,1)
add_variables(fout,'condensation',condensation_heating_rate,a_tdt,1)
add_variables(fout,'radiation',radiation_heating_rate,a_tdt,1)
add_variables(fout,'diffusion',vertical_diffusion_rate,a_tdt,1)


fout.close()

