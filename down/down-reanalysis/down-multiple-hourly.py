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

def down(mmmm,vvvv,dddd):
    c = cdsapi.Client()
    c.retrieve(
        'reanalysis-era5-pressure-levels',
        {
            'product_type': 'reanalysis',
            'format': 'netcdf',
            'variable': vvvv,
            'pressure_level': [
                '10', '20', '30',
                '50', '70', '100',
                '125', '150', '175',
                '200', '225', '250',
                '300', '350', '400',
                '450', '500', '550',
                '600', '650', '700',
                '750', '775', '800',
                '825', '850', '875',
                '900', '925', '950',
                '975', '1000',
            ],
            'year': str(yyyy),
            'month': mmmm,
            'day':dddd,
            'time': [
                '00:00', '01:00', '02:00',
                '03:00', '04:00', '05:00',
                '06:00', '07:00', '08:00',
                '09:00', '10:00', '11:00',
                '12:00', '13:00', '14:00',
                '15:00', '16:00', '17:00',
                '18:00', '19:00', '20:00',
                '21:00', '22:00', '23:00',
            ],
        },
        vvvv+'_'+str(yyyy)+mmmm+dddd+'.nc')

year = yyyy
if leap_year(yyyy):
    m = month2
else:
    m = month1

files = os.listdir("/data1/other_data/DataUpdate/ERA5/new-era5/hourly"+str(year)+"/")
files.sort()
files.pop()
month=['01', '02', '03','04', '05', '06','07', '08', '09','10', '11', '12']
var = ['divergence', 'geopotential', 'relative_humidity','specific_humidity', 'temperature', 'u_component_of_wind','v_component_of_wind', 'vertical_velocity', 'vorticity']
day =['01', '02', '03','04', '05', '06','07', '08', '09','10', '11', '12','13', '14', '15','16', '17', '18','19', '20', '21','22', '23', '24','25', '26', '27','28', '29', '30','31']
for mmmm in range(0,len(month)):
    for vvvv in range(0,len(var)):
        for dddd in range(0,m[mmmm])
            name = var[vvvv]+'_'+str(yyyy)+month[mmmm]+day[dddd]+'.nc'
            if name in files:
                continue
            else:
                down(month[mmmm],var[vvvv],day[dddd])  


