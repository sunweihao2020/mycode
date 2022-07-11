'''
2021/1/24
把下载的era5的地表气压转为float
'''
import os
path = "/data5/2019swh/mydown/era5-single/surface_pressure/"
#for yr in range(1980,2020):
path1 = path + str(1995) +"/"
files = os.listdir(path1)