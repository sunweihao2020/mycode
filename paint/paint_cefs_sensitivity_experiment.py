'''
2022-10-27
This code paint compare between control experiment and sensitivity experiments
'''

path0  =  '/home/sun/data/model_data/daily_cross_equator_flow/'
fname  =  'yearly_cycle_merra_b1850_CEFs_11pointsmooth.nc'

def paint_cefs_inch():
    import xarray as xr
    import numpy as np
    import matplotlib.pyplot as plt

    f0  =  xr.open_dataset(path0 + fname)

    fig  =  plt.figure(figsize=(20,30))
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
    ax1.plot(f0['inch_cefs'].data[0],color='blue',linestyle='--',linewidth=2.5,label='Somali Inch')
    ax1.plot(f0['control_cefs'].data[0],color='red',linewidth=2.5,label='Somali Control')

    #plot zero line
    ax1.plot([0,365],[0,0],linestyle='--',linewidth=2)

    # add legend
    ax1.legend(fontsize=25,loc=2)

    '''BOB CEF'''
    ax1 = fig.add_subplot(spec[1, 0])

    # set axis tick and label
    ax1.set_xticks(np.arange(0, 360, 25))
    ax1.set_yticks(np.linspace(-5, 15, 9))
    ax1.tick_params(axis='both', labelsize=22)

    # set tick range
    ax1.set_ylim((-7, 13))
    ax1.set_xlim((0, 365))

    # plot
    ax1.plot(f0['inch_cefs'].data[1], color='blue', linestyle='--', linewidth=2.5, label='BOB Inch')
    ax1.plot(f0['control_cefs'].data[1], color='red', linewidth=2.5, label='BOB Control')

    # plot zero line
    ax1.plot([0, 365], [0, 0], linestyle='--', linewidth=2)

    # add legend
    ax1.legend(fontsize=25,loc=2)

    '''CS CEF'''
    ax1 = fig.add_subplot(spec[2, 0])

    # set axis tick and label
    ax1.set_xticks(np.arange(0, 360, 25))
    ax1.set_yticks(np.linspace(-5, 15, 9))
    ax1.tick_params(axis='both', labelsize=22)

    # set tick range
    ax1.set_ylim((-7, 13))
    ax1.set_xlim((0, 365))

    # plot
    ax1.plot(f0['inch_cefs'].data[2], color='blue', linestyle='--', linewidth=2.5, label='SCS Inch')
    ax1.plot(f0['control_cefs'].data[2], color='red', linewidth=2.5, label='SCS Control')

    # plot zero line
    ax1.plot([0, 365], [0, 0], linestyle='--', linewidth=2)

    # add legend
    ax1.legend(fontsize=25,loc=2)

    '''CS CEF'''
    ax1 = fig.add_subplot(spec[3, 0])

    # set axis tick and label
    ax1.set_xticks(np.arange(0, 360, 25))
    ax1.set_yticks(np.linspace(-5, 15, 9))
    ax1.tick_params(axis='both', labelsize=22)

    # set tick range
    ax1.set_ylim((-7, 13))
    ax1.set_xlim((0, 365))

    # plot
    ax1.plot(f0['inch_cefs'].data[3], color='blue', linestyle='--', linewidth=2.5, label='CS Inch')
    ax1.plot(f0['control_cefs'].data[3], color='red', linewidth=2.5, label='CS Control')

    # plot zero line
    ax1.plot([0, 365], [0, 0], linestyle='--', linewidth=2)

    # add legend
    ax1.legend(fontsize=25,loc=2)

    '''NG CEF'''
    ax1 = fig.add_subplot(spec[4, 0])

    # set axis tick and label
    ax1.set_xticks(np.arange(0, 360, 25))
    ax1.set_yticks(np.linspace(-5, 15, 9))
    ax1.tick_params(axis='both', labelsize=22)

    # set tick range
    ax1.set_ylim((-7, 13))
    ax1.set_xlim((0, 365))

    # plot
    ax1.plot(f0['inch_cefs'].data[4], color='blue', linestyle='--', linewidth=2.5, label='GN Inch')
    ax1.plot(f0['control_cefs'].data[4], color='red', linewidth=2.5, label='GN Control')

    # plot zero line
    ax1.plot([0, 365], [0, 0], linestyle='--', linewidth=2)

    # add legend
    ax1.legend(fontsize=25,loc=2)

    plt.savefig('/home/sun/paint/b1850_exp/assessment/CESM_control_inch_CEF.pdf')

