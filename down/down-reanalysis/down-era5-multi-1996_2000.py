'''
2021/10/29
本代码下载多年的era5 pressure数据
下载完再处理成日平均
用途：个人储存
'''
import cdsapi
import os

path  =  "/home/sun/mydown/swh_era5/pressure/daily/"

def down_era(year,month,var):
    c = cdsapi.Client()
    path  =  "/home/sun/mydown/swh_era5/pressure/daily/"

    c.retrieve(
        'reanalysis-era5-pressure-levels',
        {
            'product_type': 'reanalysis',
            'format': 'netcdf',
            'variable': var,
            'pressure_level': [
                '100', '125', '150',
                '175', '200', '225',
                '250', '300', '350',
                '400', '450', '500',
                '550', '600', '650',
                '700', '750', '775',
                '800', '825', '850',
                '875', '900', '925',
                '950', '975', '1000',
            ],
                'year': year,
                'month':month,
                'day': [
                    '01', '02', '03',
                    '04', '05', '06',
                    '07', '08', '09',
                    '10', '11', '12',
                    '13', '14', '15',
                    '16', '17', '18',
                    '19', '20', '21',
                    '22', '23', '24',
                    '25', '26', '27',
                    '28', '29', '30',
                    '31',
                ],
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
        path+year+'_'+month+'_'+var+'_hourly.nc')




from cdo import Cdo,CDOException,CdoTempfileStore
cdo = Cdo()
import os
import xarray as xr
import numpy as np

year= ['1996','1997', '1998', '1999','2000']

month=[
    '01', '02', '03',
    '04', '05', '06',
    '07', '08', '09',
    '10', '11', '12',
]

variable= [
    'divergence', 'geopotential', 'relative_humidity',
    'specific_humidity', 'temperature', 'u_component_of_wind',
    'v_component_of_wind', 'vertical_velocity',
]



for yyyy in year:
    for mmmm in month:
        for vvvv in variable:
            down_era(yyyy,mmmm,vvvv)
            cdo.daymean(input=path+yyyy+'_'+mmmm+'_'+vvvv+'_hourly.nc',output=path+yyyy+'_'+mmmm+'_'+vvvv+'_monthly.nc')

            os.system("rm -rf "+path+yyyy+'_'+mmmm+'_'+vvvv+'_hourly.nc')