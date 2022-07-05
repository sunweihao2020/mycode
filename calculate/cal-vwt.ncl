begin
;;;这波啊，这波画个逐月的和逐候的流场图、流函数
a = addfile("/data5/2019swh/data/mean_pentad_vwt_0926.nc","r")
p = a->level
lat = a->lat
;lon = a->lon
lev = a->level
t = a->T
omega = a->OMEGA
v     = a->V
dec = t-273.15
copy_VarCoords(t, dec)
char_pen=(/"p22","p23","p24","p25","p26","p27","p28","p29","p30","p31","p32","p33","p34"/)

;w = omega_to_w(omega,p,t)


p1 = conform(omega,p,1)      ; comform_dim()
copy_VarCoords(omega, p1)
w = omega_to_w(omega,p1,t)
w = w*(-100)
do ipen = 1,13
    wks = gsn_open_wks("png", "/data5/2019swh/paint/climatemean/height_pressure_wvt_"+ipen)
    res   = True                                     ; plot mods desired
    res@tiMainString      = "Pressure/Height Streamline" ; title
    res@gsnCenterString   = " "

    res@cnFillOn          = True                ; turn on color fill
    res@cnFillPalette     = "BlAqGrYeOrReVi200" ; choose color map
    res@cnLineLabelsOn    = False               ; turn off line labels
    res@lbLabelStride     = 2                   ; label every other box
    res@cnLevelSelectionMode       = "ExplicitLevels" 
    res@cnLevels             = ispan(-72,36,4)
    res@cnMissingValPerimOn     = True            ; turn on the missing value perimeter
    res@gsnLeftString     = char_pen(ipen-1)
    res@cnLinesOn         = False
    res@gsnRightString    = "units:degC"
    res@cnMissingValPerimColor  = "black"           ; outline the perimeter red
    res@cnMissingValFillPattern = 0               ; choose fill pattern 0 (solid fill) 
    res@cnMissingValFillColor   = "black"          ; color fill missing areas blue
    
    res@stLevelSelectionMode  =  "ManualLevels"
    ;res@stLevelSpacingF       =  8
    res@stMinLineSpacingF  = 0.005
   ; res@stMinArrowSpacingF = 0.5
    res@stMinArrowSpacingF = 0.02             ; arrow spacing.
    res@stArrowLengthF     = 0.008             ; arrow length
    res@stMinDistanceF     = 0.05
;=========下面是画等值线的设置    
    ;res@tiMainString    = "Ensemble Average 1987-89" ; title
    ;res@gsnLeftString         = char_pen(ipen-1) 
    ;res@cnLevelSpacingF = 0.3                        ; contour level spacing
    ;res@gsnContourZeroLineThicknessF = 2. 	          ; doubles thickness of zero contour
    ;res@gsnContourNegLineDashPattern = 1 		  ; sets negative contours to dash pattern 1
    ;res@cnFillOn        = True
    ;res@cnFillPalette         = "BlAqGrYeOrRe"
    ;res@cnMissingValPerimOn     = True            ; turn on the missing value perimeter
    ;res@cnMissingValPerimColor  = "black"           ; outline the perimeter red
    ;res@cnMissingValFillPattern = 0               ; choose fill pattern 0 (solid fill) 
    ;res@cnMissingValFillColor   = "black"          ; color fill missing areas blue
;

    plot  = gsn_csm_pres_hgt_streamline(wks,dec(ipen-1,0:26,:),v(ipen-1,0:26,:),w(ipen-1,0:26,:),res )  
end do
end