def paint_cefs_indian():
    import xarray as xr
    import numpy as np
    import matplotlib.pyplot as plt

    f0  =  xr.open_dataset(path0 + fname)

    fig  =  plt.figure(figsize=(20,30))
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
    ax1.plot(f0['indian_cefs'].data[0],color='blue',linestyle='--',linewidth=2.5,label='Somali Indian')
    ax1.plot(f0['control_cefs'].data[0],color='red',linewidth=2.5,label='Somali Control')

    #plot zero line
    ax1.plot([0,365],[0,0],linestyle='--',linewidth=2)

    # add legend
    ax1.legend(fontsize=25,loc=2)

    '''BOB CEF'''
    ax1 = fig.add_subplot(spec[1, 0])

    # set axis tick and label
    ax1.set_xticks(np.arange(0, 360, 25))
    ax1.set_yticks(np.linspace(-5, 15, 9))
    ax1.tick_params(axis='both', labelsize=22)

    # set tick range
    ax1.set_ylim((-7, 13))
    ax1.set_xlim((0, 365))

    # plot
    ax1.plot(f0['indian_cefs'].data[1], color='blue', linestyle='--', linewidth=2.5, label='BOB Indian')
    ax1.plot(f0['control_cefs'].data[1], color='red', linewidth=2.5, label='BOB Control')

    # plot zero line
    ax1.plot([0, 365], [0, 0], linestyle='--', linewidth=2)

    # add legend
    ax1.legend(fontsize=25,loc=2)

    '''CS CEF'''
    ax1 = fig.add_subplot(spec[2, 0])

    # set axis tick and label
    ax1.set_xticks(np.arange(0, 360, 25))
    ax1.set_yticks(np.linspace(-5, 15, 9))
    ax1.tick_params(axis='both', labelsize=22)

    # set tick range
    ax1.set_ylim((-7, 13))
    ax1.set_xlim((0, 365))

    # plot
    ax1.plot(f0['indian_cefs'].data[2], color='blue', linestyle='--', linewidth=2.5, label='SCS Indian')
    ax1.plot(f0['control_cefs'].data[2], color='red', linewidth=2.5, label='SCS Control')

    # plot zero line
    ax1.plot([0, 365], [0, 0], linestyle='--', linewidth=2)

    # add legend
    ax1.legend(fontsize=25,loc=2)

    '''CS CEF'''
    ax1 = fig.add_subplot(spec[3, 0])

    # set axis tick and label
    ax1.set_xticks(np.arange(0, 360, 25))
    ax1.set_yticks(np.linspace(-5, 15, 9))
    ax1.tick_params(axis='both', labelsize=22)

    # set tick range
    ax1.set_ylim((-7, 13))
    ax1.set_xlim((0, 365))

    # plot
    ax1.plot(f0['indian_cefs'].data[3], color='blue', linestyle='--', linewidth=2.5, label='CS Indian')
    ax1.plot(f0['control_cefs'].data[3], color='red', linewidth=2.5, label='CS Control')

    # plot zero line
    ax1.plot([0, 365], [0, 0], linestyle='--', linewidth=2)

    # add legend
    ax1.legend(fontsize=25,loc=2)

    '''NG CEF'''
    ax1 = fig.add_subplot(spec[4, 0])

    # set axis tick and label
    ax1.set_xticks(np.arange(0, 360, 25))
    ax1.set_yticks(np.linspace(-5, 15, 9))
    ax1.tick_params(axis='both', labelsize=22)

    # set tick range
    ax1.set_ylim((-7, 13))
    ax1.set_xlim((0, 365))

    # plot
    ax1.plot(f0['indian_cefs'].data[4], color='blue', linestyle='--', linewidth=2.5, label='GN Indian')
    ax1.plot(f0['control_cefs'].data[4], color='red', linewidth=2.5, label='GN Control')

    # plot zero line
    ax1.plot([0, 365], [0, 0], linestyle='--', linewidth=2)

    # add legend
    ax1.legend(fontsize=25,loc=2)

    plt.savefig('/home/sun/paint/b1850_exp/assessment/CESM_control_indian_CEF.pdf')

