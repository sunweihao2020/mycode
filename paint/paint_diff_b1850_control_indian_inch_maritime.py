'''
2022-9-21
This code paint difference between b1850 control experiment and sensitive experiments
'''
import numpy as np
src_path  =  '/home/sun/data/model_data/climate/'

# range option
lon_slice  =  slice(90,100)
lev_slice  =  slice(1000,100)

clev       =  np.linspace(-0.05,0.05,11)

def cal_diff():
    import numpy as np
    import xarray as xr

    f0  =  xr.open_dataset(src_path + 'b1850_control_atmospheric_monthly_average.nc').sel(lev=lev_slice,lon=lon_slice)

    inch    =  xr.open_dataset(src_path + 'b1850_inch_atmospheric_monthly_average.nc').sel(lev=lev_slice,lon=lon_slice)
    indian  =  xr.open_dataset(src_path + 'b1850_indian_atmospheric_monthly_average.nc') .sel(lev=lev_slice,lon=lon_slice)
    maritime=  xr.open_dataset(src_path + 'b1850_maritime_atmospheric_monthly_average.nc').sel(lev=lev_slice,lon=lon_slice)

    diff_indian  =  np.subtract(f0.OMEGA.data*-1, indian.OMEGA.data*-1)
    diff_inch    =  np.subtract(f0.OMEGA.data*-1, inch.OMEGA.data*-1)
    diff_maritime    =  np.subtract(f0.OMEGA.data*-1, maritime.OMEGA.data*-1)

    return np.nanmean(diff_indian,axis=3),np.nanmean(diff_inch,axis=3),np.nanmean(diff_maritime,axis=3)

