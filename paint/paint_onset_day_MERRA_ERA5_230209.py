'''
2023-02-09
This script plot the onset day time sequence using MERRA2 and ERA5 data for compare purpose
'''
import json
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

import pymannkendall as mk

# -------------- 1. read data -----------------------------
# 1-1 MERRA-2 data
def open_onsetdate(file):
    with open(file,'r') as load_f:
        a = json.load(load_f)

    year = np.array(list(a.keys()))    ;  year  =  year.astype(int)
    day  = np.array(list(a.values()))  ;  day   =  day.astype(int)

    return year,day

year_merra, day_merra = open_onsetdate("/home/sun/qomo-data/onsetdate.json")

# 1-2 ERA5 data
f0  =  xr.open_dataset('/home/sun/data/onset_day_data/1959-2021_BOBSM_onsetday_level300500.nc')
year_era = f0['year'].data
day_era  = f0['onset_day'].data

# 1-3 average day
print(np.average(day_merra)) # 122.35
print(np.average(day_era))   # 124.7

# 1-4 linear regression
z_merra  =  np.polyfit(year_merra, day_merra, 1)
z_era    =  np.polyfit(year_era, day_era, 1)

print('Line of Merra2 is {0}x + {1}'.format(*z_merra))
print('Line of ERA5 is {0}x + {1}'.format(*z_era))

print(mk.original_test(day_era))
print(mk.original_test(day_merra))


# -------------- 2. paint pic ------------------------------
# 2-1 set figure
fig,ax   =  plt.subplots(figsize=(15,10))

# 2-2 x-label and y-label
y_label  =  ['1 Apr', '10Apr','20Apr','1May','10May','20May', '30 May']
x_label  =  np.arange(1959, 2022 , 10)

# 2-3 xtick and ytick
ytick    =  np.arange(-30, 31, 10)  
xtick    =  np.arange(1959, 2022 , 10)

# 2-4 add set to the axes
#from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,AutoMinorLocator)
ax.set_xticks(xtick)
ax.set_yticks(ytick)
ax.set_xticklabels(x_label)
ax.set_yticklabels(y_label)
# set minimum tick
#ax.xaxis.set_minor_locator(MultipleLocator(5))
#ax.yaxis.set_minor_locator(MultipleLocator(5))
ax.tick_params(labelsize=20)
ax.set_xlabel("Year",fontsize=25)
ax.set_ylabel("Onset Day",fontsize=25)

# 2-5 plot the pic
ax.set_xlim(1958, 2022)

ax.plot(year_merra, day_merra - 120, color = 'red', marker = 'o', markersize = 10,  linewidth=2, label='MERRA-2')
ax.plot(year_era, day_era - 120, color='black', marker = 'v', markersize = 10, linewidth=2, label='ERA5')

plt.legend(loc=3, fontsize='xx-large')

#plt.show()
#plt.savefig('/home/sun/paint/onset_day/MERRA2_ERA5_onset_day_compare.pdf',dpi=450)



