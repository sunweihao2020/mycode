;这波啊，这波是计算u的垂直剖面图  候平均
begin
f = addfile("/data5/2019swh/data/mean_pentad_multilayer_0924.nc","r")
u = f->uwind
umean = dim_avg_n_Wrap(u(:,:,:,416:448), 3)
char_pen=(/"p22","p23","p24","p25","p26","p27","p28","p29","p30","p31","p32","p33","p34"/)

do ipen = 1,13
    wks = gsn_open_wks("png", "/data5/2019swh/paint/climatemean/height_pressure_u_vertival_"+ipen)
    res   = True                                     ; plot mods desired
    res@tiMainString      = "Pressure/Height U Field" ; title
    res@gsnCenterString   = " "
    ;res@tiMainString    = "Ensemble Average 1987-89" ; title
    res@gsnLeftString         = char_pen(ipen-1) 
    ;res@cnLevelSpacingF = 0.3                        ; contour level spacing
    res@gsnContourZeroLineThicknessF = 4. 	          ; doubles thickness of zero contour
    res@gsnContourNegLineDashPattern = 1 		  ; sets negative contours to dash pattern 1
    res@cnFillOn        = True
    res@cnLevelSelectionMode       = "ExplicitLevels" 
    res@cnLevels             = ispan(-30,50,5)
    res@cnFillPalette         = "BlAqGrYeOrRe"
    res@cnMissingValPerimOn     = True            ; turn on the missing value perimeter
    res@cnMissingValPerimColor  = "black"           ; outline the perimeter red
    res@cnMissingValFillPattern = 0               ; choose fill pattern 0 (solid fill) 
    res@cnMissingValFillColor   = "black"          ; color fill missing areas blue

    plot  = gsn_csm_pres_hgt(wks, umean(ipen-1,0:24,:), res )

end do
end