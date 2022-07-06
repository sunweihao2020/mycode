;2021/4/19
;所用资料：merra2季风爆发的合成分析
;要素：风场、散度
;层次：多层次
begin
f = addfile("/data5/2019swh/data/composite-thermal_wind.nc","r")
u = f->uti
v = f->vti


char_day=(/"D0-30","D0-29","D0-28","D0-27","D0-26","D0-25","D0-24","D0-23","D0-22","D0-21","D0-20","D0-19","D0-18","D0-17","D0-16","D0-15","D0-14","D0-13","D0-12","D0-11","D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10","D0+11","D0+12","D0+13","D0+14","D0+15"/)
lev = (/3,6,12,16,22,24/)
level = (/"925hPa","850hPa","700hPa","500hPa","200hPa","100hPa"/)


vcres = True
vcres@gsnDraw                 = False             ; do not draw the plot      
vcres@gsnFrame                = False            ; so we can draw time stamp
vcres@vcRefAnnoOrthogonalPosF = -1.35             ; move ref vector up
vcres@vpWidthF              = 0.6
vcres@vpHeightF             = 0.55
vcres@gsnAddCyclic          =  False
vcres@vcRefMagnitudeF         = 10            ; define vector ref mag
vcres@vcRefLengthF            = 0.045            ; define length of vec ref
vcres@vcGlyphStyle            = "FillArrow"    ; turn on curly vectors
vcres@vcMinDistanceF          = 0.017
vcres@vcRefAnnoOrthogonalPosF = -1.0
vcres@gsnRightString             = ""    
vcres@vcMinDistanceF          = 0.02
vcres@gsnLeftString         = ""
vcres@vcLineArrowThicknessF =1
vcres@mpMinLatF            =  10 
vcres@mpMaxLatF            =  30.
vcres@mpMinLonF            =  60.
vcres@mpMaxLonF            =  120.


polyres                   = True
polyres@gsLineColor       = "black"
polyres@gsLineThicknessF  = 1
polyres@gsLineDashPattern = 2


do ll = 0,5
plot1 = new(15,graphic)
dum1  = new(15,graphic)
wks1 = gsn_open_wks("pdf","/data5/2019swh/paint/day/thermal_wind_"+level(ll))

do day = 20,34
    vcres@gsnLeftString = char_day(day)
    plot1(day-20) = gsn_csm_vector_map(wks1,u(day,lev(ll),:,:),v(day,lev(ll),:,:),vcres)
end do
    pnlres = True
    pnlres@gsnPanelMainString = "wind at "+level(ll)+" & divergence"
    pnlres@gsnPanelLabelBar  = True
    pnlres@gsnPanelDebug     = True     ; To get information from panel
    pnlres@lbLabelFontHeightF = 0.015
    gsn_panel(wks1,plot1,(/5,3/),pnlres)

    ;frame(wks)
end do
end