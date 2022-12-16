'''
2022-12-14
This code paint the time-series for the ensemble control experiment spinup
To see whether the model archive stable
'''
path0  =  '/home/sun/model_output/b1850_exp/b1850_con_ensemble_official_1_spinup_1/atm/hist/'
var_name  =  ['TS']

def cal_monthly_global_mean_average(f0,varname):
    '''This function calculate global-mean for the input file and varname'''
    import xarray as xr
    import numpy as np

    ff  =  xr.open_dataset(path0 + f0)

    avg_global  =  np.average(ff[varname].data)

    return avg_global
def paint_series(series):
    import matplotlib.pyplot as plt
    import numpy as np

    with plt.style.context('Solarize_Light2'):
        fig, ax = plt.subplots()
        plt.plot(np.linspace(1,120,120),series)

        plt.xlabel("Global-Mean TS",fontsize=20)
        plt.ylabel("Model year",fontsize=20)

        ax.set_xticks(np.linspace(1,120,12,dtype=int))

        plt.savefig('/home/sun/paint/b1850_exp/spinup/ensemble_con_ts_hybrid.pdf',dpi=400)


def main():
    '''1. get the 30-year time series for the variable name'''
    import os
    import numpy as np

    file_list  =  os.listdir(path0) ; file_list.sort()

    time_series  =  np.array([])
    for ffff in file_list:
        time_series  =  np.append(time_series,cal_monthly_global_mean_average(ffff,var_name[0]))

    #print(time_series)
    paint_series(time_series)
    

if __name__ == '__main__':
    main()