;计算合成平均后的辐合辐散
begin
system("rm -rf div_vor.nc")
f = addfile("/data5/2019swh/data/composite3.nc","r")
lon = f->lon
lat = f->lat
u = f->uwind
v = f->vwind
div  =  uv2dv_cfd(u(:,:,:,:), v(:,:,:,:), lat, lon, 2)
vor  =  uv2vr_cfd(u(:,:,:,:), v(:,:,:,:), lat, lon, 2)
copy_VarCoords(u,div)


do lat1 = 0,360
        vor(:,:,lat1,:)=vor(:,:,lat1,:) + coriolis_param(lat(lat1))
end do
copy_VarCoords(u,vor)
fout = addfile("/data5/2019swh/data/div_vor.nc","c")
filedimdef(fout, "time", -1, True)
div@units = "s-1"
vor@units = "s-1"
div = div*1E+6
vor = vor*1E+5
fout->div = div
fout->vor = vor

fatt = True
fatt@description = "div*1E+6 vor*1E+5 "
fileattdef(fout, fatt)
end