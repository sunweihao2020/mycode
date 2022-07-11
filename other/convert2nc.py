import os
path = "/data5/2019swh/mydown/jra55/"
files = os.listdir(path)
os.chdir(path)
for vvvv in files:
    os.system("mv "+vvvv+" "+vvvv+".grb1")
    os.system("ncl_convert2nc "+vvvv+".grb1")
