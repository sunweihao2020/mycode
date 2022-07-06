;2021/5/29
;本代码根据地转偏差资料绘制：地转偏差绝对值、角度
begin 
f1 = addfile("/data5/2019swh/data/geostrophic_deviation.nc","r")
deviation =    f1->deviation
cosu      =    f1->cosu
u         =    f1->u_deviation
v         =    f1->v_deviation

deviation  =  where(abs(deviation).ge.100,deviation@_FillValue,deviation)
u  =  where(abs(u).ge.100,u@_FillValue,u)
v  =  where(abs(v).ge.100,v@_FillValue,v)
char_day=(/"D0-30","D0-29","D0-28","D0-27","D0-26","D0-25","D0-24","D0-23","D0-22","D0-21","D0-20","D0-19","D0-18","D0-17","D0-16","D0-15","D0-14","D0-13","D0-12","D0-11","D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10","D0+11","D0+12","D0+13","D0+14","D0+15"/)

;绘制角度用fill
res = True
res@cnFillOn              = True   ; turn on color fill
res@gsnDraw               = False
res@gsnFrame              = False
res@mpMinLatF            =  5 
res@mpMaxLatF            =  30.
res@mpMinLonF            =  30.
res@mpMaxLonF            =  120.
res@cnFillPalette         = "sunshine_9lev"
res@cnLineLabelsOn        = False 
res@cnInfoLabelOn         = False 
res@vpWidthF              = 0.6
res@cnLinesOn             = False 
res@vpHeightF             = 0.55
res@gsnAddCyclic         = False
res@mpGeophysicalLineThicknessF  = 1
res@cnLevelSelectionMode       = "ExplicitLevels" 
res@cnLevels             = fspan(0,6,13)
res@lbLabelBarOn         = False 
res@tmYLLabelFontHeightF      = 0.024
res@tmXBLabelFontHeightF      = 0.024
res@gsnStringFont        = 2
res@cnLineLabelsOn       = False
res@cnLineLabelFontAspectF = 2

vcres = True
vcres@gsnDraw                 = False             ; do not draw the plot      
vcres@gsnFrame                = False            ; so we can draw time stamp
vcres@vcRefAnnoOrthogonalPosF = -1.35             ; move ref vector up
vcres@vpWidthF              = 0.6
vcres@vpHeightF             = 0.55
vcres@gsnAddCyclic          =  False
vcres@vcRefMagnitudeF         = 5               ; define vector ref mag
vcres@vcRefLengthF            = 0.045            ; define length of vec ref
vcres@vcGlyphStyle            = "CurlyVector"    ; turn on curly vectors
vcres@vcMinDistanceF          = 0.02
vcres@vcRefAnnoOrthogonalPosF = -1.0   
vcres@vcMinDistanceF          = 0.02
vcres@vcLineArrowThicknessF =  1



level = (/925,850,700,500,300,200/)
levels = (/"925hPa","850hPa","700hPa","500hPa","300hPa","200hPa"/)
do yy = 22,33
    wks  =  gsn_open_wks("pdf","/data5/2019swh/paint/day/geostrophic_deviation_"+char_day(yy))
    plot1 =  new(6,graphic)
    plot2 =  new(6,graphic)
    do ll = 0,5
        res@gsnLeftString   =      levels(ll)
        res@gsnRightString  =      char_day(yy)
        plot1(ll) = gsn_csm_contour_map(wks, deviation(yy,{level(ll)},{5:30},{30:120}), res)
        plot2(ll) = gsn_csm_vector(wks,u(yy,{level(ll)},:,:),v(yy,{level(ll)},:,:),vcres)
        overlay(plot1(ll), plot2(ll))
    end do
pnlres = True
pnlres@gsnPanelMainString = "geostrophic deviation"
pnlres@gsnPanelLabelBar  = True
pnlres@gsnPanelDebug     = True     ; To get information from panel
pnlres@pmLabelBarWidthF  = 0.55
pnlres@lbLabelFontHeightF = 0.012
gsn_panel(wks,plot1,(/2,3/),pnlres)
delete(wks)
end do

end