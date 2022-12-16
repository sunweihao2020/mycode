'''
2022-12-2
This code paint the difference between the coupled and AGCM experiment
Month selected is April and May
'''
import os

# set colormap
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import matplotlib.pyplot as plt
import numpy as np

viridis = cm.get_cmap('Blues', 16)
newcolors = viridis(np.linspace(0, 1, 16))
newcmp = ListedColormap(newcolors)
newcmp.set_under('white')
#newcmp.set_over('blue')

def deal_with_data_3d(f0,level,varname,month_name,april_range=slice(90,119),may_range=slice(120,150)):
    '''this function calculate monthly average for the varname at level'''
    import numpy as np
    import xarray as nr

    if month_name == 'April':
        f  =  f0.sel(lev=level,time=april_range)
    else:
        f  =  f0.sel(lev=level,time=may_range)

    month_avg  =  np.nanmean(f[varname],axis=0)

    return month_avg

def deal_with_data_2d(f0,varname,month_name,april_range=slice(90,119),may_range=slice(120,150)):
    '''this function calculate monthly average for the varname at level'''
    import numpy as np
    import xarray as nr

    if month_name == 'April':
        print('The month is {}'.format(month_name))
        f  =  f0.sel(time=april_range)
    else:
        print('The month is {}'.format(month_name))
        f  =  f0.sel(time=may_range)

    month_avg  =  np.nanmean(f[varname],axis=0)

    return month_avg

