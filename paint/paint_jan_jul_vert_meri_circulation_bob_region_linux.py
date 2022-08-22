'''
This code paint January and July meridional circulation in the BOB region
To depict the characteristic of the Hadley cell
'''
path0  =  "/home/sun/data/merra2_climate_vars_multi/daily/"
path1  =  "/home/sun/data/merra2_climate_vars_multi/monthly/"

#path0  =  "/Users/sunweihao/data/merra2_climate_vars_multi/daily/"
#path1  =  "/Users/sunweihao/data/merra2_climate_vars_multi/monthly/"

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

    ## --------calculate monthly average----------
    ### create  empty dataset
    monthly_avg  =  xr.Dataset()
    for vvvv in vars:
        base  =  create_base_array(f0[vvvv])

        for mon in range(len(days)):
            start   = int(np.sum(days[0:mon]))
            end     = int(np.sum(days[0:(mon+1)]))
            period  = end-start
            #print("start is %d" % start)
            #print("end is %d" % end)

            for dd in range(start,end):
                f1         =   xr.open_dataset(path0+file_list[dd])
                base[mon]  +=  f1[vvvv].data[0] / period

        # save array to xarray dataarray
        monthly_avg[vvvv]  =  create_base_dataarray(base)
    

def create_base_dataarray(array):
    '''This function create dataarray for input array'''
    import xarray as xr
    import numpy as np

    # reference file
    f0   =   xr.open_dataset(path0 + "0101.climate.nc")
    dim  =   len(array.shape)
    if dim == 3:
        da = xr.DataArray(
            data=array,
            dims=["time","lat","lon"],
            coords={
                "time":np.linspace(1,12,12),
                "lat":f0.lat.data,
                "lon":f0.lon.data,
            },
        )
    else:
        da = xr.DataArray(
            data=array,
            dims=["time","lev", "lat", "lon"],
            coords={
                "time": np.linspace(1, 12, 12),
                "lat": f0.lat.data,
                "lon": f0.lon.data,
                "lev": f0.lev.data,
            },
        )
        return da

def create_base_array(array):
    '''This function returns base array based on the input array'''
    import numpy as np
    time_length  =  12

    dims         =  len(array.shape)

    if dims == 3:
        base_array  =  np.zeros((time_length,array.shape[1],array.shape[2]))
    elif dims == 4:
        base_array  = np.zeros((time_length, array.shape[1], array.shape[2], array.shape[3]))
    else:
        print("Error, the dimension is "+str(dims))

    return base_array


def test():
    import xarray as xr

    # reference file
    f0 = xr.open_dataset(path0 + "0101.climate.nc")
    a  = list(f0.attrs)
    print(f0["H"].attrs.keys())

def main():
    import warnings
    import time
    start = time.time()
    warnings.filterwarnings("ignore")

    cal_jan_jul_average()
    end = time.time()
    print(end-start)


if __name__ == "__main__":
    main()