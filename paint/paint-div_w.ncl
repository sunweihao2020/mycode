;2021/1/17
;所用资料：merra2季风爆发的合成分析
;要素：散度、垂直运动
;层次：多层次
begin
f = addfile("/data5/2019swh/data/composite3.nc","r")
ff = addfile("/data5/2019swh/data/div_vor.nc","r")
omega = f->OMEGA
p = f->level
pp = conform_dims(dimsizes(omega), p, 1)
t = f->T
w = omega_to_w(omega, pp, t)
div = ff->div


char_day=(/"D0-30","D0-29","D0-28","D0-27","D0-26","D0-25","D0-24","D0-23","D0-22","D0-21","D0-20","D0-19","D0-18","D0-17","D0-16","D0-15","D0-14","D0-13","D0-12","D0-11","D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10","D0+11","D0+12","D0+13","D0+14","D0+15"/)
lev = (/3,6,12,16,22,24/)
level = (/"925hPa","850hPa","700hPa","500hPa","200hPa","100hPa"/)

do ll = 0,5
plot1 = new(15,graphic)
dum1   = new(15,graphic)
plot2 = new(15,graphic)
dum2   = new(15,graphic)

wks1 = gsn_open_wks("pdf","/data5/2019swh/paint/day/div_field_"+level(ll))
wks2 = gsn_open_wks("pdf","/data5/2019swh/paint/day/w_field_"+level(ll))

do day = 4,33,2
    res3 = True
    res3@cnFillOn              = True     ; turn on color fill
    res3@gsnDraw               = False
    res3@gsnFrame              = False
    res3@mpMinLatF            = -10 
    res3@mpMaxLatF            =  30.
    res3@mpMinLonF            =  30.
    res3@mpMaxLonF            =  120.
    res3@cnFillPalette         = "NCV_blu_red"
    res3@cnLineLabelsOn        = True
    res3@lbOrientation         = "Vertical"  
    res3@gsnRightString        = level(ll)
    res3@cnInfoLabelOn         = False 
    res3@vpWidthF              = 0.6
    res3@cnLinesOn             = False 
    res3@vpHeightF             = 0.55
    res3@mpGeophysicalLineThicknessF  = 1.5
    res3@cnLevelSelectionMode       = "ExplicitLevels" 
    res3@cnLevels             = ispan(-8,8,2)
    res3@cnLineLabelDensityF  = 2
    res3@cnLineLabelInterval  = 1
    res3@cnLevelSpacingF      = 2
    res3@lbLabelBarOn     = False  
    res3@tmYLLabelFontHeightF      = 0.024
    res3@tmXBLabelFontHeightF      = 0.024
    res3@gsnStringFont        = 2

    res3@cnLineLabelsOn       = False
    res3@cnLineLabelFontAspectF = 2
    res3@gsnLeftString         = char_day(day)

    plot1((day-4)/2)  = gsn_csm_contour_map(wks1, div(day,lev(ll),:,:), res3)

    res2 = True
    res2@cnFillOn              = True     ; turn on color fill
    res2@gsnDraw               = False
    res2@gsnFrame              = False
    res2@cnLineLabelsOn        = True
    res2@mpMinLatF            = -10 
    res2@mpMaxLatF            =  30.
    res2@mpMinLonF            =  30.
    res2@mpMaxLonF            =  120.
    res3@cnFillPalette         = "NCV_blu_red"
    res2@cnLinesOn             = False 
    res2@cnInfoLabelOn         = False
    res2@lbLabelBarOn     = False  
    res2@cnLineLabelsOn   = False
    res2@cnLineThicknessF      = 1
    res2@gsnContourNegLineDashPattern = 1 		  ; sets negative contours to dash pattern 1
    res2@cnLevelSelectionMode       = "ExplicitLevels" 
    res2@cnLevels             = fspan(-3,3,13)
    res2@cnLineLabelDensityF  = 2
    res2@cnLineLabelInterval  = 1
    res2@cnLineLabelFontAspectF = 2
    res2@cnLineLabelBackgroundColor = -1
    res2@gsnLeftString         = char_day(day)


    plot2((day-4)/2)  = gsn_csm_contour_map(wks2, w(day,lev(ll),:,:), res2)

    polyres                   = True
    polyres@gsLineColor       = "black"
    polyres@gsLineThicknessF  = 1.5
    polyres@gsLineDashPattern = 2

    dum1((day-4)/2)   = gsn_add_polyline(wks1, plot1((day-4)/2), (/30,120/), (/0,0/), polyres)
    dum2((day-4)/2)   = gsn_add_polyline(wks2, plot2((day-4)/2), (/30,120/), (/0,0/), polyres)
    end do
    pnlres = True
    pnlres@gsnPanelMainString = "div at "+level(ll)
    pnlres@gsnPanelLabelBar  = True
    pnlres@gsnPanelDebug     = True     ; To get information from panel
    pnlres@pmLabelBarWidthF  = 0.55
    pnlres@lbLabelFontHeightF = 0.012
    gsn_panel(wks1,plot1,(/5,3/),pnlres)
    pnlres@gsnPanelMainString = "w at "+level(ll)
    gsn_panel(wks2,plot2,(/5,3/),pnlres)
    frame(wks1)
    frame(wks2)

end do
end