'''
2022-12-29
This script plot time series for experiments
'''

''' 1. First I need to trim the four ts time-series '''
import numpy as np
path0  =  '/home/sun/data/model_data/spin-up/ts_time_series/'

#----------- 1.1 Control ---------------
time_series  =  np.array([]) # result array

# -------------- series 1 ----------------------
############################################################
with open(path0  +  'con_ts_s1.npy', 'rb') as f:
    s1 = np.load(f)

time_series  =  np.append(time_series, s1)

# --------------- series 8 --------------------
with open(path0 + 'con_ts_s8.npy',  'rb') as f:
    s8 = np.load(f)

time_series  =  np.append(time_series,  s8[:144])

# ----------- series 4 and 5 ----------------
with open(path0  +  'con_ts_s4.npy', 'rb') as f:
    s4 = np.load(f)

time_series  =  np.append(time_series, s4[180:])

with open(path0  +  'con_ts_s5.npy', 'rb') as f:
    s5 = np.load(f)

time_series  =  np.append(time_series, s5[180:])

#print(time_series.shape[0] / 12)

# --------------- series 3 --------------------
with open(path0 + 'con_ts_s3.npy',  'rb') as f:
    s3 = np.load(f)

time_series  =  np.append(time_series,  s3)

# --------------- series 2 --------------------
with open(path0 + 'con_ts_s2.npy',  'rb') as f:
    s2 = np.load(f)

time_series  =  np.append(time_series,  s2)

# --------------- series 6 --------------------
with open(path0 + 'con_ts_s6.npy',  'rb') as f:
    s6 = np.load(f)

time_series  =  np.append(time_series,  s6)

# --------------- series 7 --------------------
with open(path0 + 'con_ts_s7.npy',  'rb') as f:
    s7 = np.load(f)

time_series  =  np.append(time_series,  s7)

print(time_series.shape[0] / 12)
time_series_con  =  time_series
time_series_con_year  =  np.zeros((150), dtype=np.float64)
for i in range(150):
    time_series_con_year[i]  =  np.average(time_series_con[i*12 : (i*12+12)])
############################################################

# ------------ series 2 Indian -----------------------
############################################################
time_series  =  np.array([]) # result array

# -------------- series 1 ----------------------
with open(path0  +  'indian_ts_s2.npy', 'rb') as f:
    s1 = np.load(f)

time_series  =  np.append(time_series, s1)

# --------------- series 8 --------------------
with open(path0 + 'indian_ts_s3.npy',  'rb') as f:
    s8 = np.load(f)

time_series  =  np.append(time_series,  s8[24:])

# ----------- series 4 and 5 ----------------
with open(path0  +  'indian_ts_s1.npy', 'rb') as f:
    s4 = np.load(f)

time_series  =  np.append(time_series, s4[:12*12])
time_series  =  np.append(time_series, s4[30*12:])

time_series_indian  =  time_series
time_series_indian_year  =  np.zeros((150), dtype=np.float64)
for i in range(150):
    time_series_indian_year[i]  =  np.average(time_series_indian[i*12 : (i*12+12)])
##############################################################

# ------------- series 3 Inco-china -----------------
time_series  =  np.array([]) # result array

# -------------- series 1 ----------------------
with open(path0  +  'in_ts_s3.npy', 'rb') as f:
    s1 = np.load(f)

time_series  =  np.append(time_series, s1)

# --------------- series 8 --------------------
with open(path0 + 'in_ts_s2.npy',  'rb') as f:
    s8 = np.load(f)

time_series  =  np.append(time_series,  s8)

# ----------- series 4 and 5 ----------------
with open(path0  +  'in_ts_s1.npy', 'rb') as f:
    s4 = np.load(f)

time_series  =  np.append(time_series, s4[:-12*4])

time_series_inch  =  time_series
time_series_inch_year  =  np.zeros((150), dtype=np.float64)
for i in range(150):
    time_series_inch_year[i]  =  np.average(time_series_inch[i*12 : (i*12+12)])
##############################################################

