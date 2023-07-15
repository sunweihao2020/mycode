'''
2023-6-28
This script calculate the daily mean of slp data
'''
import os
path0 = '/home/sun/data/other_data/single/hour/'

file_list = os.listdir(path0)
slp_file = []
for ffff in file_list:
    if 'mean_sea_level_pressure' in ffff:
        slp_file.append(ffff)

path1 = '/home/sun/data/other_data/single/daily/slp/'
slp_file.sort()
for ffff in slp_file:
    print('Now it is dealing with {}'.format(ffff))
    os.system('cdo daymean ' + path0 + ffff + ' ' + path1 + ffff)