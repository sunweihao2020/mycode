'''
2021/9/19
本代码对gecbo的地形文件进行插值处理
'''
import xarray as xr
import numpy as np

f = xr.open_dataset("/home/sun/data/GEBCO_2021.nc")

new_elevaton  =  f.elevation.data.copy()
new_elevaton[:,0:43200] = f.elevation.data[:,43200:86400]
new_elevaton[:,43200:86400] = f.elevation.data[:,0:43200]

new_lon        =  f.lon.data.copy()
new_lon[0:43200]  =  f.lon.data[43200:86400]
new_lon[43200:86400] = f.lon.data[0:43200]+360

in_lon         =  np.linspace(0, 360, num=720, endpoint=False)
in_lat         =  np.linspace(-90,90,num=361)

#先插值纬向的
in_ele_1       =  np.zeros((f.elevation.shape[0],in_lon.shape[0]))
in_ele_2       =  np.zeros((in_lat.shape[0],in_lon.shape[0]))

for yy in range(0,f.lat.shape[0]):
    in_ele_1[yy,:]  =  np.interp(in_lon,new_lon,new_elevaton[yy,:])

for xx in range(0,in_ele_1.shape[1]):
    in_ele_2[:,xx]  =  np.interp(in_lat,f.lat.data,in_ele_1[:,xx])