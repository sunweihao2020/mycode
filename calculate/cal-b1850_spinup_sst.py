'''
This code calculate and paint spinup sst to see whether the model is stable
'''

import os

path_control  =  '/home/sun/segate/model_data/spinup/b1850_control/ocean_new/'
path_indian   =  '/home/sun/segate/model_data/spinup/b1850_indian/ocean_new/'
path_inch     =  '/home/sun/segate/model_data/spinup/b1850_inch/ocean/'
path_maritime =  '/home/sun/segate/model_data/spinup/b1850_maritime/ocean_new/'

def calculate_yearly_average(path,filelist):
    '''This function calculate year average for input files, filelist contains 12 times file'''
    import numpy as np
    import xarray as xr

    global_sst = 0
    for ffff in filelist:
        f0  =  xr.open_dataset(path + ffff)

        monthly_sst  =  np.nanmean(f0['tos'].data)

        global_sst   += monthly_sst / 12

    return global_sst

def calculate_yearly_average_indianocean(path,filelist):
    '''This function calculate year average for input files, filelist contains 12 times file, the area is indian ocean'''
    import numpy as np
    import xarray as xr

    global_sst = 0
    for ffff in filelist:
        f0  =  xr.open_dataset(path + ffff).sel(xh=slice(40,110),yh=slice(-60,60))

        monthly_sst  =  np.nanmean(f0['tos'].data)

        global_sst   += monthly_sst / 12

    return global_sst

def calculate_yearly_average_pacificocean(path,filelist):
    '''This function calculate year average for input files, filelist contains 12 times file, the area is pacific ocean'''
    import numpy as np
    import xarray as xr

    global_sst = 0
    for ffff in filelist:
        f0  =  xr.open_dataset(path + ffff).sel(xh=slice(110,270),yh=slice(-60,60))

        monthly_sst  =  np.nanmean(f0['tos'].data)

        global_sst   += monthly_sst / 12

    return global_sst

def cal_spinup_series():
    import numpy as np
    import xarray as xr


    files_control  =  os.listdir(path_control)    ;    files_control.sort()
    files_indian   =  os.listdir(path_indian)     ;    files_indian.sort()
    files_inch     =  os.listdir(path_inch)       ;    files_inch.sort()
    files_maritime =  os.listdir(path_maritime)   ;    files_maritime.sort()

    # print(len(files_indian)/12)
    # print(len(files_inch)/12)
    # print(len(files_control)/12)
    # print(len(files_maritime)/12)
    
    # deal with control exp
    series_control  =  np.array([])
    for i in range(int(len(files_control)/12)):
        series_control  =  np.append(series_control,calculate_yearly_average(path_control,files_control[i*12:i*12+12]))

    # deal with indian exp
    series_indian   =  np.array([])
    for i in range(int(len(files_indian)/12)):
        series_indian  =  np.append(series_indian,calculate_yearly_average(path_indian,files_indian[i*12:i*12+12]))

    # deal with inch exp
    series_inch   =  np.array([])
    for i in range(int(len(files_inch)/12)):
        series_inch  =  np.append(series_inch,calculate_yearly_average(path_inch,files_inch[i*12:i*12+12]))

    # deal with maritime exp
    series_maritime   =  np.array([])
    for i in range(int(len(files_maritime)/12)):
        series_maritime  =  np.append(series_maritime,calculate_yearly_average(path_maritime,files_maritime[i*12:i*12+12]))

# ----------------------  Indian Ocean  ----------------------------------------------------
    # deal with control exp
    series_control_indian  =  np.array([])
    for i in range(int(len(files_control)/12)):
        series_control_indian =  np.append(series_control_indian,calculate_yearly_average_indianocean(path_control,files_control[i*12:i*12+12]))

    # deal with indian exp
    series_indian_indian   =  np.array([])
    for i in range(int(len(files_indian)/12)):
        series_indian_indian  =  np.append(series_indian_indian,calculate_yearly_average_indianocean(path_indian,files_indian[i*12:i*12+12]))

    # deal with inch exp
    series_inch_indian   =  np.array([])
    for i in range(int(len(files_inch)/12)):
        series_inch_indian  =  np.append(series_inch_indian,calculate_yearly_average_indianocean(path_inch,files_inch[i*12:i*12+12]))

    # deal with maritime exp
    series_maritime_indian   =  np.array([])
    for i in range(int(len(files_maritime)/12)):
        series_maritime_indian  =  np.append(series_maritime_indian,calculate_yearly_average_indianocean(path_maritime,files_maritime[i*12:i*12+12]))

# ------------------------ pacific ocean  -----------------------------------------------------
    # deal with control exp
    series_control_pacific  =  np.array([])
    for i in range(int(len(files_control)/12)):
        series_control_pacific =  np.append(series_control_pacific,calculate_yearly_average_pacificocean(path_control,files_control[i*12:i*12+12]))

    # deal with indian exp
    series_indian_pacific   =  np.array([])
    for i in range(int(len(files_indian)/12)):
        series_indian_pacific  =  np.append(series_indian_pacific,calculate_yearly_average_pacificocean(path_indian,files_indian[i*12:i*12+12]))

    # deal with inch exp
    series_inch_pacific    =  np.array([])
    for i in range(int(len(files_inch)/12)):
        series_inch_pacific  =  np.append(series_inch_pacific,calculate_yearly_average_pacificocean(path_inch,files_inch[i*12:i*12+12]))

    # deal with maritime exp
    series_maritime_pacific   =  np.array([])
    for i in range(int(len(files_maritime)/12)):
        series_maritime_pacific  =  np.append(series_maritime_pacific,calculate_yearly_average_pacificocean(path_maritime,files_maritime[i*12:i*12+12]))

    ncfile  =  xr.Dataset(
    {
        "control_global_sst":      (["time_control"],     series_control),
        "indian_global_sst":       (["time_indian"],      series_indian),
        "inch_global_sst":         (["time_inch"],        series_inch),
        "maritime_global_sst":     (["time_maritime"],    series_maritime),
        "control_indian_sst":      (["time_control"],     series_control_indian),
        "indian_indian_sst":       (["time_indian"],      series_indian_indian),
        "inch_indian_sst":         (["time_inch"],        series_inch_indian),
        "maritime_indian_sst":     (["time_maritime"],    series_maritime_indian),
        "control_pacific_sst":      (["time_control"],     series_control_pacific),
        "indian_pacific_sst":       (["time_indian"],      series_indian_pacific),
        "inch_pacific_sst":         (["time_inch"],        series_inch_pacific),
        "maritime_pacific_sst":     (["time_maritime"],    series_maritime_pacific),
    },
    coords={
        "time_control": (["time_control"], np.linspace(1,int(len(files_control)/12),int(len(files_control)/12))),
        "time_inch": (["time_inch"], np.linspace(1,int(len(files_inch)/12),int(len(files_inch)/12))),
        "time_indian": (["time_indian"], np.linspace(1,int(len(files_indian)/12),int(len(files_indian)/12))),
        "time_maritime": (["time_maritime"], np.linspace(1,int(len(files_maritime)/12),int(len(files_maritime)/12))),
    },
    )

    ncfile.to_netcdf("/home/sun/data/model_data/spin-up/spinup_sst_data.nc")



def main():
    cal_spinup_series()

if __name__ == '__main__':
    main()
