;2020/11/18 2021/1/18
;GPCP降水的合成平均
;单层（总降水）
begin
f = addfile("/data5/2019swh/data/composite_GPCP.nc","r")
pre = f->precipitation
pre = where(pre .lt. 0,pre@_FillValue,pre)
char_day=(/"D0-30","D0-29","D0-28","D0-27","D0-26","D0-25","D0-24","D0-23","D0-22","D0-21","D0-20","D0-19","D0-18","D0-17","D0-16","D0-15","D0-14","D0-13","D0-12","D0-11","D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10","D0+11","D0+12","D0+13","D0+14","D0+15"/)

plot = new(15,graphic)
dum  = new(15,graphic)
wks = gsn_open_wks("pdf","/data5/2019swh/paint/day/GPCP_prect")

do day = 0,14
    res = True
    res@gsnDraw               = False
    res@gsnFrame              = False
    res@cnFillOn              = True     ; turn on color fill
    res@cnFillPalette         = "MPL_Blues"
    res@cnLineLabelsOn        = False
    res@lbLabelsOn            = False
    res@lbLabelBarOn          = False
    res@cnLevelSelectionMode       = "ExplicitLevels" 
    res@cnLevels             = ispan(2,26,4)
    res@mpMinLatF            = -10      ; range to zoom in on
    res@mpMaxLatF            =  30.
    res@mpMinLonF            =  30.
    res@mpMaxLonF            = 120.
    
    res@gsnRightString        = "mm/day"
    res@gsnLeftString         = char_day(day)
    res@gsnStringFont         = 2
    res@tmYLLabelFontHeightF      = 0.024
    res@tmXBLabelFontHeightF      = 0.024
    ;res@tmYLLabelDeltaF = -0.6  ;坐标值跑出去了就调这个

    res@cnInfoLabelOn         = False
    plot(day) = gsn_csm_contour_map(wks,pre(day,:,:), res)  ; create plot
  
    polyres                   = True
    polyres@gsLineColor       = "black"
    polyres@gsLineThicknessF  = 3
    polyres@gsLineDashPattern = 2
    dum(day) = gsn_add_polyline(wks, plot(day), (/30,120/), (/0,0/), polyres)
    
end do
pnlres = True
pnlres@gsnPanelMainString = "precipitation"
pnlres@gsnPanelLabelBar  = True
pnlres@gsnPanelDebug     = True     ; To get information from panel
pnlres@pmLabelBarWidthF  = 0.55
pnlres@lbLabelFontHeightF = 0.012
gsn_panel(wks,plot,(/5,3/),pnlres)
;frame(wks)

end