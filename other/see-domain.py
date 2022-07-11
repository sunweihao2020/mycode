'''
2021/9/6
本代码调查试验中的domain文件
'''
import xarray as xr
import numpy as np

path  =  "/data5/2019swh/data/domain/"
f1    =  xr.open_dataset(path+"domain.lnd.fv0.9x1.25_gx1v7.151020.nc")
f2    =  xr.open_dataset(path+"domain.ocn.gx1v7.151008.nc")
f3    =  xr.open_dataset(path+"domain.ocn.1x1.111007.nc")