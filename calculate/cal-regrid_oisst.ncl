;2021/3/30
;本代码使用ncl插值函数将OISST里面的数据插值到1*1°上
begin
f = addfile("/data5/2019swh/data/composite_OISST.nc","r")
sst = f->SST(:,:,{0:360})
lon = f->lon({0:360})
newlat = fspan(-90,90,181)
newlon = fspan(0,359,360)
newlat@units = "degrees_north"
newlon@units = "degrees_east"

sst2 = linint2_Wrap(lon, sst&lat, sst, True, newlon, newlat, 0)


sst2!0   ="time"
sst2!1   = "lat"
sst2!2   ="lon"
sst2&time = sst&time
sst2&lat = newlat
sst2&lon = newlon

sst3 = lonFlip(sst2)

fout = addfile("/data5/2019swh/data/composite_OISST_trans2.nc", "c")
filedimdef(fout, "time",-1, True)
fout->sst = sst2
end