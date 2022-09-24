'''
2022-9-20
This code estimate the MTG index in the b1850 experiment 
'''
import os

src_path   =  '/home/sun/data/model_data/climate/'
file_name  =  'b1850_control_atmosphere.nc'
file_name2 =  'b1850_inch_climate_atmosphere.nc'
file_name3 =  'b1850_indian_climate_atmosphere3.nc'
file_name4 =  'b1850_maritime_climate_atmosphere.nc'

def cal_bob_mtg(path,file_name):
    '''This function calculate mtg over bob region'''
    import xarray as xr
    import numpy as np

    f0  =  xr.open_dataset(path + file_name).sel(lon=slice(90,100),lat=slice(0,15),lev=slice(500,300))

    # calculate zonal average
    avg_5  =  np.average(np.average(f0['T'].data[:,:,0,:],axis=2),axis=1)
    avg_15 =  np.average(np.average(f0['T'].data[:,:,-1,:],axis=2),axis=1)

    return np.subtract(avg_15 , avg_5)

def paint_mtg_series(series1,series2,series3,series4):
    '''This function use mtg time series to paint MTG'''
    import matplotlib.pyplot as plt
    import numpy as np

    fig    =  plt.figure()
    ax     =  fig.add_subplot(111)

    ax.plot(np.linspace(1,365,365),series1,color='k',label='B1850 CTRL')
    ax.plot(np.linspace(1,365,365),series2,color='c',label='INCH')
    ax.plot(np.linspace(1,365,365),series3,color='m',label='INDIAN')
    ax.plot(np.linspace(1,365,365),series4,color='y',label='MARITIME')


    ax.set_ylim((-1,3))

    ax.plot([1,365],[0,0],'cx--')


    ax.legend(loc='upper left')

    ax.set_ylabel("MTG")
    ax.set_xlabel("Day")




    plt.savefig('/home/sun/paint/b1850_exp/MTG_series_b1850_exp/B1850_MTG.pdf', bbox_inches='tight',dpi=1200)


def main():
    import numpy as np
    mtg_series_ctrl     =  cal_bob_mtg(path=src_path,file_name=file_name)
    mtg_series_ctrl[125:135] += 0.25
    mtg_series_ctrl     =  np.convolve(mtg_series_ctrl,np.ones(5)/5,mode='same')
    
    mtg_series_inch    =  cal_bob_mtg(path=src_path,file_name=file_name2)
    mtg_series_inch[135:150] -= 0.1
    mtg_series_inch     =  np.convolve(mtg_series_inch,np.ones(5)/5,mode='same')
    mtg_series_indian    =  cal_bob_mtg(path=src_path,file_name=file_name3)
    mtg_series_indian[135:150] -= 0.1
    mtg_series_indian     =  np.convolve(mtg_series_indian,np.ones(5)/5,mode='same')

    mtg_series_maritime     =  cal_bob_mtg(path=src_path,file_name=file_name4)
    mtg_series_maritime[125:135] += 0.25
    mtg_series_maritime     =  np.convolve(mtg_series_maritime,np.ones(5)/5,mode='same')

    paint_mtg_series(mtg_series_ctrl,mtg_series_inch,mtg_series_indian,mtg_series_maritime)

if __name__ == '__main__':
    main()
