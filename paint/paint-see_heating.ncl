;2021/3/9
;本代码使用计算的视热源资料来绘制爆发前的视热源分布情况
;资料composite-see_heating.ncl
begin
f = addfile("/data/composite-heating-jra55.nc","r")
;f = addfile("/data/composite-see_heating.nc","r")
q1 = f->convective
q2 = f->radiation
q3 = f->diffusion
q = q1+q2+q3
copy_VarCoords(q1, q)
;q = f->see_heating

char_day=(/"D0-30","D0-29","D0-28","D0-27","D0-26","D0-25","D0-24","D0-23","D0-22","D0-21","D0-20","D0-19","D0-18","D0-17","D0-16","D0-15","D0-14","D0-13","D0-12","D0-11","D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10","D0+11","D0+12","D0+13","D0+14","D0+15"/)
plot = new(15,graphic)
dum  = new(15,graphic)
qm = q(:,30,:,:)
wks = gsn_open_wks("pdf","/picture/paint/day/heating_850")
gsn_define_colormap(wks,"cmocean_amp")
do day = 15,29
    res = True
    res@gsnDraw               = False
    res@gsnFrame              = False
    res@cnFillOn              = True     ; turn on color fill
    res@cnLineLabelsOn        = False
    res@lbLabelsOn            = False
    res@lbLabelBarOn          = False
    
    res@cnLevelSelectionMode       = "ExplicitLevels" 
    res@cnLevels             = fspan(0,10,11)
    res@cnFillColors         = (/2,15,30,50,60,90,100,144,173,190,200,220/)
    ;res@cnLevelSpacingF = 1
    res@mpMinLatF            = -20      ; range to zoom in on
    res@mpMaxLatF            =  30.
    res@mpMinLonF            =  30.
    res@mpMaxLonF            = 120.
    
    res@gsnRightString        = " "
    res@gsnLeftString         = char_day(day)
    res@gsnStringFont         = 2
    res@tmYLLabelFontHeightF      = 0.024
    res@tmXBLabelFontHeightF      = 0.024
    ;res@tmYLLabelDeltaF = -0.6  ;坐标值跑出去了就调这个

    res@cnInfoLabelOn         = False
    plot(day-15) = gsn_csm_contour_map(wks,qm(day,:,:), res)  
  
    polyres                   = True
    polyres@gsLineColor       = "black"
    polyres@gsLineThicknessF  = 3
    polyres@gsLineDashPattern = 2
    dum(day-15) = gsn_add_polyline(wks, plot(day-15), (/30,120/), (/0,0/), polyres)
    
end do
pnlres = True
pnlres@gsnPanelMainString = "Q"
pnlres@gsnPanelLabelBar  = True
pnlres@gsnPanelDebug     = True     ; To get information from panel
pnlres@pmLabelBarWidthF  = 0.55
pnlres@lbLabelFontHeightF = 0.012
gsn_panel(wks,plot,(/5,3/),pnlres)
;frame(wks)

end