import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs

path  =  "/Users/sunweihao/data/model_data/input/"

f0    =  xr.open_dataset(path+"sst_HadOIBl_bc_1x1_1850_2017_c180507.nc")

fig,ax   =  plt.subplots(figsize=(13,10),subplot_kw=dict(projection=ccrs.PlateCarree()))

ax.contourf(f0.lon,f0.lat,f0.SST_cpl.data[774],50,cmap='coolwarm',extend='both',zorder=0)
ax.coastlines(resolution='110m',lw=1)

plt.show()

#print(f0.SST_cpl.data[2000])