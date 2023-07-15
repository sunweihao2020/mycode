'''
2023-6-5
This script calculate global correlation between onsetdate and sst gradient
'''
import os
import xarray as xr
import numpy as np
from scipy import stats

path0 = '/home/sun/wd_disk/era5_sst_gradient/monthly_mean/'
file_list = os.listdir(path0) ; file_list.sort()

onset_date = xr.open_dataset('/home/sun/data/onset_day_data/onsetdate.nc')
ref_file   = xr.open_dataset(path0 + 'era5_single_sea_surface_temperature_01_gradient.nc')

def calculate_global_correlation(fname, vname='sst_gradient'):
    f1 = xr.open_dataset(path0 + fname).isel(time=slice(21, 61)) #corresponding to the 1980 to 2019

    # Claim correlation
    corre_matrix = np.zeros((181, 360))
    p_matrix     = corre_matrix.copy()

    for i in range(181):
        for j in range(360):
            if np.isnan(f1[vname][0, i, j].data):
                continue
            else:
                corr_index = stats.pearsonr(onset_date['bob_onset_date'].data - np.average(onset_date['bob_onset_date'].data), f1[vname][:, i, j].data - np.average(f1[vname][:, i, j].data))
                corre_matrix[i, j] = corr_index[0]
                p_matrix[i, j] = corr_index[1]
    #print(f1.time.data)
    return corre_matrix, p_matrix


def main():
    #f_test = xr.open_dataset(path0 + 'era5_single_sea_surface_temperature_01_gradient.nc') 
    #print(f_test['sst_gradient'].data[:, 6, 284] == np.nan)
    corre_jan, p_jan = calculate_global_correlation('era5_single_sea_surface_temperature_01_gradient.nc') # 6, 284
    print('jan yes')
    corre_feb, p_feb = calculate_global_correlation('era5_single_sea_surface_temperature_02_gradient.nc')
    print('feb yes')
    corre_mar, p_mar = calculate_global_correlation('era5_single_sea_surface_temperature_03_gradient.nc')
    print('mar yes')
    corre_apr, p_apr = calculate_global_correlation('era5_single_sea_surface_temperature_04_gradient.nc')
    print('apr yes')
    corre_may, p_may = calculate_global_correlation('era5_single_sea_surface_temperature_05_gradient.nc')
    print('may yes')
    corre_jun, p_jun = calculate_global_correlation('era5_single_sea_surface_temperature_06_gradient.nc')
    print('jun yes')
#
    ## Write to nc file
    ncfile  =  xr.Dataset(
                    {
                        'corre_jan': (["lat", "lon"], corre_jan),
                        'corre_feb': (["lat", "lon"], corre_feb),
                        'corre_mar': (["lat", "lon"], corre_mar),
                        'corre_apr': (["lat", "lon"], corre_apr),
                        'corre_may': (["lat", "lon"], corre_may),
                        'corre_jun': (["lat", "lon"], corre_jun),
                        'p_jan': (["lat", "lon"], p_jan),
                        'p_feb': (["lat", "lon"], p_feb),
                        'p_mar': (["lat", "lon"], p_mar),
                        'p_apr': (["lat", "lon"], p_apr),
                        'p_may': (["lat", "lon"], p_may),
                        'p_jun': (["lat", "lon"], p_jun),
                    },
                    coords={
                        "lat": (["lat"], ref_file.latitude.data),
                        "lon": (["lon"], ref_file.longitude.data),
                    },
                    )
    ncfile.attrs['description'] = 'created on 2023-6-5. This is global correlation and p value matrix between BOBSM onset date and SST gradient(north)'
#
    ncfile.to_netcdf('/home/sun/data/ERA5_data_monsoon_onset/correlation/global_correlation_bobsm_onset_SST_north_gradient.nc')

if __name__ == '__main__':
    main()