;2021/1/18
;绘制逐候海表面温度

begin

  a = addfile("/data5/2019swh/data/pentad_OISST.nc","r")

  lat = a->lat
  lon = a->lon
  sst = a->SST
  sst = sst*0.01
  char_pen=(/"p22","p23","p24","p25","p26","p27","p28","p29","p30","p31","p32","p33","p34"/)

plot = new(4,graphic)
dum  = new(4,graphic)
wks = gsn_open_wks("pdf","/data5/2019swh/paint/pentad/OISST")

do ipen = 0,3

  res = True
  res@gsnDraw               = False
  res@gsnFrame              = False
  res@cnFillOn              = True     ; turn on color fill
  res@cnFillPalette         = "MPL_coolwarm"
  res@cnLineLabelsOn        = False
  res@cnLevelSelectionMode       = "ExplicitLevels" 
  res@cnLevels             = ispan(18,32,1)
  res@mpMinLatF            = -10      ; range to zoom in on
  res@mpMaxLatF            =  30.
  res@mpMinLonF            =  30.
  res@mpMaxLonF            = 120.
  res@lbLabelBarOn           = False
  res@gsnRightString        = "units:degC"
  res@gsnLeftString         = char_pen(ipen)
  res@gsnStringFont         = 2
  res@tmYLLabelFontHeightF      = 0.024
  res@tmXBLabelFontHeightF      = 0.024
  ;res@cnInfoLabelOrthogonalPosF = -0.07
  plot(ipen) = gsn_csm_contour_map(wks,sst(ipen,:,:), res)  ; create plot

  polyres                   = True
  polyres@gsLineColor       = "black"
  polyres@gsLineThicknessF  = 5
  polyres@gsLineDashPattern = 2
  dum(ipen) = gsn_add_polyline(wks, plot(ipen), (/30,120/), (/0,0/), polyres)

end do
pnlres = True
pnlres@gsnPanelMainString = "sea surface temperature"
pnlres@gsnPanelLabelBar  = True
pnlres@gsnPanelDebug     = True     ; To get information from panel
pnlres@pmLabelBarWidthF  = 0.55
pnlres@lbLabelFontHeightF = 0.012
gsn_panel(wks,plot,(/2,2/),pnlres)
end