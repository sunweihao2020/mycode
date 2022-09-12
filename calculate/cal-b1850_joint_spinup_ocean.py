'''
2022-9-10
This code joint the series for the spin-up ocean model output
'''

'''
Here is the summary for the spinup experiment:
1. control:     1.1  b1850m_control3_220617 01 - 52
                1.2  b1850_control4_220624  53 - 96
                This may be branch run in these experiments

2. indian:      2.1  b1850_tx_indian_h0_220718 01 - 58
                2.2  b1850_tx_indian_h1_220726 59 - 84
                2.3  b1850_tx_indian_h2_220731 01 - 26

3. maritime:    3.1  b1850_tx4_maritime_220624     01 - 26
                3.2  b1850_tx_maritime_h1_220629   01 - 46
                3.3  b1850_tx_maritime_h1_220721   47 - 58
                3.4  b1850_tx_maritime_h2_220725   59 - 94

4. inch:        4.1  b1850_tx_inch_220811  01 - 90

5. global1m     5.1  b1850_global_1m_220620 21 - 98
'''

import os

def joint_control():
    '''spinup exp for control is two'''
    exp_names  =  ['b1850m_control3_220617','b1850_control4_220624']

    path0      =  '/home/sun/segate/model_data/spinup/b1850_control/ocean/'
    path1      =  '/home/sun/segate/model_data/spinup/b1850_control/ocean_new/'
    all_files  =  os.listdir(path0)

    year      =  0

    for nnnn in exp_names:
        # first: get the file names
        nnnn_2    =   nnnn[:-6]
        namelist  =  []
        for ffff in all_files:
            if nnnn_2 in ffff:
                namelist.append(ffff)

        namelist.sort()

        range1    =  int(len(namelist)/12)

        print("The year for the {} is {}".format(nnnn,range1))


        for i in range(range1):  # year_loop
            year_number  =  year + 1
            for j in range(12):  # month_loop
                if year_number < 10:
                    y_n   =   "0" + str(year_number)
                else:
                    y_n   =   str(year_number)
                month_number =  j + 1
                if month_number < 10:
                    m_n   =   "0" + str(j+1)
                else:
                    m_n   =   str(j + 1)
                new_name  =  "b1850_control_hm_spinup_" + y_n + "_" + m_n +'.nc'
#
                os.system('mv '+path0+namelist[i*12+j] + ' '+path1+new_name)
                print('old_name is {}, new name is {}'.format(namelist[i*12+j],new_name))
#
            year += 1

def joint_indian():
    '''spinup exp for control is three'''
    exp_names  =  ['b1850_tx_indian_h0_220718','b1850_tx_indian_h1_220726','b1850_tx_indian_h2_220731']

    path0      =  '/home/sun/segate/model_data/spinup/b1850_indian/ocean/'
    path1      =  '/home/sun/segate/model_data/spinup/b1850_indian/ocean_new/'
    all_files  =  os.listdir(path0)

    year      =  0

    for nnnn in exp_names:
        # first: get the file names
        nnnn_2    =   nnnn[:-6]
        namelist  =  []
        for ffff in all_files:
            if nnnn_2 in ffff:
                namelist.append(ffff)

        namelist.sort()

        range1    =  int(len(namelist)/12)

        print("The year for the {} is {}".format(nnnn,range1))


        for i in range(range1):  # year_loop
            year_number  =  year + 1
            for j in range(12):  # month_loop
                if year_number < 10:
                    y_n   =   "0" + str(year_number)
                else:
                    y_n   =   str(year_number)
                month_number =  j + 1
                if month_number < 10:
                    m_n   =   "0" + str(j+1)
                else:
                    m_n   =   str(j + 1)
                new_name  =  "b1850_indian_hm_spinup_" + y_n + "_" + m_n +'.nc'
#
                os.system('mv '+path0+namelist[i*12+j] + ' '+path1+new_name)
                print('old_name is {}, new name is {}'.format(namelist[i*12+j],new_name))
#
            year += 1

def joint_maritime():
    '''spinup exp for control is 4'''
    exp_names  =  ['b1850_tx4_maritime_220624','b1850_tx_maritime_h1_220629','b1850_tx_maritime_h2_220725']

    path0      =  '/home/sun/segate/model_data/spinup/b1850_maritime/ocean/'
    path1      =  '/home/sun/segate/model_data/spinup/b1850_maritime/ocean_new/'
    all_files  =  os.listdir(path0)

    year      =  0

    for nnnn in exp_names:
        # first: get the file names
        nnnn_2    =   nnnn[:-6]
        namelist  =  []
        for ffff in all_files:
            if nnnn_2 in ffff:
                namelist.append(ffff)

        namelist.sort()


        range1    =  int(len(namelist)/12)

        print("The year for the {} is {}".format(nnnn,range1))


        for i in range(range1):  # year_loop
            year_number  =  year + 1
            for j in range(12):  # month_loop
                if year_number < 10:
                    y_n   =   "0" + str(year_number)
                else:
                    y_n   =   str(year_number)
                month_number =  j + 1
                if month_number < 10:
                    m_n   =   "0" + str(j+1)
                else:
                    m_n   =   str(j + 1)
                new_name  =  "b1850_maritime_hm_spinup_" + y_n + "_" + m_n +'.nc'
#
                os.system('mv '+path0+namelist[i*12+j] + ' '+path1+new_name)
                print('old_name is {}, new name is {}'.format(namelist[i*12+j],new_name))
#
            year += 1

def joint_inch():
    '''spinup exp for control is 1'''
    exp_names  =  ['b1850_tx_inch_220811']

    path0      =  '/home/sun/segate/model_data/spinup/b1850_inch/ocean/'
    all_files  =  os.listdir(path0)

    year      =  0

    for nnnn in exp_names:
        # first: get the file names
        nnnn_2    =   nnnn[:-6]
        namelist  =  []
        for ffff in all_files:
            if nnnn_2 in ffff:
                namelist.append(ffff)

        namelist.sort()

        range1    =  int(len(namelist)/12)

        print("The year for the {} is {}".format(nnnn,range1))


        

def main():
    joint_control()
    joint_indian()
    joint_maritime()
    #joint_inch()

if __name__ == '__main__':
    main()