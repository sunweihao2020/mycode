'''
2022-8-16
This code paint meridional SST and diabatic heating flux, including sensible and latent heating
'''

def data_process():
    import xarray as xr
    # ------- set range -----------
    lon_slice  =  slice(90,100)

    # ----------------------- read data -------------------------------------
    src_path1  =  "/Users/sunweihao/data/composite/"

    src_file1  =  "composite_OISST_trans2.nc"
    src_file2  =  "composite_shlh_liuxl.nc"

    f1         =  xr.open_dataset(src_path1 + src_file1).sel(lon = lon_slice)
    f2         =  xr.open_dataset(src_path1 + src_file2).sel(lon = lon_slice)
    #-------------------------------------------------------------------------

    # ------------------------ cal zonal average ----------------------------
    import numpy as np
    avg_sst       =  np.nanmean(f1["sst"].data,axis=2)
    avg_sensible  =  np.nanmean(f2["SSHF"].data,axis=2)
    avg_latent    =  np.nanmean(f2["SLHF"].data,axis=2)

    return avg_sst,avg_sensible,avg_latent

def generate_xlabel(array):
    '''This code generate labels for x axis'''
    labels = []
    for i in array:
        if i < 0:
            labels.append(str(abs(i)) + "S")
        elif i > 0:
            labels.append(str(i) + "N")
        else:
            labels.append("EQ")
    return labels


def add_text(ax, string, props=dict(boxstyle='square', edgecolor='white', facecolor='white', alpha=1),
             location=(0.05, 0.9), fontsize=15):
    ax.text(location[0], location[1], string, transform=ax.transAxes, bbox=props, fontsize=fontsize)

def pic_paint(sst,sensible,latent):
    '''This function paint meridional variables'''
    import matplotlib.pyplot as plt
    import numpy as np
    import xarray as xr

    # read axis message
    src_path1 = "/Users/sunweihao/data/composite/"
    src_file1 = "composite_OISST_trans2.nc"
    src_file2 =  "composite_shlh_liuxl.nc"

    f0        = xr.open_dataset(src_path1+src_file1)
    f1        = xr.open_dataset(src_path1+src_file2)

    print(f1)

    # set figure
    fig1 = plt.figure(figsize=(38.5, 26))
    spec1 = fig1.add_gridspec(nrows=3, ncols=3)

    # set the date to paint
    dates  =  [0,10,20,25,27,29,30,32,34]

    j = 0

    # ---------- paint ------------------
    for col in range(3):
        for row in range(3):
            ax = fig1.add_subplot(spec1[row, col])

            # first y axis: SST
            # set axis ticks and label
            ax.set_xticks(np.linspace(-10, 30, 9, dtype=int))
            ax.set_xticklabels(generate_xlabel(np.linspace(-10, 30, 9, dtype=int)))

            ax.set_yticks(np.linspace(27, 31, 9))
            ax.tick_params(axis='both', labelsize=22.5)

            # plot zonal mean SST
            ax.plot(f0.lat.data,sst[dates[j]],color='red',linewidth=3)

            # set range
            ax.set_xlim((-10, 25))
            ax.set_ylim((27.5,31))

            # set axis label
            ax.set_xlabel("Latitude", fontsize=18)
            ax.set_ylabel("SST (90-100E average)", fontsize=18)

            # add new axis to paint latent heat flux
            ax2  =  ax.twinx()

            # set second axis label
            ax2.set_ylabel("Latent heat flux", fontsize=18)

            # plot latent heat flux
            ax2.plot(f1.lat.data,latent[dates[j]]*-1/24/60/60,color='blue',linewidth=3)

            # add date
            add_text(ax=ax, string="D" + str(dates[j] - 30), location=(0.05, 0.91), fontsize=30)

            j += 1

    plt.savefig('/Users/sunweihao/paint/circulation_based_on_composite_result/composite_meridional_sst_zonal90to100.pdf',dpi=400)
    plt.show()


def main():
    sst,sensible,latent  =  data_process()
    pic_paint(sst,sensible,latent)

if __name__ == "__main__":
    main()