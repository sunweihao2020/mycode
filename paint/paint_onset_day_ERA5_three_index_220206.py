'''
2022-02-06
This script plot the onset day using ERA5 data. Here I defined three index of level 200-500, 300-500, 400-600. All index is ploted in the figure.
'''
import matplotlib.pyplot as plt
import xarray as xr
import numpy as np

path0  =  '/home/sun/data/onset_day_data/'
f25    =  xr.open_dataset(path0 + '1959-2021_BOBSM_onsetday_level200500.nc')
f35    =  xr.open_dataset(path0 + '1959-2021_BOBSM_onsetday_level300500.nc')
f46    =  xr.open_dataset(path0 + '1959-2021_BOBSM_onsetday_level400600.nc')

plt.plot(f25['year'].data, f25['onset_day'].data, linewidth = 1.5, color='black', label='200-500')
plt.plot(f35['year'].data, f35['onset_day'].data, ':', linewidth = 1.5, color='red',   label='300-500')
plt.plot(f25['year'].data, f46['onset_day'].data, '-.', linewidth = 1.5, color='blue',  label='400-600')

plt.grid(True)
plt.legend()

plt.savefig('/home/sun/paint/onset_day/three_index_era5_BOBSMonset.pdf', dpi=500)