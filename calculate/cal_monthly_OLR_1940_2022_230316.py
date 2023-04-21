'''
2023-3-16
This script calculate monthly average from 1940 to 2022
'''
import numpy as np
import xarray as xr
import os

path0 = '/home/sun/data/other_data/down_ERA5_hourly_OLR_convert_float_daymean/'
file_all = os.listdir(path0)

month_day = [31,28,31,30,31,30,31,31,30,31,30,31]

def get_filelist_fname(fname):
    '''
        get the filelist for the given file name
    '''
    file_all = os.listdir(path0)
    file_select = []
    for ffff in file_all:
        if fname in ffff:
            file_select.append(ffff)

    # Sort the list
    file_select.sort()

    return file_select

def calculate_monthly_single_variable(fname='OLR', vname='ttr'):
    '''
        Calculate month sst
    '''
    # 1. Get file list
    f_list = get_filelist_fname(fname)
    #print(len(f_list))

    # 2. Reference file
    ref_file = xr.open_dataset(path0 + f_list[0])

    # 3. Claim base array
    base_array = np.zeros((83, 12, 181, 360))

    # 4. Calculate monthly data for each year
    for yy in range(83):
        f0 = xr.open_dataset(path0 + f_list[yy])
        for mm in range(12):
            base_array[yy, mm, ] = np.average(f0[vname].data[int(np.sum(month_day[0:mm])) : int(np.sum(month_day[0:mm+1]))] / -3600, axis=0)
            #print(np.average(f0[vname].data[np.sum(month_day[0:mm]) : np.sum(month_day[0:mm+1])], axis=0))
            #print(f0[vname].data[int(np.sum(month_day[0:mm])) : int(np.sum(month_day[0:mm+1]))])

    return base_array

#for mm in range(12):
#    print(np.sum(month_day[0:mm]))
#    print(np.sum(month_day[0:mm+1]))

#print(month_day[0:12])
def main():
    # 1. monthly SST
    m_sst = calculate_monthly_single_variable()

    # -------- 5. Write to the file ----------------
    ref_file = xr.open_dataset(path0 + '1961_hourly_OLR.nc')
    ncfile  =  xr.Dataset(
                    {
                        'monthly_olr': (["year", "month", "lat", "lon"], m_sst),
                    },
                    coords={
                        "lat": (["lat"], ref_file.latitude.data),
                        "lon": (["lon"], ref_file.longitude.data),
                        "month": (["month"], np.linspace(1, 12, 12)),
                        "year": (["year"], np.linspace(1940, 2022, 83)),
                    },
                    )
    ncfile['lat'].attrs = ref_file.latitude.attrs
    ncfile['lon'].attrs = ref_file.longitude.attrs
    ncfile.attrs['description'] = 'created on 2023-3-16. This is single-layer monthly average data from 1940 to 2022 using ERA5 data.'

    ncfile.to_netcdf('/home/sun/data/ERA5_data_monsoon_onset/index/ERA5_single_monthly_OLR_1940_2022.nc')

if __name__ == '__main__':
    main()