def paint_month_mean(ncfile_4,ncfile_5,month_name,lat_range=slice(-10,30),lon_range=slice(40,120)):
    '''Paint the specific month low-level circulation'''
    import cartopy.crs as ccrs
    import matplotlib.pyplot as plt
    import numpy as np
    import sys

    sys.path.append("/home/sun/mycode/paint/")
    from paint_lunwen_version3_0_fig2b_2m_tem_wind_20220426 import set_cartopy_tick,save_fig
    from paint_lunwen_version3_0_fig2a_tem_gradient_20220426 import add_text

    # figure
    proj  =  ccrs.PlateCarree()
    fig   =  plt.figure(figsize=(26,20))
    spec  =  fig.add_gridspec(nrows=1,ncols=2) # fouth figure first row is AGCM April and May, second row is CGCM April and May

    # set the scope
    lonmin,lonmax,latmin,latmax  =  45,115,-10,30
    extent     =  [lonmin,lonmax,latmin,latmax]

    # -------- AGCM April 850 hPa wind, Omega and Prect -----------------
    ax  =  fig.add_subplot(spec[0,0], projection = proj)

    # set tick
    set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(50,110,4,dtype=int),yticks=np.linspace(-10,30,5,dtype=int),nx=1,ny=1,labelsize=25)

    # equator line
    ax.plot([40,120],[0,0],'k--')

    # shade - prect
    im2  =  ax.contourf(ncfile_4.lon.data, ncfile_4.lat.data, ncfile_4['prect']*86400*1000, np.array([3,9,15,21,27]),cmap=newcmp,alpha=1,extend='both')

    # contour line - omega
    im1  =  ax.contour(ncfile_4.lon.data, ncfile_4.lat.data, -1 * ncfile_4['omega'], np.linspace(-0.15,0.15,11),colors='red',linewidths=2,alpha=1,zorder=1)
    im3  =  ax.contour(ncfile_4.lon.data, ncfile_4.lat.data, -1 * ncfile_4['omega'],  [0],colors='red',linewidths=3,alpha=1,zorder=1)

    # coastline
    ax.coastlines(resolution='110m',lw=1)

    # title
    ax.set_title('AGCM-April',loc='left',fontsize=30)
    ax.set_title('850 wind',loc='right',fontsize=30)

    # vector - 850 hPa wind
    q  =  ax.quiver(ncfile_4.lon.data, ncfile_4.lat.data, ncfile_4['u'], ncfile_4['v'], 
                regrid_shape=15, angles='uv',   # regrid_shape这个参数越小，是两门就越稀疏
                scale_units='xy', scale=1,        # scale是参考矢量，所以取得越大画出来的箭头就越短
                units='xy', width=0.25,
                transform=proj,
                color='k',linewidth=1.2,headlength = 5, headaxislength = 4, headwidth = 5)

    # -------- AGCM May 850 hPa wind, Omega and Prect -----------------
    ax  =  fig.add_subplot(spec[0,1], projection = proj)

    # set tick
    set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(50,110,4,dtype=int),yticks=np.linspace(-10,30,5,dtype=int),nx=1,ny=1,labelsize=25)

    # equator line
    ax.plot([40,120],[0,0],'k--')

    # shade - prect
    im2  =  ax.contourf(ncfile_4.lon.data, ncfile_4.lat.data, ncfile_5['prect']*86400*1000, np.array([3,9,15,21,27]),cmap=newcmp,alpha=1,extend='both')

    # contour line - omega
    im1  =  ax.contour(ncfile_4.lon.data, ncfile_4.lat.data, -1 * ncfile_5['omega'],  np.linspace(-0.15,0.15,11),colors='red',linewidths=2,alpha=1,zorder=1)
    im3  =  ax.contour(ncfile_4.lon.data, ncfile_4.lat.data, -1 * ncfile_5['omega'],  [0],colors='red',linewidths=3,alpha=1,zorder=1)

    # coastline
    ax.coastlines(resolution='110m',lw=1)

    # title
    ax.set_title('AGCM-May',loc='left',fontsize=30)
    ax.set_title('850 wind',loc='right',fontsize=30)

    # vector - 850 hPa wind
    q  =  ax.quiver(ncfile_4.lon.data, ncfile_4.lat.data, ncfile_5['u'], ncfile_5['v'], 
                regrid_shape=15, angles='uv',   # regrid_shape这个参数越小，是两门就越稀疏
                scale_units='xy', scale=1,        # scale是参考矢量，所以取得越大画出来的箭头就越短
                units='xy', width=0.25,
                transform=proj,
                color='k',linewidth=1.2,headlength = 5, headaxislength = 4, headwidth = 5)

    # add colorbar
    fig.subplots_adjust(top=0.8) 
    cbar_ax = fig.add_axes([0.2, 0.05, 0.6, 0.03]) 
    cb  =  fig.colorbar(im2, cax=cbar_ax, shrink=0.1, pad=0.01, orientation='horizontal')
    cb.ax.tick_params(labelsize=25)

    plt.savefig('/home/sun/paint/b1850_exp/f2000_ensemble/Apr_May_850_wind_prect.pdf',dpi=400)

