begin
;************************************************
; read in netCDF file
;************************************************
  a = addfile("/data5/2019swh/data/b0920.nc","r")
;************************************************
; read in zonal winds
;************************************************
  lat = a->lat
  lon = a->lon

do imon = 1,12

  ps = a->PS(imon-1,:,:)                                ; read July zonal winds
  ;t2m!0 = "lat"
  ;t2m!1 = "lon"
  ;t2m&lat = lat  
  ;t2m&lon = lon
  ;t2m&lat@units = "degrees_north"
  ;t2m&lon@units = "degrees_east"
;printVarSummary(t2m&lon)
 ;qv2m_C = qv2m   ;exit

 ps_C = ps/100
 copy_VarCoords(ps, ps_C)
 
 char_mon=(/"Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"/)

;************************************************
; create plot
;************************************************
  wks = gsn_open_wks("png","/data5/2019swh/paint/climatemean/PS_"+imon)                ; send graphics to PNG file
  res = True                                    ; plot mods desired

  ;res@cnLevelSelectionMode = "ManualLevels"     ; set manual contour levels
  ;res@cnMinLevelValF       = -10.               ; set min contour level
  ;res@cnMaxLevelValF       =  35.               ; set max contour level
  ;res@cnLevelSpacingF      =   5               ; set contour spacing
  res@cnFillOn              = True     ; turn on color fill
  res@cnFillPalette         = "BlAqGrYeOrRe"
  res@lbOrientation         = "Vertical"

  res@mpMinLatF            = -30      ; range to zoom in on
  res@mpMaxLatF            =  60.
  res@mpMinLonF            =  30.
  res@mpMaxLonF            = 150.
  
  res@tmYLMode = "Explicit"
  res@tmYLLabelDeltaF = -0.6
;  res@caXArray = lon
;  res@caYArray = lat

  ;res@tmYLMode = "Manual"
  ;res@tmYLTickSpacing = 10
  ;res@tmXLTickSpacing = 10

  res@tiMainString         = char_mon(imon-1) ;"January"    ; plot title
  res@gsnCenterString      = "surface pressure"           ; plot center string
  res@gsnRightString        = "units:hPa"

  res@cnInfoLabelOrthogonalPosF = -0.07         ; move the label inside the plot

  plot = gsn_csm_contour_map(wks,ps_C, res)  ; create plot
end do
end
