import cdsapi
import sys
sys.path.append("/data5/2019swh/mycode/module/")
from module_sun import *
def down(year,date):
    c = cdsapi.Client()
    c.retrieve('reanalysis-era5-complete', {
        'class': 'ea',
        'date': date,
        'expver': '1',
        'levelist': '134/135/136/137',
        'levtype': 'ml',
        'area': [
                60, 30, -60,
                120],
        'param': '129/130/131/132/135/138/235005',
        'step': '0',
        'stream': 'oper',
        'time': '06:00:00/18:00:00',
        'grid'    : '1.0/1.0',
        'type': 'fc',
        'format'  : 'netcdf', 
    }, str(year)+'.nc')

year = 1981
if leap_year(year):
    day = 61
else:
    day = 60

day_end = day+120
date = []
for dddd in range(day,day_end):
    date.append(out_date(year,dddd))

down(year,date)

#!/usr/bin/env python
import cdsapi
c = cdsapi.Client()
c.retrieve('reanalysis-era5-complete', {
    'class': 'ea',
    'date': '1985-06-12',
    'expver': '1',
    'levelist': '136/137',
    'levtype': 'ml',
    'area': [60, 30, -60,
                120],
    'param': '235005',
    'step': '1/2/3/4/5/6/7/8/9/10/11/12',
    'stream': 'oper',
    'time': '06:00:00/18:00:00',
    'grid': '1.0/1.0',
    'type': 'fc',
    'format': 'netcdf',
},'11.nc')