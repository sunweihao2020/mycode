'''
2022-9-21
This code is to calculate and paint monthly meri-vertical temperature

data is from b1850 control experiment 
'''
import xarray as xr
import numpy as np
import os
import matplotlib


src_path  =  "/home/sun/data/model_data/climate/"

# range option
lon_slice  =  slice(90,100)
lev_slice  =  slice(1000,100)

def cal_monthly_tem():  # file is already monthly acerage
    import os
    import xarray as xr
    import numpy as np
    '''This function calculate temperature between 90 to 100E
       time period: Jan to May
    '''
    file_list  =  os.listdir(src_path) ; file_list.sort()
    
    date       =  [0,30,60,90,120,150,180]


    # reference file
    f0         =  xr.open_dataset(src_path+"0830.climate.nc").sel(lev=lev_slice,lon=lon_slice)
    
    # array to save
    avg_tem    =  np.zeros((6,25,361))

    # calculate monthly average
    for i in range(6):
        # Jan to May
        start_day  =  date[i]
        end_day    =  date[i+1]
        for dd in range(start_day,end_day):
            f1        =  xr.open_dataset(src_path+file_list[dd]).sel(lev=lev_slice,lon=lon_slice)

            # calculate daily average
            avg_dd_t  =  np.nanmean(f1.T.data[0],axis=2)

            # save to array
            avg_tem[i]  +=  avg_dd_t/30  

    
    return avg_tem

def paint_meri_tem(tem):
    '''This code paint meri-vertical temperature
       In this function, the level use asymmetric level,
       above 290K the space is 2K 
    '''
    import matplotlib.pyplot as plt
    import sys
    sys.path.append("/home/sun/mycode/module/paint")
    import paint_lunwen_version3_0_fig1_bob_onset_seris as plv3
    
    from paint_lunwen_version3_0_fig2a_tem_gradient_20220426 import create_label_lat

    # month name
    month     =  ['Jan','Feb','Mar','Apr','May','Jun']

    # reference file
    f0         =  xr.open_dataset(src_path+"b1850_control_atmospheric_monthly_average.nc").sel(lev=lev_slice,lon=lon_slice)

    fig1    =  plt.figure(figsize=(26,20))
    spec1   =  fig1.add_gridspec(nrows=2,ncols=3)

    j = 0

    for row in range(2):
        for col in range(3):

            axs = fig1.add_subplot(spec1[row,col])


            # contour lines
            im  =  axs.contour(f0.lat,f0.lev,tem[j],levels=set_levels(),colors='k',linewidths=2.34)
            axs.clabel(im,inline_spacing=0, fontsize=15)

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


    path_out = "/home/sun/paint/b1850_exp/monthly/" ; plv3.check_path(path_out)
    file_out = "Jan_to_May_temperature_90to100_b1850_control.pdf"
    plt.savefig(path_out+file_out,dpi=600)



    
def set_levels():
    '''This function generate levels for contour, values above 290K space is 2K'''
    array1  =  np.linspace(220,290,15)
    array2  =  np.linspace(292,310,10)

    level   =  np.hstack((array1,array2))

    return level

def main():
    import xarray as xr
    avg_tem  =  xr.open_dataset('/home/sun/data/model_data/climate/b1850_control_atmospheric_monthly_average.nc').sel(lev=lev_slice,lon=lon_slice)
    
    paint_meri_tem(np.nanmean(avg_tem.T.data,axis=3))

    
    

if __name__ == "__main__":
    main()