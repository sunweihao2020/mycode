'''
2022-9-13
This code calculate monthly mean for the model output
'''
import os
import sys
import xarray as xr
import numpy as np
import time

month_dates  =  np.array([31,28,31,30,31,30,31,31,30,31,30,31])
exp_files    =  ["b1850_control_climate_atmosphere.nc","b1850_indian_climate_atmosphere.nc","b1850_inch_climate_atmosphere.nc","b1850_maritime_climate_atmosphere.nc"]
exp_names    =  ["control","indian","inch","maritime"]

def cal_monthly_average(input_file,exp_name):
    '''This function calculate monthly average for the whole year nc file'''
    path  =  "/home/sun/data/model_data/climate/"
    f0    =  xr.open_dataset(path + input_file)

    #  ----- vars list ------
    vars  =  list(f0.keys())

    dim0   =  12
    dim1   =  len(f0.lev.data)
    dim2   =  len(f0.lat.data)
    dim3   =  len(f0.lon.data)

    output =  []
    # declare base array
    print()
    for vvvv in vars:
        dimension  =  len(f0[vvvv].data.shape)  # get the dimension for the vars
        
        if dimension == 4:
            base_array = np.zeros((dim0,dim1,dim2,dim3))
        elif dimension == 3:
            base_array = np.zeros((dim0,dim2,dim3))
        else:
            print("The dimension error, dimension is {}".format(str(dimension)))

        input_array  =  f0[vvvv].data

        # -------------  calculate  ---------------------
        print("Now it is calculate "+vvvv)
        for m0 in range(0,12):
            print(str(np.sum(month_dates[0:m0]))+" to "+str(np.sum(month_dates[0:(m0+1)])))
            base_array[m0]  =  np.average(input_array[np.sum(month_dates[0:m0]):np.sum(month_dates[0:(m0+1)])],axis=0)

        # --------  generate dataarray  ------------
        if dimension == 4:
            dataarray  =  xr.DataArray(base_array, 
                                    coords=[np.linspace(1,12,12), f0.lev.data,f0.lat.data,f0.lon.data],
                                    dims=["time", "lev","lat","lon"],name=vvvv)
        elif dimension == 3:
            dataarray  =  xr.DataArray(base_array, 
                                    coords=[np.linspace(1,12,12), f0.lat.data,f0.lon.data],
                                    dims=["time", "lat","lon"],name=vvvv)

        output.append(dataarray)

    ## --------  merge to output dataset  -------------
    out_set  =  xr.merge([array for array in output])
    for vvvv in vars:
        out_set[vvvv].attrs  =  f0[vvvv].attrs
    
    out_set.attrs["description"]  =  "Generated in 2022-9-21. This file based on daily climate variables, is monthly average"
    ## ------------------------------------------------

    #  ----------      to ncfile     ------------------
    path_out  =  "/home/sun/data/model_data/climate/"
    file_out  =  "b1850_"+exp_name+"_atmospheric_monthly_average.nc"

    os.system("rm -rf "+path_out+file_out)
    out_set.to_netcdf(path_out+file_out)
    

def main():
    for i in range(len(exp_files)):
        cal_monthly_average(exp_files[i],exp_names[i])

if __name__ == "__main__":
    main()