def paint_month_mean_cgcm():
    '''Paint the specific month low-level circulation for CGCM'''
    import cartopy.crs as ccrs
    import matplotlib.pyplot as plt
    import numpy as np
    import sys
    import xarray as xr

    sys.path.append("/home/sun/mycode/paint/")
    from paint_lunwen_version3_0_fig2b_2m_tem_wind_20220426 import set_cartopy_tick,save_fig
    from paint_lunwen_version3_0_fig2a_tem_gradient_20220426 import add_text

    # figure
    proj  =  ccrs.PlateCarree()
    fig   =  plt.figure(figsize=(26,20))
    spec  =  fig.add_gridspec(nrows=1,ncols=2) # fouth figure first row is AGCM April and May, second row is CGCM April and May

    # set the scope
    lonmin,lonmax,latmin,latmax  =  45,115,-10,30
    extent     =  [lonmin,lonmax,latmin,latmax]

    # read the monthly data
    ncfile  =  xr.open_dataset('/home/sun/data/model_data/climate/b1850_control_atmospheric_monthly_average.nc')

    # -------- AGCM April 850 hPa wind, Omega and Prect -----------------
    ax  =  fig.add_subplot(spec[0,0], projection = proj)

    # set tick
    set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(50,110,4,dtype=int),yticks=np.linspace(-10,30,5,dtype=int),nx=1,ny=1,labelsize=25)

    # equator line
    ax.plot([40,120],[0,0],'k--')

    # shade - prect
    im2  =  ax.contourf(ncfile.lon.data, ncfile.lat.data, ncfile['PRECT'].data[3]*86400*1000, np.array([3,9,15,21,27]),cmap=newcmp,alpha=1,extend='both')

    # contour line - omega
    im1  =  ax.contour(ncfile.lon.data, ncfile.lat.data, -1 * ncfile['OMEGA'].sel(lev=700).data[3], np.linspace(-0.15,0.15,11),colors='red',linewidths=2,alpha=1,zorder=1)
    im3  =  ax.contour(ncfile.lon.data, ncfile.lat.data, -1 * ncfile['OMEGA'].sel(lev=700).data[3],  [0],colors='red',linewidths=3,alpha=1,zorder=1)

    # coastline
    ax.coastlines(resolution='110m',lw=1)

    # title
    ax.set_title('CGCM-April',loc='left',fontsize=30)
    ax.set_title('850 wind',loc='right',fontsize=30)

    # vector - 850 hPa wind
    q  =  ax.quiver(ncfile.lon.data, ncfile.lat.data, ncfile['U'].sel(lev=850).data[3], ncfile['V'].sel(lev=850).data[3], 
                regrid_shape=15, angles='uv',   # regrid_shape这个参数越小，是两门就越稀疏
                scale_units='xy', scale=1,        # scale是参考矢量，所以取得越大画出来的箭头就越短
                units='xy', width=0.25,
                transform=proj,
                color='k',linewidth=1.2,headlength = 5, headaxislength = 4, headwidth = 5)

    # -------- AGCM May 850 hPa wind, Omega and Prect -----------------
    ax  =  fig.add_subplot(spec[0,1], projection = proj)

    # set tick
    set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(50,110,4,dtype=int),yticks=np.linspace(-10,30,5,dtype=int),nx=1,ny=1,labelsize=25)

    # equator line
    ax.plot([40,120],[0,0],'k--')

    # shade - prect
    im2  =  ax.contourf(ncfile.lon.data, ncfile.lat.data, ncfile['PRECT'].data[4]*86400*1000, np.array([3,9,15,21,27]),cmap=newcmp,alpha=1,extend='both')

    # contour line - omega
    im1  =  ax.contour(ncfile.lon.data, ncfile.lat.data, -1 * ncfile['OMEGA'].sel(lev=700).data[4],  np.linspace(-0.15,0.15,11),colors='red',linewidths=2,alpha=1,zorder=1)
    im3  =  ax.contour(ncfile.lon.data, ncfile.lat.data, -1 * ncfile['OMEGA'].sel(lev=700).data[4],  [0],colors='red',linewidths=3,alpha=1,zorder=1)

    # coastline
    ax.coastlines(resolution='110m',lw=1)

    # title
    ax.set_title('CGCM-May',loc='left',fontsize=30)
    ax.set_title('850 wind',loc='right',fontsize=30)

    # vector - 850 hPa wind
    q  =  ax.quiver(ncfile.lon.data, ncfile.lat.data, ncfile['U'].sel(lev=850).data[4], ncfile['V'].sel(lev=850).data[4], 
                regrid_shape=15, angles='uv',   # regrid_shape这个参数越小，是两门就越稀疏
                scale_units='xy', scale=1,        # scale是参考矢量，所以取得越大画出来的箭头就越短
                units='xy', width=0.25,
                transform=proj,
                color='k',linewidth=1.2,headlength = 5, headaxislength = 4, headwidth = 5)

    # add colorbar
    fig.subplots_adjust(top=0.8) 
    cbar_ax = fig.add_axes([0.2, 0.05, 0.6, 0.03]) 
    cb  =  fig.colorbar(im2, cax=cbar_ax, shrink=0.1, pad=0.01, orientation='horizontal')
    cb.ax.tick_params(labelsize=25)

    plt.savefig('/home/sun/paint/b1850_exp/f2000_ensemble/Apr_May_850_wind_prect_CGCM.pdf',dpi=400)

