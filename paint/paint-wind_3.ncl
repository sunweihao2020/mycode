;2021/6/4
;所用资料：merra2季风爆发的合成分析
;要素：风场、散度
;层次：多层次
begin
f = addfile("/data5/2019swh/data/composite3.nc","r")
u = f->uwind
v = f->vwind


char_day=(/"D0-30","D0-29","D0-28","D0-27","D0-26","D0-25","D0-24","D0-23","D0-22","D0-21","D0-20","D0-19","D0-18","D0-17","D0-16","D0-15","D0-14","D0-13","D0-12","D0-11","D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10","D0+11","D0+12","D0+13","D0+14","D0+15"/)
lev = (/3,6,12,16,22,24/)
level = (/"925hPa","850hPa","700hPa","500hPa","200hPa","100hPa"/)
days =  (/10,23,29,32/)


vcres = True
vcres@gsnDraw                 = False             ; do not draw the plot      
vcres@gsnFrame                = False            ; so we can draw time stamp
vcres@vcRefAnnoOrthogonalPosF = -1.35             ; move ref vector up
vcres@vpWidthF              = 0.6
vcres@vpHeightF             = 0.55
vcres@gsnAddCyclic          =  False
vcres@vcRefMagnitudeF         = 15            ; define vector ref mag
vcres@vcRefLengthF            = 0.045            ; define length of vec ref
vcres@vcGlyphStyle            = "LineArrow"    ; turn on curly vectors
vcres@vcMinDistanceF          = 0.017
vcres@vcRefAnnoOrthogonalPosF = -1.0
vcres@gsnRightString             = ""    
vcres@vcMinDistanceF          = 0.02
vcres@vcRefLengthF               = 0.03
vcres@gsnLeftString         = ""
vcres@vcLineArrowThicknessF =   2
vcres@mpMinLatF            =  -10 
vcres@mpMaxLatF            =  30.
vcres@mpMinLonF            =  30.
vcres@mpMaxLonF            =  120.


polyres                   = True
polyres@gsLineColor       = "black"
polyres@gsLineThicknessF  = 1
polyres@gsLineDashPattern = 2


do ll = 0,5
plot1 = new(4,graphic)
dum1  = new(4,graphic)
wks1 = gsn_open_wks("pdf","/data5/2019swh/paint/day/4_wind_"+level(ll))

do day = 0,3
    vcres@gsnLeftString = char_day(days(day))
    vcres@gsnRightString = level(ll)
    plot1(day) = gsn_csm_vector_map(wks1,u(days(day),lev(ll),:,:),v(days(day),lev(ll),:,:),vcres)
    dum1(day)  = gsn_add_polyline(wks1, plot1(day), (/30,120/), (/0,0/), polyres)
end do
    pnlres = True
    pnlres@gsnPanelMainString = "wind at "+level(ll)
    pnlres@gsnPanelLabelBar  = True
    pnlres@gsnPanelDebug     = True     ; To get information from panel
    pnlres@lbLabelFontHeightF = 0.015
    gsn_panel(wks1,plot1,(/2,2/),pnlres)
    delete(wks1)

    ;frame(wks)
end do
end
