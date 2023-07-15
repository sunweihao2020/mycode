'''
2023-6-6
This script calculate BOB area precipitation during the monsoon onset -2 0 +2 totally 5 days
'''
import xarray as xr
import numpy as np
import calendar
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

precip = xr.open_dataset('/home/sun/data/trmm_prect_cat.nc').sel(lon=slice(80, 100), lat=slice(0, 20))
#print(precip['time'].data[7670:-365*2-1]) #compared to 1980 - 2019
#print(v_wind['time'].data[7670:-365*2-1]) #compared to 1980 - 2019
pt = precip['precipitation']


# Read monsoon onset date
date_file = xr.open_dataset('/home/sun/data/onset_day_data/onsetdate.nc').sel(year=slice(1998, 2019))
date = date_file['bob_onset_date'].data
#print(date)

day0 = 0
onset_prect = np.array([])
onset_somali = np.array([])
onset_bob = np.array([])
for i in range(0, len(date)):
    year = 1998 + i
    this_year_prect = np.average(pt[day0 + date[i] -2 : day0 + date[i] +3])
    onset_prect = np.append(onset_prect, this_year_prect)
    if calendar.isleap(year):
        day0 += 366
    else:
        day0 += 365

#x_train = np.array(date - np.average(date)).reshape((len(date - np.average(date)), 1))
#y_train = np.array(onset_somali - np.average(onset_somali)).reshape((len( onset_somali - np.average(onset_somali)), 1))
#lineModel = LinearRegression()
#lineModel.fit(x_train, y_train)
#Y_predict1 = lineModel.predict(x_train)
#
x_train = np.array(date - np.average(date)).reshape((len(date - np.average(date)), 1))
y_train = np.array(onset_prect - np.average(onset_prect)).reshape((len( onset_prect), 1))
lineModel = LinearRegression()
lineModel.fit(x_train, y_train)
Y_predict2 = lineModel.predict(x_train)

plt.xlim((-20, 20))
plt.ylim((-6.5, 6.5))
plt.scatter(date - np.average(date), onset_prect - np.average(onset_prect))
#plt.twinx()
#plt.scatter(date - np.average(date), onset_somali - np.average(onset_somali), marker='^',c='red')
#plt.scatter(date - np.average(date), onset_bob - np.average(onset_bob), marker='o',c='green',s=5)
#plt.plot(x_train, Y_predict1, c='red')
plt.plot(x_train, Y_predict2, c='green')
plt.savefig('/home/sun/paint/monsoon_onset_composite_ERA5/onset_period_trmm_prect_with_dates.pdf')
#print(onset_prect*24)