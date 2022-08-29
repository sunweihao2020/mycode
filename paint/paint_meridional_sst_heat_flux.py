'''
2022-8-26
This code plot meridional sea surface temperature added heat flux (latent heat flux)
based on composite file and time period is pentad average
'''
src_path  =  "/Users/sunweihao/data/composite/"

file0     =  "composite_OISST.nc"
file1     =  "composite_shlh_liuxl.nc"

def cal_zonal_avg():
    '''This function calculate zonal average for SST and latent flux'''
    import xarray as xr
    import numpy as np

    # set the zonal average
    lon_slice  =  slice(90,100)

    # read the file
    f0         =  xr.open_dataset(src_path + file0).sel(lon=lon_slice)
    f1         =  xr.open_dataset(src_path + file1).sel(lon=lon_slice)

    # calculate zonal average
    sst        =  np.nanmean(f0.SST.data,  axis=2)
    slhf       =  np.nanmean(f1.SLHF.data, axis=2)

    return sst,slhf

def paint_meridional_field():
    '''This function paint meridional for the sst and slhf'''
    import xarray as xr
    import numpy as np
    import matplotlib.pyplot as plt
    import cmasher as cmr

    import sys
    sys.path.append("/Users/sunweihao/mycode/module")
    from module_sun_new import generate_xlabel