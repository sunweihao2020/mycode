'''
2022-12-27
This script paint the ts time-series of 150 years to response the reviewer
No_Inch experiment
'''
####################################################################################################
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

        plt.savefig('/home/sun/paint/lunwen/version6.0/spinup/b1850_inch_150year.pdf',dpi=400)

path0  =  '/home/sun/data/model_data/spin-up/ts_time_series/'
time_series  =  np.array([]) # result array

# -------------- series 1 ----------------------
with open(path0  +  'in_ts_s3.npy', 'rb') as f:
    s1 = np.load(f)

time_series  =  np.append(time_series, s1)
print(s1.shape)

# --------------- series 8 --------------------
with open(path0 + 'in_ts_s2.npy',  'rb') as f:
    s8 = np.load(f)

time_series  =  np.append(time_series,  s8)
print(s8.shape)

# ----------- series 4 and 5 ----------------
with open(path0  +  'in_ts_s1.npy', 'rb') as f:
    s4 = np.load(f)

time_series  =  np.append(time_series, s4)
print(s4.shape)


print(time_series.shape[0]/12)


paint_series(time_series)
