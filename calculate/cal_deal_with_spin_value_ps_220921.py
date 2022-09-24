'''
2022-09-05
This code deal with spin up files for b1850 experiment to see whether the model is in equilibrium
This index here is global mean temperature (var name: TS)
'''

from ntpath import join


src_path  =  "/home/sun/model_output/spinup/"

# experiment name: [control, indian, maritime, inch, global1m]
'''
here we need to discriminate each period for different experiments:
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
def joint_control():
    '''This function do:
        1. calculate global temperature
        2. joint array from different experiment
    '''
    import os
    import xarray as xr
    import numpy as np

    exp_name  =  ['b1850m_control3_220617','b1850_control4_220624']

    # First step : get the file list and sort by date
    # Here I create lists including each exp respectively, and then joint them
    file_list =  os.listdir(src_path)

    list0     =  []
    list1     =  []
    for ffff in file_list:
        if (exp_name[0] in ffff) and ('cam' in ffff) and ('mom' not in ffff):
            list0.append(ffff)
        elif exp_name[1] in ffff and ('cam' in ffff) and ('mom' not in ffff):
            list1.append(ffff)
        else:
            continue
    
    list0.sort()  ;  list1.sort()
    files     =  list0 + list1   # all files for exp control
    
    print("now calculate global mean TS and joint it")
    # --------- now calculate global mean TS and joint it --------------------
    ts        =  []
    for ffff in files:
        f0    =  xr.open_dataset(src_path + ffff)
        ts.append(np.average(f0.TS.data))

    # here transfer monthly average to yearly average
    print("The years number is {:.2f}".format(len(files)/12))
    year_n    =  int(len(files)/12)

    ts_year   =  []
    
    for i in range(year_n):
        ts_year.append(np.average(ts[i*12:i*12+12]))


    import matplotlib.pyplot as plt
    plt.plot(ts_year)

    plt.savefig('/home/sun/paint/b1850_exp/spinup/ts_control.pdf')

    return ts_year

def joint_indian():
    '''This function do:
        1. calculate global temperature
        2. joint array from different experiment
    '''
    import os
    import xarray as xr
    import numpy as np

    exp_name  =  ['b1850_tx_indian_h0_220718','b1850_tx_indian_h1_220726','b1850_tx_indian_h2_220731']

    # First step : get the file list and sort by date
    # Here I create lists including each exp respectively, and then joint them
    file_list =  os.listdir(src_path)

    list0     =  []
    list1     =  []
    list2     =  []
    for ffff in file_list:
        if (exp_name[0] in ffff) and ('cam' in ffff) and ('mom' not in ffff):
            list0.append(ffff)
        elif exp_name[1] in ffff and ('cam' in ffff) and ('mom' not in ffff):
            list1.append(ffff)
        elif exp_name[2] in ffff and ('cam' in ffff) and ('mom' not in ffff):
            list2.append(ffff)
        else:
            continue
    
    list0.sort()  ;  list1.sort()  ;  list2.sort()
    files     =  list0 + list1 + list2  # all files for exp control
    
    print("now calculate global mean TS and joint it")
    # --------- now calculate global mean TS and joint it --------------------
    ts        =  []
    for ffff in files:
        f0    =  xr.open_dataset(src_path + ffff)
        ts.append(np.average(f0.TS.data))

    # here transfer monthly average to yearly average
    print("The years number is {:.2f}".format(len(files)/12))
    year_n    =  int(len(files)/12)

    ts_year   =  []
    
    for i in range(year_n):
        ts_year.append(np.average(ts[i*12:i*12+12]))


    import matplotlib.pyplot as plt
    plt.plot(ts_year)

    plt.savefig('/home/sun/paint/b1850_exp/spinup/ts_indian.pdf')

    return ts_year

def joint_inch():
    '''This function do:
        1. calculate global temperature
        2. joint array from different experiment
    '''
    import os
    import xarray as xr
    import numpy as np

    exp_name  =  ['b1850_tx_inch_220811']

    # First step : get the file list and sort by date
    # Here I create lists including each exp respectively, and then joint them
    file_list =  os.listdir(src_path)

    list0     =  []
    for ffff in file_list:
        if (exp_name[0] in ffff) and ('cam' in ffff) and ('mom' not in ffff):
            list0.append(ffff)
        else:
            continue
    
    list0.sort()  
    files     =  list0   # all files for exp control
    
    print("now calculate global mean TS and joint it")
    # --------- now calculate global mean TS and joint it --------------------
    ts        =  []
    for ffff in files:
        f0    =  xr.open_dataset(src_path + ffff)
        ts.append(np.average(f0.TS.data))

    # here transfer monthly average to yearly average
    print("The years number is {:.2f}".format(len(files)/12))
    year_n    =  int(len(files)/12)

    ts_year   =  []
    
    for i in range(year_n):
        ts_year.append(np.average(ts[i*12:i*12+12]))


    import matplotlib.pyplot as plt
    plt.plot(ts_year)

    plt.savefig('/home/sun/paint/b1850_exp/spinup/ts_inch.pdf')

    return ts_year

def joint_global1m():
    '''This function do:
        1. calculate global temperature
        2. joint array from different experiment
    '''
    import os
    import xarray as xr
    import numpy as np

    exp_name  =  ['b1850_global_1m_220620']

    # First step : get the file list and sort by date
    # Here I create lists including each exp respectively, and then joint them
    file_list =  os.listdir(src_path)

    list0     =  []
    for ffff in file_list:
        if (exp_name[0] in ffff) and ('cam' in ffff) and ('mom' not in ffff):
            list0.append(ffff)
        else:
            continue
    
    list0.sort()  
    files     =  list0   # all files for exp control
    
    print("now calculate global mean TS and joint it")
    # --------- now calculate global mean TS and joint it --------------------
    ts        =  []
    for ffff in files:
        f0    =  xr.open_dataset(src_path + ffff)
        ts.append(np.average(f0.TS.data))

    # here transfer monthly average to yearly average
    print("The years number is {:.2f}".format(len(files)/12))
    year_n    =  int(len(files)/12)

    ts_year   =  []
    
    for i in range(year_n):
        ts_year.append(np.average(ts[i*12:i*12+12]))


    import matplotlib.pyplot as plt
    plt.plot(ts_year)

    plt.savefig('/home/sun/paint/b1850_exp/spinup/ts_global1m.pdf')

    return ts_year

def joint_maritime():
    '''This function do:
        1. calculate global temperature
        2. joint array from different experiment
    '''
    import os
    import xarray as xr
    import numpy as np

    exp_name  =  ['b1850_tx4_maritime_220624','b1850_tx_maritime_h1_220629','b1850_tx_maritime_h1_220721','b1850_tx_maritime_h2_220725']

    # First step : get the file list and sort by date
    # Here I create lists including each exp respectively, and then joint them
    file_list =  os.listdir(src_path)

    list0     =  []
    list1     =  []
    list2     =  []
    list3     =  []
    for ffff in file_list:
        if (exp_name[0] in ffff) and ('cam' in ffff) and ('mom' not in ffff):
            list0.append(ffff)
        elif exp_name[1] in ffff and ('cam' in ffff) and ('mom' not in ffff):
            list1.append(ffff)
        elif exp_name[2] in ffff and ('cam' in ffff) and ('mom' not in ffff):
            list2.append(ffff)
        elif exp_name[3] in ffff and ('cam' in ffff) and ('mom' not in ffff):
            list3.append(ffff)
        else:
            continue
    
    list0.sort()  ;  list1.sort()  ;  list2.sort()  ;  list3.sort()
    files     =  list0 + list1 + list2 +list3 # all files for exp control
    
    print("now calculate global mean TS and joint it")
    # --------- now calculate global mean TS and joint it --------------------
    ts        =  []
    for ffff in files:
        f0    =  xr.open_dataset(src_path + ffff)
        ts.append(np.average(f0.TS.data))

    # here transfer monthly average to yearly average
    print("The years number is {:.2f}".format(len(files)/12))
    year_n    =  int(len(files)/12)

    ts_year   =  []
    
    for i in range(year_n):
        ts_year.append(np.average(ts[i*12:i*12+12]))


    import matplotlib.pyplot as plt
    plt.plot(ts_year)

    plt.savefig('/home/sun/paint/b1850_exp/spinup/ts_maritime.pdf')

    return ts_year



def main():
    import numpy as np
    
    control  =  np.array(joint_control())
    indian   =  np.array(joint_indian())
    inch     =  np.array(joint_inch())
    global1m =  np.array(joint_global1m())
    maritime =  np.array(joint_maritime())

    spinup   =  np.array([control,indian,inch,global1m,maritime])

    print(spinup)

    np.save("/home/sun/data/model_data/spin-up/spinup_TS.npy",spinup)

    #with open("/home/sun/data/model_data/spin-up/spinup.txt", 'w') as f:


if __name__ == '__main__':
    main()