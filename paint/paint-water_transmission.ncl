;2021/3/1
;此代码绘制水汽的输送
;要素：降水 水汽输送（矢量图） 水汽的辐合辐散
begin
f1 = addfile("/data/composite_GPCP.nc","r")
f2 = addfile("/data/water_transmission.nc","r")
precip = f1->precipitation
uq = f2->uq
vq = f2->vq
uxq = f2->uxq
vxq = f2->vxq
q_div = uxq + vxq
copy_VarCoords(uxq,q_div)
q_div = q_div*1E+7
precip = where(precip .lt. 0,precip@_FillValue,precip)
char_day=(/"D0-30","D0-29","D0-28","D0-27","D0-26","D0-25","D0-24","D0-23","D0-22","D0-21","D0-20","D0-19","D0-18","D0-17","D0-16","D0-15","D0-14","D0-13","D0-12","D0-11","D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10","D0+11","D0+12","D0+13","D0+14","D0+15"/)

plot = new(15,graphic)
dum  = new(15,graphic)
wks = gsn_open_wks("pdf","/data5/2019swh/paint/day/water_transmission")

;降水的设置
res1 = True
res1@gsnDraw               = False
res1@gsnFrame              = False
res1@cnFillOn              = True     ; turn on color fill
res1@cnFillPalette         = "MPL_Blues"
res1@cnLineLabelsOn        = False
res1@lbLabelsOn            = False
;res1@lbLabelBarOn          = False
res1@cnLevelSelectionMode       = "ExplicitLevels" 
res1@cnLevels             = ispan(2,26,4)
res1@mpMinLatF            = -20      ; range to zoom in on
res1@mpMaxLatF            =  30.
res1@mpMinLonF            =  30.
res1@mpMaxLonF            = 120.
res1@gsnRightString        = " "
res1@gsnStringFont         = 2
res1@tmYLLabelFontHeightF      = 0.024
res1@tmXBLabelFontHeightF      = 0.024
res1@cnInfoLabelOn         = False

;风矢量的设置
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
vcres@vcLineArrowThicknessF = 3

;水汽通量散度的设置
res2 = True
res2@cnFillOn              = False 
res2@cnLinesOn             = True  
res2@gsnDraw               = False
res2@gsnFrame              = False
res2@cnLevelSelectionMode  =  "ExplicitLevels"
res2@cnLevelSpacingF       = 0.5
res2@cnSmoothingOn         = True
res2@cnSmoothingDistanceF  = 0.006
res2@cnInfoLabelOn         = False
res2@cnLineThicknessF      = 1.5
res2@cnLineLabelsOn        = True
res2@cnMissingValPerimOn     = True            ; turn on the missing value perim
res2@cnMissingValPerimColor  = "black"           ; outline the perimeter red
res2@cnMissingValFillPattern = 0               ; choose fill pattern 0 (solid fi
res2@cnMissingValFillColor   = "gray"          ; color fill missing areas blue
res2@gsnRightString        = ""

do day = 20,31,1
    res1@gsnLeftString         = char_day(day)
    plot(day-20) = gsn_csm_contour_map(wks,precip(day,:,:),res1)
    plot1 = gsn_csm_vector(wks,uq(day,3,:,:),vq(day,3,:,:),vcres)
    plot2 = gsn_csm_contour(wks, q_div(day,3,:,:), res2)
    overlay(plot(day-20),plot1)
    overlay(plot(day-20),plot2)
end do
pnlres = True
pnlres@lgPerimOn             = False
pnlres@lgAutoManage          = False
pnlres@lgLineLabelStrings    = (/"",""/)
pnlres@gsnPanelDebug     = True     ; To get information from panel
pnlres@gsnPanelMainString = "(10N,80E) vertical heating profile"
gsn_panel(wks1,plot1,(/3,4/),pnlres)
pnlres@gsnPanelMainString = "(10N,100E) vertical heating profile"
gsn_panel(wks2,plot2,(/3,4/),pnlres)
end

