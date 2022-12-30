'''
22-12-20
This script aims to response the reviewer first question: demonstrate the model has achieved stable
I have to constructure 150 year time series of surface temperature
'''
####################################################################################################
#  Total: 30 + 16 + 6 + 5 + 5 + 30 + 25 = 127
#
#  First series: b1850_con_ensemble_spinup_1
#                period: 360 months
#                path: /home/sun/model_output/b1850_exp/b1850_control/b1850_con_ensemble_spinup_1/atm/hist
#
#  Second series: b1850_con_ensemble_official_1
#                 period: 5840 days ( 16 years )
#                 path: /home/sun/model_output/b1850_exp/b1850_con_ensemble_official_1/atm/hist
#
#  Third series:  b1850_con_ensemble_official_1_spinup_1_official_1
#                 period: 2191 days ( 6 years 1day)
#                 path: /home/sun/model_output/b1850_exp/b1850_con_ensemble_official_1_spinup_1_official_1/atm/hist
#
#  Fourth series: b1850_con_ensemble_spinup_2
#                 period: 180 months only use late 5 years
#                 path: /home/sun/model_output/b1850_exp/b1850_control/b1850_con_ensemble_spinup_2/atm/hist

#  Fifth series:  b1850_con_ensemble_spinup_3
#                 period: 180 months only use late 5 years
#                 path: /home/sun/model_output/b1850_exp/b1850_control/b1850_con_ensemble_spinup_3/atm/hist
#
#  Sixth series:  b1850_con_ensemble_official_2
#                 period:  9490 days (26 years)
#                 path: /home/sun/model_output/b1850_exp/b1850_con_ensemble_official_2/atm/hist
#
#  Seventh series:  b1850_con_ensemble_official_2
#                   period:  10950 ( 30 years )
#                   path: /home/sun/model_output/b1850_exp/b1850_con_ensemble_official_3/atm/hist
#
#  Eighth series:  Well I find the old spinup file, That's lucky
#                  casename: b1850_control4_220624
#                  period:  53 - 90 (38 years)
####################################################################################################
import os
import numpy as np
import xarray as xr

path1  =  '/home/sun/model_output/b1850_exp/b1850_control/b1850_con_ensemble_spinup_1/atm/hist/'
path2  =  '/home/sun/model_output/b1850_exp/b1850_con_ensemble_official_1/atm/hist/'
path3  =  '/home/sun/model_output/b1850_exp/b1850_con_ensemble_official_1_spinup_1_official_1/atm/hist/'
path4  =  '/home/sun/model_output/b1850_exp/b1850_control/b1850_con_ensemble_spinup_2/atm/hist/'
path5  =  '/home/sun/model_output/b1850_exp/b1850_control/b1850_con_ensemble_spinup_3/atm/hist/'
path6  =  '/home/sun/model_output/b1850_exp/b1850_con_ensemble_official_2/atm/hist/'
path7  =  '/home/sun/model_output/b1850_exp/b1850_con_ensemble_official_3/atm/hist/'
path8  =  '/home/sun/model_output/spinup/'
month_day  =  np.array([31,28,31,30,31,30,31,31,30,31,30,31])


def paint_time_series(series, path='/home/sun/paint/lunwen/version6.0/spinup/', name='test.pdf'):
    import matplotlib.pyplot as plt
    import numpy as np

    with plt.style.context('Solarize_Light2'):
        fig, ax = plt.subplots()
        plt.plot(series)

        plt.xlabel("Global-Mean TS",fontsize=20)
        plt.ylabel("Model year",fontsize=20)

        plt.savefig(path + name, dpi=400)

def deal_with_series1(path, filetype):
    file_list1  =  os.listdir(path)  ;  file_list1.sort()

    print("This is series1 filelist, the save type is {}, length is {}".format(filetype, len(file_list1)))

    ts_series1  =  np.array([], dtype=np.float32)

    for fname in file_list1:
        f0          =  xr.open_dataset(path + fname)
        ts_series1  =  np.append(ts_series1, np.average(f0['TS'].data))

    return ts_series1

