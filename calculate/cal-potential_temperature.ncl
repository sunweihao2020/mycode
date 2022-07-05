;2020/11/12
;merra2合成分析资料
;计算位温和相当位温
;61个时次
begin
f1 = addfile("/data5/2019swh/data/composite3.nc","r")
f2 = addfile("/data5/2019swh/data/composite_rh.nc","r")
t = f1->T
p = f1->level
rh = f2->RH
pt1 = pot_temp(p, t, 1, False)
pt2 = pot_temp_equiv(p, t, rh, 1, "rh")

fout = addfile("/data5/2019swh/data/potential_temperature.nc","c")
filedimdef(fout, "time", -1, True)

fout->pt = pt1
fout->ept = pt2

end