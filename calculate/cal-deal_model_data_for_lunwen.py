import os
import xarray as xr

path1  =  "/home/sun/model_output/control_220416_vin2p/atm/vin2p/"
path2  =  "/home/sun/model_output/replace_indian_vin2p/vin2p/"
path3  =  "/home/sun/model_output/replace_inch_vin2p/vin2p/"
path4  =  "/home/sun/model_output/replace_inch_indian_vin2p/vin2p/"

def select_data(path):
    files  =  os.listdir(path)
    path_out  =  "/home/sun/data/upload/"
    for ff in files:
        f0  =  xr.open_dataset(path+ff).sel(lev=925)
        f1  =  xr.open_dataset(path+ff)

        f0_o  =  f0[["U","V"]]
        f1_o  =  f1["PRECT"]

        f0_o.to_netcdf(path_out+"wind/"+ff)
        f1_o.to_netcdf(path_out+"prect/"+ff)

def main():
    select_data(path1)
    select_data(path2)
    select_data(path3)
    select_data(path4)

if __name__ == '__main__':
    main()
