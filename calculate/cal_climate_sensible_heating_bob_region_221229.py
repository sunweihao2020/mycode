'''
22-12-29
For the reviewer question, I need to add diabatic heating of sensible in my figure
But I do not have data, in this script I calculate climate average for the sensible heating
'''
import warnings
warnings.filterwarnings("ignore")

path0  =  '/home/sun/data/merra2_select_diabatic_heating/data/'

year_range  =  [1980, 2019]
month_day   =  [31,30,31] # Jan Apr Jul

#--------1. base array-----------------
import xarray as xr
import numpy as np

f0  =  xr.open_dataset(path0 + 'MERRA2_200.tavg3_3d_tdt_Np.19930727.nc4.nc4')
#print(f0)
# Time-Axis is 8, meaning every 3 hours. Thus I have to calculate day-average first
avg_month  =  np.zeros((3, f0['DTDTTRB'].data.shape[1], f0['DTDTTRB'].data.shape[2], f0['DTDTTRB'].data.shape[3]))

#--------2. file list------------------
import os
file_list  =  os.listdir(path0)
file_list.sort()

#--------3. calculate average----------
j  =  0
for yyyy in range(40):
    for mmmm in range(3):
        for dddd in range(month_day[mmmm]):
            f1  =  xr.open_dataset(path0 + file_list[int((yyyy * np.sum(month_day)) + np.sum(month_day[0:mmmm]) + dddd)])
            if j == int((yyyy * np.sum(month_day)) + np.sum(month_day[0:mmmm]) + dddd):
                day_avg  =  np.nanmean(f1['DTDTTRB'].data, axis=0)
                avg_month[mmmm]  +=  (day_avg / month_day[mmmm])

                j += 1
            else:
                print('ERROR, the number is {}, j is {}'.format(int((yyyy * np.sum(month_day)) + np.sum(month_day[0:mmmm]) + dddd), j))

#--------4. write to ncfile--------------
ncfile  =  xr.Dataset(
                    {
                        "sensible": (["time", "lev", "lat", "lon"], avg_month / 40),
                    },
                    coords={
                        "lat": (["lat"], f0.lat.data),
                        "lon": (["lon"], f0.lon.data),
                        "time": (["time"], np.array([1,4,7], dtype=int)),
                        "lev":  (["lev"], f0.lev.data),
                    },
                    )

ncfile.attrs['description'] = 'created on 2022-12-29. This is monthly average diabatic heating only for bob region and only for the 1-4-7 month. I need this data to add new element to my figure and for responsing to the reviewer'
ncfile.to_netcdf('/home/sun/data/merra2_climate_vars_multi/Jan_Apr_Jul_bob_sensible_heating.nc')