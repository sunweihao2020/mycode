;本代码用ncl绘制xarray计算出来的降水
begin
f = addfile("/data5/2019swh/data/trmm_prect_365_climate.nc","r")
pre = f->prect
pre&lon@units = "degrees_east"
pre&lat@units = "degrees_north"

plot = new(15,graphic)
dum  = new(15,graphic)
wks = gsn_open_wks("pdf","/data5/2019swh/paint/day/GPCP_prect_test")

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
    res@gsnLeftString = ""
    res@gsnRightString = ""
    res@cnLevels             = ispan(0,26,2)
    
    res@gsnRightString        = "mm/day"
    res@gsnStringFont         = 2
    res@tmYLLabelFontHeightF      = 0.024
    res@tmXBLabelFontHeightF      = 0.024
    ;res@tmYLLabelDeltaF = -0.6  ;坐标值跑出去了就调这个

    res@cnInfoLabelOn         = False
    plot(day) = gsn_csm_contour_map(wks,pre(day,:,:), res)  ; create plot
    
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