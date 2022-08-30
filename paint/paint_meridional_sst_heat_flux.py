'''
2022-8-26
This code plot meridional sea surface temperature added heat flux (latent heat flux)
based on composite file and time period is pentad average
'''
src_path  =  "/Users/sunweihao/data/composite/"

file0     =  "composite_OISST.nc"
file1     =  "composite_shlh_liuxl.nc"

def cal_zonal_avg():
    '''This function calculate zonal average for SST and latent flux'''
    import xarray as xr
    import numpy as np

    # set the zonal average
    lon_slice  =  slice(90,100)

    # read the file
    f0         =  xr.open_dataset(src_path + file0).sel(lon=lon_slice)
    f1         =  xr.open_dataset(src_path + file1).sel(lon=lon_slice)
    #print(f0.SST.data)

    # calculate zonal average
    sst        =  np.nanmean(f0.SST.data,  axis=2)
    slhf       =  np.nanmean(f1.SLHF.data, axis=2)
    #print(sst)

    # calculate composite pentad average
    '''
        Here I define the -2 -1 0 1 2 as the onset pentad
        '''
    date0 = 10  # correspond to d -22

    # base array
    avg_sst         =  np.zeros((6,720,))
    avg_slhf        =  np.zeros((6,181,))
    for pp in range(6):
        start_date = date0 + pp * 5
        end_date = date0 + (pp + 1) * 5

        avg_sst[pp]  = np.nanmean(sst[start_date:end_date], axis=0)
        avg_slhf[pp] = np.nanmean(slhf[start_date:end_date], axis=0)

    return avg_sst,avg_slhf

def paint_meridional_field():
    '''This function paint meridional for the sst and slhf'''
    import xarray as xr
    import numpy as np
    import matplotlib.pyplot as plt
    import cmasher as cmr

    import sys
    sys.path.append("/Users/sunweihao/mycode/module")
    from module_sun_new import generate_xlabel

    # get the vars value
    sst,slhf  =  cal_zonal_avg()

    # reference
    f0 = xr.open_dataset(src_path + file0)
    f1 = xr.open_dataset(src_path + file1)

    # set figure
    fig = plt.figure(figsize=(34, 15))
    spec1 = fig.add_gridspec(nrows=2, ncols=3)

    # set pentad label
    pentads = ["P-4", "P-3", "P-2", "P-1", "P0", "P+1"]

    j = 0

    #  ---------- start paint ------------------
    for col in range(3):
        for row in range(2):
            print(sst[j])
            ax  =  fig.add_subplot(spec1[row,col])

            # set tick and ticklabel
            ax.set_xticks(np.linspace(-10, 30, 9, dtype=int))
            ax.set_yticks(np.linspace(28, 31, 7))
            ax.set_xticklabels(generate_xlabel(np.linspace(-10, 30, 9, dtype=int)))
            ax.tick_params(axis='both', labelsize=22.5)

            # set range
            ax.set_xlim((-10, 30))
            ax.set_ylim((28,31))

            # plot
            ax.plot(f0.lat.data,sst[j],color='red',linewidth=4)

            # second var
            ax2  =  ax.twinx()
            ax2.tick_params(axis='both', labelsize=22.5)

            ax2.plot(f1.lat.data,(slhf[j] * -1)/24/3600,color='blue',linewidth=3.5,linestyle = '--')

            # title
            ax.set_title(pentads[j],loc='left',fontsize=25)

            j += 1


    plt.savefig('/Users/sunweihao/paint/circulation_based_on_composite_result/meridional_sst_slhf_90to100_check.pdf', dpi=400)
    plt.show()

def main():
    paint_meridional_field()

if __name__  ==  "__main__":
    main()
