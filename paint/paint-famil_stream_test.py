'''
2021/9/19
本代码测试绘制流线图
'''
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import metpy.calc as mpcalc
import numpy as np
import xarray as xr
import sys

sys.path.append("/home/sun/mycode/module/")
from module_sun import *

u  =  xr.open_dataset("/home/sun/qomo-data/zhuang_plev/plev_icid_U.nc")["U"]
v  =  xr.open_dataset("/home/sun/qomo-data/zhuang_plev/plev_icid_V.nc")

month_u  =  cal_monthly_average_daily(u.U)
month_v  =  cal_monthly_average_daily(v.V)

u1  =  month_u[1,3,:] ; v1  =  month_v[1,3,:]

f   =  plt.figure(figsize=(10,5))
ax  =  f.add_subplot(
    111,
    projection=ccrs.PlateCarree(central_longitude=0)
)
ax.streamplot(
    u.lon,u.lat,
    u1,v1,
    transform=ccrs.PlateCarree(),
    density=3
)
ax.coastlines()
plt.show()



