;这波啊，这波是画一下垂直的P
;乘以 10e+6
begin
a = addfile("/data5/2019swh/data/mean_pentad_multilayer_0924.nc","r")
epv = a->EPV
lat = a->lat
lon = a->lon
lev = a->level

epvm = dim_avg_n_Wrap(epv(:,:,:,{80:100}), 3)
epvm = epvm*1E+6
char_pen=(/"Apr 16-20","Apr 21-25","Apr 26-30","May 01-05","May 06-10","May 11-15","May 16-20","May 21-25","May 26-30","May 31-Jun 04","Jun 05-09","Jun 10-14","Jun 15-19"/)
char_pen2=(/"p22","p23","p24","p25","p26","p27","p28","p29","p30","p31","p32","p33","p34"/)

do ipen = 1,13
    wks = gsn_open_wks("png", "/data5/2019swh/paint/pentad/vertival_P2_"+ipen)
    res   = True
    res@gsnDraw     = False                                ; plot mods desired
    res@gsnFrame     =  False
    res@tiMainString    =  "PV (80-100E)"
    res@gsnLeftString   =  char_pen(ipen-1)
    res@gsnContourZeroLineThicknessF = 8
    res@gsnContourNegLineDashPattern = 1
    res@cnLevelSpacingF       =0.1
    ;res@gsnRightString        =  "10~S~-6~N~"
    res@cnFillOn        = True
    ;res@cnLevelSelectionMode       = "ExplicitLevels" 
    ;res@cnLevels             = ispan(-30,50,5)
    res@cnFillPalette         = "BlAqGrYeOrRe"
    res@gsnRightString        = ""
    res@cnMissingValPerimOn     = True            ; turn on the missing value perimeter
    res@cnMissingValPerimColor  = "gray"           ; outline the perimeter red
    res@cnMissingValFillPattern = 0               ; choose fill pattern 0 (solid fill) 
    res@cnMissingValFillColor   = "gray"          ; color fill missing areas blue

    plot = gsn_csm_pres_hgt(wks,epvm(ipen-1,0:24,{-8:12}) , res)
    polyres                   = True
    polyres@gsLineColor       = "black"
    polyres@gsLineThicknessF  = 5
    polyres@gsLineDashPattern = 2
    dum = gsn_add_polyline(wks, plot, (/0,0/), (/1000,100/), polyres)
    draw(plot) ;delete(dum)
    frame(wks)
end do

end

