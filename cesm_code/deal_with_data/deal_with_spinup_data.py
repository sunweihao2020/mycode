'''
2022-6-29
This script is to deal with spin up data for paint
'''
import xarray as xr
import numpy as np
import os

path0      =  "/home/sun/model_output/spinup/"
file_list  =  os.listdir(path0)

exp_name  =  ["global_1m","control","indian","maritime"]
''' global_1m : include: b1850_global_1m_220620 (period: 21 to 71)
    control   : include: b1850m_control3_220617 (period: 01 to 52)
                         b1850_control4_220624  (period: 53 to 76)
    indian    : include: b1850_tx6_indian_220622 (period: 43 to 60)
                         b1850_tx_indian_220627 (period: 01 to 18)
    maritime  : include: b1850_tx4_maritime_220624 (period: 01 to 26)
                         b1850_tx_maritime_h1_220629

'''

'''
Methods: Here we focus two quantities (TOA budget) and (TS), I will calculate the variables' year average
TOA calculate process: FSNT - FLNT
'''

def cal_year_mean(list,name,year):
    '''This function using name and year to screen files for calculate. The output is year average'''
    if year < 10:
        yyyy = "000" + str(year)
    elif 10 <= year  <100:
        yyyy = "00"  + str(year)
    else:
        yyyy = "0" + str(year)

    # sclect 12 months file this year
    list2    =  []
    for ff in list:
        if (name in ff) and (yyyy in ff) and ("cam" in ff):
            list2.append(ff)

    if len(list2) > 12:
        print("error in %d %-20s" % year % name)  # test whether it has over 12 times
    else:
        list2.sort()

    # initialization
    ts  =  0 ; toa  =  0
    for ff in list2:     # calculate year average
        f0  =   xr.open_dataset(path0+ff)
        ts  +=  np.average(f0.TS)/12
        toa +=  (np.average(f0.FSNT) - np.average(f0.FLNT))/12

    return ts,toa

def deal_global_1m():
    '''This function deal with experiment: global 1m'''
    start0  =  21 ; end0  =  71
    name    =   "global_1m"
    list0   =  []
    for ff in file_list:
        if name in ff:
            list0.append(ff)
    # initialization
    ts  =  np.zeros((end0-start0+1)) ; toa  =  np.zeros((end0-start0+1))

    for i in range(start0,end0+1):
        ts_i,toa_i = cal_year_mean(list0,name,i)
        ts[i-start0]     =    ts_i
        toa[i-start0]    =    toa_i

    return ts,toa

def deal_control():
    '''This function deal with experiment: control'''
    length  =  52 + (76-53+1) # two experiment
    start1  =  1  ;  start2  =  53
    end1    =  52 ;  end2    =  76
    name1   =  "b1850m_control3_220617"
    name2   =  "b1850_control4_220624"
    list1   =   [] ; list2    =    []
    for ff in file_list:
        if name1 in ff:
            list1.append(ff)
        elif name2 in ff:
            list2.append(ff)
    ts  =  np.zeros((length))  ;  toa  =  np.zeros((length))

    for i1 in range(start1,end1+1):
        ts_i1,toa_i1   =  cal_year_mean(list1,name1,i1)
        ts[i1-start1]  =  ts_i1
        toa[i1-start1] =  toa_i1
    for i2 in range(start2,end2+1):
        ts_i2, toa_i2  = cal_year_mean(list2, name2, i2)
        ts[i2-start1] = ts_i2
        toa[i2-start1] = toa_i2
    return ts,toa

def deal_indian():
    '''This function deal with experiment: no_indian'''
    length = (60-43+1) + (18 - 1 + 1)  # two experiment
    start1 = 43
    start2 = 1
    end1   = 60
    end2   = 18
    name1 = "b1850_tx6_indian_220622"
    name2 = "b1850_tx_indian_220627"
    list1 = []
    list2 = []
    for ff in file_list:
        if name1 in ff:
            list1.append(ff)
        elif name2 in ff:
            list2.append(ff)
    ts  = np.zeros((length))
    toa = np.zeros((length))

    for i1 in range(start1, end1 + 1):
        ts_i1, toa_i1 = cal_year_mean(list1, name1, i1)
        ts[i1 - start1] = ts_i1
        toa[i1 - start1] = toa_i1
    for i2 in range(start2, end2 + 1):
        ts_i2, toa_i2 = cal_year_mean(list2, name2, i2)
        ts[(i2 - start2) + (60-43+1)] = ts_i2
        toa[(i2 - start2) + (60-43+1)] = toa_i2
    return ts, toa

def deal_maritime():
    '''This function deal with experiment: no_indian'''
    length = (26-1+1) + ( - 1 + 1)  # two experiment
    start1 = 43
    start2 = 1
    end1   = 60
    end2   = 18
    name1 = "b1850_tx6_indian_220622"
    name2 = "b1850_tx_indian_220627"
    list1 = []
    list2 = []
    for ff in file_list:
        if name1 in ff:
            list1.append(ff)
        elif name2 in ff:
            list2.append(ff)
    ts  = np.zeros((length))
    toa = np.zeros((length))

    for i1 in range(start1, end1 + 1):
        ts_i1, toa_i1 = cal_year_mean(list1, name1, i1)
        ts[i1 - start1] = ts_i1
        toa[i1 - start1] = toa_i1
    for i2 in range(start2, end2 + 1):
        ts_i2, toa_i2 = cal_year_mean(list2, name2, i2)
        ts[(i2 - start2) + (60-43+1)] = ts_i2
        toa[(i2 - start2) + (60-43+1)] = toa_i2
    return ts, toa

def main():
    ts_1,toa_1 = deal_indian()
    #ts_2, toa_2 = deal_global_1m()
    import matplotlib.pyplot as plt
    plt.plot(ts_1)
    #plt.plot(ts_2)
    plt.show()

if __name__ == "__main__":
    main()