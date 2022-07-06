;2020/1/7
;绘制W随时间变化项的平面图
;使用资料： /data5/2019swh/data/W_change_with_t.nc 

char_day=(/"D0-30","D0-29","D0-28","D0-27","D0-26","D0-25","D0-24","D0-23","D0-22","D0-21","D0-20","D0-19","D0-18","D0-17","D0-16","D0-15","D0-14","D0-13","D0-12","D0-11","D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10","D0+11","D0+12","D0+13","D0+14","D0+15"/)
pressure = (/"985","970","955","940","925","910","895","880","865","850","835","820","800","775","750","725","700","675","637","600","562","525","487","450","412","375","337","288","244","208","176","150","127"/)

begin
f = addfile("/data5/2019swh/data/W_change_with_t.nc","r")
wt = f->Wt
wt = wt*1E+7


res = True
res@gsnDraw               = False
res@gsnFrame              = False
res@cnFillOn              = True     ; turn on color fill
res@cnFillPalette         = "WhiteYellowOrangeRed"
res@cnLineLabelsOn        = True
;res@cnFillDrawOrder  = "Predraw"             ; fill and lines before map
res@lbLabelBarOn     = False  
res@cnLineLabelsOn        = False
res@cnLevelSpacingF       = 0.5
res@gsnRightString = ""
res@cnLevelSelectionMode = "ExplicitLevels"
res@cnLevels             =  fspan(-2, 2,9) 
res@cnFillPalette         = "hotcolr_19lev"
res@mpMinLatF            =  -10      ; range to zoom in on
res@mpMaxLatF            =  30.
res@mpMinLonF            =  30.
res@mpMaxLonF            =  120.
res@tmYROn           = False     ; Turn off right and top tick marks
res@tmXTOn           = False     ; Turn off right and top tick marks
res@tmYLLabelFontHeightF      = 0.024
res@tmXBLabelFontHeightF      = 0.024
do ll = 0,32
plots = new(15,graphic)
wks = gsn_open_wks("pdf", "/data5/2019swh/paint/day/wt_"+pressure(ll))
do day = 0,29,2
    res@gsnCenterString = char_day(day)
    plots(day/2) = gsn_csm_contour_map(wks,wt(day,ll,:,:), res)

end do
pnlres = True
pnlres@gsnPanelMainString = "pWpt at about "+pressure(ll)+"hPa"
pnlres@gsnPanelLabelBar  = True
pnlres@gsnPanelDebug     = True     ; To get information from panel
pnlres@gsnMaximize       = True
gsn_panel(wks,plots,(/3,5/),pnlres)
end do



end