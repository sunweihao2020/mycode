'''
2021/10/29
本代码下载多年的era5 land数据
下载完再处理成日平均
用途：个人储存
'''
import cdsapi
import os

path  =  "/home/sun/mydown/swh_era5/land/daily/"

def down_era(year,var):
    c = cdsapi.Client()
    path  =  "/home/sun/mydown/swh_era5/land/daily/"

    c.retrieve(
        'reanalysis-era5-land',
        {
            'format': 'netcdf',
            'variable':var,
            'year': str(year),
            'month': [
                '01', '02', '03',
                '04', '05', '06',
                '07', '08', '09',
                '10', '11', '12',
            ],
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
            'grid':[1,1],
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
        path+str(year)+'_'+var+'_land_hourly.nc')


from cdo import Cdo,CDOException,CdoTempfileStore
cdo = Cdo()
import os
import xarray as xr
import numpy as np

variable=[
    '10m_u_component_of_wind', '10m_v_component_of_wind', '2m_temperature',
    'surface_latent_heat_flux', 'surface_net_solar_radiation', 'surface_pressure',
    'surface_sensible_heat_flux', 'surface_solar_radiation_downwards', 'total_precipitation',
]

for yyyy in range(2001,2022):
    for var in variable:
        down_era(yyyy,var)
        cdo.daymean(input=path+str(yyyy)+'_'+var+'_land_hourly.nc',output=path+str(yyyy)+'_'+var+'_land_monthly.nc')

        os.system("rm -rf "+path+str(yyyy)+'_'+var+'_land_hourly.nc')