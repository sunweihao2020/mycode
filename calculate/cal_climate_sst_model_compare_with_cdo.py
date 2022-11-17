'''
2022-11-11
This code compare the result of cdo and calculate using python
Data is the model output SST and I need to calculate the climatology monthly average
'''
path0 =  '/home/sun/data/ocean_data/'

def calculate_monthly_average():
    '''
    1. calculate monthly average
    2. calculate climatology
    '''
    import numpy as np
    import xarray as xr
    import os

    # ---------  1. get the file lists  --------------
    files = os.listdir(path0) ; file_list = []
    for nnnn in files:
        if 'sfc_' in nnnn:
            file_list.append(nnnn)

    #print(file_list)
    # ---------  2. claim the base array  ------------
    f0 = xr.open_dataset(path0 + file_list[1])
    avg_sst = np.zeros((365,458,540))

    years   = len(file_list)

    for i in range(years):
        print('Now it is in year {yy}'.format(yy=i))
        f1  = xr.open_dataset(path0 + file_list[i])

        avg_sst += f1.tos.data / years

    print(avg_sst[20,:,10])

    # ---------  3. calculate monthly mean  ---------
    month_day  =  np.array([31,28,31,30,31,30,31,31,30,31,30,31])
    print(np.sum(month_day))

    monthly_avg_sst  =  np.zeros((12,458,540))

    start  =  0
    for j in range(12):
        end  =  start + month_day[j]
        monthly_avg_sst[j]  =  np.average(avg_sst[start:end],axis=0)

        start += month_day[j]

    print(monthly_avg_sst[2,:,20])

    # --------  4. write to ncfile -----------------
    ncfile  =  xr.Dataset(
    {
        "tos": (["time", "yh", "xh"], monthly_avg_sst),
    },
    coords={
        "xh": (["xh"], f0.xh.data),
        "yh": (["yh"], f0.yh.data),
        "time": (["time"], np.linspace(1,12,12)),
    },
    )
    ncfile.tos.attrs   =  f0.tos.attrs
    ncfile["xh"].attrs  =  f0["xh"].attrs
    ncfile["yh"].attrs  =  f0["yh"].attrs

    ncfile.to_netcdf(path0 + "all_climate_monthly_means_python.nc")

def main():
    calculate_monthly_average()

if __name__ == '__main__':
    main()