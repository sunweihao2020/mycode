'''
2022-12-24
This code calculate the time series of the no_indian experiments TS variable
'''
###############################################################################
#  54
#  1. /home/sun/model_output/b1850_exp/exp_output/
#     b1850_tx_indian_o1_220808
#     period: 1 - 54 (total 54*365 + 1 days)
#
#  2. /home/sun/model_output/spinup/
#     b1850_tx_indian_220627
#     period: 1 - 58 (month data)
#
#  3. b1850_tx_indian_h0_220718
#     period: 1 - 84 (month data)
# ------------------- 1. get the file list ----------------------------------
#import os
#path0  =  '/home/sun/model_output/spinup/'
#file_list  =  os.listdir(path0)  ;  file_list.sort()
#file_indian=  []
#
#with open('/home/sun/data/model_data/spin-up/list/indian_spinup_path.txt', 'w') as fp:
#    for ffff in file_list:
#        if ('indian' in ffff) and ('inch' not in ffff) and ('mom' not in ffff):
#            fp.write("%s\n" % ffff)

import os
import xarray as xr
import numpy as np

from cal_150year_spinup_ts_control_221220 import save_array

path1  =  '/home/sun/model_output/b1850_exp/exp_output/'
path2  =  '/home/sun/model_output/spinup/'
month_day  =  np.array([31,28,31,30,31,30,31,31,30,31,30,31])

file_list0  =  os.listdir(path2)

def deal_with_series1(path):
    ''' Because I have write to the txt file, here I read from txt-file to get name'''

    ts_series1  =  np.array([], dtype=np.float32)
    file_list   =  []
    with open('/home/sun/data/model_data/spin-up/list/indian_expout_path.txt', 'r') as fp:
        for line in fp:
            file_list.append(line[:-1])

    file_list.sort()
    #print(file_list)
    ts_series3  =  np.array([], dtype=np.float32)

    for yyyy in range(int(len(file_list) / 365)):
        file_list3_subset_year  =  file_list[yyyy * 365 : yyyy * 365 + 365]
        for mmmm in range(12):
            # claim month average
            avg_month  =  0
            file_list3_subset_month  =  file_list3_subset_year[np.sum(month_day[0:mmmm]) : np.sum(month_day[0:(mmmm + 1)])]

            #print(len(file_list3_subset_month))

            for ffff in file_list3_subset_month:
                f0  =  xr.open_dataset(path + ffff, engine='netcdf4')
                avg_month += np.average(f0['TS'].data) / len(file_list3_subset_month)
            
            #print(avg_month)
            ts_series3  =  np.append(ts_series3, avg_month)

    return ts_series3

def deal_with_series2(path, list):
    ts_series1  =  np.array([], dtype=np.float32)

    for fname in list:
        print(fname)
        f0          =  xr.open_dataset(path + fname, engine='netcdf4')
        ts_series1  =  np.append(ts_series1, np.average(f0['TS'].data))

    return ts_series1


def main():
    # --------- series 1 -----------
    ts1  =  deal_with_series1(path1)

    # --------- series 2 -----------
    name2  =  'b1850_tx_indian_220627'
    list2  =  []
    for ffff in file_list0:
        if name2 in ffff and '.b185' not in ffff and 'mom' not in ffff:
            list2.append(ffff)
    list2.sort()
    ts2  =  deal_with_series2(path2, list2)

    # --------- series 3 -----------
    name2  =  'b1850_tx_indian_h0_220718'
    list2  =  []
    for ffff in file_list0:
        if name2 in ffff and '.b185' not in ffff and 'mom' not in ffff:
            list2.append(ffff)
    list2.sort()
    ts3  =  deal_with_series2(path2, list2)

    # -------- save array ------------------
    path_out  =  '/home/sun/data/model_data/spin-up/ts_time_series/'
    save_array(ts1, path_out, 'indian_ts_s1.npy')
    save_array(ts2, path_out, 'indian_ts_s2.npy')
    save_array(ts3, path_out, 'indian_ts_s3.npy')

    print(ts1.shape)
    print(ts2.shape)
    print(ts3.shape)

if __name__ == '__main__':
    main()