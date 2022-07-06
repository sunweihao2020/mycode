;2020/11/2 2020/12/9
;所用资料：merra2季风爆发的合成分析
;要素：风场、散度、等位势高度线
;层次：多层次
begin
f = addfile("/data5/2019swh/data/composite3.nc","r")
ff = addfile("/data5/2019swh/data/div_vor.nc","r")
;fff = addfile("/data5/2019swh/data/composite_OLR_1021.nc","r")
u = f->uwind
v = f->vwind
;h = f->H
div = ff->div
;vorticity = ff->vor
;olr = fff->OLR

char_day=(/"D0-30","D0-29","D0-28","D0-27","D0-26","D0-25","D0-24","D0-23","D0-22","D0-21","D0-20","D0-19","D0-18","D0-17","D0-16","D0-15","D0-14","D0-13","D0-12","D0-11","D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10","D0+11","D0+12","D0+13","D0+14","D0+15"/)
lev = (/3,6,12,16,22,24/)
level = (/"925hPa","850hPa","700hPa","500hPa","200hPa","100hPa"/)

do ll = 0,5
plot1 = new(15,graphic)
plot2 = new(15,graphic)
dum1  = new(15,graphic)
dum2  = new(15,graphic)
wks1 = gsn_open_wks("pdf","/data5/2019swh/paint/day/wind_field_"+level(ll))
wks2 = gsn_open_wks("pdf","/data5/2019swh/paint/day/stream_field_"+level(ll))

do day = 4,33,2
    vcres = True
    vcres@gsnDraw                 = False             ; do not draw the plot      
    vcres@gsnFrame                = False            ; so we can draw time stamp
    ;vcres@vcRefAnnoOrthogonalPosF = -1.35             ; move ref vector up
    vcres@vpWidthF              = 0.8
    vcres@mpMinLatF            = -10 
    vcres@mpMaxLatF            =  30.
    vcres@mpMinLonF            =  30.
    vcres@mpMaxLonF            =  120.
    vcres@vcRefAnnoOrthogonalPosF = -1.0
    vcres@vpHeightF             = 0.55
    vcres@vcRefMagnitudeF         = 5             ; define vector ref mag
    vcres@vcRefLengthF            = 0.045            ; define length of vec ref
    vcres@vcGlyphStyle            = "CurlyVector"    ; turn on curly vectors
    vcres@vcMinDistanceF          = 0.017
    vcres@gsnRightString             = ""    
    vcres@vcMinDistanceF          = 0.025
    vcres@vcLineArrowThicknessF   = 1.5
    vcres@gsnLeftString         = ""
    vcres@gsnLeftString         = char_day(day)
    vcres@gsnRightString        = level(ll)
    vcres@gsnStringFont         = 2
    vcres@tmYLLabelFontHeightF      = 0.024
    vcres@tmXBLabelFontHeightF      = 0.024
    plot1((day-4)/2) = gsn_csm_vector_map(wks1,u(day,lev(ll),:,:),v(day,lev(ll),:,:),vcres)


    res3 = True
    res3@cnFillOn              = True     ; turn on color fill
    res3@gsnDraw               = False
    res3@gsnFrame              = False
    vcres@mpMinLatF            = -10 
    vcres@mpMaxLatF            =  30.
    vcres@mpMinLonF            =  30.
    vcres@mpMaxLonF            =  120.
    res3@cnFillPalette         = "NCV_blu_red"
    res3@cnLineLabelsOn        = True
    res3@lbOrientation         = "Vertical"  
    vcres@gsnRightString        = level(ll)
    res3@cnInfoLabelOn         = False 
    res3@vpWidthF              = 0.6
    res3@cnLinesOn             = False 
    res3@vpHeightF             = 0.55
    res3@mpGeophysicalLineThicknessF  = 2
    res3@cnLevelSelectionMode       = "ExplicitLevels" 
    res3@cnLevels             = ispan(-8,8,2)
    res3@cnLineLabelDensityF  = 2
    res3@cnLineLabelInterval  = 1
    res3@cnLevelSpacingF      = 2
    res3@cnLineLabelsOn       = False
    res3@cnLineLabelFontAspectF = 2
    vcres@gsnLeftString         = char_day(day)

    ;plot2  = gsn_csm_contour_map(wks, div(day,lev(ll),:,:), res3)

    res = True
    res@cnFillOn              = False     ; turn on color fill
    res@gsnDraw               = False
    res@gsnFrame              = False
    res@cnLineLabelsOn        = True 
    res@cnInfoLabelOn         = False 
    res@vpWidthF              = 0.6
    res@cnLinesOn             = True
    res@cnLineLabelBackgroundColor = -1
    res@cnLineThicknesses     = 7
    res@cnSmoothingOn         = True
    res@cnSmoothingDistanceF  = 0.003
    res@cnLevelSpacingF       = 40
    res@cnLineColor           = "brown"
    res@vpHeightF             = 0.55
    ;res@cnLevelSelectionMode  = "ExplicitLevels" 
    ;res@cnLevels              =  ispan(190, 230, 10) ;(/160,180,200,220,240,260/);(/280,260,240,220,200,180,160/);ispan(-
    res@gsnRightString        = level(ll)
    
    ;plot1 = gsn_csm_contour(wks,h(day,lev(ll),:,:), res)  ; create plot


    ;overlay(plot2,vector)
    ;overlay(plot2,plot1)
    stres = True
    stres@gsnDraw    = False
    stres@gsnFrame   = False
    stres@stArrowLengthF     = 0.008  
    stres@stLengthCheckCount = 15
    stres@stArrowStride      = 1
    stres@mpMinLatF            = -10
    stres@mpMaxLatF            = 30
    stres@mpMinLonF            = 30
    stres@mpMaxLonF            = 120
    stres@gsnLeftString         = char_day(day)
    stres@gsnRightString      = level(ll)
    stres@stMinArrowSpacingF = 0.025
    stres@stLineThicknessF   = 1.5
    ;stres@stLevelSpacingF    = 25
    stres@gsnStringFont         = 2
    stres@tmYLLabelFontHeightF      = 0.024
    stres@tmXBLabelFontHeightF      = 0.024
    stres@stLineStartStride  = 20                    ; default is 2
    stres@stMinArrowSpacingF = 0.035                ; default is 0.0             
    stres@stStepSizeF        = 0.001                ; default is dynamic
    plot2((day-4)/2) = gsn_csm_streamline_map(wks2,u(day,lev(ll),:,:),v(day,lev(ll),:,:),stres)
    
    polyres                   = True
    polyres@gsLineColor       = "black"
    polyres@gsLineThicknessF  = 1.5
    polyres@gsLineDashPattern = 2

    dum1((day-4)/2) = gsn_add_polyline(wks1, plot1((day-4)/2), (/30,120/), (/0,0/), polyres)
    dum2((day-4)/2) = gsn_add_polyline(wks2, plot2((day-4)/2), (/30,120/), (/0,0/), polyres)
  


end do
    pnlres = True
    pnlres@gsnPanelMainString = "wind at "+level(ll)
    pnlres@gsnPanelDebug     = True     ; To get information from panel
    pnlres@lbLabelFontHeightF = 0.015
    gsn_panel(wks1,plot1,(/5,3/),pnlres)
    gsn_panel(wks2,plot2,(/5,3/),pnlres)

    ;frame(wks)
end do
end