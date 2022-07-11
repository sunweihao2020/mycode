'''
2021/1/22
目的：将服务器里面的3小时加热资料求取日平均
资料路径：/data1/MERRA2/3hourly_lres/plev/tdt/
'''
import os
path_0 = "/data5/2019swh/merra2/tdt/"
for i in range(1980,2019):
    os.system("mkdir /data5/2019swh/merra2/tdt/"+str(i))
    path_1 = path_0+str(i)+"/"
    path = "/data1/MERRA2/3hourly_lres/plev/tdt/"+str(i)+"/"
    files = os.listdir(path)
    files.sort()
    for ffff in files:
        os.system("cdo daymean /data1/MERRA2/3hourly_lres/plev/tdt/"+str(i)+"/"+ffff+" "+path_1+ffff)