'''
2022-7-20
This code is to calculate and paint monthly meri-vertical temperature
'''
import xarray as xr
import numpy as np
import os
import matplotlib

src_path  =  "/home/sun/data/merra2_climate_vars_multi/"

# range option
lon_slice  =  slice(90,100)
lev_slice  =  slice(1000,100)

def cal_monthly_tem():
    import os
    import xarray as xr
    import numpy as np
    '''This function calculate temperature between 90 to 100E
       time period: Jan to May
    '''
    file_list  =  os.listdir(src_path) ; file_list.sort()
    
    date       =  [0,30,60,90,120,150]

    # reference file
    f0         =  xr.open_dataset(src_path+"0830.climate.nc").sel(lev=lev_slice,lon=lon_slice)
    
    # array to save
    avg_tem    =  np.zeros((5,25,361))

    # calculate monthly average
    for i in range(5):
        # Jan to May
        start_day  =  date[i]
        end_day    =  date[i+1]
        for dd in range(start_day,end_day):
            f1        =  xr.open_dataset(src_path+file_list[dd]).sel(lev=lev_slice,lon=lon_slice)

            # calculate daily average
            avg_dd_t  =  np.average(f1.T.data[0],axis=2)

            # save to array
            avg_tem[i]  +=  avg_dd_t/30  

    print("yes")
    return avg_tem


def main():
    cal_monthly_tem()

if __name__ == "__main__":
    main()