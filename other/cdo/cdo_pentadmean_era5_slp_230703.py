'''
2023-7-3
This script calculate pentad-mean using cdo for slp data
'''
import os

path0 = '/home/sun/data/other_data/single/daily/slp/'
path1 = '/home/sun/data/other_data/single/pentad/slp/'

lists = os.listdir(path0) ; lists.sort()
for ffff in lists:
    os.system('cdo timselmean,5 ' + path0 + ffff + ' ' + path1 + ffff)