'''
This code paint January and July meridional circulation in the BOB region
To depict the characteristic of the Hadley cell
'''
#path0  =  "/home/sun/data/merra2_climate_vars_multi/daily/"
#path1  =  "/home/sun/data/merra2_climate_vars_multi/monthly/"

path0  =  "/Users/sunweihao/data/merra2_climate_vars_multi/daily/"
path1  =  "/Users/sunweihao/data/merra2_climate_vars_multi/monthly/"

def cal_jan_jul_average():
    '''This function calculate climate monthly vars average and save to the path'''
    import numpy as np
    import xarray as xr
    import os

    # get the files list
    file_list  =  os.listdir(path0) ; file_list.sort()

    # month days
    days       =  [31,28,31,30,31,30,31,31,30,31,30,31]

    # calculate monthly
    ## reference file
    f0         =  xr.open_dataset(path0+"0101.climate.nc")

    ### get datasets vars name
    vars = list(f0.keys())

    ## --------calculate monthly average----------
    ### create  empty dataset
    monthly_avg  =  xr.Dataset()
    for vvvv in vars:
        base  =  create_base_array(f0[vvvv])

        for mon in range(len(days)):
            start   = int(np.sum(days[0:mon]))
            end     = int(np.sum(days[0:(mon+1)]))
            period  = end-start
            #print("start is %d" % start)
            #print("end is %d" % end)

            for dd in range(start,end):

                f1         =   xr.open_dataset(path0+file_list[dd])
                base[mon]  +=  f1[vvvv].data[0] / period

        # save array to xarray dataarray
        monthly_avg[vvvv]  =  create_base_dataarray(base)

    # save monthly dataset to nc file
    monthly_avg.to_netcdf(path1+"merra2_climate_monthly_vars.nc")

def create_base_dataarray(array):
    '''This function create dataarray for input array'''
    import xarray as xr
    import numpy as np

    # reference file
    f0   =   xr.open_dataset(path0 + "0101.climate.nc")
    dim  =   len(array.shape)
    if dim == 3:
        da = xr.DataArray(
            data=array,
            dims=["time","lat","lon"],
            coords={
                "time":np.linspace(1,12,12),
                "lat":f0.lat.data,
                "lon":f0.lon.data,
            },
        )
    else:
        da = xr.DataArray(
            data=array,
            dims=["time","lev", "lat", "lon"],
            coords={
                "time": np.linspace(1, 12, 12),
                "lat": f0.lat.data,
                "lon": f0.lon.data,
                "lev": f0.lev.data,
            },
        )
        return da

def create_base_array(array):
    '''This function returns base array based on the input array'''
    import numpy as np
    time_length  =  12

    dims         =  len(array.shape)

    if dims == 3:
        base_array  =  np.zeros((time_length,array.shape[1],array.shape[2]))
    elif dims == 4:
        base_array  = np.zeros((time_length, array.shape[1], array.shape[2], array.shape[3]))
    else:
        print("Error, the dimension is "+str(dims))

    return base_array

