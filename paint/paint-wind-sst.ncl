;2020/11/2
;所用资料：merra2季风爆发的合成分析
;要素：绝对涡度零线，风场，olr
;层次：925hpa
begin
f = addfile("/data5/2019swh/data/composite_OISST.nc","r")
ff = addfile("/data5/2019swh/data/composite_u10v10.nc","r")
;fff = addfile("/data5/2019swh/data/composite_OLR_1021.nc","r")
u = ff->u10m
v = ff->v10m
sst = f->SST
;vorticity = ff->vor
;olr = fff->OLR

char_day=(/"D0-15","D0-14","D0-13","D0-12","D0-11","D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10","D0+11","D0+12","D0+13","D0+14","D0+15"/)


do day = 15,45
    wks = gsn_open_wks("pdf","/data5/2019swh/paint/day/10mwind_sst_"+day)
    vcres = True
    vcres@gsnDraw                 = False             ; do not draw the plot      
    vcres@gsnFrame                = False            ; so we can draw time stamp
    vcres@vcRefAnnoOrthogonalPosF = -1.35             ; move ref vector up
    vcres@vpWidthF              = 0.6
    vcres@vpHeightF             = 0.55
    vcres@vcRefMagnitudeF         = 10.0             ; define vector ref mag
    vcres@vcRefLengthF            = 0.045            ; define length of vec ref
    vcres@vcGlyphStyle            = "CurlyVector"    ; turn on curly vectors
    vcres@vcMinDistanceF          = 0.017
    vcres@gsnRightString             = ""    
    vcres@vcMinDistanceF          = 0.02
    vcres@gsnLeftString         = ""
    vcres@vcLineArrowThicknessF =3

  

    res3 = True
    res3@cnFillOn              = True     ; turn on color fill
    res3@gsnDraw               = False
    res3@gsnFrame              = False
    res3@mpMinLatF            = -20 
    res3@mpMaxLatF            =  30.
    res3@mpMinLonF            =  30.
    res3@mpMaxLonF            =  120.
    res3@cnFillPalette         = "CBR_coldhot"
    res3@cnLineLabelsOn        = True
    res3@lbOrientation         = "Vertical"  
    res3@cnInfoLabelOn         = False 
    res3@vpWidthF              = 0.6
    res3@cnLinesOn             = False
    ;res3@gsnContourZeroLineThicknessF = 5
    ;res3@gsnContourNegLineDashPattern = 1
    ;res3@cnLineThicknessF      = 5
    ;res3@cnLineColor           = "red" 
    res3@vpHeightF             = 0.55
    res3@mpGeophysicalLineThicknessF  = 2
   res3@cnLevelSelectionMode       = "ExplicitLevels" 
   res3@cnLevels             = ispan(20,30,1)
    res3@cnLineLabelDensityF  = 2
    res3@cnLineLabelInterval  = 1
    res3@cnLevelSpacingF      = 2
    res3@cnLineLabelsOn       = False
    res3@cnLineLabelFontAspectF = 2
    res3@gsnLeftString         = char_day(day-15)

    plot2  = gsn_csm_contour_map(wks, sst(day,:,:), res3)
    vector = gsn_csm_vector(wks,u(day,:,:),v(day,:,:),vcres)
    res = True
    res@cnFillOn              = False     ; turn on color fill
    res@gsnDraw               = False
    res@gsnFrame              = False
    res@cnLineLabelsOn        = True 
    res@cnInfoLabelOn         = False 
    res@vpWidthF              = 0.6
    res@cnLinesOn             = True
    res@cnLineLabelBackgroundColor = -1
    res@cnLineThicknesses     = 5
    res@cnSmoothingOn         = True
    res@cnSmoothingDistanceF  = 0.003
    res@cnLineColor           = "blue"
    res@vpHeightF             = 0.55
    res@cnLevelSelectionMode  = "ExplicitLevels" 
    res@cnLevels              =  ispan(190, 230, 10) ;(/160,180,200,220,240,260/);(/280,260,240,220,200,180,160/);ispan(-
    res@gsnRightString        = ""
    
    ;plot1 = gsn_csm_contour(wks,olr(day,{-10:25},:), res)  ; create plot

    polyres                   = True
    polyres@gsLineColor       = "black"
    polyres@gsLineThicknessF  = 3
    polyres@gsLineDashPattern = 2
    dum = gsn_add_polyline(wks, plot2, (/30,120/), (/0,0/), polyres)

    overlay(plot2,vector)
    ;overlay(vector,plot2)
    draw(plot2)
    frame(wks)
end do
end