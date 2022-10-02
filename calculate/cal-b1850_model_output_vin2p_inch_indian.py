'''
20220929
This script due to process the model output for b1850 experiments
two problems need to be resolved in this code:
1. In the past I noticed that after interpolate the level under the suface pressure also has wrong value, here I want to mask them using compare
2. unify the name and time series among the different experiments
'''
src_path  =  '/home/sun/model_output/b1850_exp/exp_output/'
end_path  =  '/home/sun/segate/model_data/b1850_inch_indian/'

from curses import doupdate
import os
import numpy as np

# all file list
file_all  =  os.listdir(src_path)
var       =  ["LHFLX","OMEGA","PRECT","PS","Q","SHFLX","T","TS","U","V","Z3"]
var_3d    =  ["OMEGA","Q","T","U","V","Z3"]
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



def deal_control():
    # first I need to get the file list for the experiment
    import os

    exp_name  =  ['b1850_tx_inch_indian_official_220926']

    namelist  =  []

    # here I abandon the 43 year
    for ffff in file_all:
        if (exp_name[0] in ffff) and ('cam' in ffff) and ('mom' not in ffff):
            namelist.append(ffff)
    namelist.sort()
    namelist.pop()

    print("Now it is {}, the affirm year number is {}".format("indian",len(namelist)/365))  # affirm that the number of files is nyear
    # period range
    year_length =  int(len(namelist)/365)

    # try to get the date mmmm-dddd, using len1 below I can get the date
    #a1          =  namelist2[10]
    #len1        =  len(exp_name[0]) + len('.cam.h1.') + 5
    #print(a1[len1:len1+5])

    # --------------  data process  ----------------------------------
    for yyyy in range(year_length):
        print("It is dealing with year {}".format(yyyy))

        start  =   yyyy * 365
        end    =   (yyyy + 1) *365
        for ffff in namelist[start:end]:
            print("{} year file name is {}".format(yyyy, ffff))
            out_ds    =  cesm_vin2p(src_path,ffff,pnew)

            yy        =  yyyy + 1
            if yy < 10:
                new_name  =  "b1850_inch_indian_atmosphere_h1_0" + str(yy) + "_" + ffff[(len(exp_name[0]) + len('.cam.h1.') + 5) : (len(exp_name[0]) + len('.cam.h1.') + 10)] + ".nc"
            else:
                new_name  =  "b1850_inch_indian_atmosphere_h1_" + str(yy) + "_" + ffff[(len(exp_name[0]) + len('.cam.h1.') + 5) : (len(exp_name[0]) + len('.cam.h1.') + 10)] + ".nc"
            
            out_ds.to_netcdf(end_path + new_name)

            print("successfully transform {} to {}".format(ffff, new_name))




def main():
    deal_control()

if __name__ == "__main__":
    main() 