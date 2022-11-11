'''
2022-10-26
This code plot year cycle of the CEF
'''
path0  =  '/home/sun/data/model_data/daily_cross_equator_flow/'
fname  =  'yearly_cycle_merra_b1850_CEFs_9pointsmooth.nc'

def paint_cefs1():
    import xarray as xr
    import numpy as np
    import matplotlib.pyplot as plt

    f0  =  xr.open_dataset(path0 + fname)

    fig  =  plt.figure(figsize=(24,30))
    spec =  fig.add_gridspec(nrows=5,ncols=1)

    '''Somali CEF'''
    ax1  =  fig.add_subplot(spec[0,0])

    # set axis tick and label
    ax1.set_xticks(np.arange(0,360,25))
    ax1.set_yticks(np.linspace(-5,15,9))
    ax1.tick_params(axis='both',labelsize=22)

    # set tick range
    ax1.set_ylim((-7,13))
    ax1.set_xlim((0,365))

    #plot
    ax1.plot(f0['merra_cefs'].data[0],color='black',linewidth=2.5,label='Somali Merra-2')
    ax1.plot(f0['control_cefs'].data[0],color='red',linewidth=2.5,label='Somali CESM2')

    #plot zero line
    ax1.plot([0,365],[0,0],linestyle='--',linewidth=2)

    # add legend
    ax1.legend(fontsize=25,loc=2)

    '''BOB CEF'''
    ax2 = fig.add_subplot(spec[1, 0])

    # set axis tick and label
    ax2.set_xticks(np.arange(0, 360, 25))
    ax2.set_yticks(np.linspace(-5, 15, 9))
    ax2.tick_params(axis='both', labelsize=22)

    # set tick range
    ax2.set_ylim((-7, 13))
    ax2.set_xlim((0, 365))

    # plot
    ax2.plot(f0['merra_cefs'].data[1], color='black', linewidth=2.5, label='BOB Merra-2')
    ax2.plot(f0['control_cefs'].data[1], color='red', linewidth=2.5, label='BOB CESM2')

    # plot zero line
    ax2.plot([0, 365], [0, 0], linestyle='--', linewidth=2)

    # add legend
    ax2.legend(fontsize=25,loc=2)

    '''CS CEF'''
    ax2 = fig.add_subplot(spec[2, 0])

    # set axis tick and label
    ax2.set_xticks(np.arange(0, 360, 25))
    ax2.set_yticks(np.linspace(-5, 15, 9))
    ax2.tick_params(axis='both', labelsize=22)

    # set tick range
    ax2.set_ylim((-7, 13))
    ax2.set_xlim((0, 365))

    # plot
    ax2.plot(f0['merra_cefs'].data[2], color='black', linewidth=2.5, label='SCS Merra-2')
    ax2.plot(f0['control_cefs'].data[2], color='red', linewidth=2.5, label='SCS CESM2')

    # plot zero line
    ax2.plot([0, 365], [0, 0], linestyle='--', linewidth=2)

    # add legend
    ax2.legend(fontsize=25,loc=2)

    '''SCS CEF'''
    ax2 = fig.add_subplot(spec[3, 0])

    # set axis tick and label
    ax2.set_xticks(np.arange(0, 360, 25))
    ax2.set_yticks(np.linspace(-5, 15, 9))
    ax2.tick_params(axis='both', labelsize=22)

    # set tick range
    ax2.set_ylim((-7, 13))
    ax2.set_xlim((0, 365))

    # plot
    ax2.plot(f0['merra_cefs'].data[3], color='black', linewidth=2.5, label='CS Merra-2')
    ax2.plot(f0['control_cefs'].data[3], color='red', linewidth=2.5, label='CS CESM2')

    # plot zero line
    ax2.plot([0, 365], [0, 0], linestyle='--', linewidth=2)

    # add legend
    ax2.legend(fontsize=25,loc=2)

    '''NG CEF'''
    ax2 = fig.add_subplot(spec[4, 0])

    # set axis tick and label
    ax2.set_xticks(np.arange(0, 360, 25))
    ax2.set_yticks(np.linspace(-5, 15, 9))
    ax2.tick_params(axis='both', labelsize=22)

    # set tick range
    ax2.set_ylim((-7, 13))
    ax2.set_xlim((0, 365))

    # plot
    ax2.plot(f0['merra_cefs'].data[4], color='black', linewidth=2.5, label='GN Merra-2')
    ax2.plot(f0['control_cefs'].data[4], color='red', linewidth=2.5, label='GN CESM2')

    # plot zero line
    ax2.plot([0, 365], [0, 0], linestyle='--', linewidth=2)

    # add legend
    ax2.legend(fontsize=25,loc=2)

    plt.savefig('/home/sun/paint/b1850_exp/assessment/CESM_MERRA2_CEF.pdf')

def main():
    paint_cefs1()

if __name__ == '__main__':
    main()