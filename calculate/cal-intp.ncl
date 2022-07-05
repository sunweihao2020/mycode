;2020/11/21
;将资料插值到等熵面（位温）上
;merra2合成资料
;多层次
begin
system("rm -rf /data5/2019swh/data/isentropic_theate_data.nc")
f   =   addfile("/data5/2019swh/data/composite_equivalent_tem.nc","r")
pt1 =   f->theate_e(:,3:17,:,:)
f2  =   addfile("/data5/2019swh/data/ugvg.nc","r")
ug  =   f2->ug(:,3:17,:,:)
vg  =   f2->vg(:,3:17,:,:)
f3  =   addfile("/data5/2019swh/data/composite3.nc","r")
u   =   f3->uwind(:,3:17,:,:)
v   =   f3->vwind(:,3:17,:,:)

lvl =   (/302,304,308,312,316,320,324,328,332/)
lvl@units = "K"
ug1 =   int2p_n(pt1, ug, lvl, 1, 1)
ug1!0 = "time"
ug1!1 = "lev"
ug1!2 = "lat"
ug1!3 = "lon"
ug1&time = ug&time
ug1&lev  = lvl
ug1&lat  = ug&lat
ug1&lon  = ug&lon
vg1 =   int2p_n(pt1, vg, lvl, 1, 1)
vg1!0 = "time"
vg1!1 = "lev"
vg1!2 = "lat"
vg1!3 = "lon"
vg1&time = ug&time
vg1&lev  = lvl
vg1&lat  = ug&lat
vg1&lon  = ug&lon
u1  =   int2p_n(pt1, u, lvl, 1, 1)
u1!0 = "time"
u1!1 = "lev"
u1!2 = "lat"
u1!3 = "lon"
u1&time = ug&time
u1&lev  = lvl
u1&lat  = ug&lat
u1&lon  = ug&lon
v1  =   int2p_n(pt1, v, lvl, 1, 1)
v1!0 = "time"
v1!1 = "lev"
v1!2 = "lat"
v1!3 = "lon"
v1&time = ug&time
v1&lev  = lvl
v1&lat  = ug&lat
v1&lon  = ug&lon

fout = addfile("/data5/2019swh/data/isentropic_theate_data.nc","c")
filedimdef(fout, "time",-1, True)

;fout->lat = ug&lat
;fout->lon = ug&lon
;fout->time = ug&time
;fout->level = lvl
fout->uwind = u1
fout->vwind = v1
fout->ug    = ug1
fout->vg    = vg1

end

