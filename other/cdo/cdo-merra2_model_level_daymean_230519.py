'''
2023-5-19
This script is to cdo daymean the downloaded merra2 modellevel files
'''
import os

path0 = '/home/sun/mydown/merra_modellev/'

file0 = os.listdir(path0)
file1 = []
for ffff in file0:
    for yyyy in range(1980, 2020):
        str0 = '.' + str(yyyy)
        if str0 in ffff:
            file1.append(ffff)

            continue

print(len(file1)/365)

for yyyy in range(1980, 2020):
    file3 = []
    str1 = '.'+str(yyyy)
    for ffff in file0:
        if str1 in ffff:
            file3.append(ffff)

    print('This is year {}, file number is {}'.format(yyyy, len(file3)))
