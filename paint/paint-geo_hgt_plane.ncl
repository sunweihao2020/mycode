;2021/3/9
;绘制季风爆发前对流层的位势高度场
;选择四个层次：925 850 700 500
begin
f = addfile("/data/composite3.nc","r")
h = f->H
h1 = h(:,3,:,:)
h2 = h(:,6,:,:)
h3 = h(:,12,:,:)
h4 = h(:,16,:,:)
wks = gsn_open_wks("pdf","/picture/paint/day/H_850")
h = h*9.8

char_day=(/"D0-30","D0-29","D0-28","D0-27","D0-26","D0-25","D0-24","D0-23","D0-22","D0-21","D0-20","D0-19","D0-18","D0-17","D0-16","D0-15","D0-14","D0-13","D0-12","D0-11","D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10","D0+11","D0+12","D0+13","D0+14","D0+15"/)
plot = new(15,graphic)
dum  = new(15,graphic)
do day = 16,30
    res = True
    res@gsnDraw               = False
    res@gsnFrame              = False
    res@cnFillOn              = False     ; turn on color fill
    res@cnFillPalette         = "cmocean_balance"
    res@cnLineLabelsOn        = True
    res@lbLabelsOn            = False
    res@lbLabelBarOn          = False
    ;res@cnLevelSelectionMode       = "ExplicitLevels" 
    res@cnLevelSpacingF = 4
    res@mpMinLatF            = -20      ; range to zoom in on
    res@mpMaxLatF            =  30.
    res@mpMinLonF            =  70.
    res@mpMaxLonF            = 180.
    
    res@gsnRightString        = " "
    res@gsnLeftString         = char_day(day)
    res@gsnStringFont         = 2
    res@tmYLLabelFontHeightF      = 0.024
    res@tmXBLabelFontHeightF      = 0.024
    ;res@tmYLLabelDeltaF = -0.6  ;坐标值跑出去了就调这个

    res@cnInfoLabelOn         = False
    plot(day-16) = gsn_csm_contour_map(wks,h2(day,:,:), res)  ; create plot
  
    polyres                   = True
    polyres@gsLineColor       = "black"
    polyres@gsLineThicknessF  = 3
    polyres@gsLineDashPattern = 2
    dum(day-16) = gsn_add_polyline(wks, plot(day-16), (/70,200/), (/0,0/), polyres)
    
end do
pnlres = True
pnlres@gsnPanelMainString = "geopotential height"
pnlres@gsnPanelLabelBar  = True
pnlres@gsnPanelDebug     = True     ; To get information from panel
pnlres@pmLabelBarWidthF  = 0.55
pnlres@lbLabelFontHeightF = 0.012
gsn_panel(wks,plot,(/5,3/),pnlres)
;frame(wks)

end