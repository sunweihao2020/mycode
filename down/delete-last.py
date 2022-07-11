import os
import numpy
import time
tt = "00:03"
for yyyy in range(1980,2001):
    path = "/.share/CACHEDEV3_DATA/qomo-era5/monthly/"+str(yyyy)+"/"
    files = os.listdir(path)
    files.sort()
    for f in files:
        if time.ctime(os.path.getmtime(path+f))[11:16] == tt:
            os.system("rm -rf "+path+f)
        else:
            continue