def paint_diff_sensitive_exp(indian,inch,maritime):
    '''This code paint temperature difference between sensitive experiments'''
    import matplotlib.pyplot as plt
    import xarray as xr
    import numpy as np
    import sys
    sys.path.append("/home/sun/mycode/module/paint")
    import paint_lunwen_version3_0_fig1_bob_onset_seris as plv3
    
    from paint_lunwen_version3_0_fig2a_tem_gradient_20220426 import create_label_lat

    # month name
    month     =  ['Jan','Feb','Mar','Apr','May','Jun']

    # reference file
    f0         =  xr.open_dataset(src_path+"b1850_control_atmospheric_monthly_average.nc").sel(lev=lev_slice,lon=lon_slice)

    # ----------paint diff with indian-------------------------------
    fig1    =  plt.figure(figsize=(26,20))
    spec1   =  fig1.add_gridspec(nrows=2,ncols=3)

    j = 0

    for row in range(2):
        for col in range(3):

            axs = fig1.add_subplot(spec1[row,col])


            # contour lines
            im  =  axs.contourf(f0.lat,f0.lev,indian[j],clev,cmap='coolwarm',extend='both')


            # deal with topography
            topofile   =   xr.open_dataset("/home/sun/data/topography/bathymetric.nc").sel(lon=lon_slice)
            dixing  =  topofile.elevation.data
            dixing[dixing <= 0]  =  0
            topo    =  np.average(dixing,axis=1)


            # set label
            axs.set_xticks(np.linspace(-10,40,6))
            axs.set_xticklabels(create_label_lat(np.linspace(-10,40,6,dtype=int)))
            axs.set_yticks(np.linspace(1000,200,5,dtype=int))
            axs.set_yticklabels(np.linspace(1000,200,5,dtype=int))
            axs.tick_params(axis='both',labelsize=20.5)

            # set axis range
            axs.set_xlim((-10,40))

            axs.invert_yaxis()

            # set title
            axs.set_title(month[j],fontsize=30)

            # add topography graph
            ax2  =  axs.twinx()

            ax2.set_ylim((0,9))
            ax2.tick_params(axis='both',labelsize=20.5)

            ax2.plot(topofile.lat.data,topo/1000,color='k')
            ax2.fill_between(topofile.lat.data,0,topo/1000,where=topo>0,color='k')

            j += 1

    # 加colorbar
    fig1.subplots_adjust(top=0.8) 
    cbar_ax = fig1.add_axes([0.2, 0.05, 0.6, 0.03]) 
    cb  =  fig1.colorbar(im, cax=cbar_ax, shrink=0.1, pad=0.01, orientation='horizontal')
    cb.ax.tick_params(labelsize=20)

    path_out = "/home/sun/paint/b1850_exp/monthly/" ; plv3.check_path(path_out)
    file_out = "Jan_to_May_omega_diff_control_indian_90to100.pdf"
    plt.savefig(path_out+file_out,dpi=600)

    # ----------paint diff with inch-------------------------------
    fig1    =  plt.figure(figsize=(26,20))
    spec1   =  fig1.add_gridspec(nrows=2,ncols=3)

    j = 0

    for row in range(2):
        for col in range(3):

            axs = fig1.add_subplot(spec1[row,col])


            # contour lines
            im  =  axs.contourf(f0.lat,f0.lev,inch[j],clev,cmap='coolwarm',extend='both')


            # deal with topography
            topofile   =   xr.open_dataset("/home/sun/data/topography/bathymetric.nc").sel(lon=lon_slice)
            dixing  =  topofile.elevation.data
            dixing[dixing <= 0]  =  0
            topo    =  np.average(dixing,axis=1)


            # set label
            axs.set_xticks(np.linspace(-10,40,6))
            axs.set_xticklabels(create_label_lat(np.linspace(-10,40,6,dtype=int)))
            axs.set_yticks(np.linspace(1000,200,5,dtype=int))
            axs.set_yticklabels(np.linspace(1000,200,5,dtype=int))
            axs.tick_params(axis='both',labelsize=20.5)

            # set axis range
            axs.set_xlim((-10,40))

            axs.invert_yaxis()

            # set title
            axs.set_title(month[j],fontsize=30)

            # add topography graph
            ax2  =  axs.twinx()

            ax2.set_ylim((0,9))
            ax2.tick_params(axis='both',labelsize=20.5)

            ax2.plot(topofile.lat.data,topo/1000,color='k')
            ax2.fill_between(topofile.lat.data,0,topo/1000,where=topo>0,color='k')

            j += 1

    # 加colorbar
    fig1.subplots_adjust(top=0.8) 
    cbar_ax = fig1.add_axes([0.2, 0.05, 0.6, 0.03]) 
    cb  =  fig1.colorbar(im, cax=cbar_ax, shrink=0.1, pad=0.01, orientation='horizontal')
    cb.ax.tick_params(labelsize=20)

    path_out = "/home/sun/paint/b1850_exp/monthly/" ; plv3.check_path(path_out)
    file_out = "Jan_to_May_omega_diff_control_inch_90to100.pdf"
    plt.savefig(path_out+file_out,dpi=600)

    # ----------paint diff with maritime-------------------------------
    fig1    =  plt.figure(figsize=(26,20))
    spec1   =  fig1.add_gridspec(nrows=2,ncols=3)

    j = 0

    for row in range(2):
        for col in range(3):

            axs = fig1.add_subplot(spec1[row,col])


            # contour lines
            im  =  axs.contourf(f0.lat,f0.lev,maritime[j],clev,cmap='coolwarm',extend='both')


            # deal with topography
            topofile   =   xr.open_dataset("/home/sun/data/topography/bathymetric.nc").sel(lon=lon_slice)
            dixing  =  topofile.elevation.data
            dixing[dixing <= 0]  =  0
            topo    =  np.average(dixing,axis=1)


            # set label
            axs.set_xticks(np.linspace(-10,40,6))
            axs.set_xticklabels(create_label_lat(np.linspace(-10,40,6,dtype=int)))
            axs.set_yticks(np.linspace(1000,200,5,dtype=int))
            axs.set_yticklabels(np.linspace(1000,200,5,dtype=int))
            axs.tick_params(axis='both',labelsize=20.5)

            # set axis range
            axs.set_xlim((-10,40))

            axs.invert_yaxis()

            # set title
            axs.set_title(month[j],fontsize=30)

            # add topography graph
            ax2  =  axs.twinx()

            ax2.set_ylim((0,9))
            ax2.tick_params(axis='both',labelsize=20.5)

            ax2.plot(topofile.lat.data,topo/1000,color='k')
            ax2.fill_between(topofile.lat.data,0,topo/1000,where=topo>0,color='k')

            j += 1

    # 加colorbar
    fig1.subplots_adjust(top=0.8) 
    cbar_ax = fig1.add_axes([0.2, 0.05, 0.6, 0.03]) 
    cb  =  fig1.colorbar(im, cax=cbar_ax, shrink=0.1, pad=0.01, orientation='horizontal')
    cb.ax.tick_params(labelsize=20)

    path_out = "/home/sun/paint/b1850_exp/monthly/" ; plv3.check_path(path_out)
    file_out = "Jan_to_May_omega_diff_control_maritime_90to100.pdf"
    plt.savefig(path_out+file_out,dpi=600)

def main():
    indian,inch,maritime  =  cal_diff()

    paint_diff_sensitive_exp(indian,inch,maritime)

if __name__ == '__main__':
    main()
