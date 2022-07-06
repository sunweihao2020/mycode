;2021/4/10
;本代码绘制用10m风绘制散度风、旋转风

begin
f = addfile("/data5/2019swh/data/10m_divergent_rotational_wind.nc","r")

vd = f->vd
ud = f->ud

ur = f->ur
vr = f->vr

div = f->div
vor = f->vor
vor = vor*1E+6
div = div*1E+6

char_day=(/"D0-30","D0-29","D0-28","D0-27","D0-26","D0-25","D0-24","D0-23","D0-22","D0-21","D0-20","D0-19","D0-18","D0-17","D0-16","D0-15","D0-14","D0-13","D0-12","D0-11","D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10","D0+11","D0+12","D0+13","D0+14","D0+15"/)

wks1 = gsn_open_wks("pdf","/data5/2019swh/paint/day/divergent_wind")
wks2 = gsn_open_wks("pdf","/data5/2019swh/paint/day/rotational_wind")
plot1 = new(15,graphic)
plot2 = new(15,graphic)
plot3 = new(15,graphic)
plot4 = new(15,graphic)
dum1  = new(15,graphic)
dum2  = new(15,graphic)

res = True
res@cnFillOn              = True
res@gsnDraw               = False
res@gsnFrame              = False
res@mpMinLatF            = -20 
res@mpMaxLatF            =  30.
res@mpMinLonF            =  30.
res@mpMaxLonF            =  120.
res@cnFillPalette         = "BlueDarkRed18"
res@cnLineLabelsOn        = False
res@cnInfoLabelOn         = False 
res@vpWidthF              = 0.6
res@cnLinesOn             = False
res@vpHeightF             = 0.55
res@mpGeophysicalLineThicknessF  = 1
res@cnLevelSelectionMode       = "ExplicitLevels" 
res@cnLevels             = ispan(-10,10,2)
res@lbLabelBarOn = True
res@tmYLLabelFontHeightF      = 0.024
res@tmXBLabelFontHeightF      = 0.024
res@gsnRightString = "10~S~6~N~ s~S~-1~n~"
res@gsnStringFont = 2


vcres = True
vcres@gsnDraw                 = False             ; do not draw the plot      
vcres@gsnFrame                = False            ; so we can draw time stamp
vcres@vcRefAnnoOrthogonalPosF = -1            ; move ref vector up
vcres@vpWidthF              = 0.6
vcres@vpHeightF             = 0.55
vcres@mpMinLatF            = -20 
vcres@mpMaxLatF            =  30.
vcres@mpMinLonF            =  30.
vcres@mpMaxLonF            =  120.
vcres@vcRefMagnitudeF         = 5             ; define vector ref mag
vcres@vcRefLengthF            = 0.045            ; define length of vec ref
vcres@vcGlyphStyle            = "CurlyVector"    ; turn on curly vectors
vcres@vcMinDistanceF          = 0.017
vcres@gsnRightString             = " "    
vcres@vcMinDistanceF          = 0.02
vcres@vcLineArrowThicknessF = 2
vcres@gsnStringFont         = 2


polyres                   = True
polyres@gsLineColor       = "black"
polyres@gsLineThicknessF  = 1
polyres@gsLineDashPattern = 2


do day = 16,30
res@gsnLeftString = char_day(day)
plot1(day-16) = gsn_csm_vector(wks1,ud(day,:,:),vd(day,:,:),vcres)
plot2(day-16) = gsn_csm_vector(wks2,ur(day,:,:),vr(day,:,:),vcres)
plot3(day-16) = gsn_csm_contour_map(wks1,div(day,:,:),res)
plot4(day-16) = gsn_csm_contour_map(wks2,vor(day,:,:),res)
overlay(plot3(day-16),plot1(day-16))
overlay(plot4(day-16),plot2(day-16))
dum1(day-16)  = gsn_add_polyline(wks1, plot3(day-16), (/30,120/), (/0,0/), polyres)
dum2(day-16)  = gsn_add_polyline(wks2, plot4(day-16), (/30,120/), (/0,0/), polyres)
end do

pnlres = True
pnlres@gsnPanelMainString = "divergent wind(10m)"
pnlres@gsnPanelLabelBar  = True
pnlres@gsnPanelDebug     = True     ; To get information from panel
pnlres@pmLabelBarWidthF  = 0.55
pnlres@lbLabelFontHeightF = 0.012
gsn_panel(wks1,plot3,(/3,5/),pnlres)
pnlres@gsnPanelMainString = "rotational wind(10m)"
gsn_panel(wks2,plot4,(/3,5/),pnlres)
end