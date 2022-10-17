'''
2022-10-12
This code assess the difference between the climatology using reanalysis and b1850 model simulation

Variables compared: precipitation; 850hPa wind; zonal_pressure section for cross-equator flow 
'''
import os

merra_climate  =  '/home/sun/data/merra2_climate_vars_multi/monthly/merra2_climate_monthly_vars.nc'
b1850_control  =  '/home/sun/data/model_data/climate/b1850_control_atmospheric_monthly_average.nc'

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

    q   =   ax.streamplot(f0.lon, f0.lat, f0.U.data[4], f0.V.data[4],linewidth=3, color = 'k',density=[1, 1.15], arrowsize=2.75, arrowstyle='->')


    save_fig(path_out="/home/sun/paint/lunwen/assessment/",file_out="b1850_control_apr_925_wind.pdf")

def paint_jja_850_precip_wind(extent,lon_slice,lat_slice):
    '''This function plot jja mean 850hpa wind and precipitation for merra-climate and b1850_control'''
    import xarray as xr
    import numpy as np


    '''read the monthly mean file'''
    f1  =  xr.open_dataset(merra_climate)
    f2  =  xr.open_dataset(b1850_control)

    ## 1. The resolution between MERRA-2 and CESM2 is different, I need intepolate it to keep them consistent
    merra_les_u,merra_les_v  =  interp_merra_to_cam(f1,f2)

    '''calculate wind speed for merra2 and model'''
    speed_merra = np.sqrt(np.square(merra_les_u) + np.square(merra_les_v))
    speed_model = np.sqrt(np.square(f2.U.data)   + np.square(f2.V.data))

    
def interp_merra_to_cam(f,ref_f):
    '''This function intepolate merra2 variables to the B1850 output. Variables include U V'''
    import numpy as np
    import time

    '''Array save the result'''
    merra_u  =  ref_f.U.data.copy()
    merra_v  =  merra_u.copy()

    '''information of the lat/lon'''
    # print(f.lon.data)      # -180 - 179.375 ; position 288 corresponds to 0
    # print(ref_f.lon.data)  # 0-368.75

    ''' transfer merra2 origin data's longitude
        [288 to end] + [0 to 288] sequence
    '''
    origin_merra_u  =  f.U.data.copy()
    origin_merra_v  =  origin_merra_u.copy()

    origin_merra_u[:,:,:,0:288]  =  f.U.data[:,:,:,288:]
    origin_merra_u[:,:,:,288:]   =  f.U.data[:,:,:,0:288]
    origin_merra_v[:, :, :, 0:288] = f.V.data[:, :, :, 288:]
    origin_merra_v[:, :, :, 288:]  = f.V.data[:, :, :, 0:288]

    # change the data in the f
    f.U.data  =  origin_merra_u
    f.V.data  =  origin_merra_v

    # replace the old longitude for merra-2
    new_lon          =   np.zeros((576))
    new_lon[0:288]   =   f.lon.data[288:]
    new_lon[288:]    =   f.lon.data[0:288]   +  360

    #print(new_lon)  # 0 - 359.375

    '''interpolate origin data to the new longitude
       lev lat lon need to be interpolated 
       Thus three interim array are needed
       Here I declare a function for this process
    '''
    start  =  time.time()
    interp_u  =  interpolate_4d_resolution_second(f,ref_f,'U')
    interp_v  =  interpolate_4d_resolution_second(f,ref_f,'V')
    print('interpolation spend %f second' % (time.time() - start))

    return interp_u,interp_v




def interpolate_4d_resolution(f,ref_f,varname):
    '''This function can interpolate f to the ref_f's resolution
       dimensions should be (time,lev,lat,lon)
       The time dimension have to be the same
    '''
    import numpy as np

    '''I need to declare 3 interim array for interpolation
       1. interpolate from right to left
       2. interpolate from left to right
    '''
    interp_lev  =  np.zeros((f[varname].shape[0],len(ref_f['lev']),f[varname].shape[2],f[varname].shape[3]))
    interp_lat  =  np.zeros((f[varname].shape[0],len(ref_f['lev']),len(ref_f['lat']),f[varname].shape[3]))
    interp_lon  =  np.zeros(ref_f[varname].shape)

    for xx in range(len(f['lon'])):
        for yy in range(len(f['lat'])):
            for tt in range(len(f['time'])):
                interp_lev[tt,:,yy,xx]  =  np.interp(ref_f['lev'].data,f['lev'].data,f[varname].data[tt,:,yy,xx])

    for xx in range(len(f['lon'])):
        for ll in range(len(ref_f['lev'])):
            for tt in range(len(f['time'])):
                interp_lat[tt,ll,:,xx]  =  np.interp(ref_f['lat'].data,f['lat'].data,interp_lev[tt,ll,:,xx])

    # replace the old longitude for merra-2
    new_lon = np.zeros((576))
    new_lon[0:288] = f.lon.data[288:]
    new_lon[288:] = f.lon.data[0:288] + 360

    for yy in range(len(ref_f['lat'])):
        for ll in range(len(ref_f['lev'])):
            for tt in range(len(ref_f['time'])):
                interp_lon[tt,ll,yy,:]  =  np.interp(ref_f['lon'].data,new_lon,interp_lat[tt,ll,yy,:])

    return interp_lon

