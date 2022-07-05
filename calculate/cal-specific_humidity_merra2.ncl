;2021/10/31
;本代码使用之前计算过的气候态年逐日数据中的rh来计算q比湿
begin
path  =  "/home/sun/qomo-data/year_mean/multi/"
file_name  =  "yyyy.climate.nc"
f          =  addfile(path+file_name,"r")

t          =  f->T(0,:,:,:)
rh         =  f->RH(0,:,:,:)
p          =  f->lev

pp         =  conform_dims(dimsizes(t), p, 0)
q          =  mixhum_ptrh(pp,t,rh,-2) ;g/kg

q!0    = "lev"
q!1    = "lat"
q!2    = "lon"
q&lev  = t&lev
q&lat  = t&lat
q&lon  = t&lon

q@units    =  "g/kg"

path2      =  "/home/sun/data/merra2_specific/"
file_name2 =  "yyyy.climate_specific_humidity.nc"
fout       =  addfile(path2+file_name2,"c")

fout->specific_humidity  =  q

end