def paint_jan_jul_tem_stream():
    '''This function paint Jan and Jul temperature add circulation'''
    import numpy as np
    import xarray as xr

    import cmasher as cmr  # third part colormap
    import matplotlib.pyplot as plt

    import sys
    module_path = "/Users/sunweihao/mycode/module"
    sys.path.append(module_path)
    from module_sun_new import generate_xlabel
    from module_sun_new import add_text

    # set range
    lon_slice  =  slice(90,100)

    f0   =  xr.open_dataset(path1 + "merra2_climate_monthly_vars.nc").sel(lon=lon_slice)

    # calculate zonal average
    tem  =  np.nanmean(f0.T.data,axis=3)
    w    =  np.nanmean(f0.OMEGA.data,axis=3)
    v    =  np.nanmean(f0.V.data,axis=3)

    # set figure and axs
    fig  =  plt.figure(figsize=(30,23))
    spec =  fig.add_gridspec(nrows=2, ncols=3)

    # set colormap
    cmap =  cmr.holly

    # deal with data for paint
    tem_y,v,w  =  deal_data_for_paint(tem=tem,w=w,v=v,old_level=f0.lev.data,lat=f0.lat.data,lon=f0.lon.data)
    w *= -500  # scale the w
    new_level  =  np.linspace(1000,100,37)

    j = 0

    # select month
    month       =  [1,2,3,4,5,6]
    month_name  =  ["Feb","Mar","Apr","May","Jun","Jul"]

    for row in range(2):
        for col in range(3):
            ax  =  fig.add_subplot(spec[row,col])

            # set tick and tick label
            xtick  =  np.linspace(-10,30,9,dtype=int)
            ytick  =  np.linspace(1000,100,10,dtype=int)

            xtick_label  =  generate_xlabel(xtick)

            ax.set_xticks(xtick)
            ax.set_yticks(ytick)
            ax.set_xticklabels(xtick_label)

            # set axis tick attribute
            ax.tick_params(axis='both', labelsize = 22.5)

            # plot temperature gradient contourf
            im  =  ax.contourf(f0.lat.data, new_level, tem_y[month[j]]*1e5,np.linspace(-2,2,21),cmap=cmap,extend='both')

            # plot zeros line
            cr  =  ax.contour(f0.lat.data, new_level, tem_y[month[j]]*1e5,[0],colors='gray',linestyles='--',linewidths=3)

            # set range
            ax.set_xlim((-10, 30))

            # set axis label
            ax.set_xlabel("Latitude", fontsize=18)

            # invert y axis
            ax.invert_yaxis()

            # give nan value black color
            plt.gca().set_facecolor("black")

            # add streamline to picture
            ax2  =  ax.twinx()
            ax2.streamplot(f0.lat.data, new_level[::-1], v[month[j], ::-1], w[month[j], ::-1], color='k', linewidth=2.5,
                           density=2, arrowsize=2.75, arrowstyle='->')
            ax2.set_yticks([])

            # add month name
            ax.set_title(month_name[j],loc='left',fontsize=30)

            j += 1

    fig.subplots_adjust(top=0.8)
    cbar_ax = fig.add_axes([0.2, 0.05, 0.6, 0.02])
    cb = fig.colorbar(im, cax=cbar_ax, shrink=0.1, pad=0.01, orientation='horizontal')
    cb.ax.tick_params(labelsize=25)

    plt.savefig("/Users/sunweihao/paint/monthly_meri_vertical_tem_90to100E/Feb_to_Jul_temperature_gradient_streamline.png",dpi=500)
    plt.show()



def deal_data_for_paint(tem,w,v,old_level,lat,lon):
    '''
    The data for paint need to deal with
        1. vertical interpolate
        2. calculate meridional gradient of the temperature
    '''
    import numpy as np
    import sys
    module_path = "/Users/sunweihao/mycode/module"
    sys.path.append(module_path)
    from module_sun_new import cal_xydistance

    # calculate vertical interpolate for the temperature and v w
    # the input var has shape of (12,42,361)
    new_level  =  np.linspace(1000,100,37)

    new_t      =      np.zeros((v.shape[0],37,v.shape[2]))
    new_v      =      new_t.copy()
    new_w      =      new_v.copy()

    for tt in range(v.shape[0]):
        for yy in range(v.shape[2]):
            new_v[tt, :, yy] = np.interp(new_level[::-1], old_level[::-1], v[tt, ::-1, yy])  # Here I did not invert after interpolate
            new_w[tt, :, yy] = np.interp(new_level[::-1], old_level[::-1], w[tt, ::-1, yy])  # But the result paint is not error

            new_t[tt, :, yy] = np.interp(new_level[::-1], old_level[::-1], tem[tt, ::-1, yy])   ;  new_t[tt, :, yy] = new_t[tt, ::-1, yy]

    # calculate meridional temperature gradient
    disy,disx,location  =  cal_xydistance(lat,lon)
    new_t_y  =  np.gradient(new_t,location,axis=2)

    return new_t_y,new_v,new_w


def test():
    import xarray as xr

    # reference file
    f0 = xr.open_dataset(path0 + "0101.climate.nc")
    a  = list(f0.attrs)
    print(f0["H"].attrs.keys())
def main():
    import warnings
    import time
    start = time.time()
    warnings.filterwarnings("ignore")

    #cal_jan_jul_average()
    paint_jan_jul_tem_stream()
    end = time.time()
    print(end - start)


if __name__ == "__main__":
    main()