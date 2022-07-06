;2021/4/5
;本代码绘制合成分析前的海温，和上次的区别是增大精度
;使用数据：composite_OISST.nc
begin
f = addfile("/data/composite_OISST.nc","r")
sst = f->SST

pens = (/"P0-6","P0-5","P0-4","P0-3","P0-2","P0-1"/)
wks1 = gsn_open_wks("pdf","/picture/paint/day/SST1")
;wks2 = gsn_open_wks("pdf","/picture/paint/day/SST2")
gsn_define_colormap(wks1,"BlueDarkRed18")
;gsn_define_colormap(wks2,"BlueDarkRed18")
plot = new(6,graphic)
dum = new(6,graphic)

res = True
res@gsnDraw               = False
res@gsnFrame              = False
res@cnFillOn              = True     ; turn on color fill
res@cnFillPalette         = "cmp_b2r"
res@cnLineLabelsOn        = False
res@cnLevelSelectionMode       = "ExplicitLevels" 
res@cnLevels             = fspan(25,30,21)
res@mpMinLatF            = -20      ; range to zoom in on
res@mpMaxLatF            =  20.
res@mpMinLonF            =  30.
res@mpMaxLonF            = 120.
res@lbLabelBarOn           = False
res@gsnRightString        = "units:degC"
res@gsnStringFont         = 2
res@tmYLLabelFontHeightF      = 0.024
res@tmXBLabelFontHeightF      = 0.024

polyres                   = True
polyres@gsLineColor       = "black"
polyres@gsLineThicknessF  = 2
polyres@gsLineDashPattern = 2

do pentad  = 0,5
sst1 = dim_avg_n(sst(pentad*5:(pentad*5+4),:,:),0)
sst1!0 = "lat"
sst1!1 = "lon"
sst1&lat = sst&lat
sst1&lon = sst&lon
res@gsnLeftString         = pens(pentad)
plot(pentad) = gsn_csm_contour_map(wks1,sst1(:,:), res)
dum(pentad) = gsn_add_polyline(wks1, plot(pentad), (/30,120/), (/0,0/), polyres)
end do

pnlres = True
pnlres@gsnPanelMainString = "sea surface temperature"
pnlres@gsnPanelLabelBar  = True
pnlres@gsnPanelDebug     = True     ; To get information from panel
pnlres@pmLabelBarWidthF  = 0.55
pnlres@lbLabelFontHeightF = 0.012
gsn_panel(wks1,plot,(/2,3/),pnlres)
end