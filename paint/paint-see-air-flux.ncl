;2021/4/5
;本代码绘制合成分析的海气通量
;使用数据：composite_OISST.nc
begin
f = addfile("/data/composite-sea-air-flux.nc","r")
flux = f->flux
dt = f->delta_T

char_day=(/"D0-30","D0-29","D0-28","D0-27","D0-26","D0-25","D0-24","D0-23","D0-22","D0-21","D0-20","D0-19","D0-18","D0-17","D0-16","D0-15","D0-14","D0-13","D0-12","D0-11","D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10","D0+11","D0+12","D0+13","D0+14","D0+15"/)
wks1 = gsn_open_wks("pdf","/picture/paint/day/sea_air_flux")
wks2 = gsn_open_wks("pdf","/picture/paint/day/delta_t")
plot1 = new(15,graphic)
dum1 = new(15,graphic)
plot2 = new(15,graphic)
dum2 = new(15,graphic)

res = True
res@gsnDraw               = False
res@gsnFrame              = False
res@cnFillOn              = True     ; turn on color fill
res@cnFillPalette         = "cmp_b2r"
res@cnLineLabelsOn        = False
;res@cnLevelSelectionMode       = "ExplicitLevels" 
;res@cnLevels             = fspan(25,30,21)
res@mpMinLatF            = -30      ; range to zoom in on
res@mpMaxLatF            =  30.
res@mpMinLonF            =  30.
res@mpMaxLonF            = 120.
res@lbLabelBarOn           = False
;res@gsnRightString        = "units:degC"
res@gsnStringFont         = 2
res@tmYLLabelFontHeightF      = 0.024
res@tmXBLabelFontHeightF      = 0.024

polyres                   = True
polyres@gsLineColor       = "black"
polyres@gsLineThicknessF  = 2
polyres@gsLineDashPattern = 2

do pentad  = 16,30

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