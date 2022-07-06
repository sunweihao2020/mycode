;2020/11/14
;



begin
;************************************************
; read in netCDF file
;************************************************
  a = addfile("/data5/2019swh/data/mean_merra2_multilayer_0921.nc","r")
;************************************************
; read in zonal winds
;************************************************
  lat = a->lat
  lon = a->lon
  lev = a->level
 char_mon=(/"Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"/)

do imon = 1,12
  h = a->H
  u = a->uwind
  v = a->vwind



  wks = gsn_open_wks("png", "/data5/2019swh/paint/climatemean/height_wind_700hpa_"+imon)
  res = True
  res@gsnDraw      =  False                   ; do not draw the plot
  res@gsnFrame     =  False
  res@cnLinesOn    = False
  res@mpCenterLonF               = 90

  res@gsnMaximize           = True     ; Make plot fit the frame
  res@cnFillOn              = True     ; turn on color fill
  res@cnLevelSelectionMode       = "ExplicitLevels" 
  res@cnLevels             = ispan(1000,1600,20)
  ;res@cnLevels                   = (/ -5,-4,-3,-2,-1,-0.1,0.1,1,2,3,4,5/)*40+5600      
;res1@cnLevels                   = (/-10,-8,-6,-4,-2,-1,1,2,4,6,8,10/)*7 
  ;res@cnFillColors               = (/5,6,7,8,9,10,0,13,14,15,16,17,18/)
  ;res@cnLinesOn             = False    ; turn of contour lines
 ; res@cnLevelSpacingF       = 40      ; contour spacing
  res@cnFillPalette         = "BlueWhiteOrangeRed"
  ;res@lbOrientation         = "Vertical"
  res@gsnCenterString        = "850hPa Geopotential Height&Wind Field"
  res@gsnRightString         = ""
  res@gsnLeftString         = char_mon(imon-1)
  ;缺测值
  res@cnMissingValPerimOn     = True            ; turn on the missing value perimeter
  res@cnMissingValPerimColor  = "red"           ; outline the perimeter red
  res@cnMissingValFillPattern = 0               ; choose fill pattern 0 (solid fill) 
  res@cnMissingValFillColor   = "black"          ; color fill missing areas blue
  ;res@mpMinLonF             = 30
  ;res@mpMaxLonF             = 130
  ;res@mpMinLatF             = -37
  ;res@mpMaxLatF             = 60
  plot = gsn_csm_contour_map(wks,h(imon-1,6,:,:),res)
  
  sres = True
  sres@gsnDraw              = False             ; do not draw the plot
  sres@gsnFrame             = False      
  sres@cnLevelSelectionMode       = "ExplicitLevels" 
  sres@cnLevels             = (/16600/)
  sres@cnLineLabelsOn             = True
  sres@cnMonoLineThickness        = True
  sres@cnLineThicknessF           = 2.5
  sres@cnMonoLineColor            = True
  sres@cnLineColor                = "black" 
  sres@cnLineLabelFontColors      = "black"
  sres@cnLineLabelFontThicknessF  =  0.6
  sres@cnConstFLabelFontHeightF   =  0.06
  sres@gsnLeftString              = ""
  sres@gsnRightString             = ""
  sres@cnLineLabelBackgroundColor = -1
  sres@cnFillOn              = False
  sres@cnLineThicknessF           = 6 
  sres@cnInfoLabelOn              = False
  ;sres@xyLineDashSegLenF          = 1
  sres@cnLineLabelPlacementMode   = "Constant"
  sres@cnLineDashSegLenF          = 0.3
  sres@cnLineLabelInterval        = 10000             ; default = 2
  ;plot2 = gsn_csm_contour(wks,h(imon-1,24,:,:),sres)

  vcres = True
  vcres@gsnDraw                 = False             ; do not draw the plot      
  vcres@gsnFrame                = False            ; so we can draw time stamp
  vcres@vcRefAnnoOrthogonalPosF = -1.35             ; move ref vector up
  vcres@vcRefMagnitudeF         = 10.0             ; define vector ref mag
  vcres@vcRefLengthF            = 0.045            ; define length of vec ref
  vcres@vcGlyphStyle            = "CurlyVector"    ; turn on curly vectors
  vcres@vcMinDistanceF          = 0.017
  vcres@gsnRightString             = ""
  vcres@vcMinDistanceF          = 0.022

  vector = gsn_csm_vector(wks,u(imon-1,6,:,:),v(imon-1,6,:,:),vcres)

 ; overlay(plot,plot2)
  overlay(plot,vector)
  draw(plot)
  frame(wks)

end do
end
