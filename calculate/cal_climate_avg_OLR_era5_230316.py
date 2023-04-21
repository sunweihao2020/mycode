'''
2023-3-16
This script calculate the climate average for the ERA5 OLR data
Here I want to check up the quality of the ERA5 data among different period(1940 - 1959)
'''
import xarray as xr
import os
import numpy as np

path_in = '/home/sun/data/other_data/down_ERA5_hourly_OLR_convert_float_daymean/'

year_1 = 1940 ; year_2 = 1980 ; year_3 = 2022

def calculate_climate_period(start_year, end_year):
    '''
    calculate the climate average given the start and end year
    '''
    # =============== 1. claim the ref array ====================
    ref_f = xr.open_dataset(path_in + '1941_hourly_OLR.nc')
    base_array = np.zeros(ref_f['ttr'].data.shape)

    year_number = end_year - start_year + 1

    for yyyy in range(start_year, end_year + 1):
        f0 = xr.open_dataset(path_in + str(yyyy) + '_hourly_OLR.nc')

        base_array += f0['ttr'].data[0:365] / year_number

    return base_array

def main():
    # 1. calculate average among 1940 - 1980
    ref_f = xr.open_dataset(path_in + '1941_hourly_OLR.nc')

    # 4. Write to ncfile
    ncfile  =  xr.Dataset(
                    {
                        'ttr_40to80': (["time", "lat", "lon"], calculate_climate_period(year_1, year_2)),
                        'ttr_40to22': (["time", "lat", "lon"], calculate_climate_period(year_1, year_3)),
                        'ttr_80to22': (["time", "lat", "lon"], calculate_climate_period(year_2, year_3)),
                    },
                    coords={
                        "lat": (["lat"], ref_f.latitude.data),
                        "lon": (["lon"], ref_f.longitude.data),
                        "time": (["time"], np.linspace(1,365,365,dtype=int)),
                    },
                    )
    ncfile['ttr_40to80'].attrs = ref_f['ttr'].attrs
    ncfile['ttr_40to22'].attrs = ref_f['ttr'].attrs
    ncfile['ttr_80to22'].attrs = ref_f['ttr'].attrs
    ncfile.attrs['description'] = 'created on 2023-3-16. This is climate average OLR based on ERA5 data, including the period among three different time slice'

    ncfile.to_netcdf('/home/sun/data/ERA5_data_monsoon_onset/climatic_daily_ERA5/single/OLR_climatic_daily.nc')

if __name__ == '__main__':
    main()