def deal_with_series2(path, filetype):
    file_list2  =  os.listdir(path)
    for ffff in file_list2:
        if '.b185' in ffff:
            file_list2.remove(ffff)
    file_list2.sort()

    print("This is series2 filelist, the save type is {}, length is {}, years is {}".format(filetype, len(file_list2), len(file_list2)/365))

    ts_series2  =  np.array([], dtype=np.float32)

    for yyyy in range(int(len(file_list2) / 365)):
        file_list2_subset_year  =  file_list2[yyyy * 365 : yyyy * 365 + 365]
        for mmmm in range(12):
            # claim month average
            avg_month  =  0
            file_list2_subset_month  =  file_list2_subset_year[np.sum(month_day[0:mmmm]) : np.sum(month_day[0:(mmmm + 1)])]

            #print(len(file_list2_subset_month))

            for ffff in file_list2_subset_month:
                f0  =  xr.open_dataset(path + ffff)
                avg_month += np.average(f0['TS'].data) / len(file_list2_subset_month)
            
            #print(avg_month)
            ts_series2  =  np.append(ts_series2, avg_month)

    return ts_series2

def deal_with_series3(path, filetype):
    file_list3  =  os.listdir(path)
    for ffff in file_list3:
        if '.b185' in ffff:
            file_list3.remove(ffff)
    file_list3.sort()

    print("This is series3 filelist, the save type is {}, length is {}, years is {}".format(filetype, len(file_list3), len(file_list3)/365))

    ts_series3  =  np.array([], dtype=np.float32)

    for yyyy in range(int(len(file_list3) / 365)):
        file_list3_subset_year  =  file_list3[yyyy * 365 : yyyy * 365 + 365]
        for mmmm in range(12):
            # claim month average
            avg_month  =  0
            file_list3_subset_month  =  file_list3_subset_year[np.sum(month_day[0:mmmm]) : np.sum(month_day[0:(mmmm + 1)])]

            #print(len(file_list3_subset_month))

            for ffff in file_list3_subset_month:
                f0  =  xr.open_dataset(path + ffff)
                avg_month += np.average(f0['TS'].data) / len(file_list3_subset_month)
            
            #print(avg_month)
            ts_series3  =  np.append(ts_series3, avg_month)

    return ts_series3

def deal_with_series4(path, filetype):
    file_list4  =  os.listdir(path)  ;  file_list4.sort()

    print("This is series1 filelist, the save type is {}, length is {}".format(filetype, len(file_list4)))

    ts_series4  =  np.array([], dtype=np.float32)

    for fname in file_list4:
        f0          =  xr.open_dataset(path + fname)
        ts_series4  =  np.append(ts_series4, np.average(f0['TS'].data))

    return ts_series4

def deal_with_series8(path, filetype):
    file_list  =  os.listdir(path)

    file_list2 =  []
    for ffff in file_list:
        if ('b1850_control4_220624' in ffff) and ('.cam.h0.' in ffff) and ('.b185' not in ffff):
            file_list2.append(ffff)
        else:
            continue
    
    file_list2.sort()
    print("This is series8 filelist, the save type is {}, length is {}".format(filetype, len(file_list2)))
    #print(file_list2)
    ts_series1  =  np.array([], dtype=np.float32)

    for fname in file_list2:
        #print(fname)
        f0          =  xr.open_dataset(path + fname)
        #print(fname)
        ts_series1  =  np.append(ts_series1, np.average(f0['TS'].data))

    return ts_series1


def save_array(vars, path, name):
    '''This function save the numpy array'''
    os.system('rm -rf ' + path + name)

    with open(path + name, 'wb') as f:
        np.save(f, vars)

def main():
    # calculate time series
    series1  =  deal_with_series1(path1, 'Month')
    print('series1 successfully')
    series2  =  deal_with_series2(path2, 'Day')
    print('series2 successfully')
    series3  =  deal_with_series3(path3, 'Day')
    print('series3 successfully')
    series4  =  deal_with_series4(path4, 'Month')
    print('series4 successfully')
    series5  =  deal_with_series4(path5, 'Month')  # only change path thus use the same path
    print('series5 successfully')
    series6  =  deal_with_series2(path6, 'Day')
    print('series6 successfully')
    series7  =  deal_with_series2(path7, 'Day')
    print('series7 successfully')
    series8  =  deal_with_series8(path8, 'Month')  # I found the old experiments spinup file
    print('series8 successfully')

    # save the series
    path_out  =  '/home/sun/data/model_data/spin-up/ts_time_series/'
    save_array(series1, path_out, 'con_ts_s1.npy')
    save_array(series2, path_out, 'con_ts_s2.npy')
    save_array(series3, path_out, 'con_ts_s3.npy')
    save_array(series4, path_out, 'con_ts_s4.npy')
    save_array(series5, path_out, 'con_ts_s5.npy')
    save_array(series6, path_out, 'con_ts_s6.npy')
    save_array(series7, path_out, 'con_ts_s7.npy')
    save_array(series8, path_out, 'con_ts_s8.npy')


    paint_time_series(series8, name='con_series8_spinup.pdf')

    #print(series1)

if __name__ == '__main__':
    main()