def main():
    import xarray as xr
    import numpy as np
    # ------ 1. get the target variable for April-----------------------

    # U V
    agcm_u  =  xr.open_dataset('/home/sun/data/model_data/f2000_ensemble/U_climate2.nc')
    avg_agcm_u  =  deal_with_data_3d(agcm_u,level=850,varname='U',month_name='April',)

    agcm_v  =  xr.open_dataset('/home/sun/data/model_data/f2000_ensemble/V_climate2.nc')
    avg_agcm_v  =  deal_with_data_3d(agcm_v,level=850,varname='V',month_name='April',)

    # Omega
    agcm_omega = xr.open_dataset('/home/sun/data/model_data/f2000_ensemble/OMEGA_climate2.nc')
    avg_agcm_omega = deal_with_data_3d(agcm_omega,level=700,varname='OMEGA',month_name='April',)

    #print(np.nanmin(avg_agcm_omega))

    # Prect
    agcm_prect = xr.open_dataset('/home/sun/data/model_data/f2000_ensemble/PRECT_climate2.nc')
    avg_agcm_prect = deal_with_data_2d(agcm_prect,varname='PRECT',month_name='April',)

    # ------ 2. pack the results to the ncfile ---------------------------
    #couple_file  =  xr.open_dataset('/home/sun/data/model_data/climate/b1850_control_atmospheric_monthly_average_2.nc')
    ncfile_april  =  xr.Dataset(
    {
        "u": (["lat", "lon"], avg_agcm_u),
        "v": (["lat", "lon"], avg_agcm_v),
        "omega": (["lat", "lon"], avg_agcm_omega),
        "prect": (["lat", "lon"], avg_agcm_prect),
    },
    coords={
        "lat": (["lat"], agcm_u.lat.data),
        "lon": (["lon"], agcm_u.lon.data),
    },
    )

    # ------------------------ May average variable ---------------------
    # U V
    agcm_u  =  xr.open_dataset('/home/sun/data/model_data/f2000_ensemble/U_climate2.nc')
    avg_agcm_u  =  deal_with_data_3d(agcm_u,level=850,varname='U',month_name='May',)

    agcm_v  =  xr.open_dataset('/home/sun/data/model_data/f2000_ensemble/V_climate2.nc')
    avg_agcm_v  =  deal_with_data_3d(agcm_v,level=850,varname='V',month_name='May',)

    # Omega
    agcm_omega = xr.open_dataset('/home/sun/data/model_data/f2000_ensemble/OMEGA_climate2.nc')
    avg_agcm_omega = deal_with_data_3d(agcm_omega,level=700,varname='OMEGA',month_name='May',)

    # Prect
    agcm_prect = xr.open_dataset('/home/sun/data/model_data/f2000_ensemble/PRECT_climate2.nc')
    avg_agcm_prect = deal_with_data_2d(agcm_prect,varname='PRECT',month_name='May',)

    # ------ pack the results to the ncfile ---------------------------
    #couple_file  =  xr.open_dataset('/home/sun/data/model_data/climate/b1850_control_atmospheric_monthly_average_2.nc')
    ncfile_may  =  xr.Dataset(
    {
        "u": (["lat", "lon"], avg_agcm_u),
        "v": (["lat", "lon"], avg_agcm_v),
        "omega": (["lat", "lon"], avg_agcm_omega),
        "prect": (["lat", "lon"], avg_agcm_prect),
    },
    coords={
        "lat": (["lat"], agcm_u.lat.data),
        "lon": (["lon"], agcm_u.lon.data),
    },
    )

    # ------ 3. send to paint ----------------------------------------------
    paint_month_mean(ncfile_april,ncfile_may,month_name='a')
    paint_month_mean_cgcm()

if __name__  ==  '__main__':
    main()
