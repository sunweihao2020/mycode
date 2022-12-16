'''
2022-12-04
This script compare the AGCM and CGCM experiment output based on pentad average
Variables: 925 hPa wind
'''
path0  =  '/home/sun/data/model_data/climate/b1850_exp/'         # CGCM output
path1  =  '/home/sun/data/model_data/f2000_ensemble/hybrid-2/pentad/'   # AGCM output

pentads  =  [22,23,24,25,26,27]

def paint_diff_pentad(agcm_u,cgcm_u,agcm_v,cgcm_v,extent=[45,115,-10,30]):
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

            # coast line
            ax.coastlines(resolution='110m',lw=2)

            print(agcm_u[j])
            # vector map
            q  =  ax.quiver(f0.lon, f0.lat, cgcm_u[j] - agcm_u[j], cgcm_v[j] - agcm_v[j], 
                regrid_shape=15, angles='uv',   # regrid_shape这个参数越小，是两门就越稀疏
                scale_units='xy', scale=0.45,        # scale是参考矢量，所以取得越大画出来的箭头就越短
                units='xy', width=0.25,
                transform=proj,
                color='k',linewidth=1.2,headlength = 5, headaxislength = 4, headwidth = 5,alpha=1)

            # set title
            ax.set_title('Pentad '+str(pentads[j]), loc='left', fontsize=25)
            ax.set_title('CGCM - AGCM', loc='right', fontsize=25)

            # vector legend
            add_vector_legend(ax = ax, q = q, speed=1)

            j += 1

    save_fig(path_out="/home/sun/paint/b1850_exp/f2000_ensemble/compare_with_cgcm/",file_out="Pentad_diff_agcm_cgcm_925wind.pdf")


def main():
    import xarray as xr

    lev      =  925
    # 1. read AGCM U and V
    f0   =  xr.open_dataset(path1 + 'U_pentad.nc').sel(lev = lev, time = pentads)
    f1   =  xr.open_dataset(path1 + 'V_pentad.nc').sel(lev = lev, time = pentads)

    # 2. read CGCM U and V
    f2   =  xr.open_dataset(path0 + 'b1850_control_atmosphere_pentad.nc').sel(lev = lev, time = pentads)

    # 3. send to paint pic
    paint_diff_pentad(f0.U, f2.U, f1.V, f2.V)

if __name__ == '__main__':
    main()