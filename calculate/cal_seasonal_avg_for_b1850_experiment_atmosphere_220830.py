'''
2022-8-30
This code calculate season average for the b1850 experiment
season is define as MAM JJA SON DJF
The input has already been calculate monthly average 
'''

src_path  =  "/Users/sunweihao/data/model_data/climate/"

exp_file_name  =  ["b1850_control_atmospheric_monthly_average.nc","b1850_global1m_atmospheric_monthly_average.nc","b1850_maritime_atmospheric_monthly_average.nc"]

def cal_season_avg(filename):
    '''This function use monthly avg to calculate season average'''
    import numpy as np
    import xarray as xr

    f0  =  xr.open_dataset(src_path + filename)

    # get the variables list
    vars = list(f0.keys())

    # define the season location
    season  =  [[11,0,1],[2,3,4],[5,6,7],[8,9,10]]
    # calculate season avg for every variables
    for vvvv in vars:
        dimension  =  len(f0[vvvv].shape)
        if dimension  ==  3:
            base =  np.zeros((4,f0[vvvv].shape[1],f0[vvvv].shape[2]))
        elif dimension == 4:
            base = np.zeros((4,f0[vvvv].shape[1],f0[vvvv].shape[2],f0[vvvv].shape[3]))
        else:
            print("Error the dimension is "+str(dimension))

        for ssss in range(4):
            base[ssss]  =  

        print(test.shape)

def main():
    import warnings
    warnings.filterwarnings("ignore")  # close warning message
    cal_season_avg(exp_file_name[1])

if __name__ == "__main__":
    main()