'''
2022-10-26
This code is to calculate moving average for the daily variation of the CEFs
9 point smooth using np convolve
'''

def main():
    import numpy as np
    import xarray as xr

    file   =   xr.open_dataset('/home/sun/data/model_data/daily_cross_equator_flow/yearly_cycle_merra_b1850_CEFs.nc')
    for i in range(5):
        file['merra_cefs'].data[i]   =  np.convolve(file['merra_cefs'].data[i],np.ones(11)/11,mode='same')
        file['control_cefs'].data[i] =  np.convolve(file['control_cefs'].data[i], np.ones(11)/11, mode='same')
        file['inch_cefs'].data[i]    =  np.convolve(file['inch_cefs'].data[i], np.ones(11)/11, mode='same')
        file['indian_cefs'].data[i]  =  np.convolve(file['indian_cefs'].data[i], np.ones(11)/11, mode='same')
        file['inch_indian_cefs'].data[i] = np.convolve(file['inch_indian_cefs'].data[i], np.ones(11)/11, mode='same')
        file['maritime_cefs'].data[i]    = np.convolve(file['maritime_cefs'].data[i], np.ones(11)/11, mode='same')

    file.to_netcdf('/home/sun/data/model_data/daily_cross_equator_flow/yearly_cycle_merra_b1850_CEFs_11pointsmooth.nc')

if __name__ == '__main__':
    main()