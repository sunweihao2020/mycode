'''
2023-2-20
This script calculate and plot the CEF intensity
'''
import xarray as xr
import numpy as np

# ------------ 1. Information --------------------------------
# 1.1 Range
lat_range = slice(10, 0)
lon_range = slice(80, 90)

# 1.2 file path
path0 = '/home/sun/data/ERA5_data_monsoon_onset/climatic_daily_ERA5/single/'

file0 = 'surface_sensible_heat_flux_climatic_daily.nc'
file1 = 'surface_sensible_heat_flux_climatic_daily_year_early.nc'
file2 = 'surface_sensible_heat_flux_climatic_daily_year_late.nc'

ref_file = xr.open_dataset(path0 + file0)

# ------------- 2. Calculate the Deviation --------------------
def cal_abnormal_CEF_timeseries():
    # 2.1 Claim the series array
    avg_cef = np.array([])
    early_cef = np.array([])
    late_cef = np.array([])

    # 2.2 Read the file
    f0 = xr.open_dataset(path0 + file0).sel(lat=lat_range, lon=lon_range)
    f1 = xr.open_dataset(path0 + file1).sel(lat=lat_range, lon=lon_range)
    f2 = xr.open_dataset(path0 + file2).sel(lat=lat_range, lon=lon_range)

    # 2.3 calculate area average
    for i in range(365):
        avg_cef = np.append(avg_cef, np.average(f0['sshf'].data[i]))
        early_cef = np.append(early_cef, np.average(f1['sshf'].data[i]))
        late_cef  = np.append(late_cef,  np.average(f2['sshf'].data[i]))

    # 2.4 Return the deviation value
    return (early_cef - avg_cef), (late_cef - avg_cef)

# --------------- 3. Paint the Picture --------------------------
def paint_early_late_cef_intensity(early_cef, late_cef):
    import matplotlib.pyplot as plt

    # 3.1 Tick Settings
    # time range from 20 Feb to 1 Jun
    x_tick = [50, 59, 68, 78, 90, 99, 109, 120, 129, 139, 151]
    x_label = ['20 Feb', '1 Mar', '10 Mar', '20 Mar', '1 Apr', '10 Apr', '20 Apr', '1 May', '10 May', '20 May', '1 Jun']

    # y-axis
    y_tick = np.linspace(-2, 2, 16)

    # 3.2 Plot the early year using blue color
    plt.bar(ref_file['time'].data, early_cef / 86400 * 24 * -1, color='blue')

    # 3.3 Plot the late year using red color
    plt.bar(ref_file['time'].data, late_cef / 86400 * 24 * -1, color='red')

    # 3.4 Set limitation
    plt.ylim(-2, 2)
    plt.xlim(45, 155)

    # 3.5 Tick information
    plt.xticks(x_tick, x_label, rotation=45)
    plt.yticks(y_tick)

    plt.savefig('/home/sun/paint/monsoon_onset_composite_ERA5/abnormal_southbob_sshf_series.pdf')

def main():
    early_cef, late_cef = cal_abnormal_CEF_timeseries()

    paint_early_late_cef_intensity(early_cef, late_cef)


if __name__ == '__main__':
    main()