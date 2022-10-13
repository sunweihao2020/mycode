'''
2022-10-12
This code assess the difference between the climatology using reanalysis and b1850 model simulation

Variables compared: precipitation; 850hPa wind; zonal_pressure section for cross-equator flow 
'''
import os

merra_climate  =  '/home/sun/data/merra2_climate_vars_multi/monthly/merra2_climate_monthly_vars.nc'
<<<<<<< HEAD
b1850_control  =  '/home/sun/data/model_data/climate/b1850_control_atmospheric_monthly_average.nc'
=======
b1850_control  =  '/home/sun/data/model_data/climate/b1850_control_climate_atmosphere.nc'
>>>>>>> origin/master

def paint_model_apr_925(extent):
    '''check the model result in the april wind'''
    '''The result is correct!'''
    import xarray as xr
    import cartopy.crs as ccrs
    import matplotlib.pyplot as plt
    import numpy as np
    import sys

    sys.path.append("/home/sun/mycode/paint/")
    from paint_lunwen_version3_0_fig2b_2m_tem_wind_20220426 import set_cartopy_tick,save_fig


    f0  =  xr.open_dataset(b1850_control).sel(lon=slice(30,120),lat=slice(-10,40),lev=925)

    # set figure
    proj     =  ccrs.PlateCarree()
    fig1     =  plt.figure(figsize=(10,8))
    
    ax       =  fig1.add_subplot(projection=proj)

    # set tick
    set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(30,120,7,dtype=int),yticks=np.linspace(-10,40,6,dtype=int),nx=1,ny=1,labelsize=25)

    # coastline
    ax.coastlines(resolution='110m',lw=1)

    # streamline
    print(f0.U)
<<<<<<< HEAD
    q   =   ax.streamplot(f0.lon, f0.lat, f0.U.data[3], f0.V.data[3],linewidth=3, color = 'k',density=[1, 1.15], arrowsize=2.75, arrowstyle='->')
=======
    q   =   ax.streamplot(f0.lon, f0.lat, f0.U.data[125], f0.V.data[125],linewidth=3, color = 'k',density=[1, 1.15], arrowsize=2.75, arrowstyle='->')
>>>>>>> origin/master

    save_fig(path_out="/home/sun/paint/lunwen/assessment/",file_out="b1850_control_apr_925_wind.pdf")

def paint_jja_850_precip_wind(extent,lon_slice,lat_slice):
    '''This function plot jja mean 850hpa wind and precipitation for merra-climate and b1850_control'''
    import xarray as xr
    import numpy as np
<<<<<<< HEAD

    '''read the monthly mean file'''
    f1  =  xr.open_dataset(merra_climate)
    f2  =  xr.open_dataset(b1850_control)
=======
>>>>>>> origin/master
    

def main():
    lonmin,lonmax,latmin,latmax  =  30,120,-10,40
    extent     =  [lonmin,lonmax,latmin,latmax]

<<<<<<< HEAD
    paint_model_apr_925(extent=extent)
=======
    #paint_model_apr_925(extent=extent)
>>>>>>> origin/master



if __name__ == "__main__":
    main()