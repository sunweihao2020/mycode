'''
2022-7-24
This script focus on meridional circulation and diabatic heating
include:
1. v-w circulation
2. temperature gradient
3. diabatic heating
'''
path  =  "/home/sun/data/composite/"


def cal_zonal_average(lon_slice,time_slice):
    '''
    Calculate zonal mean for input lon_slice
    '''
    # -------  import  --------------------- 
    import xarray as xr
    import numpy as np
    ##--------------------------------------

    #  ---------files-----------------------
    f0    =    xr.open_dataset(path + "composite3.nc").sel(lon=lon_slice).isel(time=time_slice)
    f1    =    xr.open_dataset(path + "composite-heating-merra.nc").sel(lon=lon_slice).isel(time=time_slice)

    # use variables: vwind omega T turbulence moist physics
    vwind     =    np.nanmean(f0.vwind,axis=3)
    omega     =    np.nanmean(f0.OMEGA,axis=3)

    tem_gradient       =    cal_gradient_meridional(f0.T.data)
    tem_gradient_avg   =    np.nanmean(tem_gradient,axis=3)

    latent    =    np.nanmean(f1.moist,axis=3)
    sensible  =    np.nanmean(f1.turbulence,axis=3)
    physics   =    np.nanmean(f1.physics,axis=3)

    return vwind,omega,tem_gradient_avg,latent,sensible,physics


def cal_gradient_meridional(vars):
    '''
    This function calculate meridional gradient. 
    support arrays: (time,level,lat,lon) and (time,lat,lon)

    process: 1. calculate zonal average  2. calculate meridional gradient
    '''
    # ---------- import -----------------------
    import sys
    sys.path.append("/home/sun/mycode/module/")
    from module_sun_new import cal_xydistance
    import xarray as xr
    import numpy as np
    from geopy.distance import distance
    ##-----------------------------------------

    # ----------------- get disx disy location ---------------------
    f0                   =    xr.open_dataset(path + "composite3.nc")
    disy,disx,location   =    cal_xydistance(f0.lat,f0.lon)

    # ------------------ calculate gradient ------------------------
    dimension  =  len(vars.shape)
    if dimension == 3:
        v_gradient  =  np.gradient(vars,location,axis=1)
    elif dimension == 4:
        v_gradient  =  np.gradient(vars,location,axis=2)

    return v_gradient

def generate_xlabel(array):
    '''This code generate labels for x axis'''
    labels = []
    for i in array:
        if i<0:
            labels.append(str(abs(i))+"S")
        elif i>0:
            labels.append(str(i)+"N")
        else:
            labels.append("EQ")
    return labels

def paint_meridional_circulation():
    '''This script paint meridional circulation and diabatic heating'''
    # -------------- import module ---------------------------------
    import numpy as np
    import matplotlib.pyplot as plt
    import sys
    import xarray as xr
    import plotly.figure_factory as ff
    sys.path.append("/home/sun/mycode_git/paint/")
    from paint_lunwen_version3_0_fig2a_tem_gradient_20220426 import add_text
    #import matplotlib
    #matplotlib.use('Agg')
    
    ## -------------------------------------------------------------

    # -------------- reference -------------------------------------
    f0        =  xr.open_dataset(path + "composite3.nc")

    # -------------- variables -------------------------------------
    var_list  =  cal_zonal_average(lon_slice=slice(90,100),time_slice=[0,10,20,25,27,29,30,32,34])

    v         =  var_list[0]
    w         =  var_list[1] * -1


    ## --------------  unify v and w  ------------------------------
    multiple  =  np.nanmean(abs(v))/np.nanmean(abs(w))
    w         =  w * 1000

    ## --------------   vertical interpolate  ----------------------
    ## fuck python stream plot, it need reverse and interpolate vertical axis
    old_level =  f0.level.data
    new_level =  np.linspace(1000,100,37)

    print(new_level)
    print(old_level)

    new_v     =  np.zeros((v.shape[0],37,v.shape[2]))
    new_w     =  new_v.copy()

    for tt in range(v.shape[0]):
        for yy in range(v.shape[2]):
            
            new_v[tt,:,yy]     =  np.interp(new_level[::-1],old_level[::-1],v[tt,::-1,yy]) 
            new_w[tt,:,yy]     =  np.interp(new_level[::-1],old_level[::-1],w[tt,::-1,yy]) 
            #print(new_w[tt,:,yy])
            
    # ------------      date    ----------------------------------
    dates  =  [-30,-20,-10,-5,-3,-1,0,2,4]


    # ------------     paint    ----------------------------------
    ## set figure
    fig1 = plt.figure(figsize=(32, 26))
    spec1 = fig1.add_gridspec(nrows=3, ncols=3)

    j = 0

    for col in range(3):
        for row in range(3):
            ax  =  fig1.add_subplot(spec1[row, col])

            # set axis ticks and label
            ax.set_xticks(np.linspace(-10, 40, 11, dtype=int))
            ax.set_yticks(np.linspace(1000, 100, 10))
            ax.set_xticklabels(generate_xlabel(np.linspace(-10, 40, 11, dtype=int)))
            ax.set_yticklabels(np.linspace(100,1000,10,dtype=int))
            ax.tick_params(axis='both', labelsize=22.5)

            # set axis limit
            ax.set_xlim((-10,30))

            # plot stream line
            ax.streamplot(f0.lat.data, new_level[::-1], new_v[j,::-1], new_w[j,::-1], color='k',linewidth=2.5,density=2,arrowsize=2.75, arrowstyle='->')
            #ax.invert_yaxis()
            #ax.contour(f0.lat, new_level, new_w[j])
           # ax.streamplot(f0.lat, new_level[::-1], new_v[j], new_w[j], color='k',linewidth=2.5,density=1.2,arrowsize=2.75, arrowstyle='->')

            # add date
            add_text(ax=ax, string="D" + str(dates[j]), location=(0.05, 0.91), fontsize=30)


            j += 1



    plt.savefig("/home/sun/paint/monthly_meri_vertical_tem_90to100E/circulation_vertical.pdf", dpi=350)

    plt.show()

    



def main():
    paint_meridional_circulation()

if __name__ == "__main__":
    main()

