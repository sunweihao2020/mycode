'''
This script calculate the climate of the b1850-maritime experiment result

The design for this script is every day per loop to calculate its climate value
'''
import numpy as np
import xarray as xr
import os

src_path = '/home/sun/segate/model_data/b1850_maritime/atmosphere/'
end_path = ''

# Get all file name
file_list = os.listdir(src_path) ; file_list.sort()

# Confirm the location of the date string: 37 to 42
print(file_list[100][37:42])

'''
Deign: First, add each day dataarray to one array and then htack them. Second, calculate average through first axis
'''
varnames = ['LHFLX', 'OMEGA', 'PRECT', 'Q', 'T', 'SHFLX', 'U', 'V', 'Z3', 'PS', 'TS']
def add_arrays(date_str, varname):
    file_list_new = []
    for ffff in file_list:
        if date_str == ffff[37:42]:

            file_list_new.append(ffff)
        
        else:
            continue
    
    file_list_new.sort()

    # Add them to numpy array
    f0 = xr.open_dataset(src_path + file_list_new[0])
    array0 = f0[varname].data
    for i in range(1, len(file_list_new)):
        f0 = xr.open_dataset(src_path + file_list_new[i])
        array0 = np.append(array0, f0[varname].data, axis=0,)
    
    #print(type(array0))

    return np.expand_dims(np.average(array0, axis=0,), axis=0)

f0 = xr.open_dataset(src_path + file_list[0])
for ffff in file_list[31:33]:
    print('Now it is deal with {}'.format(ffff[37:42]))
    ncfile  =  xr.Dataset(
        {
            "LHFLX":(["time", "lat","lon"], add_arrays(ffff[37:42], "LHFLX")),
            "OMEGA":(["time","lev","lat","lon"], add_arrays(ffff[37:42], "OMEGA")),
            "PRECT":(["time","lat","lon"], add_arrays(ffff[37:42], "PRECT")),
            "Q":(["time","lev","lat","lon"], add_arrays(ffff[37:42], "Q")),
            "SHFLX":(["time","lat","lon"], add_arrays(ffff[37:42], "SHFLX")),
            "T":(["time","lev","lat","lon"], add_arrays(ffff[37:42], "T")),
            "U":(["time","lev","lat","lon"], add_arrays(ffff[37:42], "U")),
            "V":(["time","lev","lat","lon"], add_arrays(ffff[37:42], "V")),
            "Z3":(["time","lev","lat","lon"],add_arrays(ffff[37:42], "Z3")),
            "PS":(["time","lat","lon"],add_arrays(ffff[37:42], "PS")),
            "TS":(["time","lat","lon"],add_arrays(ffff[37:42], "TS")),
        },
        coords={
            "time": (["time"], np.array([0])),
            "lat": (["lat"], f0.lat.data),
            "lon":  (["lon"],  f0.lon.data),
            "lev":  (["lev"],  f0.lev.data),
        },
        )
    ncfile.LHFLX.attrs     =      f0.LHFLX.attrs
    ncfile.OMEGA.attrs     =      f0.OMEGA.attrs
    ncfile.PRECT.attrs     =      f0.PRECT.attrs
    ncfile.Q.attrs         =      f0.Q.attrs
    ncfile.SHFLX.attrs     =      f0.SHFLX.attrs
    ncfile.T.attrs         =      f0.T.attrs
    ncfile.U.attrs         =      f0.U.attrs
    ncfile.V.attrs         =      f0.V.attrs
    ncfile.Z3.attrs        =      f0.Z3.attrs
    ncfile.PS.attrs        =      f0.PS.attrs
    ncfile.TS.attrs        =      f0.TS.attrs
    ncfile.lon.attrs       =      f0.lon.attrs
    ncfile.lat.attrs       =      f0.lat.attrs
    ncfile.time.attrs      =      f0.time.attrs
    ncfile.lev.attrs["units"]    =  "hPa"
    ncfile.attrs['description']  =  'This is the climate data (51 years)'

    ncfile.to_netcdf("/home/sun/wd_disk/b1850_maritime_climate/" + "b1850_maritime_climate_" + ffff[37:42] + ".nc")

        

#
#test = add_arrays('01-01', varnames[1])
#print(test.shape)