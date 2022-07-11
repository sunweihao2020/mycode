import os
#name = ["mslp","surfpres","t2m","tskin","u10m","v10m"]
#path = "/data5/2019swh/test/"
#
#os.chdir("/data1/ERAIN/daily/surface")
#
#for var in name:
#    for yyyy in range(1979,2019):
#        cmd1 = var+"."+str(yyyy)+".nc "+path+var+"."+str(yyyy)+".daily.nc" 
#        os.system("cdo daymean "+cmd1)

#2021/2/13 cdo 七月的加热资料
#path = "/data5/2019swh/mydown/merra-tdt/2010/"
#for day in range(1,32):
#    if day<10:
#        name = "MERRA2_300.tavg3_3d_tdt_Np.2010070"+str(day)+".SUB.nc"
#    else:
#        name = "MERRA2_300.tavg3_3d_tdt_Np.201007"+str(day)+".SUB.nc"
#    os.system("cdo daymean "+path+name+" ~/"+str(day)+".nc")

#2021/2/28 cdo jra55

path = "/data5/2019swh/mydown/jra55_nc/"
files = os.listdir(path)
os.chdir(path)
for vvvv in files:
    os.system("cdo daymean "+vvvv+" "+vvvv[18:])