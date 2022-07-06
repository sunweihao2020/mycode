begin
;************************************************
; read in netCDF file
;************************************************
  a = addfile("/data5/2019swh/data/mean_pentad_multilayer_0924.nc","r")

  lat = a->lat
  lon = a->lon
  lev = a->level
  u = a->uwind
  v = a->vwind
 char_pen=(/"p22","p23","p24","p25","p26","p27","p28","p29","p30","p31","p32","p33","p34"/)
 plev    = (/"925hpa","700hpa","500hpa","200hpa"/)
 plevs   = (/3,12,16,22/)
 ;plev    = (/"700hpa","500hpa","200hpa"/)
 ;plevs   = (/12,16,22/)

 do p = 0,3
    do ipen = 0,12
        wks = gsn_open_wks("pdf","/data5/2019swh/paint/pentad/stream_"+plev(p)+"_"+char_pen(ipen))
        ;res = True
        ;res@gsnDraw      =  False                   ; do not draw the plot
        ;res@gsnFrame     =  False
        ;res@cnLinesOn    = False
        ;;res@mpCenterLonF               = 90
        ;res@mpMinLatF            = -30
        ;res@mpMaxLatF            = 60
        ;res@mpMinLonF            = 30
        ;res@mpMaxLonF            = 160
        ;res@gsnCenterString        = plev(p)+"  stream field"
        ;res@gsnLeftString         = char_pen(ipen)
        ;res@cnLineLabelsOn        = False
        ;res@gsnMaximize           = True     ; Make plot fit the frame
        ;res@cnFillOn              = False     ; turn on color fill
        ;res@cnLevelSelectionMode       = "ManualLevels" 
        ;res@cnInfoLabelOn              = False
        ;res@cnMinLevelValF             = 1000
        ;res@cnMissingValPerimOn     = True            ; turn on the missing value perimeter
        ;res@cnMissingValPerimColor  = "red"           ; outline the perimeter red
        ;res@cnMissingValFillPattern = 0               ; choose fill pattern 0 (solid fill) 
        ;res@cnMissingValFillColor   = "black"          ; color fill missing areas blue
        ;plot1 = gsn_csm_contour_map(wks,u(ipen,plevs(p),:,:),res)

        stres = True
        stres@gsnDraw    = False
        stres@gsnFrame   = False
        stres@stArrowLengthF     = 0.008  
        stres@stLengthCheckCount = 15
        stres@stArrowStride      = 1
        stres@stLineThicknessF   = 0.7
        stres@mpMinLatF            = -10
        stres@mpMaxLatF            = 30
        stres@mpMinLonF            = 30
        stres@mpMaxLonF            = 120
        stres@gsnLeftString         = char_pen(ipen)
        stres@gsnRightString      = plev(p)
        stres@stMinArrowSpacingF = 0.025
        stres@stLineThicknessF   = 2
        ;stres@stLevelSpacingF    = 25
        stres@stLineStartStride  = 25                    ; default is 2
        stres@stMinArrowSpacingF = 0.035                ; default is 0.0             
        stres@stStepSizeF        = 0.001                ; default is dynamic
        stream = gsn_csm_streamline_map(wks,u(ipen,plevs(p),:,:),v(ipen,plevs(p),:,:),stres)




        vcres = True
        vcres@gsnDraw                 = False             ; do not draw the plot      
        vcres@gsnFrame                = False            ; so we can draw time stamp
        vcres@vcRefAnnoOrthogonalPosF = -1.0             ; move ref vector up
        vcres@vcRefMagnitudeF         = 10.0             ; define vector ref mag
        vcres@vcRefLengthF            = 0.045            ; define length of vec ref
        vcres@vcGlyphStyle            = "CurlyVector"    ; turn on curly vectors
        vcres@vcMinDistanceF          = 0.017
        vcres@mpMinLatF            =  -10 
        vcres@mpMaxLatF            =  30.
        vcres@mpMinLonF            =  30.
        vcres@mpMaxLonF            =  120.
        vcres@vcLineArrowThicknessF = 3.5
        vcres@gsnLeftString         = char_pen(ipen)
        vcres@gsnRightString    = plev(p)

        vcres@vcMinDistanceF          = 0.035
        vector = gsn_csm_vector_map(wks,u(ipen,plevs(p),:,:),v(ipen,plevs(p),:,:),vcres)
    
        polyres                   = True
        polyres@gsLineColor       = "black"
        polyres@gsLineThicknessF  = 5
        polyres@gsLineDashPattern = 2
        dum = gsn_add_polyline(wks, vector, (/30,120/), (/0,0/), polyres)
        ;overlay(plot1,stream)
        draw(vector)
        frame(wks)

        
    end do
end do
end


