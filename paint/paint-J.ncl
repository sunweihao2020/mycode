;2020/1/8
;绘制三维的J=θ*涡度
;使用资料： /data5/2019swh/data/J-3d.nc 
begin
char_day=(/"D0-30","D0-29","D0-28","D0-27","D0-26","D0-25","D0-24","D0-23","D0-22","D0-21","D0-20","D0-19","D0-18","D0-17","D0-16","D0-15","D0-14","D0-13","D0-12","D0-11","D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10","D0+11","D0+12","D0+13","D0+14","D0+15"/)
pressure = (/"985","970","955","940","925","910","895","880","865","850","835","820","800","775","750","725","700","675","637","600","562","525","487","450","412","375","337","288","244","208","176","150","127"/)


f = addfile("/data5/2019swh/data/three-dimension-vorticity.nc","r")

jz = f-> z-vorticity
;jz = jz*1E+3


res = True
;res@gsnDraw               = False
;res@gsnFrame              = False
res@cnFillOn              = True     ; turn on color fill
res@cnFillPalette         = "WhiteYellowOrangeRed"
res@cnLineLabelsOn        = True
;res@cnFillDrawOrder  = "Predraw"             ; fill and lines before map
res@lbLabelBarOn     = True  
res@cnLineLabelsOn        = False
;res@cnLevelSpacingF       = 0.5
res@gsnRightString = ""
;res@cnLevelSelectionMode = "ExplicitLevels"
;res@cnLevels             =  fspan(-3, 3,13) 
res@cnFillPalette         = "hotcolr_19lev"
res@mpMinLatF            =  -10      ; range to zoom in on
res@mpMaxLatF            =  30.
res@mpMinLonF            =  30.
res@mpMaxLonF            =  120.
res@tmYROn           = False     ; Turn off right and top tick marks
res@tmXTOn           = False     ; Turn off right and top tick marks
;res@tmYLLabelFontHeightF      = 0.024
;res@tmXBLabelFontHeightF      = 0.024
do ll = 32,32
;plots = new(15,graphic)
;wks = gsn_open_wks("pdf", "/data5/2019swh/paint/day/wt_"+pressure(ll))
do day = 0,29
    wks = gsn_open_wks("png", "/data5/2019swh/paint/day/v33_"+day)
    res@gsnCenterString = char_day(day)
    res@gsnCenterStringFontHeightF = 0.015
    plot = gsn_csm_contour_map(wks,jz(day,ll,:,:), res)

end do
;pnlres = True
;pnlres@gsnPanelMainString = "pWpt at about "+pressure(ll)+"hPa"
;pnlres@gsnPanelLabelBar  = True
;pnlres@gsnPanelDebug     = True     ; To get information from panel
;pnlres@gsnMaximize       = True
;gsn_panel(wks,plots,(/3,5/),pnlres)
end do



end