def paint_cefs_maritime():
    import xarray as xr
    import numpy as np
    import matplotlib.pyplot as plt

    f0  =  xr.open_dataset(path0 + fname)

    fig  =  plt.figure(figsize=(20,30))
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
    ax1.plot(f0['maritime_cefs'].data[0],color='blue',linestyle='--',linewidth=2.5,label='Somali Maritime')
    ax1.plot(f0['control_cefs'].data[0],color='red',linewidth=2.5,label='Somali Control')

    #plot zero line
    ax1.plot([0,365],[0,0],linestyle='--',linewidth=2)

    # add legend
    ax1.legend(fontsize=25,loc=2)

    '''BOB CEF'''
    ax1 = fig.add_subplot(spec[1, 0])

    # set axis tick and label
    ax1.set_xticks(np.arange(0, 360, 25))
    ax1.set_yticks(np.linspace(-5, 15, 9))
    ax1.tick_params(axis='both', labelsize=22)

    # set tick range
    ax1.set_ylim((-7, 13))
    ax1.set_xlim((0, 365))

    # plot
    ax1.plot(f0['maritime_cefs'].data[1], color='blue', linestyle='--', linewidth=2.5, label='BOB Maritime')
    ax1.plot(f0['control_cefs'].data[1], color='red', linewidth=2.5, label='BOB Control')

    # plot zero line
    ax1.plot([0, 365], [0, 0], linestyle='--', linewidth=2)

    # add legend
    ax1.legend(fontsize=25,loc=2)

    '''CS CEF'''
    ax1 = fig.add_subplot(spec[2, 0])

    # set axis tick and label
    ax1.set_xticks(np.arange(0, 360, 25))
    ax1.set_yticks(np.linspace(-5, 15, 9))
    ax1.tick_params(axis='both', labelsize=22)

    # set tick range
    ax1.set_ylim((-7, 13))
    ax1.set_xlim((0, 365))

    # plot
    ax1.plot(f0['maritime_cefs'].data[2], color='blue', linestyle='--', linewidth=2.5, label='SCS Maritime')
    ax1.plot(f0['control_cefs'].data[2], color='red', linewidth=2.5, label='SCS Control')

    # plot zero line
    ax1.plot([0, 365], [0, 0], linestyle='--', linewidth=2)

    # add legend
    ax1.legend(fontsize=25,loc=2)

    '''CS CEF'''
    ax1 = fig.add_subplot(spec[3, 0])

    # set axis tick and label
    ax1.set_xticks(np.arange(0, 360, 25))
    ax1.set_yticks(np.linspace(-5, 15, 9))
    ax1.tick_params(axis='both', labelsize=22)

    # set tick range
    ax1.set_ylim((-7, 13))
    ax1.set_xlim((0, 365))

    # plot
    ax1.plot(f0['maritime_cefs'].data[3], color='blue', linestyle='--', linewidth=2.5, label='CS Maritime')
    ax1.plot(f0['control_cefs'].data[3], color='red', linewidth=2.5, label='CS Control')

    # plot zero line
    ax1.plot([0, 365], [0, 0], linestyle='--', linewidth=2)

    # add legend
    ax1.legend(fontsize=25,loc=2)

    '''NG CEF'''
    ax1 = fig.add_subplot(spec[4, 0])

    # set axis tick and label
    ax1.set_xticks(np.arange(0, 360, 25))
    ax1.set_yticks(np.linspace(-5, 15, 9))
    ax1.tick_params(axis='both', labelsize=22)

    # set tick range
    ax1.set_ylim((-7, 13))
    ax1.set_xlim((0, 365))

    # plot
    ax1.plot(f0['maritime_cefs'].data[4], color='blue', linestyle='--', linewidth=2.5, label='GN Maritime')
    ax1.plot(f0['control_cefs'].data[4], color='red', linewidth=2.5, label='GN Control')

    # plot zero line
    ax1.plot([0, 365], [0, 0], linestyle='--', linewidth=2)

    # add legend
    ax1.legend(fontsize=25,loc=2)

    plt.savefig('/home/sun/paint/b1850_exp/assessment/CESM_control_maritime_CEF.pdf')

