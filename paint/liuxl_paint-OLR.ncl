;这波啊，这波是画OLR,绝对涡度零线，散度
begin
f = addfile("/data5/2019swh/data/composite_OLR_bandpass.nc","r")
a = addfile("/data5/2019swh/data/composite3.nc","r")
lon = a->lon
lat = a->lat
olr = f->OLR
u   = a->uwind
u925 = u(:,3,:,:)
v   = a->vwind
v925 = v(:,3,:,:)
u925 = where(ismissing(u925),0,u925)
v925 = where(ismissing(v925),0,v925)


char_day=(/"D0-30","D0-29","D0-28","D0-27","D0-26","D0-25","D0-24","D0-23","D0-22","D0-21","D0-20","D0-19","D0-18","D0-17","D0-16","D0-15","D0-14","D0-13","D0-12","D0-11","D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10","D0+11","D0+12","D0+13","D0+14","D0+15"/)



do day = 0,45
    vorticity = uv2vr_cfd(u(day,3,:,:), v(day,3,:,:), lat, lon, 2)
    do lat1 = 0,360
        vorticity(lat1,:)=vorticity(lat1,:) + coriolis_param(lat(lat1))
    end do
    vorticity = vorticity*1E+5
    vorticity!0 = "lat"
    vorticity!1 = "lon"
    vorticity&lat = lat
    vorticity&lon = lon

    div  = uv2dv_cfd(u925(day,:,:), v925(day,:,:), lat, lon, 2)
    div!0 = "lat"
    div!1 = "lon"
    div&lat = lat
    div&lon = lon
    div     = div*1E+5

    wks = gsn_open_wks("pdf", "/data5/2019swh/paint/day/OLR_bandpass_"+day)
    ;gsn_define_colormap(wks,"CBR_coldhot")
    gsn_define_colormap(wks,"temp_19lev")

    ;gsn_reverse_colormap(wks)
    res = True
    res@cnFillOn              = True     ; turn on color fill
    res@gsnDraw               = False
    res@gsnFrame              = False
    res@mpMinLatF            = -10 
    res@mpMaxLatF            =  30.
    res@mpMinLonF            =  30.
    res@mpMaxLonF            =  120.
    ;res@cnFillPalette         = "CBR_coldhot"
    res@cnLineLabelsOn        = False
    res@cnLinesOn             = False
    res@lbOrientation         = "Vertical"  
    res@cnInfoLabelOn         = False

    res@vpWidthF              = 0.6    
    res@vpHeightF             = 0.55
    res@mpGeophysicalLineThicknessF  = 1
    res@cnLevelSelectionMode = "ExplicitLevels" 
    res@cnLevels             =  ispan(-36, 0, 4) ;(/160,180,200,220,240,260/);(/280,260,240,220,200,180,160/);ispan(-2,36,1)
    res@cnFillColors         = (/2,3,4,5,6,7,8,9,10,11,0/) ;11,10,9,8,6,5,4,3/)
    ;res@cnLevelSpacingF      = 5
    res@gsnLeftString         = char_day(day)
    
    plot1 = gsn_csm_contour_map(wks,olr(day,:,:), res)  ; create plot

    ;画0线
    res2 = True
    res2@cnFillOn              = False 
    res2@cnLinesOn             = True  
    res2@gsnDraw               = False
    res2@gsnFrame              = False
    res2@cnLevelSelectionMode  =  "ExplicitLevels"
    
    res2@cnLevels             = (/0/)
    res2@gsnContourZeroLineThicknessF = 7.
    res2@cnInfoLabelOn         = False
    res2@cnLineLabelsOn        = False
    res2@cnMissingValPerimOn     = True            ; turn on the missing value perim
    res2@cnMissingValPerimColor  = "gray"           ; outline the perimeter red
    res2@cnMissingValFillPattern = 0               ; choose fill pattern 0 (solid fi
    res2@cnMissingValFillColor   = "gray"          ; color fill missing areas blue
    ;plot2  = gsn_csm_contour(wks, vorticity({-4:4},:), res2)
    ;画散度
    res3 = True
    res3@cnFillOn              = False     ; turn on color fill
    res3@gsnDraw               = False
    res3@gsnFrame              = False
    ;res3@cnFillPalette         = "MPL_coolwarm"
    res3@cnLineLabelsOn        = True
    ;res3@lbOrientation         = "Vertical"  
    res3@cnInfoLabelOn         = True
    ;res3@vpWidthF              = 0.6
    res3@cnLinesOn             = True
    res3@cnLineThicknessF      = 4
    res3@trGridType            = "TriangularMesh"
    ;res3@vpHeightF             = 0.55
    ;res@cnLevelSelectionMode       = "ExplicitLevels" 
    ;res@cnLevels             = ispan(-2,36,1)
    res3@cnLevelSpacingF      = 2
    res3@gsnRightString         = ""
    res3@cnLineColor            = "red"
    ;plot3 = gsn_csm_contour(wks,div(:,:), res3)

    polyres                   = True
    polyres@gsLineColor       = "black"
    polyres@gsLineThicknessF  = 5
    polyres@gsLineDashPattern = 2
    dum = gsn_add_polyline(wks, plot1, (/30,120/), (/0,0/), polyres)

    ;overlay(plot1, plot2)
    ;overlay(plot1,plot3)
    draw(plot1)
    frame(wks)



end do
end