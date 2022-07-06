;2021/4/25
;本代码绘制merra2和trmm的合成降水分析
;使用资料：composite-precipitation_trmm.nc composite-precipitation_merra.nc
begin
f1     = addfile("/data5/2019swh/data/composite-precipitation_trmm.nc","r")
pre1_0 = f1->precipitation
pre1   = pre1_0(time|:,lat|:,lon|:)
printVarSummary(pre1)

f2      = addfile("/data5/2019swh/data/composite-precipitation_merra.nc","r")
pre2    = f2->precipitation

char_day=(/"D0-30","D0-29","D0-28","D0-27","D0-26","D0-25","D0-24","D0-23","D0-22","D0-21","D0-20","D0-19","D0-18","D0-17","D0-16","D0-15","D0-14","D0-13","D0-12","D0-11","D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10","D0+11","D0+12","D0+13","D0+14","D0+15"/)

plot1 = new(15,graphic)
dum1  = new(15,graphic)
plot2 = new(15,graphic)
dum2  = new(15,graphic)
wks1 = gsn_open_wks("pdf","/data5/2019swh/paint/day/precipitation_trmm")
wks2 = gsn_open_wks("pdf","/data5/2019swh/paint/day/precipitation_merra2")


do day = 16,30
    res = True
    res@gsnDraw               = False
    res@cnLinesOn             = False
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
    plot1(day-16) = gsn_csm_contour_map(wks1,pre1(day,:,:), res)  
    plot2(day-16) = gsn_csm_contour_map(wks2,pre2(day,:,:), res) 
  
    polyres                   = True
    polyres@gsLineColor       = "black"
    polyres@gsLineThicknessF  = 2
    polyres@gsLineDashPattern = 2
    dum1(day-16) = gsn_add_polyline(wks1, plot1(day-16), (/30,120/), (/0,0/), polyres)
    dum2(day-16) = gsn_add_polyline(wks2, plot2(day-16), (/30,120/), (/0,0/), polyres)
    
end do
pnlres = True
pnlres@gsnPanelMainString = "precipitation (TRMM)"
pnlres@gsnPanelLabelBar  = True
pnlres@gsnPanelDebug     = True     ; To get information from panel
pnlres@pmLabelBarWidthF  = 0.55
pnlres@lbLabelFontHeightF = 0.012
gsn_panel(wks1,plot1,(/5,3/),pnlres)
pnlres@gsnPanelMainString = "precipitation (MERRA2)"
gsn_panel(wks2,plot2,(/5,3/),pnlres)
;frame(wks)

end