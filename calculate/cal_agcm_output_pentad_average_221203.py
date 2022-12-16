'''
2022-12-3
This code calculate the pentad-average for the AGCM experiment output
original file is climate, but daily
'''
path0  =  '/home/sun/data/model_data/f2000_ensemble/hybrid-2/daily/'
var_list = ['LHFLX','PRECT','Q','T','U','V','OMEGA','PS','Z3','SHFLX','TS']
var_2d   = ['LHFLX','PRECT','PS','SHFLX','TS']

def calculate_pentad_average(varname,dimension):
    '''This function calculate the pentad-average'''
    import numpy as np
    import xarray as xr

    file_name  =  varname + '_climate2.nc'
    f0  =  xr.open_dataset(path0 + file_name)

    array0     =  f0[varname]
    dimension0 =  array0.shape

    print(array0.data)

    if dimension == 4:
        base_array  =  np.zeros((73,dimension0[1],dimension0[2],dimension0[3]))
    if dimension == 3:
        base_array  =  np.zeros((73,dimension0[1],dimension0[2]))

    for pp in range(73):
        base_array[pp] = np.average(array0[pp*5:(pp*5+5)], axis=0)

    return base_array

def main():
    '''calculate pentad average and pack to the nc file'''
    import xarray as xr
    import numpy as np

    ref_file  =  xr.open_dataset(path0 + 'T_climate2.nc')

    for nnnn in var_list:
        ref_file2  =  xr.open_dataset(path0 + nnnn + '_climate2.nc')
        if nnnn in var_2d:
            ncfile  =  xr.Dataset(
                    {
                        nnnn: (["time", "lat", "lon"], calculate_pentad_average(nnnn,dimension=3)),
                    },
                    coords={
                        "lat": (["lat"], ref_file.lat.data),
                        "lon": (["lon"], ref_file.lon.data),
                        "time": (["time"], np.linspace(1,73,73)),
                    },
                    )
            ncfile[nnnn].attrs = ref_file2[nnnn].attrs
            ncfile.attrs['description'] = 'created on 2022-12-4. This is f2000 ensemble hybrid-10 experiment output. I calculated pentad average based on the daily climate variables'

            ncfile.to_netcdf('/home/sun/data/model_data/f2000_ensemble/hybrid-2/pentad/'+nnnn+'_pentad.nc')

        else:
            ncfile  =  xr.Dataset(
                    {
                        nnnn: (["time", "lev", "lat", "lon"], calculate_pentad_average(nnnn,dimension=4)),
                    },
                    coords={
                        "lat": (["lat"], ref_file.lat.data),
                        "lon": (["lon"], ref_file.lon.data),
                        "time": (["time"], np.linspace(1,73,73)),
                        "lev":  (["lev"], ref_file.lev.data),
                    },
                    )
            ncfile[nnnn].attrs = ref_file2[nnnn].attrs
            ncfile.attrs['description'] = 'created on 2022-12-4. This is f2000 ensemble hybrid-10 experiment output. I calculated pentad average based on the daily climate variables'

            ncfile.to_netcdf('/home/sun/data/model_data/f2000_ensemble/hybrid-2/pentad/'+nnnn+'_pentad.nc')

if __name__ == '__main__':
    main()

