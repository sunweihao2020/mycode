'''
2022-8-25
This code is to paint meridional streamfunction add diabatic heating
zonal range is 90 to 100
'''
src_path  =  "/Users/sunweihao/data/composite/"

f0        =  "composite-heating-merra.nc"
f1        =  "composite_calculate_regional_streamfunction_zonal10to20_meridional_220825.nc"

def paint_meridional_field():
    import xarray as xr
    import numpy as np

    file0  =  xr.open_dataset(src_path + f0)
    file1  =  xr.open_dataset(src_path + f1)



def main():
    paint_meridional_field()

if __name__ == "__main__":
    main()