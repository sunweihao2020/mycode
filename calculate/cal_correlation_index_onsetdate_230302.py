'''
2023-3-2
This script calculate correlation between the index and monsoon onset date
'''
import numpy as np
import xarray as xr
from scipy import stats
import pandas as pd

# Day for monthly average
# Here I think I should calculate based on the monthly mean
day_jun = 150; day_may = 120 ; day_apr = 90 ; day_march = 60 ; day_feb = 31
day_list = [day_feb, day_march, day_apr, day_may, day_jun]

def calculate_monthly_mean(var):
    '''This dunction calculate the monthly mean variables from Feb to Jun (4)'''
    # 1. Claim the monthly avg array
    mon_avg = np.zeros((63, 4))

    for yyyy in range(63):
        for i in range(4):
            mon_avg[yyyy, i] = np.average(var[yyyy, day_list[i] : day_list[i+1]])
    
    return mon_avg

def main():
    # 1. calculate the month average
    file = xr.open_dataset('/home/sun/data/ERA5_data_monsoon_onset/index/quantity_index_monsoon_onset_ERA5.nc')

    s_bob_sst = calculate_monthly_mean(file['s_bob_sst'].data)
    io_sst    = calculate_monthly_mean(file['io_sst'].data)
    u_bob     = calculate_monthly_mean(file['u_bob'].data)
    ls_diff1  = calculate_monthly_mean(file['ls_diff1'].data)
    ls_diff2  = calculate_monthly_mean(file['ls_diff2'].data)
    bob_cef   = calculate_monthly_mean(file['bob_cef'].data)

    onset_date = xr.open_dataset('/home/sun/data/onset_day_data/ERA5_onset_day_include_early_late_years.nc')
    dates     = onset_date['onset_day'].data
    
    # 2. Calculate pearson relation
    # This is a 6 * 4 = 24 matrix
    indexs = [s_bob_sst, io_sst, u_bob, ls_diff1, ls_diff2, bob_cef]
    indexs_name = ['Southern_BOB_SST', 'Tropical_Indian_Ocean_SST', 'Southern_BOB_U', 'Land-Sea_diff_1', 'Land-Sea_diff_2', 'BOB_CEF']
    #print(stats.pearsonr(dates - np.average(dates), (s_bob_sst[:,2] - np.average(s_bob_sst[:, 2]))))
    corr_matrix = np.zeros((4, 6))
    p_matrix = corr_matrix.copy()
    for i in range(4):
        for j in range(6):
            corr_index = stats.pearsonr(dates - np.average(dates), indexs[j][:, i] - np.average(indexs[j][:, i]))
            corr_matrix[i, j] = corr_index[0]
            p_matrix[i, j] = corr_index[1]

    #print(corr_matrix)
    df1 = pd.DataFrame(corr_matrix, index=['Feb', 'Mar', 'Apr', 'May'], columns=indexs_name)
    df2 = pd.DataFrame(p_matrix, index=['Feb', 'Mar', 'Apr', 'May'], columns=indexs_name)

    df1.to_csv('/home/sun/data/ERA5_data_monsoon_onset/index/index_correlation_with_onsetdates.csv')
    df2.to_csv('/home/sun/data/ERA5_data_monsoon_onset/index/p_value.csv')

if __name__ == '__main__':
    main()
