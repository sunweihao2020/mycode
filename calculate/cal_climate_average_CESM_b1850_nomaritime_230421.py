'''
2023-4-21
This script calculate climate average for the b1850 no maritime experiment
'''
import xarray as xr
import numpy as np
import os

path0 = '/home/sun/wd_disk/b1850_maritime_output/' #Include 18615 (51 years) files
file_list = os.listdir(path0) ; file_list.sort()

ref_file = xr.open_dataset(path0 + 'b1850_tx_maritime_2022.cam.h1.0017-12-03-00000.nc')