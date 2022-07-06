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

  u   = a->U2M
  v   = a->V2M

  char_mon=(/"Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"/)

do imon = 1,12
  wks = gsn_open_wks("png","/data5/2019swh/paint/climatemean/vector"+imon)

  vcres                         = True             ; plot mods desired
  vcres@gsnFrame                = False            ; so we can draw time stamp
  vcres@vcRefAnnoOrthogonalPosF = -1.0             ; move ref vector up
  vcres@vcRefMagnitudeF         = 10.0             ; define vector ref mag
  vcres@vcRefLengthF            = 0.045            ; define length of vec ref
  vcres@vcGlyphStyle            = "CurlyVector"    ; turn on curly vectors
  vcres@vcMinDistanceF          = 0.017
  vcres@tiMainString         = char_mon(imon-1) ;"January"    ; plot title
  vcres@gsnCenterString      = "2m wind"           ; plot center string
  vcres@gsnRightString        = "units:m s-1"

  vcres@mpCenterLonF            = 90
  vector = gsn_csm_vector_map(wks,u(imon-1,:,:),v(imon-1,:,:),vcres)

  
;---Add time stamp to plot
  ;infoTimeStamp(wks,0.025,"uv300.nc")      ; arguments are workstation
                                           ; size of text desired, and
                                           ; right string.         
  frame (wks)  

end do
end