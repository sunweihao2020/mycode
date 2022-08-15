'''
2022-8-10
This code is to interp data to plev. The experiment is b1850 maritime
time period: 04 - 55

metion: In the b1850 experiment, the p level for interp is different with before
'''
import os
import numpy as np
def cesm_vin2p(path,file,pnew):
    import numpy as np
    import xarray as xr
    import Ngl
    vars  =  ["LHFLX","OMEGA","PRECT","PS","Q","SHFLX","T","TS","U","V","Z3"]
    files = xr.open_dataset(path+file)
    ds    = xr.Dataset(
        {
            "LHFLX":(["time","lat","lon"],np.float32(files.LHFLX.data)),
            "OMEGA":(["time","lev","lat","lon"],np.float32(Ngl.vinth2p(files.OMEGA.data,files.hyam.data,files.hybm.data,pnew,files.PS.data,1,files.P0.data/100,1,True))),
            "PRECT":(["time","lat","lon"],np.float32(files.PRECT.data)),
            "Q":(["time","lev","lat","lon"],np.float32(Ngl.vinth2p(files.Q.data,files.hyam.data,files.hybm.data,pnew,files.PS.data,1,files.P0.data/100,1,True))),
            "SHFLX":(["time","lat","lon"],np.float32(files.SHFLX.data)),
            "T":(["time","lev","lat","lon"],np.float32(Ngl.vinth2p(files.T.data,files.hyam.data,files.hybm.data,pnew,files.PS.data,1,files.P0.data/100,1,True))),
            "U":(["time","lev","lat","lon"],np.float32(Ngl.vinth2p(files.U.data,files.hyam.data,files.hybm.data,pnew,files.PS.data,1,files.P0.data/100,1,True))),
            "V":(["time","lev","lat","lon"],np.float32(Ngl.vinth2p(files.V.data,files.hyam.data,files.hybm.data,pnew,files.PS.data,1,files.P0.data/100,1,True))),
            "Z3":(["time","lev","lat","lon"],np.float32(Ngl.vinth2p(files.Z3.data,files.hyam.data,files.hybm.data,pnew,files.PS.data,1,files.P0.data/100,1,True))),
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

path       =     '/home/sun/model_output/b1850_exp/exp_output/'
path_out   =     '/home/sun/data/model_data/'
file_list  =     os.listdir(path)
file_list.sort()

# 把maritime的给挑出来
maritime  =      []
for nn in file_list:

    if "maritime" in nn and ".b185" not in nn:
        maritime.append(nn)


pnew     = np.array([1000, 975, 950, 925, 900, 875, 850, 825, 800, 775, 750, 700, 650, 600, 550, 500, 450, 400, 350, 300, 250, 225, 200, 175, 150, 125, 100, 70, 50])
for name in maritime:
    if ".cam.h1." in name:
        print("now it is deal "+name)
        out_ds  =  cesm_vin2p(path,name,pnew)
        out_ds.attrs["description"]  =  "maritime to ocean - b1850 after vin2p. 220810"
        out_ds.to_netcdf(path_out+name)

        del out_ds
        print("successfully transform "+name)
    else:
        continue