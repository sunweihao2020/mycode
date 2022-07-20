'''
2022-7-20
This code is to calculate and paint monthly meri-vertical temperature
'''
import xarray as xr
import numpy as np
import os
import matplotlib

src_path  =  "/home/sun/data/merra2_climate_vars_multi/"

def cal_monthly_tem():
    import os
    import xarray as xr
    import numpy as np
    '''This function calculate temperature between 90 to 100E
       time period: Jan to May
    '''
    file_list  =  os.listdir(src_path) ; file_list.sort()
    print(file_list)

def main():
    cal_monthly_tem()

if __name__ == "__main__":
    main()