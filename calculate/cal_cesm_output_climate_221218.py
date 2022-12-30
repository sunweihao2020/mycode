'''
2022-12-17
This code calculate the climate average for the b1850 control experiment which has three members
The message of the ensemble experiments can be seen in https://www.notion.so/con_ensemble_official-19e400cb36994be6a471f9b74bebb19c
'''
import os
import numpy as np

# all file list
vars      =  ["LHFLX","OMEGA","PRECT","PS","Q","SHFLX","T","TS","U","V","Z3"]
vars_3d   =  ["OMEGA","Q","T","U","V","Z3"]
pnew      =  np.array([1000, 975, 950, 925, 900, 875, 850, 825, 800, 775, 750, 700, 650, 600, 550, 500, 450, 400, 350, 300, 250, 225, 200, 175, 150, 125, 100, 70, 50])

def cesm_vin2p(path,file,pnew):
    import numpy as np
    import xarray as xr
    import Ngl
    vars  =  ["LHFLX","OMEGA","PRECT","PS","Q","SHFLX","T","TS","U","V","Z3"]
    files = xr.open_dataset(path+file)
    ds    = xr.Dataset(
        {
            "LHFLX":(["time","lat","lon"],np.float32(files.LHFLX.data)),
            "OMEGA":(["time","lev","lat","lon"],mask_nan(ps = files.PS.data, var = np.float32(Ngl.vinth2p(files.OMEGA.data,files.hyam.data,files.hybm.data,pnew,files.PS.data,1,files.P0.data/100,1,True)), level = pnew)),
            "PRECT":(["time","lat","lon"],np.float32(files.PRECT.data)),
            "Q":(["time","lev","lat","lon"],mask_nan(ps = files.PS.data, var = np.float32(Ngl.vinth2p(files.Q.data,files.hyam.data,files.hybm.data,pnew,files.PS.data,1,files.P0.data/100,1,True)), level = pnew)),
            "SHFLX":(["time","lat","lon"],np.float32(files.SHFLX.data)),
            "T":(["time","lev","lat","lon"],mask_nan(ps = files.PS.data, var = np.float32(Ngl.vinth2p(files.T.data,files.hyam.data,files.hybm.data,pnew,files.PS.data,1,files.P0.data/100,1,True)), level = pnew)),
            "U":(["time","lev","lat","lon"],mask_nan(ps = files.PS.data, var = np.float32(Ngl.vinth2p(files.U.data,files.hyam.data,files.hybm.data,pnew,files.PS.data,1,files.P0.data/100,1,True)), level = pnew)),
            "V":(["time","lev","lat","lon"],mask_nan(ps = files.PS.data, var = np.float32(Ngl.vinth2p(files.V.data,files.hyam.data,files.hybm.data,pnew,files.PS.data,1,files.P0.data/100,1,True)), level = pnew)),
            "Z3":(["time","lev","lat","lon"],mask_nan(ps = files.PS.data, var = np.float32(Ngl.vinth2p(files.Z3.data,files.hyam.data,files.hybm.data,pnew,files.PS.data,1,files.P0.data/100,1,True)), level = pnew)),
            "PS":(["time","lat","lon"],np.float32(files.PS.data)),
            "TS":(["time","lat","lon"],np.float32(files.TS.data)),
        },
        coords={
            "lon":(["lon"],files.lon.data),
            "lat":(["lat"],files.lat.data),
            "time":(["time"],files.time.data),
            "lev":(["lev"],pnew)
        },
    )
    ds.LHFLX.attrs     =      files.LHFLX.attrs
    ds.OMEGA.attrs     =      files.OMEGA.attrs
    ds.PRECT.attrs     =      files.PRECT.attrs
    ds.Q.attrs         =      files.Q.attrs
    ds.SHFLX.attrs     =      files.SHFLX.attrs
    ds.T.attrs         =      files.T.attrs
    ds.U.attrs         =      files.U.attrs
    ds.V.attrs         =      files.V.attrs
    ds.Z3.attrs        =      files.Z3.attrs
    ds.PS.attrs        =      files.PS.attrs
    ds.TS.attrs        =      files.TS.attrs
    ds.lon.attrs       =      files.lon.attrs
    ds.lat.attrs       =      files.lat.attrs
    ds.time.attrs      =      files.time.attrs
    ds.lev.attrs["units"]    =      "hPa"

    return ds

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
    
    return var_mask

def add_attributes(infile, ref, varname):
    '''This function add attribute from ref to the infile'''
    infile[varname].attrs  =  ref[varname].attrs

    return infile

