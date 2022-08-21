'''
This code paint January and July meridional circulation in the BOB region
To depict the characteristic of the Hadley cell
'''
path0  =  "/home/sun/data/merra2_climate_vars_multi/daily/"
path1  =  "/home/sun/data/merra2_climate_vars_multi/monthly/"

def cal_jan_jul_average():
    '''This function calculate climate monthly vars average and save to the path'''
    import numpy as np
    import xarray as xr
    import os

    # get the files list
    file_list  =  os.listdir(path0) ; file_list.sort()

    # month days
    days       =  [31,28,31,30,31,30,31,31,30,31,30,31]

    # calculate monthly
    ## reference file
    f0         =  xr.open_dataset(path0+"0101.climate.nc")

    ### get datasets vars name
    vars = list(f0.keys())
    print(vars)



def main():
    cal_jan_jul_average()

if __name__ == "__main__":
    main()