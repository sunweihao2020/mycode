import sys
import re
import os

f1 = open("/data5/2019swh/mycode/test/test-model_wind_3.ncl","r+")
text = f1.readlines()
files = os.listdir('/data5/2019swh/mydown/merra_modellev')
files.sort()
f1.close()

for ff in files:
    f = open("/data5/2019swh/data/cal_thermal_p/"+ff+".ncl","w")
    for ss in text:
        text2 = re.sub('name',ff,ss)
        f.writelines(text2)
    f.close()
    os.system("ncl /data5/2019swh/data/cal_thermal_p/"+ff+".ncl")