def paint_cefs_indian_inch():
    import xarray as xr
    import numpy as np
    import matplotlib.pyplot as plt

    f0  =  xr.open_dataset(path0 + fname)

    fig  =  plt.figure(figsize=(20,30))
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
    ax1.plot(f0['inch_indian_cefs'].data[0],color='blue',linestyle='--',linewidth=2.5,label='Somali Inch_Indian')
    ax1.plot(f0['control_cefs'].data[0],color='red',linewidth=2.5,label='Somali Control')

    #plot zero line
    ax1.plot([0,365],[0,0],linestyle='--',linewidth=2)

    # add legend
    ax1.legend(fontsize=25,loc=2)

    '''BOB CEF'''
    ax1 = fig.add_subplot(spec[1, 0])

    # set axis tick and label
    ax1.set_xticks(np.arange(0, 360, 25))
    ax1.set_yticks(np.linspace(-5, 15, 9))
    ax1.tick_params(axis='both', labelsize=22)

    # set tick range
    ax1.set_ylim((-7, 13))
    ax1.set_xlim((0, 365))

    # plot
    ax1.plot(f0['inch_indian_cefs'].data[1], color='blue', linestyle='--', linewidth=2.5, label='BOB Inch_Indian')
    ax1.plot(f0['control_cefs'].data[1], color='red', linewidth=2.5, label='BOB Control')

    # plot zero line
    ax1.plot([0, 365], [0, 0], linestyle='--', linewidth=2)

    # add legend
    ax1.legend(fontsize=25,loc=2)

    '''CS CEF'''
    ax1 = fig.add_subplot(spec[2, 0])

    # set axis tick and label
    ax1.set_xticks(np.arange(0, 360, 25))
    ax1.set_yticks(np.linspace(-5, 15, 9))
    ax1.tick_params(axis='both', labelsize=22)

    # set tick range
    ax1.set_ylim((-7, 13))
    ax1.set_xlim((0, 365))

    # plot
    ax1.plot(f0['inch_indian_cefs'].data[2], color='blue', linestyle='--', linewidth=2.5, label='SCS Inch_Indian')
    ax1.plot(f0['control_cefs'].data[2], color='red', linewidth=2.5, label='SCS Control')

    # plot zero line
    ax1.plot([0, 365], [0, 0], linestyle='--', linewidth=2)

    # add legend
    ax1.legend(fontsize=25,loc=2)

    '''CS CEF'''
    ax1 = fig.add_subplot(spec[3, 0])

    # set axis tick and label
    ax1.set_xticks(np.arange(0, 360, 25))
    ax1.set_yticks(np.linspace(-5, 15, 9))
    ax1.tick_params(axis='both', labelsize=22)

    # set tick range
    ax1.set_ylim((-7, 13))
    ax1.set_xlim((0, 365))

    # plot
    ax1.plot(f0['inch_indian_cefs'].data[3], color='blue', linestyle='--', linewidth=2.5, label='CS Inch_Indian')
    ax1.plot(f0['control_cefs'].data[3], color='red', linewidth=2.5, label='CS Control')

    # plot zero line
    ax1.plot([0, 365], [0, 0], linestyle='--', linewidth=2)

    # add legend
    ax1.legend(fontsize=25,loc=2)

    '''NG CEF'''
    ax1 = fig.add_subplot(spec[4, 0])

    # set axis tick and label
    ax1.set_xticks(np.arange(0, 360, 25))
    ax1.set_yticks(np.linspace(-5, 15, 9))
    ax1.tick_params(axis='both', labelsize=22)

    # set tick range
    ax1.set_ylim((-7, 13))
    ax1.set_xlim((0, 365))

    # plot
    ax1.plot(f0['inch_indian_cefs'].data[4], color='blue', linestyle='--', linewidth=2.5, label='GN Inch_Indian')
    ax1.plot(f0['control_cefs'].data[4], color='red', linewidth=2.5, label='GN Control')

    # plot zero line
    ax1.plot([0, 365], [0, 0], linestyle='--', linewidth=2)

    # add legend
    ax1.legend(fontsize=25,loc=2)

    plt.savefig('/home/sun/paint/b1850_exp/assessment/CESM_control_inch_indian_CEF.pdf')


