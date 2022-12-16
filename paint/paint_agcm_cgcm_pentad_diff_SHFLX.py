'''
2022-12-05
This script compare the AGCM and CGCM experiment output based on pentad average
Variables: surface temperature (TS)
'''
path0  =  '/home/sun/data/model_data/climate/b1850_exp/'         # CGCM output
path1  =  '/home/sun/data/model_data/f2000_ensemble/hybrid-2/pentad/'   # AGCM output

pentads  =  [22,23,24,25,26,27]

def paint_diff_pentad(agcm_ts, cgcm_ts, extent=[45,115,-10,30]):
    '''This function paint pentad diffenerce between AGCM and CGCM
    1. select 4 pentad to compare: 22 24 26 28
    '''
    import matplotlib.pyplot as plt
    import cartopy.crs as ccrs
    import numpy as np
    import xarray as xr

    import sys
    sys.path.append("/home/sun/mycode/paint/")
    from paint_lunwen_version3_0_fig2b_2m_tem_wind_20220426 import set_cartopy_tick,add_vector_legend,save_fig

    # set figure
    proj    =  ccrs.PlateCarree()
    fig1    =  plt.figure(figsize=(30,14))
    spec1   =  fig1.add_gridspec(nrows=2,ncols=3)


    # reference file
    f0  =  xr.open_dataset(path1 + 'U_pentad.nc')

    j = 0
    for row in range(2):
        for col in range(3):
            ax  =  fig1.add_subplot(spec1[row,col], projection = proj)

            # set tick
            set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(50,110,4,dtype=int),yticks=np.linspace(-10,30,5,dtype=int),nx=1,ny=1,labelsize=25)

            # equator-line
            ax.plot([40,120],[0,0],'k--')

            # shade - SHFLX
            im2  =  ax.contourf(f0.lon.data, f0.lat.data, (cgcm_ts[j] - agcm_ts[j]),  np.linspace(-5,5,21),cmap='coolwarm',alpha=1,extend='both')
            im3  =  ax.contour(f0.lon.data, f0.lat.data,  (cgcm_ts[j] - agcm_ts[j]),  np.linspace(-5,5,21), colors='black',linewidths=2,alpha=1,zorder=1)

            # coast line
            ax.coastlines(resolution='110m',lw=2)

            # set title
            ax.set_title('Pentad '+str(pentads[j]), loc='left', fontsize=25)
            ax.set_title('CGCM - AGCM', loc='right', fontsize=25)

            j += 1
    #  加colorbar
    fig1.subplots_adjust(top=0.8) 
    cbar_ax = fig1.add_axes([0.2, 0.05, 0.6, 0.03]) 
    cb  =  fig1.colorbar(im2, cax=cbar_ax, shrink=0.1, pad=0.01, orientation='horizontal')
    cb.ax.tick_params(labelsize=20)

    save_fig(path_out="/home/sun/paint/b1850_exp/f2000_ensemble/compare_with_cgcm/",file_out="Pentad_diff_agcm_cgcm_SHFLX.pdf")


def main():
    import xarray as xr

    lev      =  925
    # 1. read AGCM TS
    f1   =  xr.open_dataset(path1 + 'SHFLX_pentad.nc').sel(time = pentads)

    # 2. read CGCM TS
    f2   =  xr.open_dataset(path0 + 'b1850_control_atmosphere_pentad.nc').sel(time = pentads)

    # 3. send to paint pic
    paint_diff_pentad(f1.SHFLX, f2.SHFLX)

if __name__ == '__main__':
    main()