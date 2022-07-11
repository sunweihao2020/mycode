'''
2021/9/21
本代码调用cdo实现对ERA5文件求日平均
'''
import os
vars  =  ["w"]
path  =  "/data1/ERA5/datasets/muti-levels/hourly/"
path2 =  "/data5/2019swh/data/test/"

for vv in vars:
    file_list  =  os.listdir(path+vv)
    for ff in file_list:
        os.system("cdo daymean "+path+vv+"/"+ff+" "+path2+ff[:-3]+"-daymean.nc")
