;这波啊，这波是画OLR,绝对涡度零线，散度
begin
f = addfile("/data5/2019swh/data/composite_OLR_1021.nc","r")
a = addfile("/data5/2019swh/data/composite3.nc","r")
c = addfile("/data5/2019swh/data/divergence.nc","r")
lon = a->lon
lat = a->lat
olr = f->OLR
u   = a->uwind
v   = a->vwind
div = c->div
div = div*1E+6



char_day=(/"D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10"/)



do day = 20,40
    vorticity = uv2vr_cfd(u(day,3,:,:), v(day,3,:,:), lat, lon, 2)
    do lat1 = 0,360
        vorticity(lat1,:)=vorticity(lat1,:) + coriolis_param(lat(lat1))
    end do
    vorticity = vorticity*1E+5
    vorticity!0 = "lat"
    vorticity!1 = "lon"
    vorticity&lat = lat
    vorticity&lon = lon


    wks = gsn_open_wks("png", "/data5/2019swh/paint/day/OLR"+day)

    res = True
    res@cnFillOn              = True     ; turn on color fill
    res@gsnDraw               = False
    res@gsnFrame              = False
    res@mpMinLatF            = -10 
    res@mpMaxLatF            =  20.
    res@mpMinLonF            =  60.
    res@mpMaxLonF            =  115.

    res@cnLineLabelsOn        = False
    res@lbOrientation         = "Vertical"  
    res@cnInfoLabelOn         = False 
    res@vpWidthF              = 0.6
    res@cnLinesOn             = False
    res@vpHeightF             = 0.55
    res@mpGeophysicalLineThicknessF  = 1
    res@cnLevelSelectionMode  = "ExplicitLevels"
    res@cnLevels             =  ispan(170, 270, 10) ;(/160,180,200,220,240,260/);(/280,260,240,220,200,180,160/);ispan(-
    res@cnFillPalette         = "CBR_coldhot"
    res@gsnLeftString         = char_day(day-20)
    
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
    plot2  = gsn_csm_contour(wks, vorticity({-4:4},:), res2)
    ;画散度
    res3 = True
    res3@cnFillOn              = False     ; turn on color fill
    res3@gsnDraw               = False
    res3@gsnFrame              = False
    res3@cnLineLabelsOn        = True
    res3@cnInfoLabelOn         = False 
    res3@vpWidthF              = 0.6
    res3@cnLineLabelBackgroundColor = -1
    res3@cnLinesOn             = True
    res3@gsnContourZeroLineThicknessF = 5
    res3@gsnContourNegLineDashPattern = 1
    res3@gsnRightString        = ""
    res3@gsnLeftString         = ""
    res3@cnLineThicknessF      = 3
    res3@cnLineColor           = "white" 
    res3@vpHeightF             = 0.55
    ;res3@mpGeophysicalLineThicknessF  = 1
    res3@cnLevelSelectionMode       = "ExplicitLevels" 
    res3@cnLevels             = ispan(-4,2,2)
    res3@cnLineLabelDensityF  = 1
    res3@cnLineLabelInterval  = 1
    res3@cnLevelSpacingF      = 2.5
    plot3 = gsn_csm_contour(wks,div(day,3,:,:), res3)  ; create plot

    polyres                   = True
    polyres@gsLineColor       = "black"
    polyres@gsLineThicknessF  = 5
    polyres@gsLineDashPattern = 2
    dum = gsn_add_polyline(wks, plot1, (/60,115/), (/0,0/), polyres)


    overlay(plot1, plot2)
    overlay(plot1,plot3)
    draw(plot1)
    frame(wks)



end do
end