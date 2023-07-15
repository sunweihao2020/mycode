'''
2023-5-24
This script plot the time-evolution for the area-averaged spv over Indian
'''
from matplotlib import projections
import xarray as xr
import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import sys

sys.path.append("/home/sun/mycode/module/")
from module_sun import *

sys.path.append("/home/sun/mycode/paint/")
from paint_lunwen_version3_0_fig2b_2m_tem_wind_20220426 import set_cartopy_tick,save_fig
from paint_lunwen_version3_0_fig2a_tem_gradient_20220426 import add_text

f0 = xr.open_dataset('/home/sun/wd_disk/merra2_modellev/spv/cdo/spv_pentad_1980_2019_multi_year_pentad.nc').sel(lev=72, lon=slice(75,85), lat=slice(5, 20))

average = np.average(np.average(f0['__xarray_dataarray_variable__'], axis=1), axis=1)

plt.plot(np.linspace(1,73,73), average, 'k')

plt.title("Pentad evolution Indian SPV")

plt.savefig('/home/sun/paint/monthly_variable/spv/time_evolution_indian.pdf')