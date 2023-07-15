import metpy.calc as mpcalc
import xarray as xr
import os

src_path = '/home/sun/wd_disk/merra2_modellev/daymean/'
end_path = '/home/sun/wd_disk/merra2_modellev/abs_vorticity/'

# == test function ==
f0 = xr.open_dataset(src_path + "MERRA2_300.tavg3_3d_asm_Nv.20080718.SUB.nc")

file_list = os.listdir(src_path) ; file_list.sort()
for ffff in file_list:
    f1 = xr.open_dataset(src_path + ffff)

    f2 = xr.DataArray(mpcalc.absolute_vorticity(f1.U, f1.V).data, coords=[f1.time.data, f1.lev.data, f1.lat.data, f1.lon.data], dims=["time", "lev", "lat", "lon"])
    f2.to_netcdf(end_path + ffff)
