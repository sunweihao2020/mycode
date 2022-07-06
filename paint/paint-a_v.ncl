;这波啊，这波是画OLR,绝对涡度零线，散度
begin
f = addfile("/data5/2019swh/data/composite_OLR_1021.nc","r")
a = addfile("/data5/2019swh/data/composite3.nc","r")
olr = f->OLR
u   = a->uwind
v   = a->vwind
lon = a->lon
lat = a->lat

char_day=(/"D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10"/)



do day = 20,40
    vorticity = uv2vr_cfd(u(day,3,:,:), v(day,3,:,:), lat, lon, 2)
    do lat1 = 0,360
        vorticity(lat1,:)=vorticity(lat1,:) + coriolis_param(lat(lat1))
    end do
    vorticity = vorticity*1E+5
    wks = gsn_open_wks("png", "/data5/2019swh/paint/day/av"+day)
    res2 = True
    res2@mpMinLatF            = -10 
    res2@mpMaxLatF            =  20.
    res2@mpMinLonF            =  75.
    res2@mpMaxLonF            =  115.
    res2@cnFillOn              = False 
    res2@cnLinesOn             = True  
    res2@gsnDraw               = False
    res2@gsnFrame              = False
    res2@cnLevelSelectionMode  =  "ExplicitLevels"
    res2@cnLevels             = (/0/)
    res2@gsnContourZeroLineThicknessF = 7.
    res2@cnInfoLabelOn         = False
    res2@cnLineLabelsOn        = False
    plot2  = gsn_csm_contour_map(wks, vorticity(:,:), res2)
    polyres                   = True
    polyres@gsLineColor       = "black"
    polyres@gsLineThicknessF  = 5
    polyres@gsLineDashPattern = 2
    dum = gsn_add_polyline(wks, plot2, (/30,150/), (/0,0/), polyres)

    draw(plot2)
    frame(wks)
end do
end