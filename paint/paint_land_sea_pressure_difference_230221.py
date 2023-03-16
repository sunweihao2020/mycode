'''
2023-2-21
This script plot the land sea pressure difference between Indian Continent and surrounding Ocean
'''
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

# =================== 1. Region info ==============================
land_range_lat = slice(20, 0)
land_range_lon = slice(70, 90)

sea_range_lat = slice(8, -8)
sea_range_lon = slice(80, 100)

# ================== 2. Read file =================================
path0 = '/home/sun/data/ERA5_data_monsoon_onset/climatic_daily_ERA5/single/'

f0_land = xr.open_dataset(path0 + 'surface_pressure_climatic_daily.nc').sel(lat=land_range_lat, lon=land_range_lon)
f1_land = xr.open_dataset(path0 + 'surface_pressure_climatic_daily_year_early.nc').sel(lat=land_range_lat, lon=land_range_lon)
f2_land = xr.open_dataset(path0 + 'surface_pressure_climatic_daily_year_late.nc').sel(lat=land_range_lat, lon=land_range_lon)

f0_sea  = xr.open_dataset(path0 + 'surface_pressure_climatic_daily.nc').sel(lat=sea_range_lat, lon=sea_range_lon)
f1_sea  = xr.open_dataset(path0 + 'surface_pressure_climatic_daily_year_early.nc').sel(lat=sea_range_lat, lon=sea_range_lon)
f2_sea  = xr.open_dataset(path0 + 'surface_pressure_climatic_daily_year_late.nc').sel(lat=sea_range_lat, lon=sea_range_lon)

# =================== 3. Mask the land value ========================
mask_file_land = xr.open_dataset('/home/sun/data/mask/ERA5_land_sea_mask_1x1.nc').sel(latitude=land_range_lat, longitude=land_range_lon)
mask_file_sea  = xr.open_dataset('/home/sun/data/mask/ERA5_land_sea_mask_1x1.nc').sel(latitude=sea_range_lat,  longitude=sea_range_lon)
land_climate_mask = f0_land['sp'].data ; sea_climate_mask = f0_sea['sp'].data
land_early_mask   = f1_land['sp'].data ; sea_early_mask   = f1_sea['sp'].data
land_late_mask    = f2_land['sp'].data ; sea_late_mask    = f2_sea['sp'].data

for i in range(365):
    land_climate_mask[i][mask_file_land['lsm'].data[0] < 0.3] = np.nan
    land_early_mask[i][mask_file_land['lsm'].data[0] < 0.3]   = np.nan
    land_late_mask[i][mask_file_land['lsm'].data[0] < 0.3]    = np.nan
    sea_climate_mask[i][mask_file_sea['lsm'].data[0] > 0.1]  = np.nan
    sea_early_mask[i][mask_file_sea['lsm'].data[0] > 0.1]    = np.nan
    sea_late_mask[i][mask_file_sea['lsm'].data[0] > 0.1]     = np.nan
# 1. Test the sp time series
#f_test = f0.sel(lat=land_range_lat, lon=land_range_lon)
#import matplotlib.pyplot as plt
#
#avg_test = np.array([])
#for i in range(365):
#    avg_test = np.append(avg_test, np.average(f_test['sp'].data[i]))
#
#plt.plot(avg_test)
#
#plt.savefig('/home/sun/paint/monsoon_onset_composite_ERA5/test_surface_pressure.pdf')
diff_climate = np.array([])
diff_early   = np.array([])
diff_late    = np.array([])

x_tick = [50, 59, 68, 78, 90, 99, 109, 120, 129, 139, 151]
x_label = ['20 Feb', '1 Mar', '10 Mar', '20 Mar', '1 Apr', '10 Apr', '20 Apr', '1 May', '10 May', '20 May', '1 Jun']

for i in range(365):
    diff_climate = np.append(diff_climate, np.nanmean(land_climate_mask[i]) - np.nanmean(sea_climate_mask[i]))
    diff_early   = np.append(diff_early, np.nanmean(land_early_mask[i]) - np.nanmean(sea_early_mask[i]))
    diff_late    = np.append(diff_late, np.nanmean(land_late_mask[i]) - np.nanmean(sea_late_mask[i]))

# Standard
diff_climate = diff_climate - np.average(diff_climate)
diff_early = diff_early - np.average(diff_early)
diff_late = diff_late - np.average(diff_late)

plt.plot(-1 * np.convolve(diff_climate, np.ones(3)/3, mode='same'), color='black')
plt.plot(-1 * np.convolve(diff_early, np.ones(3)/3, mode='same'), color='blue')
plt.plot(-1 * np.convolve(diff_late, np.ones(3)/3, mode='same'), color='red')

plt.xticks(x_tick, x_label, rotation=45)

plt.xlim((45, 155))
#plt.ylim((4200, 4800))


plt.savefig('/home/sun/paint/monsoon_onset_composite_ERA5/test_surface_pressure.pdf')