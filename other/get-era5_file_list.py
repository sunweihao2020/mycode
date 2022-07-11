'''
2021/6/1
本代码获取era5的资料列表
'''
import os
import subprocess
path = '/data1/other_data/DataUpdate/ERA5/new-era5/hourly/'
for yyyy in range(1979,1980):
    path1 = path+str(yyyy)
    files = subprocess.check_output('ls -t /data1/other_data/DataUpdate/ERA5/new-era5/hourly/'+str(yyyy), shell=True)
    files = files.decode('utf-8')
    files = files.split('\n')
    del files[0]
    del files[0]
    f     = open('/data5/2019swh/data/'+str(yyyy)+'.txt','w+')
    for ss in files:
        f.write(ss)
        f.write('\r\n')
    f.close()