def interpolate_4d_resolution_second(f,ref_f,varname):
    '''This function can interpolate f to the ref_f's resolution
       dimensions should be (time,lev,lat,lon)
       The time dimension have to be the same
    '''
    import numpy as np

    '''I need to declare 3 interim array for interpolation
       1. interpolate from right to left
       2. interpolate from left to right
    '''
    interp_lon  =  np.zeros((f[varname].shape[0],f[varname].shape[1],f[varname].shape[2],len(ref_f['lon'])))
    interp_lat  =  np.zeros((f[varname].shape[0],f[varname].shape[1],len(ref_f['lat']),len(ref_f['lon'])))
    interp_lev  =  np.zeros(ref_f[varname].shape)

    # replace the old longitude for merra-2
    new_lon = np.zeros((576))
    new_lon[0:288] = f.lon.data[288:]
    new_lon[288:] = f.lon.data[0:288] + 360

    for tt in range(len(f['time'])):
        for ll in range(len(f['lev'])):
            for yy in range(len(f['lat'])):
                interp_lon[tt,ll,yy,:]  =  np.interp(ref_f['lon'].data,new_lon,f[varname].data[tt,ll,yy,:])

    for tt in range(len(f['time'])):
        for ll in range(len(f['lev'])):
            for xx in range(len(ref_f['lon'])):
                interp_lat[tt,ll,:,xx]  =  np.interp(ref_f['lat'].data,f['lat'].data,interp_lon[tt,ll,:,xx])


    for tt in range(len(ref_f['time'])):
        for yy in range(len(ref_f['lat'])):
            for xx in range(len(ref_f['lon'])):
                interp_lev[tt,:,yy,xx]  =  np.interp(ref_f['lev'].data,f['lev'].data,interp_lat[tt,:,yy,xx])

    return interp_lev

def interpolate_4d_resolution_third(f,ref_f,varname):
    '''This function can interpolate f to the ref_f's resolution
       dimensions should be (time,lev,lat,lon)
       The time dimension have to be the same
    '''
    import numpy as np

    '''I need to declare 3 interim array for interpolation
       1. interpolate from right to left
       2. interpolate from left to right
    '''
    interp_lev  =  np.zeros((f[varname].shape[0],len(ref_f['lev']),f[varname].shape[2],f[varname].shape[3]))
    interp_lat  =  np.zeros((f[varname].shape[0],len(ref_f['lev']),len(ref_f['lat']),f[varname].shape[3]))
    interp_lon  =  np.zeros(ref_f[varname].shape)

    for tt in range(len(f['time'])):
        for yy in range(len(f['lat'])):
            for xx in range(len(f['lon'])):
                interp_lev[tt,:,yy,xx]  =  np.interp(ref_f['lev'].data,f['lev'].data,f[varname].data[tt,:,yy,xx])

    for tt in range(len(f['time'])):
        for ll in range(len(ref_f['lev'])):
            for xx in range(len(f['lon'])):
                interp_lat[tt,ll,:,xx]  =  np.interp(ref_f['lat'].data,f['lat'].data,interp_lev[tt,ll,:,xx])

    # replace the old longitude for merra-2
    new_lon = np.zeros((576))
    new_lon[0:288] = f.lon.data[288:]
    new_lon[288:] = f.lon.data[0:288] + 360

    for tt in range(len(ref_f['time'])):
        for ll in range(len(ref_f['lev'])):
            for yy in range(len(ref_f['lat'])):
                interp_lon[tt,ll,yy,:]  =  np.interp(ref_f['lon'].data,new_lon,interp_lat[tt,ll,yy,:])

    return interp_lon




def main():
    lonmin,lonmax,latmin,latmax  =  30,120,-10,40
    extent     =  [lonmin,lonmax,latmin,latmax]


    paint_jja_850_precip_wind(1,2,3)

if __name__ == "__main__":
    main()