import cdsapi
import sys
import os
month1 = [31,28,31,30,31,30,31,31,30,31,30,31]
month2 = [31,29,31,30,31,30,31,31,30,31,30,31]

def leap_year(year):
    #判断是不是闰年，是就返回1，不是就返回0
    if (year % 4) == 0:
        if (year % 100) == 0:
            if (year % 400) == 0:
                return 1  # 整百年能被400整除的是闰年
            else:
                return 0
        else:
            return 1  # 非整百年能被4整除的为闰年
    else:
        return 0

def down(yyyy,mmmm,vvvv,dddd):
    c = cdsapi.Client()
    c.retrieve(
        'reanalysis-era5-pressure-levels',
        {
            'product_type': 'reanalysis',
            'format': 'netcdf',
            'variable': vvvv,
            'pressure_level': [
                '10', '30',
                '50', '100',
                '150',
                '200', '250',
                '300', '350', '400',
                '450', '500', '550',
                '600', '650', '700',
                '750', '775', '800',
                '825', '850', '875',
                '900', '925', '950',
                '975', '1000',
            ],
            'grid': [1.0, 1.0],
            'year': str(yyyy),
            'month': mmmm,
            'day':dddd,
            'time': [
                '00:00',
                '03:00',
                '06:00',
                '09:00',
                '12:00',
                '15:00',
                '18:00',
                '21:00',
            ],
        },
        vvvv+'_'+str(yyyy)+mmmm+dddd+'.nc')

def down(yyyy):
    c.retrieve(
        'reanalysis-era5-pressure-levels-monthly-means',
        {
            'format': 'netcdf',
            'product_type': 'monthly_averaged_reanalysis',
            'variable': [
                'geopotential', 'specific_humidity', 'temperature',
                'u_component_of_wind', 'v_component_of_wind', 'vertical_velocity',
            ],
            'pressure_level': [
                '100', '125', '150',
                '175', '200', '225',
                '250', '300', '350',
                '400', '450', '500',
                '550', '600', '650',
                '700', '750', '800',
                '850', '900', '925',
                '950', '1000',
            ],
            'year': str(yyyy),
            'grid': [1.0, 1.0],
            'month': [
                '01', '02', '03',
                '04', '05', '06',
                '07', '08', '09',
                '10', '11', '12',
            ],
            'time': '00:00',
        },
        'download.nc')

year = [1979,2022]

files = os.listdir("/home/pi/segate/down_era5/")
files.sort()
files.pop()
month=['01', '02', '03','04', '05', '06','07', '08', '09','10', '11', '12']
var = ['geopotential', 'relative_humidity', 'temperature', 'u_component_of_wind','v_component_of_wind', 'vertical_velocity',]
day =['01', '02', '03','04', '05', '06','07', '08', '09','10', '11', '12','13', '14', '15','16', '17', '18','19', '20', '21','22', '23', '24','25', '26', '27','28', '29', '30','31']
for yyyy in range(year[0],year[1]+1):
    if leap_year(yyyy):
        m = month2
    else:
        m = month1
    for mmmm in range(0,len(month)):
        for vvvv in range(0,len(var)):
            for dddd in range(0,m[mmmm]):
                name = var[vvvv]+'_'+str(yyyy)+month[mmmm]+day[dddd]+'.nc'
                if name in files:
                    continue
                else:
                    down(yyyy,month[mmmm],var[vvvv],day[dddd])