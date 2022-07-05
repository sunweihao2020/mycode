'''
2021/9/6
本代码对印度大陆挖去后的海洋进行插值操作
'''
import xarray as xr
import numpy as np

path = "/data5/2019swh/data/domain/"
sst  = xr.open_dataset(path+"sst_HadOIBl_bc_1x1_1850_2017_c180507.nc")

lon    = slice(70, 90) ; lat = slice(0, 20)
sst2   = sst["SST_cpl_prediddle"][5,:,:].sel(lon=lon,lat=lat)

def nan_helper(y):
    """Helper to handle indices and logical indices of NaNs.

    Input:
        - y, 1d numpy array with possible NaNs
    Output:
        - nans, logical indices of NaNs
        - index, a function, with signature indices= index(logical_indices),
          to convert logical indices of NaNs to 'equivalent' indices
    Example:
        >>> # linear interpolation of NaNs
        >>> nans, x= nan_helper(y)
        >>> y[nans]= np.interp(x(nans), x(~nans), y[~nans])
    """

    return np.isnan(y), lambda z: z.nonzero()[0]

#for yy in range(0,sst2.shape[0]):
#    nans,x = nan_helper(sst2.data[yy,:])
#    sst2.data[yy,:]
#
yy = 5