def main():
    import xarray as xr

    ''' 1. path message '''
    paths  =  '/home/sun/model_output/b1850_exp/'
    case_name  =  ['b1850_con_ensemble_official_1','b1850_con_ensemble_official_2','b1850_con_ensemble_official_3']

    ''' 2. claim the base datasets '''
    ref_file  =  xr.open_dataset(paths + '/b1850_con_ensemble_official_1/atm/hist/b1850_con_ensemble_official_1.cam.h0.0038-12-05-00000.nc')
    
    # 2D-variable dimension
    dim_2d  =  (365, ref_file['LHFLX'].data.shape[1], ref_file['LHFLX'].data.shape[2])
    # 3d-variable dimension
    dim_3d  =  (365, len(pnew), ref_file['T'].data.shape[2], ref_file['T'].data.shape[3])

    avg_dataset  =  xr.Dataset(
        {
            "LHFLX":(["time","lat","lon"],       np.zeros(dim_2d, dtype = np.float32)),
            "OMEGA":(["time","lev","lat","lon"], np.zeros(dim_3d, dtype = np.float32)),
            "PRECT":(["time","lat","lon"],       np.zeros(dim_2d, dtype = np.float64)),
            "Q":(["time","lev","lat","lon"],     np.zeros(dim_3d, dtype = np.float32)),
            "SHFLX":(["time","lat","lon"],       np.zeros(dim_2d, dtype = np.float32)),
            "T":(["time","lev","lat","lon"],     np.zeros(dim_3d, dtype = np.float32)),
            "U":(["time","lev","lat","lon"],     np.zeros(dim_3d, dtype = np.float32)),
            "V":(["time","lev","lat","lon"],     np.zeros(dim_3d, dtype = np.float32)),
            "Z3":(["time","lev","lat","lon"],    np.zeros(dim_3d, dtype = np.float32)),
            "PS":(["time","lat","lon"],          np.zeros(dim_2d, dtype = np.float32)),
            "TS":(["time","lat","lon"],          np.zeros(dim_2d, dtype = np.float32)),
        },
        coords={
            "lon":(["lon"],    ref_file.lon.data),
            "lat":(["lat"],    ref_file.lat.data),
            "time":(["time"],  np.linspace(1,365,365)),
            "lev":(["lev"],    pnew)
        },
    )
    
    # add attributes to the datasets
    for nnnn in vars:
        avg_dataset = add_attributes(avg_dataset, ref_file, nnnn)
    avg_dataset.lon.attrs       =      ref_file.lon.attrs
    avg_dataset.lat.attrs       =      ref_file.lat.attrs
    avg_dataset.time.attrs['name']      =      'climate-day'
    avg_dataset.lev.attrs["units"]    =      "hPa"

    # -----------------------------------------------------#

    ''' 3. calculate the climate-average and add to the avg_dataset'''
    # 3.1 Ensemble_member 1
    atm_path      =  paths + case_name[0] + '/atm/hist/'
    year_member1  =  16
    file_list1    =  os.listdir(atm_path) 
    # Some hidden term I need to remove
    for nnnn in file_list1:
        if '.b1850' in nnnn:
            file_list1.remove(nnnn)
    file_list1.sort()
    print("files number / 365 is {}, the correct year number is {}".format(len(file_list1) / 365, year_member1))
    
    for yyyy in range(year_member1):
        j = 0
        for dddd in range(365):
            print('Now it is file {}'.format(file_list1[yyyy*365 + dddd]))

            # get the intepolated dataset
            interp_ds  =  cesm_vin2p(atm_path, file_list1[yyyy*365 + dddd], pnew=pnew)
            interp_ds.to_netcdf('/home/sun/segate/model_data/b1850_control_ensemble_vin2p/' + file_list1[yyyy*365 + dddd])

            # add each variable to the avg_dataset
            for nnnn in vars:
                avg_dataset[nnnn].data[j] += interp_ds[nnnn].data[0] / (year_member1 * 3)

                #print(avg_dataset["SHFLX"].data[j])

            j += 1

    # 3.1.1 Here I would like to output to netcdf for checking purpose
    avg_dataset_test  =  avg_dataset
    for vvvv in vars:
        avg_dataset_test[vvvv].data *= 3
    avg_dataset_test.attrs['description']  =  'In this file I only calculate 2 years in ensemble1 to check the calculate result'
    avg_dataset_test.to_netcdf('/home/sun/data/model_data/climate/b1850_exp/b1850_con_ensemble/test_avg_dataset.nc')

    del avg_dataset_test

    # 3.2 Ensemble_member 2
    atm_path      =  paths + case_name[1] + '/atm/hist/'
    year_member2  =  26
    file_list2    =  os.listdir(atm_path) 

    for nnnn in file_list2:
        if '.b1850' in nnnn:
            file_list2.remove(nnnn)
    file_list2.sort()
    print("files number / 365 is {}, the correct year number is {}".format(len(file_list2) / 365, year_member2))
    
    for yyyy in range(year_member2):
        j = 0
        for dddd in range(365):
            print('Now it is file {}'.format(file_list2[yyyy*365 + dddd]))

            # get the intepolated dataset
            interp_ds  =  cesm_vin2p(atm_path, file_list2[yyyy*365 + dddd], pnew=pnew)
            interp_ds.to_netcdf('/home/sun/segate/model_data/b1850_control_ensemble_vin2p/' + file_list2[yyyy*365 + dddd])

            # add each variable to the avg_dataset
            for nnnn in vars:
                avg_dataset[nnnn].data[j] += interp_ds[nnnn].data[0] / (year_member2 * 3)
            
            j += 1

    # 3.3 Ensemble_member 3
    atm_path      =  paths + case_name[2] + '/atm/hist/'
    year_member3  =  30
    file_list3    =  os.listdir(atm_path) 
    
    for nnnn in file_list3:
        if '.b1850' in nnnn:
            file_list3.remove(nnnn)
    file_list3.sort()
    print("files number / 365 is {}, the correct year number is {}".format(len(file_list3) / 365, year_member3))
    
    
    for yyyy in range(year_member3):
        j = 0
        for dddd in range(365):
            print('Now it is file {}'.format(file_list3[yyyy*365 + dddd]))

            # get the intepolated dataset
            interp_ds  =  cesm_vin2p(atm_path, file_list3[yyyy*365 + dddd], pnew=pnew)
            interp_ds.to_netcdf('/home/sun/segate/model_data/b1850_control_ensemble_vin2p/' + file_list3[yyyy*365 + dddd])

            # add each variable to the avg_dataset
            for nnnn in vars:
                avg_dataset[nnnn].data[j] += interp_ds[nnnn].data[0] / (year_member3 * 3)

            j += 1

    ''' 4. save to the ncfile'''
    avg_dataset.to_netcdf('/home/sun/data/model_data/climate/b1850_exp/b1850_con_ensemble/b1850_climate_daily_control_ensemble_average_atm.nc')


if __name__ == '__main__':
    main()