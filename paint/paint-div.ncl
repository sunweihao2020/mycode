;2020/11/1 2020/11/14
begin
f = addfile("/data5/2019swh/data/divergence.nc","r")
div = f->div
div = div*1E+6

char_day=(/"D0-15","D0-14","D0-13","D0-12","D0-11","D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10","D0+11","D0+12","D0+13","D0+14","D0+15"/)

do day = 15,35
    wks = gsn_open_wks("png", "/data5/2019swh/paint/day/divergence_wind_"+day)
    res3 = True
    res3@cnFillOn              = False     ; turn on color fill
    res3@gsnDraw               = False
    res3@gsnFrame              = False
    res3@mpMinLatF            = -10 
    res3@mpMaxLatF            =  20.
    res3@mpMinLonF            =  75.
    res3@mpMaxLonF            =  115.
    res3@cnFillPalette         = "CBR_coldhot"
    res3@cnLineLabelsOn        = True
    res3@lbOrientation         = "Vertical"  
    res3@cnInfoLabelOn         = False 
    res3@vpWidthF              = 0.6
    res3@cnLinesOn             = True
    res3@gsnContourZeroLineThicknessF = 5
    res3@gsnContourNegLineDashPattern = 1
    res3@cnLineThicknessF      = 5
    res3@cnLineColor           = "red" 
    res3@vpHeightF             = 0.55
    res3@mpGeophysicalLineThicknessF  = 1
    res3@cnLevelSelectionMode       = "ExplicitLevels" 
    res3@cnLevels             = ispan(-4,2,2)
    res3@cnLineLabelDensityF  = 2
    res3@cnLineLabelInterval  = 1
    res3@cnLevelSpacingF      = 2
    res3@cnLineLabelFontAspectF = 2
    res3@gsnLeftString         = char_day(day-20)
    plot1 = gsn_csm_contour_map(wks,div(day,3,:,:), res3)  ; create plot

    polyres                   = True
    polyres@gsLineColor       = "black"
    polyres@gsLineThicknessF  = 5
    polyres@gsLineDashPattern = 2
    dum = gsn_add_polyline(wks, plot1, (/75,115/), (/0,0/), polyres)

    draw(plot1)
    frame(wks)
end do
end