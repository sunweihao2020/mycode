;2020/11/5
;所用资料：merra2
;要素 ：计算合成平均的PS
;level ：单层
begin
f1 = addfile("/data5/2019swh/data/composite3.nc","r")
f2 = addfile("/data5/2019swh/data/composite_PS.nc","r")
f3 = addfile("/data5/2019swh/data/divergent_wind.nc","r")
g = 9.8
a = 6378388
pi = atan(1.0)*4
h  =  f1->H
p = f1->level
lat = f1->lat
time = f1->time
dv = f3->dv
dv@_FillValue = h@_FillValue
dv = where(ismissing(h),h@_FillValue , dv)
p = p*100
ps = f2->PS
dp = dpres_plevel(p,ps,0,0)
dvm1 = dim_avg_n(dv(:,:,:,416:432),3)
dvm2 = dim_avg_n(dv(:,:,:,432:448),3)
dpm1 = dim_avg_n(dp(:,:,:,416:432),3)
dpm2 = dim_avg_n(dp(:,:,:,432:448),3)
;msf1  = new((/61,42,361/),double)
;msf2  = new((/61,42,361/),double)

dvm1 := dvm1(:,0:27,:)
dvm2 := dvm2(:,0:27,:)
dpm1 := dpm1(:,0:27,:)
dpm2 := dpm2(:,0:27,:)
msf1 = dvm1
msf2 = dvm2
;msf1@_FillValue = 

do t = 0,60
    do lev = 0,27,1
        msf1(t,lev,:) = dim_sum_n(dvm1(t,lev:27,:)*dpm1(t,lev:27,:), 0)
        msf2(t,lev,:) = dim_sum_n(dvm2(t,lev:27,:)*dpm2(t,lev:27,:), 0)
    end do
end do
do yy = 0,360
    msf1(:,:,yy) = msf1(:,:,yy)*2*pi*cos(lat(yy)*pi/180.0)*a/g
    msf2(:,:,yy) = msf2(:,:,yy)*2*pi*cos(lat(yy)*pi/180.0)*a/g
end do
msf1!0 = "time"
msf1!1 = "lev"
msf1!2 = "lat"
msf1&time = time
msf1&lev = dv&level(0:27)
msf1&lat = lat
msf2!0 = "time"
msf2!1 = "lev"
msf2!2 = "lat"
msf2&time = time
msf2&lev  = dv&level(0:27)
msf2&lat  = lat
msf1 = where(ismissing(dvm1),dvm1@_FillValue , msf1)
msf2 = where(ismissing(dvm2),dvm2q@_FillValue , msf2)
system("rm -rf /data5/2019swh/data/stream_function.nc")
fout = addfile("/data5/2019swh/data/stream_function.nc","c")
filedimdef(fout, "time", -1, True)

fout->sf1 = msf1
fout->sf2 = msf2

end