'''2020/11/12
绘制爆发日期的折线图
判据：垂直温度
'''
import sys
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import numpy as np
import json
sys.path.append("/data5/2019swh/mycode/module/")
from module_sun import out_date
with open("/data5/2019swh/data/onsetdate.json",'r') as load_f:
    a = json.load(load_f)

#year = np.array(list(a.keys()))
year  = np.array([int(x) for x in np.array(list(a.keys()))])

#day = np.array(list(a.values()))
day   = np.array([int(x) for x in np.array(list(a.values()))])
date  = np.array([])
for i in range(0,40):
    date = np.append(date,out_date(([int(x) for x in year])[i],([int(y) for y in day])[i]))

dates = np.array([])
for i in range(88,152,2):
    dates = np.append(dates,out_date(1981,i))

fig, ax = plt.subplots()

x_major_locator=MultipleLocator(2)
y_major_locator=MultipleLocator(2)


ax=plt.gca()
ax.xaxis.set_major_locator(x_major_locator)

ax.yaxis.set_major_locator(y_major_locator)
ax.set_ylim(10, 150)
plt.xlim(1980,2020,2)
plt.xticks(rotation=45)
ax.set_yticklabels((dates))
line, = ax.plot(year, day, lw=2)
ax.plot(c[:,1],c[:,0],lw=3)
plt.grid(linestyle=":", color="b")
plt.show()

fig.savefig('/data5/2019swh/paint/date.eps',dpi=1200,format='eps')