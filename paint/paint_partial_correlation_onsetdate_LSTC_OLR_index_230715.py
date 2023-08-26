'''
2023-7-15
This script plot the correlation between onset dates and LSTC/OLR indexes
'''
import numpy as np
import xarray as xr
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

file0 = xr.open_dataset('/home/sun/data/ERA5_data_monsoon_onset/index/correlation/partial_correlation_onset_dates_with_pentad_OLR_LSTC_detrend.nc')
# Correlation Line
p1 = 0.182
p2 = 0.216
p3 = 0.252

fig, ax = plt.subplots()
ax.xaxis.set_minor_locator(MultipleLocator(1))
ax.plot(np.linspace(1, 35, 35), file0['onset_with_lstc_partial'].data[0:35], color='red', linewidth=2, label='LSTC')
ax.plot(np.linspace(1, 35, 35), file0['onset_with_olr_partial'].data[0:35],  color='blue', linewidth=2, label='OLR')

# paint line
ax.plot([1, 35], [0.182, 0.182], 'k--')
ax.plot([1, 35], [0.216, 0.216], 'c--')
ax.plot([1, 35], [0.252, 0.252], 'm--')

ax.grid(axis='x', color='0.95', which = "both")

ax.set_title('Partial Correlation between onset dates and pentad indexes', fontsize=10)

plt.legend()

plt.savefig('/home/sun/paint/index_correlation_with_onsetdate/pentad_partial_correlation_onsetdate_LSTC_OLR.pdf', dpi=500)