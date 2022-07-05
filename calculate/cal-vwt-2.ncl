;2020/11/30
;merra2合成分析资料
;绘制多个经度剖面的垂直风场图
;72.5 75 77.5 80 (404 408 412 416) 
begin
;;;这波啊，这波画个逐月的和逐候的流场图、流函数
a = addfile("/data5/2019swh/data/composite3.nc","r")
p = a->level
lat = a->lat
;lon = a->lon
lev = a->level
t = a->T
omega = a->OMEGA
v     = a->vwind
dec = t-273.15
copy_VarCoords(t, dec)
char_day=(/"D0-15","D0-14","D0-13","D0-12","D0-11","D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10","D0+11","D0+12","D0+13","D0+14","D0+15"/)

lon = (/404,408,412,416/)
lons = (/"72.5E","75E","77.5E","80E"/)
p1 = conform(omega,p,1)      ; comform_dim()
p1 = p1*100
p1@units = "Pa"
copy_VarCoords(omega, p1)
w = omega_to_w(omega,p1,t)
w = w*100


do x = 0,3
    do iday = 15,35
    wks = gsn_open_wks("png", "/data5/2019swh/paint/day/wvt_"+iday+"_"+lons(x))
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
    res@gsnLeftString     = char_day(iday-15)
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

    plot  = gsn_csm_pres_hgt_streamline(wks,dec(iday,0:22,{-10:45},lon(x)),v(iday,0:22,{-10:45},lon(x)),w(iday,0:22,{-10:45},lon(x)),res )  
    end do
end do
end