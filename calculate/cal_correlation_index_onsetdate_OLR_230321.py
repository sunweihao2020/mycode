'''
2023-3-21
This script calculate correlation between the maritime continent OLR index and monsoon onset date
'''
import numpy as np
import xarray as xr
from scipy import stats
import pandas as pd


def main():
    # 1. calculate the month average
    file = xr.open_dataset('/home/sun/data/other_data/maritime_avg_OLR/OLR_maritime_area_average_monthly.nc').sel(year=slice(1959, 2021))

    onset_date = xr.open_dataset('/home/sun/data/onset_day_data/ERA5_onset_day_include_early_late_years.nc')
    dates     = onset_date['onset_day'].data

    corr_matrix = np.zeros((6, ))
    p_matrix = corr_matrix.copy()
    for i in range(6):
        corr_index = stats.pearsonr(dates - np.average(dates), file['ttr_avg_mon'][:, i] - np.average(file['ttr_avg_mon'][:, i]))
        corr_matrix[i,] = corr_index[0]
        p_matrix[i,] = corr_index[1]


    #print(corr_matrix)
    df1 = pd.DataFrame(corr_matrix, index=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'], columns=['Maritime OLR'])
    df2 = pd.DataFrame(p_matrix, index=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'], columns=['Maritime OLR'])

    df1.to_csv('/home/sun/data/ERA5_data_monsoon_onset/index/OLR_index_correlation_with_onsetdates.csv')
    df2.to_csv('/home/sun/data/ERA5_data_monsoon_onset/index/OLR_p_value.csv')

if __name__ == '__main__':
    main()
