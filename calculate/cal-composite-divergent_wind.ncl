;2021/4/9
;本代码使用10m风场，计算底层的涡度和散度风等物理量
;使用数据 composite_u10v10 
begin
f = addfile("/data/composite_u10v10.nc","r")

u = f->u10m
v = f->v10m

;一、先计算散度风
; 计算散度
div = uv2dv_cfd(u, v, u&lat, u&lon, 3)
uvd = dv2uvF(div)

;计算旋转风
vor = uv2vr_cfd(u, v, u&lat, u&lon, 3)
uvr = vr2uvF(vor)

ud = uvd(0,:,:,:)
vd = uvd(1,:,:,:)

ur = uvr(0,:,:,:)
vr = uvr(1,:,:,:)

copy_VarCoords(u, ud)
copy_VarCoords(u, vd)
copy_VarCoords(u, ur)
copy_VarCoords(u, vr)
copy_VarCoords(u, div)
copy_VarCoords(u, vor)

fout = addfile("/data/10m_divergent_rotational_wind.nc","c")
filedimdef(fout, "time",-1, True)


fout->ud = ud
fout->vd = vd
fout->ur = ur
fout->vr = vr
fout->div = div
fout->vor = vor

end
