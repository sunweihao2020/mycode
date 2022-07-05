;这波啊，这波是计算一下地转风以用于和python的验证
;所用函数为：z2geouv http://www.ncl.ucar.edu/Document/Functions/Built-in/z2geouv.shtml
begin
a   = addfile("/data1/MERRA2/daily/plev/1993/MERRA2_200.inst3_3d_asm_Np.19930820.SUB.nc","r")
b   = addfile("/data5/2019swh/data/ug.nc","r")
ug  = b->uwind
lon = a->lon
lat = a->lat
level = a->level
time = a->time
h   = a->H
uv  = z2geouv(h, lat, lon, 1)
u   = uv(0,:,:,:,:)
v   = uv(1,:,:,:,:)
u@units     = "m/s"
v@units     = "m/s"

u!0 = "time"
u!1 = "lev"
u!2 = "lat"
u!3 = "lon"

u&time = time
u&lev  = level
u&lat  = lat
u&lon  = lon


v!0 = "time"
v!1 = "lev"
v!2 = "lat"
v!3 = "lon"

v&time = time
v&lev  = level
v&lat  = lat
v&lon  = lon

wks = gsn_open_wks("png","~/test/test1")               ; send graphics to PNG file
wks2 = gsn_open_wks("png","~/test/test2")

v1 = gsn_csm_contour_map(wks,u(10,16,:,:),False)
v2 = gsn_csm_contour_map(wks2,ug(10,16,:,:),False)

end