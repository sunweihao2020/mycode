'''
Because the b1850 experiments of removing the maritime continent includes two subset
This script is to organize them with uniform name
'''
import os

path_in = '/home/sun/model_output/b1850_exp/exp_output/'
path_out = '/home/sun/wd_disk/b1850_maritime_output/'

# 1. select the maritime files
file_all = os.listdir(path_in)
file_maritime = []
for ffff in file_all:
    if 'mariti' in ffff:
        file_maritime.append(ffff)

# 2. remove the particular element
file_maritime.remove('b1850_tx_maritime_o1_220730.cam.h1.0043-01-01-00000.nc')
file_maritime.remove('b1850_tx_maritime_o2_220807.cam.h1.0013-01-01-00000.nc')

file_maritime.sort()

print(len(file_maritime))

# At this moment, the number of the list is 18615 (51 * 365)
for yyyy in range(51):
    for dddd in range(365):
        old_name = file_maritime[yyyy*365 + dddd]
        # split the old_name
        split_name = old_name.split('.')

        head = 'b1850_tx_maritime_2022'

        if (yyyy + 1) < 10:
            time_name = '000'+str(yyyy + 1) + split_name[3][4:]
        else:
            time_name = '00'+str(yyyy + 1) + split_name[3][4:]

        new_name = head + '.' + split_name[1] + '.' + split_name[2] + '.' + time_name + '.' + split_name[4]

        os.system('cp ' + path_in + old_name + ' ' + path_out + new_name)