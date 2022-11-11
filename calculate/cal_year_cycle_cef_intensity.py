'''
2022-10-25
This file calculate the yearly cycle of the five CEF in the Asian-Australia monsoon region
The definition for the five CEF are:
level: 925 hPa
latitude: 2.5S - 2.5N
longitude:
Somali       BOB         SCS        Celebes          New Guinea
40-50       80-90       102-110     120-130          145-155
'''
lon_slice  =  [slice(40,50),slice(80,90),slice(102,110),slice(120,130),slice(145,155)]

def cal_yearly_CEF_intensity(file,lev=925,lat_slice=slice(-2.5,2.5)):
    '''This function calculate cycle for the five CEFs
       input file should be 365 length
    '''
    import xarray as xr
    import numpy as np

    '''array to save the output'''
    cef  =  np.array([])

    for ll in lon_slice:
        f0  =  file.sel(lev=lev,lat=lat_slice,lon=ll)

        cef  =  np.append(cef, np.nanmean(np.nanmean(f0['V'].data,axis=1),axis=1),axis=0)

    cef  =  cef.reshape((5,365))
        #print(f0)

    return cef
def cal_yearly_CEF_intensity_merra(lev=925,lat_slice=slice(-2.5,2.5)):
    '''This function calculate merra-2 CEF'''
    import os
    import xarray as xr
    import numpy as np

    file_list  =  os.listdir('/home/sun/qomo-data/merra2_multi') ; file_list.sort()

    merra_cef  =  np.array([])

    for ll in lon_slice:
        for ffff in file_list:
            f0  =  xr.open_dataset('/home/sun/qomo-data/merra2_multi/' + ffff).sel(lev=lev,lat=lat_slice,lon=ll)

            merra_cef  =  np.append(merra_cef,np.nanmean(np.nanmean(f0['V'].data[0],axis=0),axis=0))

    print(merra_cef.shape)
    merra_cef = merra_cef.reshape((5, 365))

    return merra_cef



def main():
    import xarray as xr
    import numpy as np

    path       =  '/home/sun/data/model_data/climate/'
    file_list  =   ['b1850_control_climate_atmosphere.nc','b1850_inch_climate_atmosphere.nc','b1850_indian_climate_atmosphere3.nc','b1850_inch_indian_atmosphere.nc','b1850_maritime_climate_atmosphere.nc']

    cefs       =   []
    for ffff in file_list:
        f1  =  xr.open_dataset(path + ffff)
        cefs.append(cal_yearly_CEF_intensity(file=f1))

    #print(len(cefs))
    '''calculate merra-2 five CEFs'''
    merra_cef  =  cal_yearly_CEF_intensity_merra()

    '''save to ncfile'''
    path_out  =  '/home/sun/data/model_data/daily_cross_equator_flow/'
    ncfile = xr.Dataset(
        {
            "merra_cefs": (["name",'day'], merra_cef),
            "control_cefs": (["name", 'day'], cefs[0]),
            "inch_cefs": (["name", 'day'], cefs[1]),
            "indian_cefs": (["name", 'day'], cefs[2]),
            "inch_indian_cefs": (["name", 'day'], cefs[3]),
            "maritime_cefs": (["name", 'day'], cefs[4]),
        },
        coords={
            "name": (["name"], ['somali','bob','scs','cs','ng']),
            'day': (['day'], np.linspace(1,365,365)),
        },
    )
    ncfile.attrs["description"] = "this file include five CEFs among the merra-2 and control, sensitivity experiments. lat range is -2.5 to 2.5. lev is 925. 2022-10-26"
    ncfile.to_netcdf(path_out  +  "yearly_cycle_merra_b1850_CEFs.nc")

if __name__ == '__main__':
    main()



