import os
import sys
import xarray as xr
import numpy as np
module_path = ["/home/sun/mycode/module/","/data5/2019swh/mycode/module/"]
sys.path.append(module_path[0])
from module_sun import *
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
from metpy.units import units
from matplotlib.path import Path
import matplotlib.patches as patches
import matplotlib as mpl

f  =  xr.open_dataset("/home/sun/data/gebco/bathymetric.nc")

proj = ccrs.PlateCarree()
fig = plt.figure(figsize=(16,9))
ax = fig.add_subplot(111, projection=proj)

im = ax.contourf(
    f.lon,f.lat,f.elevation,
    levels=np.linspace(-8000,8000,161),cmap='RdYlBu_r',
)
cbar = fig.colorbar(
        im, ax=ax, shrink=0.9, pad=0.1, orientation='horizontal',
    )

plt.savefig('/home/sun/paint/bathymetric_topography/bathymetric_1x1.pdf', bbox_inches='tight',dpi=1200)
plt.show()
