'''
2022-11-11
This code paint the difference between the cdo result and python result
'''
import xarray as xr
import numpy as np

path0  =  '/home/sun/data/ocean_data/'

f0     =  xr.open_dataset(path0 + 'all_climate_monthly_means_python.nc')
f1     =  xr.open_dataset(path0 + 'all_climate_monthly_means.nc')

diff_tos  =  f0.tos.data - f1.tos.data

print(diff_tos[2,:,100])

import numpy as np
import matplotlib.pyplot as plt
fig1, ax1 = plt.subplots(constrained_layout=True)

ax1.contourf(diff_tos[2], 10, cmap=plt.cm.bone)
fig1.colorbar(ax1)
plt.savefig('cdo_diff.png')
