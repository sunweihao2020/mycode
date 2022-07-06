;2021/4/5
;本代码绘制合成分析的海气通量
;使用数据：composite_OISST.nc
begin
f = addfile("/data5/2019swh/data/composite-sea-air-flux.nc","r")
flux = f->flux
dt = f->delta_T

char_day=(/"D0-30","D0-29","D0-28","D0-27","D0-26","D0-25","D0-24","D0-23","D0-22","D0-21","D0-20","D0-19","D0-18","D0-17","D0-16","D0-15","D0-14","D0-13","D0-12","D0-11","D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10","D0+11","D0+12","D0+13","D0+14","D0+15"/)
wks1 = gsn_open_wks("pdf","/data5/2019swh/paint/day/sea_air_flux")
wks2 = gsn_open_wks("pdf","/data5/2019swh/paint/day/delta_t")
plot1 = new(15,graphic)
dum1 = new(15,graphic)
plot2 = new(15,graphic)
dum2 = new(15,graphic)

res = True
res@gsnDraw               = False
res@gsnFrame              = False
res@cnFillOn              = True     ; turn on color fill
res@cnFillPalette         = "CBR_coldhot"
res@cnLineLabelsOn        = False
res@cnLevelSelectionMode       = "ExplicitLevels" 
res@mpMinLatF            = -10      ; range to zoom in on
res@mpMaxLatF            =  30.
res@mpMinLonF            =  30.
res@mpMaxLonF            = 120.
res@lbLabelBarOn           = False
;res@gsnRightString        = "units:degC"
;res@gsnStringFont         = 3
res@tmYLLabelFontHeightF      = 0.05
res@tmXBLabelFontHeightF      = 0.05

polyres                   = True
polyres@gsLineColor       = "black"
polyres@gsLineThicknessF  = 2
polyres@gsLineDashPattern = 2

do day  = 16,30
res@cnFillPalette         = "MPL_Oranges"
res@cnLevels             := fspan(0,6,7)
res@gsnLeftString         = char_day(day)
plot1(day-16) = gsn_csm_contour_map(wks1,flux(day,:,:), res)
dum1(day-16) = gsn_add_polyline(wks1, plot1(day-16), (/30,120/), (/0,0/), polyres)
res@cnLevels             := fspan(0,3,7)
res@cnFillPalette         = "MPL_Oranges"
plot2(day-16) = gsn_csm_contour_map(wks2,dt(day,:,:), res)
dum2(day-16) = gsn_add_polyline(wks2, plot2(day-16), (/30,120/), (/0,0/), polyres)
end do

pnlres = True
pnlres@gsnPanelMainString = "sea sensible heat flux"
pnlres@gsnPanelLabelBar  = True
pnlres@gsnPanelDebug     = True     ; To get information from panel
pnlres@pmLabelBarWidthF  = 0.55
pnlres@lbLabelFontHeightF = 0.012
gsn_panel(wks1,plot1,(/3,5/),pnlres)
pnlres@gsnPanelMainString = "sea-air temperature difference"
gsn_panel(wks2,plot2,(/3,5/),pnlres)
end