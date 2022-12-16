'''
2022-12-05
This script paint b1850 control experiment circulation and precipitation
The daily resolution is pentad.Thus, in this script I need to calculate pentad average
'''
import os
import sys
import xarray as xr
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
from metpy.units import units
from matplotlib.path import Path
import matplotlib.patches as patches

def cal_pentad(path,file):
    '''This function calculate pentad average for input file'''
    f0  =  xr.open_dataset(path+file) # file for calculate

    vars = ['LHFLX','PRECT','Q','T','U','V','OMEGA','PS','Z3','SHFLX','TS']

    # vars dimension
    dim0   =  73
    dim1   =  len(f0.lev.data)
    dim2   =  len(f0.lat.data)
    dim3   =  len(f0.lon.data)

    output =  []
    # declare base array
    for vvvv in vars:
        dimension  =  len(f0[vvvv].shape)  # get the dimension for the vars
        
        if dimension == 4:
            base_array = np.zeros((dim0,dim1,dim2,dim3))
        elif dimension == 3:
            base_array = np.zeros((dim0,dim2,dim3))
        else:
            print("The dimension error, dimension is {}".format(str(dimension)))

        input_array  =  f0[vvvv].data

        # -------------  calculate  ---------------------
        print("Now it is calculate "+vvvv)
        for d0 in range(0,73):
            base_array[d0]  =  np.average(input_array[d0*5:d0*5+5],axis=0)

        # --------  generate dataarray  ------------
        if dimension == 4:
            dataarray  =  xr.DataArray(base_array, 
                                    coords=[np.linspace(1,73,73), f0.lev.data,f0.lat.data,f0.lon.data],
                                    dims=["time", "lev","lat","lon"],name=vvvv)
        elif dimension == 3:
            dataarray  =  xr.DataArray(base_array, 
                                    coords=[np.linspace(1,73,73), f0.lat.data,f0.lon.data],
                                    dims=["time", "lat","lon"],name=vvvv)

        output.append(dataarray)

    ## --------  merge to output dataset  -------------
    out_set  =  xr.merge([array for array in output])
    for vvvv in vars:
        out_set[vvvv].attrs  =  f0[vvvv].attrs
    
    out_set.attrs["description"]  =  "Generated in 2022-12-05. This file based on daily climate variables, is pentad average"
    ## ------------------------------------------------
    
    #  ----------      to ncfile     ------------------
    path_out  =  "/home/sun/data/model_data/climate/b1850_exp/"
    file_out  =  "b1850_control_atmosphere_pentad.nc"

    os.system("rm -rf "+path_out+file_out)
    out_set.to_netcdf(path_out+file_out)
    


def main():
    cal_pentad(path='/home/sun/data/model_data/climate/b1850_exp/',file = 'b1850_control_climate_atmosphere.nc')
    
if __name__  ==  "__main__":
    main()