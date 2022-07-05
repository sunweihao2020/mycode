;2021/5/29
;本代码计算地转偏差以及地转偏差的角度
begin
system("rm /data5/2019swh/data/geostrophic_deviation.nc")
f1 = addfile("/data5/2019swh/data/composite3.nc","r")
u  =  f1->uwind
v  =  f1->vwind
h  =  f1->H

uv =  z2geouv(h, h&lat, h&lon, 1)

ud =  u-uv(0,:,:,:,:)
vd =  v-uv(1,:,:,:,:)

u1 = uv(0,:,:,:,:)
v1 = uv(1,:,:,:,:)

copy_VarCoords(u, ud)
copy_VarCoords(v, vd)

deviation  =  sqrt(ud^2+vd^2)
cosu       =  ud/deviation
copy_VarCoords(h, deviation)
copy_VarCoords(h, cosu)


fout = addfile("/data5/2019swh/data/geostrophic_deviation.nc","c")
filedimdef(fout, "time",-1, True)


fout->u_deviation = ud
fout->v_deviation = vd
fout->deviation   = deviation
fout->cosu        = cosu


end