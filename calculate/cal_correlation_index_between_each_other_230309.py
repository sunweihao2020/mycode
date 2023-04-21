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

    file2 = xr.open_dataset('/home/sun/data/other_data/maritime_avg_OLR/OLR_maritime_area_average_monthly.nc').sel(year=slice(1959, 2021))
    
    # 2. Calculate pearson relation
    # This is a 6 * 4 = 24 matrix
    indexs = [s_bob_sst, io_sst, u_bob, ls_diff1, ls_diff2, bob_cef]

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

    # OLR
    i = 1
    mar_u_and_olr   = stats.pearsonr(indexs[2][:, i] - np.average(indexs[2][:, i]), file2['ttr_avg_mon'][:, i+1] - np.average(file2['ttr_avg_mon'][:, i+1]))
    mar_tc_and_olr  = stats.pearsonr(indexs[4][:, i] - np.average(indexs[4][:, i]), file2['ttr_avg_mon'][:, i+1] - np.average(file2['ttr_avg_mon'][:, i+1]))
    mar_cef_and_olr = stats.pearsonr(indexs[5][:, i] - np.average(indexs[5][:, i]), file2['ttr_avg_mon'][:, i+1] - np.average(file2['ttr_avg_mon'][:, i+1]))

    i = 2
    apr_u_and_olr   = stats.pearsonr(indexs[2][:, i] - np.average(indexs[2][:, i]), file2['ttr_avg_mon'][:, i+1] - np.average(file2['ttr_avg_mon'][:, i+1]))
    apr_tc_and_olr  = stats.pearsonr(indexs[4][:, i] - np.average(indexs[4][:, i]), file2['ttr_avg_mon'][:, i+1] - np.average(file2['ttr_avg_mon'][:, i+1]))
    apr_cef_and_olr = stats.pearsonr(indexs[5][:, i] - np.average(indexs[5][:, i]), file2['ttr_avg_mon'][:, i+1] - np.average(file2['ttr_avg_mon'][:, i+1]))

    i = 3
    may_u_and_olr   = stats.pearsonr(indexs[2][:, i] - np.average(indexs[2][:, i]), file2['ttr_avg_mon'][:, i+1] - np.average(file2['ttr_avg_mon'][:, i+1]))
    may_tc_and_olr  = stats.pearsonr(indexs[4][:, i] - np.average(indexs[4][:, i]), file2['ttr_avg_mon'][:, i+1] - np.average(file2['ttr_avg_mon'][:, i+1]))
    may_cef_and_olr = stats.pearsonr(indexs[5][:, i] - np.average(indexs[5][:, i]), file2['ttr_avg_mon'][:, i+1] - np.average(file2['ttr_avg_mon'][:, i+1]))

    #print(mar_u_and_cef)
    #print(mar_u_and_tc)
    #print(mar_tc_and_cef)
    #print(apr_u_and_cef)
    #print(apr_u_and_tc)
    #print(apr_tc_and_cef)
    #print(may_u_and_cef)
    #print(may_u_and_tc)
    #print(may_tc_and_cef)

    print(mar_u_and_olr)
    print(mar_tc_and_olr)
    print(mar_cef_and_olr)
    print(apr_u_and_olr)
    print(apr_tc_and_olr)
    print(apr_cef_and_olr)
    print(may_u_and_olr)
    print(may_tc_and_olr)
    print(may_cef_and_olr)


if __name__ == '__main__':
    main()