# ------------ series 4 Inch Indian -----------------
time_series  =  np.array([])

with open(path0  +  'inch_indian_150.npy',  'rb') as f:
    ss  =  np.load(f)

time_series  =  np.append(time_series, ss)
time_series_inch_indian  =  time_series
time_series_inch_indian_year  =  np.zeros((150), dtype=np.float64)
for i in range(150):
    time_series_inch_indian_year[i]  =  np.average(time_series_inch_indian[i*12 : (i*12+12)])
##############################################################

#-------------------- 2. paint ------------------------------
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

# Set figure
proj    =  ccrs.PlateCarree()
fig1    =  plt.figure(figsize=(30,28))
spec1   =  fig1.add_gridspec(nrows=4,ncols=1)

# 2.1 paint control spinup
ax = fig1.add_subplot(spec1[0,0])

# plot setting
ax.set_xticks([0, 25, 50, 75, 100, 125, 150])
ax.set_xticklabels(["1","25","50","75","100","125","150"], fontsize = 22.5)

ax.set_ylim(277,280)
ax.set_yticks(np.linspace(277,280,4, dtype=int))
ax.set_yticklabels(np.linspace(277,280,4, dtype=int), fontsize=22.5)

# title
ax.set_xlabel("Year", fontsize=20)
ax.set_ylabel("Global-Mean TS", fontsize=20)

ax.set_title("CTRL", fontsize=20, loc='right')
ax.set_title("(a)", fontsize=20, loc='left')

ax.plot(time_series_con_year)

# 2.2 paint indian spinup
ax = fig1.add_subplot(spec1[1,0])

# plot setting
ax.set_xticks([0, 25, 50, 75, 100, 125, 150])
ax.set_xticklabels(["1","25","50","75","100","125","150"], fontsize = 22.5)

ax.set_ylim(277,280)
ax.set_yticks(np.linspace(277,280,4, dtype=int))
ax.set_yticklabels(np.linspace(277,280,4, dtype=int), fontsize=22.5)

# title
ax.set_xlabel("Year", fontsize=20)
ax.set_ylabel("Global-Mean TS", fontsize=20)

ax.set_title("No_Indian", fontsize=20, loc='right')
ax.set_title("(b)", fontsize=20, loc='left')

ax.plot(time_series_indian_year)

# 2.3 paint inch spinup
ax = fig1.add_subplot(spec1[2,0])

# plot setting
ax.set_xticks([0, 25, 50, 75, 100, 125, 150])
ax.set_xticklabels(["1","25","50","75","100","125","150"], fontsize = 22.5)

ax.set_ylim(277,280)
ax.set_yticks(np.linspace(277,280,4, dtype=int))
ax.set_yticklabels(np.linspace(277,280,4, dtype=int), fontsize=22.5)

# title
ax.set_xlabel("Year", fontsize=20)
ax.set_ylabel("Global-Mean TS", fontsize=20)

ax.set_title("No_Inch", fontsize=20, loc='right')
ax.set_title("(c)", fontsize=20, loc='left')

ax.plot(time_series_inch_year)

# 2.4 paint indian-inch spinup
ax = fig1.add_subplot(spec1[3,0])

# plot setting
ax.set_xticks([0, 25, 50, 75, 100, 125, 150])
ax.set_xticklabels(["1","25","50","75","100","125","150"], fontsize = 22.5)

ax.set_ylim(277.5,279.5)
ax.set_yticks(np.linspace(277.5,279.5,5, dtype=int))
ax.set_yticklabels(np.linspace(277.5,279.5,5, dtype=int), fontsize=22.5)

# title
ax.set_xlabel("Year", fontsize=20)
ax.set_ylabel("Global-Mean TS", fontsize=20)

ax.set_title("No_Inch_Indian", fontsize=20, loc='right')
ax.set_title("(d)", fontsize=20, loc='left')

ax.plot(time_series_inch_indian_year)

plt.savefig('/home/sun/paint/lunwen/version6.0/lunwen_extra_spinup_v6.0_150ts_yearly.pdf', dpi=450)