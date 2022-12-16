'''
2022-11-17
This code calculate the average of the ensemble experiments
The experiment is AGCM using coupled CGCM output SST
'''
import os
import sys
import numpy as np

path0  =  '/home/sun/model_output/f2000_ensemble/f2000_ensemble_after_spinup/'
pnew   =  np.array([1000, 975, 950, 925, 900, 875, 850, 825, 800, 775, 750, 700, 650, 600, 550, 500, 450, 400, 350, 300, 250, 225, 200, 175, 150, 125, 100, 70, 50])


def mask_nan(ps,var,level):
    import numpy as np
    # dimension for the variable
    dim1   =  var.shape[1]
    dim2   =  var.shape[2]
    dim3   =  var.shape[3]

    var_mask  =  var.copy()
    for latt in range(dim2):
        for lonn in range(dim3):
            ps0  =  ps[0,latt,lonn] / 100

            for levv in range(dim1):
                if level[levv] > ps0:
                    var_mask[0,levv,latt,lonn] = np.nan
                else:
                    continue
    
    return var_mask[0]

def cal_ensemble_avg_2d(var_name,start_num=1,end_num=20):
    '''start and end number indicate the ensemble range'''
    import numpy as np
    import xarray as xr

    base_array  =  np.zeros((365,192,288))
    for i in range(start_num,end_num + 1): 
        # ensemble exps loop
        path1  =  path0 + 'f2000_ensemble_official_' + str(i) + '/atm/hist/'

        # get the file list
        list1    =  os.listdir(path1)
        list_h0  =  []
        for ffff in list1:
            if '.cam.h0.' in ffff:
                list_h0.append(ffff)
        list_h0.sort()

        if len(list_h0)  >  370:
            print('Error, the length of the h0 file is {}'.format(len(list_h0)))
            print(list_h0)
            quit()
        
        for j in range(365):
            # every day loop
            print('Now it is deal with var {},ensemble number is {}, day is {}'.format(var_name,i,j))
            f1  =  xr.open_dataset(path1 + list_h0[j])

            base_array[j] += f1[var_name].data[0] / (end_num - start_num + 1)
    
    return base_array

def cal_ensemble_avg_3d(var_name,start_num=1,end_num=20):
    '''start and end number indicate the ensemble range'''
    import numpy as np
    import xarray as xr
    import Ngl

    base_array  =  np.zeros((365,29,192,288))
    pnew      =  np.array([1000, 975, 950, 925, 900, 875, 850, 825, 800, 775, 750, 700, 650, 600, 550, 500, 450, 400, 350, 300, 250, 225, 200, 175, 150, 125, 100, 70, 50])
    for i in range(start_num,end_num + 1): 
        # ensemble exps loop
        path1  =  path0 + 'f2000_ensemble_official_' + str(i) + '/atm/hist/'

        # get the file list
        list1    =  os.listdir(path1)
        list_h0  =  []
        for ffff in list1:
            if '.cam.h0.' in ffff:
                list_h0.append(ffff)
        list_h0.sort()
        print(list_h0)
        if len(list_h0)  >  370:
            print('Error, the length of the h0 file is {}'.format(len(list_h0)))
            print(list_h0)
            quit()
        
        for j in range(365):
            # every day loop
            print('Now it is deal with var {},ensemble number is {}, day is {}'.format(var_name,i,j))
            f1  =  xr.open_dataset(path1 + list_h0[j])

            # !! Notion !! Here I interpolate to the pnew and mask the nan value
            base_array[j] += mask_nan(ps = f1.PS.data, var = np.float32(Ngl.vinth2p(f1[var_name].data,f1.hyam.data,f1.hybm.data,pnew,f1.PS.data,1,f1.P0.data/100,1,True)), level = pnew) / (end_num - start_num + 1)

    return base_array

        


def deal_with_output():
    '''The format of the result I'd like be similar to:
    single variable per file
    whole year time length per file
    '''
    import xarray as xr
    import numpy as np

    # reference file
    f0 = xr.open_dataset('/home/sun/model_output/f2000_ensemble/f2000_ensemble_1/atm/hist/f2000_ensemble_1.cam.h0.0001-06-17-00000.nc')

    # get vars name
    vars = list(f0.keys())
    #print(vars[-11:])    bottom eleven to the end is the variables I set

    # --------------------- deal with data --------------------------
    variable = vars[-11:]

    for vvvv in variable:
        # 1. get the dimension of the variable
        dim0  =  len(f0[vvvv].data.shape)
        #print(dim0)   result indludes 3 or 4
        if dim0 == 3:
            ncfile  =  xr.Dataset(
                            {
                                vvvv: (["time", "lat", "lon"], cal_ensemble_avg_2d(vvvv)),
                            },
                            coords={
                                "lon": (["lon"], f0.lon.data),
                                "lat": (["lat"], f0.lat.data),
                                "time": (["time"], np.linspace(1,365,365)),
                                    },
                                )
            ncfile["lon"].attrs  =  f0["lon"].attrs
            ncfile["lat"].attrs  =  f0["lat"].attrs
            ncfile["time"].attrs =  f0["time"].attrs


            ncfile.to_netcdf("/home/sun/data/model_data/f2000_ensemble/"+vvvv+'_climate2.nc')
        
        if dim0 == 4:
            ncfile  =  xr.Dataset(
                            {
                                vvvv: (["time", "lev", "lat", "lon"], cal_ensemble_avg_3d(vvvv)),
                            },
                            coords={
                                "lon": (["lon"], f0.lon.data),
                                "lat": (["lat"], f0.lat.data),
                                "lev": (["lev"], pnew),
                                "time": (["time"], np.linspace(1,365,365)),
                                    },
                                )
            ncfile["lon"].attrs  =  f0["lon"].attrs
            ncfile["lat"].attrs  =  f0["lat"].attrs
            

            ncfile.to_netcdf("/home/sun/data/model_data/f2000_ensemble/"+vvvv+'_climate2.nc')


def main():
    deal_with_output()

if __name__ == '__main__':
    main()
