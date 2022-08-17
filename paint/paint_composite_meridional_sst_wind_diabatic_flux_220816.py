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

def pic_paint(sst,sensible,latent):
    '''This function paint meridional variables'''
    import matplotlib.pyplot as plt
    import numpy as np

    # set figure
    fig1 = plt.figure(figsize=(32, 26))
    spec1 = fig1.add_gridspec(nrows=3, ncols=3)

    # set the date to paint
    dates  =  [0,10,20,25,27,28,29,30,32]

    j = 0

    # ---------- paint ------------------
    for col in range(3):
        for row in range(3):
            ax = fig1.add_subplot(spec1[row, col])

            # set axis ticks and label
            ax.set_xticks(np.linspace(-10, 30, 9, dtype=int))
            ax.set_yticks(np.linspace(1000, 100, 10))
            ax.set_xticklabels(generate_xlabel(np.linspace(-10, 30, 9, dtype=int)))
            ax.tick_params(axis='both', labelsize=22.5)

            # plot streamfunction
            im = ax.contourf(file0.lat.data, file0.lev.data, file0.meridional_streamfunction.data[start] / 1e11,
                             levels=np.linspace(-3, 3, 13), cmap=newcmp, extend='both')

            # set range
            ax.set_xlim((-10, 30))

            # set axis label
            ax.set_xlabel("Latitude", fontsize=18)
            ax.set_ylabel("MPSI (90-100E average)", fontsize=18)

            # add date
            add_text(ax=ax, string="D" + str(start - 30), location=(0.05, 0.91), fontsize=30)

            # invert y axis
            ax.invert_yaxis()

            # fill nan value
            plt.gca().set_facecolor("black")

            start += 1


def main():
    sst,sensible,latent  =  data_process()

if __name__ == "__main__":
    main()