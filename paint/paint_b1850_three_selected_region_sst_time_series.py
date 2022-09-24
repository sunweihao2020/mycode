'''
2022-9-22
This code plot time series for SST of three selected area over the BOB
My goal is to see the status over the BOB sea
'''
import re


src_path  =  '/home/sun/segate/model_data/climate/'

file_name =  ['b1850_control_ocean_climate_sfc.nc','b1850_indian_ocean_climate_sfc.nc','b1850_inch_ocean_climate_sfc.nc','b1850_maritime_ocean_climate_sfc.nc']

lon_range   =  slice(80,100)

lat_range1  =  slice(-2,2)
lat_range2  =  slice(3,7)
lat_range3  =  slice(8,13)

def cal_average_select_region(file,lat_range):
    '''This function calculate average for the region'''
    import numpy as np
    import xarray as xr

    f0  =  xr.open_dataset(src_path + file).sel(yh=lat_range,xh=lon_range)

    mask_file  =  xr.open_dataset(src_path + file_name[0]).sel(yh=lat_range,xh=lon_range)



    base_array  =  np.zeros((365))

    for i in range(365):
        f0['tos'].data[i][np.isnan(mask_file['tos'].data[i])]  =  np.nan
        base_array[i]  =  np.nanmean(f0['tos'].data[i])

    return base_array

def get_sst_series():
    import numpy as np

    lat_range =  [lat_range1,lat_range2,lat_range3]

    result = np.array([])
    for i in file_name:
        base_array   =  np.zeros((3,365))
        for j in range(len(lat_range)):
            base_array[j]  =  cal_average_select_region(i,lat_range=lat_range[j])

        result  =  np.append(result,base_array)

    result  =  result.reshape((4,3,365))

    return result

def test():
    '''This function is to test the sequence of the reshape'''
    import numpy as np
    import xarray as xr

    f0  =  xr.open_dataset(src_path + file_name[1]).sel(yh=lat_range1,xh=lon_range)

    base_array  =  np.zeros((365))

    for i in range(365):
        base_array[i]  =  np.nanmean(f0['tos'].data[i])

    return base_array

def paint_control_series(var,name):
    import matplotlib.pyplot as plt
    import numpy as np

    fig    =  plt.figure()
    ax     =  fig.add_subplot(111)

    ax.plot(np.linspace(1,365,365),var[0],color='k',label='2S ~ 2N')
    ax.plot(np.linspace(1,365,365),var[1],color='c',label='3N ~ 7N')
    ax.plot(np.linspace(1,365,365),var[2],color='m',label='8N ~ 13N')

    ax.set_xlim((100,150))
    ax.set_ylim((29,31))

    ax.legend(loc='upper left')

    ax.set_ylabel("sea surface temperature")
    ax.set_xlabel("Day")




    plt.savefig('/home/sun/paint/b1850_exp/ocean/B1850_'+name+'_selected_sst_time_series.pdf', bbox_inches='tight',dpi=1200)

def paint_control_maritime_series(var1,var2):
    import matplotlib.pyplot as plt
    import numpy as np

    fig    =  plt.figure()
    ax     =  fig.add_subplot(111)

    ax.plot(np.linspace(1,365,365),var1[0],color='k',label='2S ~ 2N')
    ax.plot(np.linspace(1,365,365),var1[1],color='c',label='3N ~ 7N')
    ax.plot(np.linspace(1,365,365),var1[2],color='m',label='8N ~ 13N')

    ax.plot(np.linspace(1,365,365),var2[0],color='k',linestyle='--',label='2S ~ 2N')
    ax.plot(np.linspace(1,365,365),var2[1],color='c',linestyle='--',label='3N ~ 7N')
    ax.plot(np.linspace(1,365,365),var2[2],color='m',linestyle='--',label='8N ~ 13N')

    ax.set_xlim((100,150))
    ax.set_ylim((29,32))

    ax.legend(loc='upper left')

    ax.set_ylabel("sea surface temperature")
    ax.set_xlabel("Day")




    plt.savefig('/home/sun/paint/b1850_exp/ocean/B1850_ctrl_maritime_selected_sst_time_series.pdf', bbox_inches='tight',dpi=1200)





def main():
    result  =  get_sst_series()
    paint_control_maritime_series(result[0],result[3])



if __name__ == '__main__':
    main()
