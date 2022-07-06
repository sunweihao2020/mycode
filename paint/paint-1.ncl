;2021/1/19
;绘制等位温线
;使用资料：merra2合成分析资料


begin
f = addfile("/data5/2019swh/data/composite_equivalent_tem.nc","r")
pt = f->theate_e
char_day=(/"D0-30","D0-29","D0-28","D0-27","D0-26","D0-25","D0-24","D0-23","D0-22","D0-21","D0-20","D0-19","D0-18","D0-17","D0-16","D0-15","D0-14","D0-13","D0-12","D0-11","D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10","D0+11","D0+12","D0+13","D0+14","D0+15"/)
lev = (/3,6,16,22/)
level = (/"925","850","500","200"/)
longitudes  = (/416,420,424,428,432,436,440,444,448,452/)
char_lon    = (/"80E","82.5E","85E","87.5E","90E","92.5E","95E","97.5E","100E","102.5E"/)
f1 = addfile("/data5/2019swh/data/composite3.nc","r")
v = f->vwind
w = f->OMEGA
w = w*(-60)
v1 = dim_avg_n(v(:,:,:,400:416), 3)
v1!0 = "time"
v1!1 = "level"
v1!2 = "lat"
v1&time = v&time
v1&level = v&level
v1&lat = v&lat
v2 = dim_avg_n(v(:,:,:,440:456), 3)
copy_VarCoords(v1, v2)
;=====================================平面图============================================
;do z=0,3
;wks = gsn_open_wks("pdf","/data5/2019swh/paint/day/"+level(z)+"pt_field")
;plot := new(15,graphic)
;    do day = 4,33,2
;        res = True
;        res@cnLinesOn             = True  
;        res@gsnDraw               = False
;        res@gsnFrame              = False
;        res@cnLevelSelectionMode  =  "ExplicitLevels"
;        res@cnLevelSpacingF       = 2
;        res@cnSmoothingOn         = True
;        res@cnSmoothingDistanceF  = 0.006
;        res@cnInfoLabelOn         = False
;        res@cnLineThicknessF      = 1.5
;        res@cnLineLabelsOn        = True
;        res@cnLineLabelDensityF   = 2
;        res@cnMissingValPerimOn     = True            ; turn on the missing value perim
;        res@cnMissingValPerimColor  = "black"           ; outline the perimeter red
;        res@cnMissingValFillPattern = 0               ; choose fill pattern 0 (solid fi
;        res@cnMissingValFillColor   = "gray"          ; color fill missing areas blue
;        res@mpMinLatF            = -10 
;        res@mpMaxLatF            =  30.
;        res@mpMinLonF            =  30.
;        res@mpMaxLonF            =  120.
;        res@gsnStringFont         = 2
;        res@tmYLLabelFontHeightF      = 0.024
;        res@tmXBLabelFontHeightF      = 0.024
;
;        res@gsnLeftString       = char_day(day)
;        res@gsnRightString      = level(z)
;        plot((day-4)/2) = gsn_csm_contour_map(wks, pt(day,lev(z),:,:), res)
;    end do
;pnlres = True
;pnlres@gsnPanelMainString = "potential temperature"
;pnlres@gsnPanelLabelBar  = True
;pnlres@gsnPanelDebug     = True     ; To get information from panel
;pnlres@pmLabelBarWidthF  = 0.55
;pnlres@lbLabelFontHeightF = 0.012
;gsn_panel(wks,plot,(/5,3/),pnlres)
;end do
;end
;
;======================================垂直剖面图===============================
;这里先5度一平均

wks1 = gsn_open_wks("pdf","/data5/2019swh/paint/day/theate_vertical_field95105")
wks2 = gsn_open_wks("pdf","/data5/2019swh/paint/day/theate_vertical_field7080")


plot1 = new(15,graphic)
dum1 = new(15,graphic)
plot2 = new(15,graphic)
dum2 = new(15,graphic)
ptm = dim_avg_n(pt(:,:,:,440:456), 3)
ptm2 = dim_avg_n(pt(:,:,:,400:416), 3)

ptm!0 = "time"
ptm!1 = "level"
ptm!2 = "lat"
ptm&time = pt&time
ptm&level = pt&level
ptm&lat = pt&lat
copy_VarCoords(ptm, ptm2)
do day = 4,33,2
    res   = True
    res@gsnDraw     = False                                
    res@gsnFrame     =  False
    res@gsnLeftString   =  char_day(day)
    res@cnLevelSelectionMode = "ExplicitLevels" 
    res@cnLevels             =  ispan(268, 352, 2)
    res@cnFillColor         = (/0/)
    res@cnFillOn        = False
    ;res@cnLineLabelsOn  = True
    res@cnLineLabelBackgroundColor = -1
    res@cnInfoLabelOn         = False
    res@gsnStringFont         = 2
    res@cnLineLabelDensityF   = 4
    res@cnLineLabelFontThicknessF = 1
    res@cnLineLabelFont       = 2.5
    res@tmYLLabelFontHeightF      = 0.024
    res@tmXBLabelFontHeightF      = 0.024
    res@gsnRightString        = "K"
    res@cnMissingValPerimOn     = True            ; turn on the missing value perimete
    res@cnMissingValPerimColor  = "blue"           ; outline the perimeter red
    res@cnMissingValFillScaleF  = 3
    res@cnMissingValFillPattern = 0               ; choose fill pattern 0 (solid fill)
    res@cnMissingValFillColor   = "gray"          ; color fill missing areas blue
    plot1((day-4)/2) = gsn_csm_pres_hgt(wks1,ptm(day,0:14,{-10:30}), res)

end do
pnlres = True
pnlres@gsnPanelMainString = "vertical potential temperature(95-105E)"
pnlres@gsnPanelLabelBar  = False
pnlres@gsnPanelDebug     = True     ; To get information from panel
pnlres@pmLabelBarWidthF  = 0.55
pnlres@lbLabelFontHeightF = 0.012
gsn_panel(wks1,plot1,(/3,5/),pnlres)



end