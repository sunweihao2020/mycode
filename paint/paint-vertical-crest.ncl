;这波啊，这波是画一个垂直的脊线图
begin
f = addfile("/data5/2019swh/data/mean_pentad_multilayer_0924.nc", "r")
u = f->uwind
t = f->T
umean = dim_avg_n_Wrap(u(:,:,:,416:448), 3)
tmean = dim_avg_n_Wrap(t(:,:,:,416:448), 3)

char_pen=(/"p22","p23","p24","p25","p26","p27","p28","p29","p30","p31","p32","p33","p34"/)

do ipen = 1,13
    wks = gsn_open_wks("png", "/data5/2019swh/paint/climatemean/vertival_crest_"+ipen)
    res   = True     
    res@gsnDraw     = False                                ; plot mods desired
    res@gsnFrame     =  False
    res@tiMainString      = "Vertical Crest" ; title
    res@gsnCenterString   = " "
    ;res@tiMainString    = "Ensemble Average 1987-89" ; title
    res@gsnLeftString         = char_pen(ipen-1) 
    ;res@cnLevelSpacingF = 0.3                        ; contour level spacing
    res@gsnContourZeroLineThicknessF = 8. 	          ; doubles thickness of zero contour
    res@gsnContourNegLineDashPattern = 1 		  ; sets negative contours to dash pattern 1
    res@cnFillOn        = True
    ;res@cnLevelSelectionMode       = "ExplicitLevels" 
    ;res@cnLevels             = ispan(-30,50,5)
    res@cnFillPalette         = "BlAqGrYeOrRe"
    res@gsnRightString        = ""
    res@cnMissingValPerimOn     = True            ; turn on the missing value perimeter
    res@cnMissingValPerimColor  = "black"           ; outline the perimeter red
    res@cnMissingValFillPattern = 0               ; choose fill pattern 0 (solid fill) 
    res@cnMissingValFillColor   = "black"          ; color fill missing areas blue

    plot  = gsn_csm_pres_hgt(wks, tmean(ipen-1,0:24,:), res )

    res2   =  True
    res2@gsnDraw     = False  
    res2@gsnFrame     =  False
    res2@tiMainString      = "" ; title
    res2@gsnCenterString   = " "
    ;res@tiMainString    = "Ensemble Average 1987-89" ; title
    ;res@gsnLeftString         = char_pen(ipen-1) 
    ;res@cnLevelSpacingF = 0.3                        ; contour level spacing
    res2@gsnContourZeroLineThicknessF = 10. 	          ; doubles thickness of zero contour
    res2@gsnContourNegLineDashPattern = 1 		  ; sets negative contours to dash pattern 1
    res2@cnFillOn        = False
    res2@cnLevelSelectionMode       = "ExplicitLevels" 
    res2@cnLevels             = (/0/)
    res2@cnFillPalette         = "BlAqGrYeOrRe"
    res2@cnInfoLabelOn         = False
    res2@gsnRightString        = ""
    res2@cnLineLabelsOn        =  False
    res2@cnMissingValPerimOn     = True            ; turn on the missing value perimeter
    res2@cnMissingValPerimColor  = "black"           ; outline the perimeter red
    res2@cnMissingValFillPattern = 0               ; choose fill pattern 0 (solid fill) 
    res2@cnMissingValFillColor   = "black"          ; color fill missing areas blue

    plot2  = gsn_csm_pres_hgt(wks, umean(ipen-1,:,{-5:30}), res2 )

    polyres                   = True
    polyres@gsLineColor       = "black"
    polyres@gsLineThicknessF  = 5
    polyres@gsLineDashPattern = 2
    dum = gsn_add_polyline(wks, plot, (/30,150/), (/0,0/), polyres)

    overlay(plot, plot2)
    
    draw(plot)
    frame(wks)

end do
end