'''
This script calculate the monthly average OLR index over the maritime continent
'''
import xarray as xr
import numpy as np

month_day  =  np.array([31,28,31,30,31,30,31,31,30,31,30,31])

f0 = xr.open_dataset('/home/sun/data/other_data/maritime_avg_OLR/OLR_maritime_area_average_daily.nc')

# claim the monthly avg array
index_mon = np.zeros((83, 12))
for yyyy in range(83):
    for mmmm in range(12):
        index_mon[yyyy, mmmm] = np.average(f0['ttr_avg'].data[yyyy, int(np.sum(month_day[0:mmmm])) : int(np.sum(month_day[0:mmmm+1]))], axis=0) / -3600

# 4. Write to ncfile
ncfile  =  xr.Dataset(
                {
                    'ttr_avg_mon': (["year", "month",], index_mon),
                },
                coords={
                    "month": (["month"], np.linspace(1,12,12,dtype=int)),
                    "year": (["year"], np.linspace(1940,2022,83,dtype=int)),
                },
                )
ncfile['ttr_avg_mon'].attrs['units'] = 'W m-2'
ncfile.attrs['description'] = 'created on 2023-3-21. This is maritime continent area-averaged OLR based on ERA5 data, area slice is (100-130E, -5-10N). The data has been transformed to monthly average and divide with -3600 to the W m-2 units'
ncfile.to_netcdf('/home/sun/data/other_data/maritime_avg_OLR/OLR_maritime_area_average_monthly.nc')