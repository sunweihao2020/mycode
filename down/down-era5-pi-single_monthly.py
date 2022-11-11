import cdsapi
import sys
import os
month1 = [31,28,31,30,31,30,31,31,30,31,30,31]
month2 = [31,29,31,30,31,30,31,31,30,31,30,31]

def down(yyyy):
    c = cdsapi.Client()
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
        '/home/pi/segate/down_era5_month_single/monthly_averaged_single_vars_+'+str(yyyy)+'.nc')

year = [1959,2022]

for y in range(year[0],year[1]+1):
    down(y)