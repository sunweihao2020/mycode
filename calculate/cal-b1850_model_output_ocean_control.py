'''
2022-9-8
Due to the ocean data of model output whose coordination is unregular
In this code I want to change the coordination for the file
The longitude after transfer is from 0 - 360
'''
import os


src_path  =  '/home/sun/data/ocean_data/'
end_path  =  '/home/sun/segate/model_data/b1850_control/ocean/'
experiment_name  =  "b1850_control_"

ocn_one   =  'mom6.sfc'
ocn_two   =  'mom6.hm'

var_one   =  ['SSH', 'tos', 'sos', 'SSU', 'SSV', 'mlotst']  # SSU (time,yh,xq) SSV (time,yq,xh)
var_two   =  ['hfsso', 'rlntds', 'rsntds', 'hfds']          # coordinate all is (time,yh,xh)

file_all  =  os.listdir(src_path)

def transfer_lon(filename,varname):
    '''This function transfer the longitude for the input file'''
    import xarray as xr
    import numpy as np

    file0       =  xr.open_dataset(src_path + filename)
    #file0       =  xr.open_dataset('/Users/sunweihao/Downloads/' + filename)
    var         =  file0[varname].data

    var_new     =  var.copy()

    xh2         =  file0.xh.data  +  360

    critical_value  =  430  # 429 corresponds to 359

    # ocn_one file shape is (365,458,540)
    # ocn_two file shape is (1,458,540)
    dimension   =  var.shape
    for i in range(dimension[0]):
        for yy in range(dimension[1]):
            var_new[i,yy,:110]  =  var[i,yy,430:]
            var_new[i,yy,110:]  =  var[i,yy,:430]

    return var_new

def deal_control():
    '''In this function I deal with control exp ocean data'''
    import os
    import xarray as xr

    exp_name   =   ['b1850_control_o1_220703']

    namelist1  =  [] ; namelist2  =  []
    # first deal with ocn_one files
    for ffff in file_all:
        if (exp_name[0] in ffff) and ('cam' not in ffff) and (ocn_one in ffff):
            namelist1.append(ffff)
        elif (exp_name[0] in ffff) and ('cam' not in ffff) and (ocn_two in ffff):
            namelist2.append(ffff)
    namelist1.sort() ; namelist2.sort()

    print("Now it is dealing with {}, the exp name is {}".format(ocn_one,'control'))

    for ffff in namelist2:
        f0  =  xr.open_dataset(src_path + ffff)
        vars = list(f0.keys())

        for vvvv in vars:
            f0[vvvv].data  =  transfer_lon(ffff,vvvv)

        # create new name
        len1  =  len(exp_name[0]) + len('.mom6.hm_')


        new_name  =  experiment_name + 'hm_' + ffff[len1:len1+7] + '.nc'

        f0.to_netcdf(end_path + new_name)

        print('successfully transform {} to {}'.format(ffff,new_name))

    for ffff in namelist1:
        f0  =  xr.open_dataset(src_path + ffff)
        vars = list(f0.keys())

        for vvvv in vars:
            f0[vvvv].data  =  transfer_lon(ffff,vvvv)

        # create new name
        len1  =  len(exp_name[0]) + len('.mom6.sfc_')


        new_name  =  experiment_name + 'sfc_' + ffff[len1:len1+7] + '.nc'

        f0.to_netcdf(end_path + new_name)

        print('successfully transform {} to {}'.format(ffff,new_name))



def main():



    deal_control()
    
if __name__ == '__main__':
    main()
