'''
2022-12-28
This script focus on meridional circulation and diabatic heating
include:
1. v-w circulation
2. temperature gradient

version6 add:
diabatic heating

select composite day for -6 0 +6
'''
import warnings
warnings.filterwarnings("ignore")  # close warning message
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
    import cmasher as cmr
    sys.path.append("/home/sun/mycode_git/paint/")
    from paint_lunwen_version3_0_fig2a_tem_gradient_20220426 import add_text
    #import matplotlib
    #matplotlib.use('Agg')
    
    ## -------------------------------------------------------------

    # -------------- reference -------------------------------------
    f0        =  xr.open_dataset(path + "composite3.nc")
    f1        =  xr.open_dataset(path + "composite-heating-merra.nc")

    # -------------- variables -------------------------------------
    var_list  =  cal_zonal_average(lon_slice=slice(90,100),time_slice=[24,30,36])

    # circulation variables
    v         =  var_list[0]
    w         =  var_list[1] * -1

    # temperature variables
    tem_gradient  =  var_list[2]

    # diabatic heating variables
    latent        =  var_list[3]
    sensible      =  var_list[4]


    ## --------------  unify v and w  ------------------------------
    multiple  =  np.nanmean(abs(v))/np.nanmean(abs(w))
    w         =  w * 500
    print(multiple)

    ## --------------   vertical interpolate  ----------------------
    ## fuck python stream plot, it need reverse and interpolate vertical axis
    new_level =  np.linspace(1000,100,37)

    new_v     =  np.zeros((v.shape[0],37,v.shape[2]))
    new_w     =  new_v.copy()

    new_t     =  new_v.copy()

    new_s     =  np.zeros((latent.shape[0],37,latent.shape[2]))
    new_l     =  new_s.copy()

    for tt in range(v.shape[0]):
        for yy in range(v.shape[2]):
            old_level =  f0.level.data
            new_v[tt,:,yy]     =  np.interp(new_level[::-1],old_level[::-1],v[tt,::-1,yy])  #Here I did not invert after interpolate
            new_w[tt,:,yy]     =  np.interp(new_level[::-1],old_level[::-1],w[tt,::-1,yy])  #But the result paint is not error

            new_t[tt,:,yy]     =  np.interp(new_level[::-1],old_level[::-1],tem_gradient[tt,::-1,yy]) ; new_t[tt,:,yy]  =  new_t[tt,::-1,yy]

    for tt in range(sensible.shape[0]):
        for yy in range(sensible.shape[2]):
            old_level =  f1.level.data  # Because this variables belongs to two files, the vertical corrdinate is not the same
            new_s[tt,:,yy]     =  np.interp(new_level[::-1],old_level[::-1],sensible[tt,::-1,yy])     ; new_s[tt,:,yy]  =  new_s[tt,::-1,yy]
            new_l[tt,:,yy]     =  np.interp(new_level[::-1],old_level[::-1],latent[tt,::-1,yy])       ; new_l[tt,:,yy]  =  new_l[tt,::-1,yy]

    print("Successful interpolate variables")
    # ------------      date    ----------------------------------
    dates  =  ['-6','0','+6']


    # ------------     paint    ----------------------------------
    ## set figure
    fig1 = plt.figure(figsize=(30, 8))
    spec1 = fig1.add_gridspec(nrows=1, ncols=3)

    ## set cmap
    #cmap = cmr.holly                  # CMasher
    cmap = cmr.prinsenvlag_r                 # CMasher
    #cmap = plt.get_cmap('cmr.rainforest')

    j = 0
    fig_num  =  ['(d)','(e)','(f)']

    for col in range(3):
        for row in range(1):
            ax  =  fig1.add_subplot(spec1[row, col])

            # set axis ticks and label
            ax.set_xticks(np.linspace(-10, 40, 6, dtype=int))
            ax.set_yticks(np.linspace(1000, 200, 5))

            ax.set_xticklabels(generate_xlabel(np.linspace(-10, 40, 6, dtype=int)))
            #ax.set_yticklabels(np.linspace(100,1000,10,dtype=int))
            ax.tick_params(axis='both', labelsize=22.5)

            # set axis limit
            ax.set_xlim((-10,40))

            # plot contourf picture
            ## temperature gradient
            im1 = ax.contourf(f0.lat.data, new_level, new_t[j]*1e5,levels=np.linspace(-2,2,9),extend='both',cmap=cmap)
            im2 = ax.contour(f0.lat.data, new_level, new_t[j]*1e5,levels=[0],colors='black',linewidths=4.5,linestyles='--')

            # plot stream line
            ax2  =  ax.twinx()
            ax2.streamplot(f0.lat.data, new_level[::-1], new_v[j,::-1], new_w[j,::-1], color='k',linewidth=2.,density=2.35,arrowsize=2.25, arrowstyle='->')
            ax2.set_yticklabels([])

            ## diabatic heating
            im3 = ax.contour(f1.lat.data, new_level, new_s[j],levels=[2, 4, 6, 8],colors='red',linewidths=2.5)
            ax.clabel(im3,fontsize=22)
#
            #im4 = ax.contour(f1.lat.data, new_level, new_l[j],levels=np.linspace(4,12,5),colors='blue',linewidths=3)
            #ax.clabel(im4,fontsize=30)
            ax.invert_yaxis()

            # set nan value black
            ax.set_facecolor("black")
   
            # add date
            ax.set_title("D" + dates[j],loc='right',fontsize=25)
            ax.set_title(fig_num[j],loc='left',fontsize=25)

            j += 1

    ## set colorbar
    #fig1.subplots_adjust(top=0.8) 
#
    #cbar_ax = fig1.add_axes([0.2, 0.05, 0.6, 0.03])  
    #cb      = fig1.colorbar(im1, cax=cbar_ax, shrink=0.5, pad=0.2, orientation='horizontal') 
#
    #cb.ax.tick_params(labelsize=25)


    plt_path  =  "/home/sun/paint/lunwen/version6.0/"
    plt.savefig(plt_path+"lunwen_version6.0_fig3_meridional_vertical_circulation.pdf", dpi=400)

    plt.show()

def main():
    paint_meridional_circulation()

if __name__ == "__main__":
    main()

