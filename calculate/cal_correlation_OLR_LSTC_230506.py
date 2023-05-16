import numpy as np
import xarray as xr
from scipy import stats
import pandas as pd
import math

day_jul = 180; day_jun = 150; day_may = 120 ; day_apr = 90 ; day_march = 60 ; day_feb = 31; day_jan = 0
day_list = [day_jan, day_feb, day_march, day_apr, day_may, day_jun, day_jul]

def calculate_monthly_mean(var):
    '''This dunction calculate the monthly mean variables from Feb to Jun (4)'''
    # 1. Claim the monthly avg array
    mon_avg = np.zeros((63, 6))

    for yyyy in range(63):
        for i in range(6):
            mon_avg[yyyy, i] = np.average(var[yyyy, day_list[i] : day_list[i+1]])
    
    return mon_avg

file = xr.open_dataset('/home/sun/data/ERA5_data_monsoon_onset/index/quantity_index_monsoon_onset_ERA5.nc')
ls_diff1  = calculate_monthly_mean(file['ls_diff'].data)

file2 = xr.open_dataset('/home/sun/data/other_data/maritime_avg_OLR/OLR_maritime_area_average_monthly.nc').sel(year=slice(1959, 2021))

corr_index = stats.pearsonr(ls_diff1[:, 3] - np.average(ls_diff1[:, 3]), file2['ttr_avg_mon'][:, 3] - np.average(file2['ttr_avg_mon'][:, 3]))

print(corr_index)

ab = 0.65; ac = 0.51; bc = 0.39
print((ab-ac*bc)/(math.sqrt((1-ac**2)*(1-bc**2))))
print((ac-ab*bc)/(math.sqrt((1-ab**2)*(1-bc**2))))