'''
2022-10-4
This code paint January and July meridional temperature max line in the BOB region
To depict the characteristic of the Hadley cell

data is from MERRA-2
'''
path0  =  "/home/sun/data/merra2_climate_vars_multi/monthly/"

def paint_jan_jul_tem_stream():
    '''This function paint Jan and Jul temperature add circulation'''
    import numpy as np
    import xarray as xr

    import cmasher as cmr  # third part colormap
    import matplotlib.pyplot as plt

    import plotly.figure_factory as ff

    import sys
    module_path = "/home/sun/mycode/module"
    sys.path.append(module_path)
    from module_sun_new import generate_xlabel

    # set range
    lon_slice  =  slice(90,100)

    f0   =  xr.open_dataset(path0 + "merra2_climate_monthly_vars.nc").sel(lon=lon_slice)

    # calculate zonal average
    tem  =  np.nanmean(f0.T.data,axis=3)
    w    =  np.nanmean(f0.OMEGA.data,axis=3)
    v    =  np.nanmean(f0.V.data,axis=3)

    # set figure and axs
    fig  =  plt.figure(figsize=(12,8))
    ax   =  fig.subplots()

    # deal with data for paint
    tem_y,v,w  =  deal_data_for_paint(tem=tem,w=w,v=v,old_level=f0.lev.data,lat=f0.lat.data,lon=f0.lon.data)
    w *= -500  # scale the w
    new_level  =  np.linspace(1000,100,37)

    j    =  0

    # set tick and tick label
    xtick  =  np.linspace(-10,40,6,dtype=int)
    ytick  =  np.linspace(1000,200,5,dtype=int)

    xtick_label  =  generate_xlabel(xtick)

    ax.set_xticks(xtick)
    ax.set_yticks(ytick)
    ax.set_xticklabels(xtick_label)

    # set axis tick attribute
    ax.tick_params(axis='both', labelsize = 22.5)

    # set axis limit
    ax.set_xlim((-10,40))

    # plot temperature gradient contourf
    month       =  [0,3,6]
    im0  =  ax.contour(f0.lat.data, new_level, tem_y[month[j]]*1e5,[0],colors='blue',linestyles='--',linewidths=3) ; j += 1
    im1  =  ax.contour(f0.lat.data, new_level, tem_y[month[j]]*1e5,[0],colors='black',linestyles='--',linewidths=3) ; j += 1
    im2  =  ax.contour(f0.lat.data, new_level, tem_y[month[j]]*1e5,[0],colors='red',linestyles='--',linewidths=3) ; j += 1

    ax.invert_yaxis()
    plt.savefig("/home/sun/paint/lunwen/version4.0/Jan_and_Jul_temperature_max_line_MERRA2.pdf",dpi=500)
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