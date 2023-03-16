'''
2023-3-9
This script calculate correlation between the indexs
month selected is 3, 4, 5
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

    i = 1
    mar_u_and_cef = stats.pearsonr(indexs[2][:, i] - np.average(indexs[2][:, i]), indexs[5][:, i] - np.average(indexs[5][:, i]))
    mar_u_and_tc = stats.pearsonr(indexs[2][:, i] - np.average(indexs[2][:, i]), indexs[4][:, i] - np.average(indexs[4][:, i]))
    mar_tc_and_cef = stats.pearsonr(indexs[5][:, i] - np.average(indexs[5][:, i]), indexs[4][:, i] - np.average(indexs[4][:, i]))

    i = 2
    apr_u_and_cef = stats.pearsonr(indexs[2][:, i] - np.average(indexs[2][:, i]), indexs[5][:, i] - np.average(indexs[5][:, i]))
    apr_u_and_tc = stats.pearsonr(indexs[2][:, i] - np.average(indexs[2][:, i]), indexs[4][:, i] - np.average(indexs[4][:, i]))
    apr_tc_and_cef = stats.pearsonr(indexs[5][:, i] - np.average(indexs[5][:, i]), indexs[4][:, i] - np.average(indexs[4][:, i]))

    i = 3
    may_u_and_cef = stats.pearsonr(indexs[2][:, i] - np.average(indexs[2][:, i]), indexs[5][:, i] - np.average(indexs[5][:, i]))
    may_u_and_tc = stats.pearsonr(indexs[2][:, i] - np.average(indexs[2][:, i]), indexs[4][:, i] - np.average(indexs[4][:, i]))
    may_tc_and_cef = stats.pearsonr(indexs[5][:, i] - np.average(indexs[5][:, i]), indexs[4][:, i] - np.average(indexs[4][:, i]))

    print(mar_u_and_cef)
    print(mar_u_and_tc)
    print(mar_tc_and_cef)
    print(apr_u_and_cef)
    print(apr_u_and_tc)
    print(apr_tc_and_cef)
    print(may_u_and_cef)
    print(may_u_and_tc)
    print(may_tc_and_cef)


if __name__ == '__main__':
    main()
