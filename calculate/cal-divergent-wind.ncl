;2020/11/5
;所用资料：merra2季风爆发合成分析
;要素：垂直流函数（80-90）（（90-100）
;level : 纬向垂直剖面图
begin
system("rm -rf /data5/2019swh/data/divergent_wind.nc")
f = addfile("/data5/2019swh/data/composite3.nc","r")
f2 = addfile("/data5/2019swh/data/div_vor.nc","r")
lon = f->lon
lat = f->lat
dv = f2->div
dv = dv/1E+6
u = f->uwind
u = where(ismissing(u), 0, u)
v = f->vwind
v = where(ismissing(v), 0, v)
dv = where(ismissing(dv), 0, dv)

ud    = new ( dimsizes(dv),typeof(dv))	; zonal divergent wind 
vd    = new ( dimsizes(dv),typeof(dv))	; meridional divergent wind
ud    = 0
vd    = 0
dv2uvf(dv,ud,vd)
copy_VarCoords(v, vd)
copy_VarCoords(u, ud)
fout = addfile("/data5/2019swh/data/divergent_wind.nc","c")
filedimdef(fout, "time", -1, True)

fout->dv = vd
fout->du = ud

end
