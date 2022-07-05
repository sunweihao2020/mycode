;;;这波啊，这波是计算80-100E的纬向平均的温度垂直-经向剖面图
begin
f = addfile("/data5/2019swh/data/mean_merra2_multilayer_0921.nc","r")
t = f->T
char_mon=(/"Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"/)
tmean= dim_avg_n_Wrap(t(:,:,:,0:48), 3)
dec = tmean-273.15
copy_VarCoords(tmean, dec)
do imon = 1,12
    wks = gsn_open_wks("png", "/data5/2019swh/paint/climatemean/height_pressure_T2_"+imon)
    res   = True                                     ; plot mods desired
    ;res@tiMainString    = "Ensemble Average 1987-89" ; title
    res@gsnLeftString         = char_mon(imon-1) 
    res@gsnRightString        = "units:degC"
    res@tiMainString          = "vertical temperature constructure"
    res@cnLevelSpacingF = 4                        ; contour level spacing
    res@cnLevelSelectionMode       = "ExplicitLevels" 
    res@cnLevels             = ispan(-72,36,4)
    res@gsnContourZeroLineThicknessF = 2. 	          ; doubles thickness of zero contour
    res@gsnContourNegLineDashPattern = 1 		  ; sets negative contours to dash pattern 1
    res@cnFillOn        = True
    res@cnFillPalette         = "BlAqGrYeOrRe"
    res@cnMissingValPerimOn     = True            ; turn on the missing value perimeter
    res@cnMissingValPerimColor  = "black"           ; outline the perimeter red
    res@cnMissingValFillPattern = 0               ; choose fill pattern 0 (solid fill) 
    res@cnMissingValFillColor   = "black"          ; color fill missing areas blue

    plot  = gsn_csm_pres_hgt(wks, dec(imon-1,0:24,:), res )

end do
end