;2020/12/17
;这波啊，这波是画一下垂直的P
;乘以 10e+6
begin
f1 = addfile("/data5/2019swh/data/dpv_mpv.nc","r")
dpv = f1->DPV
mpv = f1->MPV


dpvm = dim_avg_n_Wrap(dpv(:,:,:,{80:100}), 3)
mpvm = dim_avg_n_Wrap(mpv(:,:,:,{80:100}), 3)

dpvm = dpvm*1E+6
mpvm = mpvm*1E+6
char_day=(/"D0-15","D0-14","D0-13","D0-12","D0-11","D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10","D0+11","D0+12","D0+13","D0+14","D0+15"/)

do iday = 15,35
    wks = gsn_open_wks("pdf", "/data5/2019swh/paint/day/DPV_"+iday)
    res   = True
    res@gsnDraw     = False                                ; plot mods desired
    res@gsnFrame     =  False
    res@tiMainString    =  "DPV (80-100E)"
    res@gsnContourZeroLineThicknessF = 8
    res@gsnContourNegLineDashPattern = 1
    ;res@cnLevelSpacingF       =0.1
    ;res@gsnRightString        =  "10~S~-6~N~"
    res@cnFillOn        = True
    ;res@cnLevelSelectionMode       = "ExplicitLevels" 
    ;res@cnLevels             = ispan(-30,50,5)
    res@cnFillPalette         = "BlAqGrYeOrRe"
    res@gsnLeftString         = char_day(iday-15)
    res@gsnRightString        = ""
    res@cnMissingValPerimOn     = True            ; turn on the missing value perimeter
    res@cnMissingValPerimColor  = "gray"           ; outline the perimeter red
    res@cnMissingValFillPattern = 0               ; choose fill pattern 0 (solid fill) 
    res@cnMissingValFillColor   = "gray"          ; color fill missing areas blue

    plot = gsn_csm_pres_hgt(wks,dpvm(iday,0:24,{-8:12}) , res)
    polyres                   = True
    polyres@gsLineColor       = "black"
    polyres@gsLineThicknessF  = 5
    polyres@gsLineDashPattern = 2
    dum = gsn_add_polyline(wks, plot, (/0,0/), (/1000,100/), polyres)
    draw(plot) ;delete(dum)
    frame(wks)
end do

end

