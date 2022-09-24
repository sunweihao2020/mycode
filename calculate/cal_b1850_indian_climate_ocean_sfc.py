'''
2022-9-21
This code calculate climate average for the sfc nc file
'''
import os

src_path  =  '/home/sun/segate/model_data/'

exp_name  =  ['b1850_control','b1850_inch','b1850_indian','b1850_maritime']

def control_ocean():
    '''This function calculate climate for control exp'''
    import os
    import numpy as np
    import xarray as xr

    path0  =  src_path + exp_name[2] + '/ocean/'

    # get files for sfc
    filelist  =  os.listdir(path0) ; filelist.sort()
    sfc_file  =  []
    for ffff in filelist:
        if 'sfc' in ffff:
            sfc_file.append(ffff)

    # get var name
    reference_f  =  xr.open_dataset(path0  +  sfc_file[1])
    #vars         =  list(reference_f.keys())
    #print(vars)
    vars          =  ['SSH', 'tos', 'sos', 'SSU', 'SSV', 'mlotst']

    dim0   =  365
    xh    =  reference_f.xh.data
    yh    =  reference_f.yh.data
    xq    =  reference_f.xq.data
    yq    =  reference_f.yq.data
    
    base_ssh     =  np.zeros((365,458,540))
    base_tos     =  np.zeros((365,458,540))
    base_sos     =  np.zeros((365,458,540))
    base_ssu     =  np.zeros((365,458,540))
    base_ssv     =  np.zeros((365,458,540))
    base_mlotst  =  np.zeros((365,458,540))

    for ffff in sfc_file:
        f0  =  xr.open_dataset(path0 + ffff)

        base_ssh    +=  f0['SSH'].data / len(sfc_file)
        base_tos    +=  f0['tos'].data / len(sfc_file)
        base_sos    +=  f0['sos'].data / len(sfc_file)
        base_ssu    +=  f0['SSU'].data / len(sfc_file)
        base_ssv    +=  f0['SSV'].data / len(sfc_file)
        base_mlotst +=  f0['mlotst'].data / len(sfc_file)

    ncfile  =  xr.Dataset(
    {
        "SSH": (["time", "yh", "xh"], base_ssh),
        "tos": (["time", "yh", "xh"], base_tos),
        "sos": (["time", "yh", "xh"], base_sos),
        "SSU": (["time", "yh", "xq"], base_ssu),
        "SSV": (["time", "yq", "xh"], base_ssv),
        "mlotst": (["time", "yh", "xh"], base_mlotst),
    },
    coords={
        "xh": (["xh"], xh),
        "yh": (["yh"], yh),
        "xq": (["xq"], xq),
        "yq": (["yq"], yq),
        "time": (["time"], np.linspace(1,365,365)),
    },
    )
    ncfile.SSH.attrs  =  reference_f.SSH.attrs
    ncfile.tos.attrs  =  reference_f.tos.attrs
    ncfile.sos.attrs  =  reference_f.sos.attrs
    ncfile.SSU.attrs  =  reference_f.SSU.attrs
    ncfile.SSV.attrs  =  reference_f.SSV.attrs
    ncfile.mlotst.attrs  =  reference_f.mlotst.attrs
    ncfile["xh"].attrs  =  f0["xh"].attrs
    ncfile["yh"].attrs  =  f0["yh"].attrs
    ncfile["xq"].attrs  =  f0["xq"].attrs
    ncfile["yq"].attrs  =  f0["yq"].attrs

    ncfile.to_netcdf("/home/sun/segate/model_data/climate/b1850_indian_ocean_climate_sfc.nc")


def main():
    control_ocean()


if __name__ == '__main__':
    main()