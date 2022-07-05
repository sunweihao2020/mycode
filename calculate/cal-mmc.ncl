begin
;;;这波啊，这波计算一个流函数
a = addfile("/data5/2019swh/data/mean_pentad_multilayer_0924.nc","r")
b = addfile("/data5/2019swh/data/mean_pentad_PS_0929.nc","r")
ps= b->PS
p = a->level
lat = a->lat
p(0) = 1004
p = p*100
p@units = "Pa"
lon = a->lon
lev = a->level
t = a->T
omega = a->OMEGA
v     = a->vwind
v(:,0,:,:)  =  0
v&level(0) = 1004
dec = t-273.15
;psm = dim_avg_n_Wrap(ps(:,:,416:448), 2)
copy_VarCoords(t, dec)
char_pen=(/"p22","p23","p24","p25","p26","p27","p28","p29","p30","p31","p32","p33","p34"/)

mpsi = new((/13,32,361/),double)
do ipen =  1,13
    mpsi(ipen-1,:,:) = zonal_mpsi(v(ipen-1,0:31:-1,:,416:448), lat, p(0:31:-1), ps(ipen-1,:,416:448))
end do
mpsi!0 = "time"
mpsi!1 = "lev"
mpsi!2 = "lat"
mpsi&lev = p(0:31:-1)
mpsi&lat = lat
mpsi = mpsi/1E+9
;print(mpsi&lev)
;printVarSummary(mpsi)
;exit

;exit
;mpsi(:.{})
do ipen = 1,13
    wks = gsn_open_wks("png", "/data5/2019swh/paint/pentad/streamfunction_2_"+ipen)
    res   = True                                     ; plot mods desired
    ;res@tiMainString    = "Ensemble Average 1987-89" ; title
    res@gsnLeftString         = char_pen(ipen-1) 
    res@gsnRightString        = " "
    res@tiMainString          = "streamfunction"
    res@cnLevelSpacingF = 10                        ; contour level spacing
    res@cnLevelSelectionMode       = "ExplicitLevels" 
    res@cnLevels             = ispan(-1000,1000,40)
    res@gsnContourZeroLineThicknessF = 2. 	          ; doubles thickness of zero contour
    res@gsnContourNegLineDashPattern = 1 		  ; sets negative contours to dash pattern 1
    res@cnFillOn        = True
    res@cnLineLabelsOn  = True
    res@cnLineLabelInterval = 3
    res@cnLineLabelBackgroundColor = -1
    res@cnFillPalette         = "BlAqGrYeOrRe"
    res@cnMissingValPerimOn     = True            ; turn on the missing value perimeter
    res@cnMissingValPerimColor  = "black"           ; outline the perimeter red
    res@cnMissingValFillPattern = 0               ; choose fill pattern 0 (solid fill) 
    res@cnMissingValFillColor   = "black"          ; color fill missing areas blue

    plot  = gsn_csm_pres_hgt(wks, mpsi(ipen-1,17:,:), res )

end do
end