def paint_cefs_all():
    import xarray as xr
    import numpy as np
    import matplotlib.pyplot as plt

    f0  =  xr.open_dataset(path0 + fname)

    fig  =  plt.figure(figsize=(20,30))
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
    ax1.plot(f0['maritime_cefs'].data[0], color='blue', linestyle='--', linewidth=2.5, label='Somali Maritime')
    ax1.plot(f0['control_cefs'].data[0], color='red', linewidth=2.5, label='Somali Control')
    ax1.plot(f0['inch_cefs'].data[0], color='black', linestyle='--', linewidth=2.5, label='Somali Inch')
    ax1.plot(f0['inch_indian_cefs'].data[0], color='green', linestyle='--', linewidth=2.5, label='Somali Inch_Indian')
    ax1.plot(f0['indian_cefs'].data[0], color='brown', linestyle='--', linewidth=2.5, label='Somali Indian')

    #plot zero line
    ax1.plot([0,365],[0,0],linestyle='--',linewidth=2)

    # add legend
    ax1.legend(fontsize=12,loc=2)

    '''BOB CEF'''
    ax1 = fig.add_subplot(spec[1, 0])

    # set axis tick and label
    ax1.set_xticks(np.arange(0, 360, 25))
    ax1.set_yticks(np.linspace(-5, 15, 9))
    ax1.tick_params(axis='both', labelsize=22)

    # set tick range
    ax1.set_ylim((-7, 13))
    ax1.set_xlim((0, 365))

    # plot
    ax1.plot(f0['maritime_cefs'].data[1], color='blue', linestyle='--', linewidth=2.5, label='BOB Maritime')
    ax1.plot(f0['control_cefs'].data[1], color='red', linewidth=2.5, label='BOB Control')
    ax1.plot(f0['inch_cefs'].data[1], color='black', linestyle='--', linewidth=2.5, label='BOB Inch')
    ax1.plot(f0['inch_indian_cefs'].data[1], color='green', linestyle='--', linewidth=2.5, label='BOB Inch_Indian')
    ax1.plot(f0['indian_cefs'].data[1], color='brown', linestyle='--', linewidth=2.5, label='BOB Indian')

    # plot zero line
    ax1.plot([0, 365], [0, 0], linestyle='--', linewidth=2)

    # add legend
    ax1.legend(fontsize=12,loc=2)

    '''SCS CEF'''
    ax1 = fig.add_subplot(spec[2, 0])

    # set axis tick and label
    ax1.set_xticks(np.arange(0, 360, 25))
    ax1.set_yticks(np.linspace(-5, 15, 9))
    ax1.tick_params(axis='both', labelsize=22)

    # set tick range
    ax1.set_ylim((-7, 13))
    ax1.set_xlim((0, 365))

    # plot
    ax1.plot(f0['maritime_cefs'].data[2], color='blue', linestyle='--', linewidth=2.5, label='SCS Maritime')
    ax1.plot(f0['control_cefs'].data[2], color='red', linewidth=2.5, label='SCS Control')
    ax1.plot(f0['inch_cefs'].data[2], color='black', linestyle='--', linewidth=2.5, label='SCS Inch')
    ax1.plot(f0['inch_indian_cefs'].data[2], color='green', linestyle='--', linewidth=2.5, label='SCS Inch_Indian')
    ax1.plot(f0['indian_cefs'].data[2], color='brown', linestyle='--', linewidth=2.5, label='SCS Indian')

    # plot zero line
    ax1.plot([0, 365], [0, 0], linestyle='--', linewidth=2)

    # add legend
    ax1.legend(fontsize=12,loc=2)

    '''CS CEF'''
    ax1 = fig.add_subplot(spec[3, 0])

    # set axis tick and label
    ax1.set_xticks(np.arange(0, 360, 25))
    ax1.set_yticks(np.linspace(-5, 15, 9))
    ax1.tick_params(axis='both', labelsize=22)

    # set tick range
    ax1.set_ylim((-7, 13))
    ax1.set_xlim((0, 365))

    # plot
    ax1.plot(f0['maritime_cefs'].data[3], color='blue', linestyle='--', linewidth=2.5, label='CS Maritime')
    ax1.plot(f0['control_cefs'].data[3], color='red', linewidth=2.5, label='CS Control')
    ax1.plot(f0['inch_cefs'].data[3], color='black', linestyle='--', linewidth=2.5, label='CS Inch')
    ax1.plot(f0['inch_indian_cefs'].data[3], color='green', linestyle='--', linewidth=2.5, label='CS Inch_Indian')
    ax1.plot(f0['indian_cefs'].data[3], color='brown', linestyle='--', linewidth=2.5, label='CS Indian')

    # plot zero line
    ax1.plot([0, 365], [0, 0], linestyle='--', linewidth=2)

    # add legend
    ax1.legend(fontsize=12,loc=2)

    '''NG CEF'''
    ax1 = fig.add_subplot(spec[4, 0])

    # set axis tick and label
    ax1.set_xticks(np.arange(0, 360, 25))
    ax1.set_yticks(np.linspace(-5, 15, 9))
    ax1.tick_params(axis='both', labelsize=22)

    # set tick range
    ax1.set_ylim((-7, 13))
    ax1.set_xlim((0, 365))

    # plot
    ax1.plot(f0['maritime_cefs'].data[4], color='blue', linestyle='--', linewidth=2.5, label='NG Maritime')
    ax1.plot(f0['control_cefs'].data[4], color='red', linewidth=2.5, label='NG Control')
    ax1.plot(f0['inch_cefs'].data[4], color='black', linestyle='--', linewidth=2.5, label='NG Inch')
    ax1.plot(f0['inch_indian_cefs'].data[4], color='green', linestyle='--', linewidth=2.5, label='NG Inch_Indian')
    ax1.plot(f0['indian_cefs'].data[4], color='brown', linestyle='--', linewidth=2.5, label='NG Indian')

    # plot zero line
    ax1.plot([0, 365], [0, 0], linestyle='--', linewidth=2)

    # add legend
    ax1.legend(fontsize=12,loc=2)

    plt.savefig('/home/sun/paint/b1850_exp/assessment/CESM_control_sensitivity_CEF.pdf')

def main():
    paint_cefs_indian_inch()
    paint_cefs_maritime()
    paint_cefs_indian()
    paint_cefs_inch()
    paint_cefs_all()

if __name__ == '__main__':
    main()