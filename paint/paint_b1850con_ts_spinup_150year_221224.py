'''
2022-12-24
This script paint the ts time-series of 150 years to response the reviewer
'''
####################################################################################################
#  Total: 30 + 16 + 6 + 5 + 5 + 30 + 25 = 127
#
#  First series: b1850_con_ensemble_spinup_1
#                period: 360 months
#                path: /home/sun/model_output/b1850_exp/b1850_control/b1850_con_ensemble_spinup_1/atm/hist
#
#  Second series: b1850_con_ensemble_official_1
#                 period: 5840 days ( 16 years )
#                 path: /home/sun/model_output/b1850_exp/b1850_con_ensemble_official_1/atm/hist
#
#  Third series:  b1850_con_ensemble_official_1_spinup_1_official_1
#                 period: 2191 days ( 6 years 1day)
#                 path: /home/sun/model_output/b1850_exp/b1850_con_ensemble_official_1_spinup_1_official_1/atm/hist
#
#  Fourth series: b1850_con_ensemble_spinup_2
#                 period: 180 months only use late 5 years
#                 path: /home/sun/model_output/b1850_exp/b1850_control/b1850_con_ensemble_spinup_2/atm/hist
#
#  Fifth series:  b1850_con_ensemble_spinup_3
#                 period: 180 months only use late 5 years
#                 path: /home/sun/model_output/b1850_exp/b1850_control/b1850_con_ensemble_spinup_3/atm/hist
#
#  Sixth series:  b1850_con_ensemble_official_2
#                 period:  9490 days (26 years)
#                 path: /home/sun/model_output/b1850_exp/b1850_con_ensemble_official_2/atm/hist
#
#  Seventh series:  b1850_con_ensemble_official_2
#                   period:  10950 ( 30 years )
#                   path: /home/sun/model_output/b1850_exp/b1850_con_ensemble_official_3/atm/hist
#
#  Eighth series:  Well I find the old spinup file, That's lucky
#                  casename: b1850_control4_220624
#                  period:  53 - 90 (38 years)
#
#  The sequence for joint:
#       s1 (30) + s4 (5) + s5 (5)
####################################################################################################
import numpy as np

def paint_series(series):
    import matplotlib.pyplot as plt
    import numpy as np

    with plt.style.context('Solarize_Light2'):
        fig, ax = plt.subplots(figsize=(30,15))
        plt.plot(series)

        plt.xlabel("Global-Mean TS",fontsize=20)
        plt.ylabel("Model year",fontsize=20)

       #ax.set_xticks(np.linspace(1,360,16,dtype=int))

        plt.savefig('/home/sun/paint/lunwen/version6.0/spinup/b1850_control_150year.pdf',dpi=400)

path0  =  '/home/sun/data/model_data/spin-up/ts_time_series/'
time_series  =  np.array([]) # result array

# -------------- series 1 ----------------------
with open(path0  +  'con_ts_s1.npy', 'rb') as f:
    s1 = np.load(f)

time_series  =  np.append(time_series, s1)

# --------------- series 8 --------------------
with open(path0 + 'con_ts_s8.npy',  'rb') as f:
    s8 = np.load(f)

print(s8.shape[0] / 12)

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
print(time_series.shape[0]/12)


paint_series(time_series)
