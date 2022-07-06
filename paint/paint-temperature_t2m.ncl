
begin
f = addfile("/data5/2019swh/data/composite-merra2-single.nc","r")
t = f->T2M
char_day=(/"D0-30","D0-29","D0-28","D0-27","D0-26","D0-25","D0-24","D0-23","D0-22","D0-21","D0-20","D0-19","D0-18","D0-17","D0-16","D0-15","D0-14","D0-13","D0-12","D0-11","D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10","D0+11","D0+12","D0+13","D0+14","D0+15"/)
day = 15

res = True
res@cnFillOn              = True
res@gsnDraw               = True
res@gsnFrame              = True
res@mpMinLatF            = -10 
res@mpMaxLatF            =  30
res@mpMinLonF            =  30
res@mpMaxLonF            =  120
res@cnFillPalette         = "BlRe"
res@cnLineLabelsOn        = False
res@lbLabelBarOn          = True 
res@cnInfoLabelOn         = False 
res@cnLinesOn             = False
res@gsnLeftString         = char_day(day)
res@gsnRightString        = "2m temperature"
res@mpGeophysicalLineThicknessF  = 1
res@cnLevelSelectionMode       = "ExplicitLevels" 
res@cnLevels             = ispan(286,316,2)
;
polyres                   = True
polyres@gsLineColor       = "black"
polyres@gsLineThicknessF  = 1
polyres@gsLineDashPattern = 2


wks = gsn_open_wks("pdf","/data5/2019swh/paint/day/temperature_at_2m")
plot =  gsn_csm_contour_map(wks,t(day,:,:),res)
dum = gsn_add_polyline(wks, plot, (/30,120/), (/0,0/), polyres)


end