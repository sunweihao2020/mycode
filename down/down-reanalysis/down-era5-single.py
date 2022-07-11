#下载era5 2m温度以及地表温度
import cdsapi
import sys
sys.path.append("/data5/2019swh/mycode/module/")
from module_sun import *
def down(mmmm,dddd)
    c = cdsapi.Client()

    c.retrieve(
        'reanalysis-era5-single-levels',
        {
            'product_type': 'reanalysis',
            'variable': [
                '2m_temperature', 'skin_temperature',
            ],
            'year': yyyy,
            'month': mmmm,
            'day': dddd,
            'time': [
                '00:00', '03:00', '06:00',
                '09:00', '12:00', '15:00',
                '18:00', '21:00',
            ],
            'area': [
                60, 30, -60,
                150,
            ],
            'format': 'netcdf',
        },
        str(yyyy)+'-'+mmmm'.nc')

year = yyyy
if leap_year(year):
    day = 61
else:
    day = 60

day_end = day+120

for dddd in range(day,day_end):
    down(out_date(year,day)[5:7],out_date(year,day)[8:10])

