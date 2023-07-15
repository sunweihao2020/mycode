'''
2023-7-4
This script calculate the LSTC index per pentad from 1940 to 2022 years
Surface pressure difference between land (5-20N, 70-90E) and sea (-5-5N, 70-90E)
'''
import xarray as xr
import numpy as np
import os

path0 = '/home/sun/data/other_data/single/pentad/slp/'

mask_file = xr.open_dataset('/home/sun/data/mask/ERA5_land_sea_mask_1x1.nc')

# ====== Claim the array ================================
LSTC_pentad = np.zeros((83, 73))

# ====== Divide the Land Sea Mask ======================
land_lon = slice(70, 90)
sea_lon  = slice(70, 90)

land_lat = slice(20, 5)
sea_lat  = slice(5, -5)

mask_land = mask_file.sel(longitude=land_lon, latitude=land_lat) # No ocean grid in the ocean area, do not need mask

file_path = '/home/sun/data/other_data/single/pentad/slp/'
file_list = os.listdir(file_path) ; file_list.sort()

def cal_LSTC_index(ffff):
    f_land = xr.open_dataset(file_path + ffff).sel(latitude=land_lat, longitude=land_lon)
    #print(f_land)

    #print(np.nanmean(f_land['msl'].data))
    # Mask the ocean value in each pentad
    for tt in range(73):
        f_land['msl'].data[tt, ][mask_land['lsm'].data[0] < 0.8] = np.nan

    # Check the result
    #print(np.nanmean(f_land['msl'].data)) # result: yes it is correct

    f_ocean = xr.open_dataset(file_path + ffff).sel(latitude=sea_lat, longitude=sea_lon)

    LSTC_index = np.zeros(73)

    for tt in range(73):
        LSTC_index[tt] = np.nanmean(f_land['msl'].data[tt]) - np.nanmean(f_ocean['msl'].data[tt])

    return LSTC_index

# ====== Test the calculation function ================
#cal_LSTC_index(file_list[2])

# ====== Calculation ==================================
LSTC = np.zeros((83, 73))
for yy in range(83):
    LSTC[yy] = cal_LSTC_index(file_list[yy])

# ==== Write into the ncfile ==========================
ncfile  =  xr.Dataset(
{
    "LSTC": (["year", "pentad"], LSTC),
},
coords={
    "year": (["year"], np.linspace(1940, 2022, 83)),
    "pentad": (["pentad"], np.linspace(1, 73, 73)),
},
)
ncfile['LSTC'].attrs['description'] = 'This is thermal difference between Indian continent(70-90, 5-15) and surround ocean(70-90, -5-5). The variable is SLP. time period is 1940 to 2022'
ncfile.attrs['description']  =  'Pentad difference between land and sea from 1940 to 2022 year'
ncfile.to_netcdf("/home/sun/data/onset_day_data/ERA5_pentad_LSTC_1940_2022.nc")