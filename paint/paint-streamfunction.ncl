begin
f = addfile("/data5/2019swh/data/stream_function.nc", "r")
sf1 = f->sf1
sf1 = sf1/10^10
sf2 = f->sf2
sf2 = sf2/10^10
char_day=(/"D0-15","D0-14","D0-13","D0-12","D0-11","D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10","D0+11","D0+12","D0+13","D0+14","D0+15"/)



do day = 15,45
    wks = gsn_open_wks("pdf", "/data5/2019swh/paint/day/streamfunction_sf1_"+day)
    wks2 = gsn_open_wks("pdf", "/data5/2019swh/paint/day/streamfunction_sf2_"+day)
    res   = True                                     ; plot mods desired
    ;res@gsnDraw = False
    ;res@gsnFrame= False
    ;res@gsnLeftString         = char_pen(ipen-1) 
    res@gsnRightString        = " "
    res@cnMissingValPerimOn     = True   
    res@cnMissingValPerimColor  = "gray" 
    res@cnMissingValFillPattern = 0      
    res@cnMissingValFillColor   = "gray" 
    res@tiMainString          = "80-90E"
    res@gsnLeftString         = char_day(day-15)
    res@cnLevelSelectionMode       = "ExplicitLevels" 
    res@cnLevels             = ispan(-24,24,4)
    res@gsnContourZeroLineThicknessF = 5 	          ; doubles thickness of zero contour
    res@gsnContourNegLineDashPattern = 1 		  ; sets negative contours to dash pattern 1
    res@cnFillOn        = True
    res@cnLineLabelsOn  = True
    res@cnLineLabelInterval = 3
    res@cnLineLabelBackgroundColor = -1
    res@cnFillPalette         = "temp_19lev"

    res2   = res
    res2@tiMainString     = "90-100E"
    plot1  = gsn_csm_pres_hgt(wks, sf1(day,:,:), res )
    plot2  = gsn_csm_pres_hgt(wks2, sf2(day,:,:), res2 )
end do
end


   