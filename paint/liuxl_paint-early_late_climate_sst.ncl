;2021/9/1
;本代码根据使用根据Hadley SST计算的气候态海温、早年合成海温、晚年合成海温来绘制看看特征
;主要画的图有以下几项
;1. 气候态的逐月海温
;2. 早晚年与同期海温之差
;3. 早晚年春季海温异常
begin

climate  =  addfile("/data5/2019swh/data/sst_climate_hadley.nc", "r")
early    =  addfile("/data5/2019swh/data/sst_early_composite_hadley.nc","r")
late     =  addfile("/data5/2019swh/data/sst_late_composite_hadley.nc","r")

climate_sst  =  climate->sst(:,::-1,:) ;()
early_sst    =  early->sst(:,::-1,:)
late_sst     =  late->sst(:,::-1,:)

years = (/"January","February","March","April","May","June","July","August","September","October","November","December"/)

;计算早晚年同期海温之差
diff_early   =  early_sst(3,:,:) - climate_sst(3,:,:)
diff_late    =  late_sst(4,:,:)  - climate_sst(4,:,:)

;计算春季海温之差
spring_climate     =  dim_avg_n_Wrap(climate_sst(0:2,:,:), 0)
spring_early       =  dim_avg_n_Wrap(early_sst(0:2,:,:), 0)
spring_late        =  dim_avg_n_Wrap(late_sst(0:2,:,:), 0)
diff_early_spring  =  spring_early - spring_climate
diff_late_spring   =  spring_late  - spring_climate

;传递属性
copy_VarCoords(climate_sst(0,:,:), diff_early)
copy_VarCoords(climate_sst(0,:,:), diff_late)
copy_VarCoords(climate_sst(0,:,:), diff_early_spring)
copy_VarCoords(climate_sst(0,:,:), diff_late_spring)

;处理nan
climate_sst@_FillValue  =  9999
early_sst@_FillValue    =  9999
late_sst@_FillValue     =  9999
diff_early@_FillValue   =  9999
diff_late@_FillValue    =  9999
diff_early_spring@_FillValue  =  9999
diff_late_spring@_FillValue   =  9999
if (any(isnan_ieee(climate_sst))) then
  replace_ieeenan (climate_sst, climate_sst@_FillValue, 0)
  replace_ieeenan (early_sst, early_sst@_FillValue, 0)
  replace_ieeenan (late_sst, late_sst@_FillValue, 0)
  replace_ieeenan (diff_early, diff_early@_FillValue, 0)
  replace_ieeenan (diff_late, diff_late@_FillValue, 0)
  replace_ieeenan (diff_early_spring, diff_early_spring@_FillValue, 0)
  replace_ieeenan (diff_late_spring, diff_late_spring@_FillValue, 0)
end if
;if (any(isnan_ieee(early_sst))) then
;  replace_ieeenan (early_sst, early_sst@_FillValue, 0)
;end if
;if (any(isnan_ieee(late_sst))) then
;  replace_ieeenan (late_sst, late_sst@_FillValue, 0)
;end if
;if (any(isnan_ieee(diff_early))) then
;  replace_ieeenan (diff_early, diff_early@_FillValue, 0)
;end if

;首先绘制气候态的逐月海温
;这里打算一张图囊括12个月的，以及12个月分开画
plot1 = new(12,graphic)
dum1  = new(12,graphic)
wks1  = gsn_open_wks("pdf","/data5/2019swh/paint/monthly/climate_sst")

;海温绘图设置
res = True
res@gsnDraw               =     False
res@gsnFrame              =     False
res@gsnAddCyclic          =     False

res@cnLinesOn             =     False   ;!!
res@cnFillOn              =     True     ; turn on color fill
res@cnFillPalette         =     "MPL_YlOrBr"
res@cnLineLabelsOn        =     False
res@cnLevelSelectionMode  =     "ExplicitLevels" 
res@cnLevels              =     fspan(25,30,11)

res@mpMinLatF             =     -10      ; range to zoom in on
res@mpMaxLatF             =      30.
res@mpMinLonF             =      30.
res@mpMaxLonF             =     120.

res@lbLabelBarOn          =     False

res@gsnRightString        =     "units:degC"
;res@gsnStringFont         =     2

res@tmYLLabelFontHeightF  =     0.024
res@tmXBLabelFontHeightF  =     0.024

polyres                   =     True
polyres@gsLineColor       =     "black"
polyres@gsLineThicknessF  =     2
polyres@gsLineDashPattern =     2

res@cnMissingValPerimOn     =   True  
res@cnMissingValPerimColor  =   "gray"
res@cnMissingValFillPattern =   0     
res@cnMissingValFillColor   =   "gray"

do mmmm = 0,11
    res@gsnLeftString  =  years(mmmm)
    plot1(mmmm)        =  gsn_csm_contour_map(wks1,climate_sst(mmmm,:,:), res)
    dum1(mmmm)         =  gsn_add_polyline(wks1, plot1(mmmm), (/30,120/), (/0,0/), polyres)
end do

pnlres                       =    True
pnlres@gsnPanelMainString    =    "climate SST (HadISST)"
pnlres@gsnPanelLabelBar      =    True
pnlres@gsnPanelDebug         =    True     ; To get information from panel
pnlres@pmLabelBarWidthF      =    0.55
pnlres@lbLabelFontHeightF    =    0.012
gsn_panel(wks1,plot1,(/3,4/),pnlres)
delete(wks1)
delete(plot1)
delete(dum1)

 
res@lbLabelBarOn             =     True
res@pmLabelBarOrthogonalPosF =     0.13

do mmmm = 0,11
    wks2               =  gsn_open_wks("pdf","/data5/2019swh/paint/monthly/hadsst_climate_"+years(mmmm))
    plot2              =  gsn_csm_contour_map(wks2,climate_sst(mmmm,:,:), res)
    dum2               =  gsn_add_polyline(wks2, plot2 , (/30,120/), (/0,0/), polyres)

    draw(plot2)
    frame(wks2)
    delete(plot2)
end do

;绘制早晚年的海温气候态，同上
;---------------------------------------------------早年----------------------------------------------------
plot1 = new(12,graphic)
dum1  = new(12,graphic)
wks1  = gsn_open_wks("pdf","/data5/2019swh/paint/monthly/early_climate_sst")
do mmmm = 0,11
    res@gsnLeftString  =  years(mmmm)
    plot1(mmmm)        =  gsn_csm_contour_map(wks1,early_sst(mmmm,:,:), res)
    dum1(mmmm)         =  gsn_add_polyline(wks1, plot1(mmmm), (/30,120/), (/0,0/), polyres)
end do

pnlres                       =    True
pnlres@gsnPanelMainString    =    "early-year SST (HadISST)"
pnlres@gsnPanelLabelBar      =    True
pnlres@gsnPanelDebug         =    True     ; To get information from panel
pnlres@pmLabelBarWidthF      =    0.55
pnlres@lbLabelFontHeightF    =    0.012
gsn_panel(wks1,plot1,(/3,4/),pnlres)
delete(wks1)
delete(plot1)
delete(dum1)

 
res@lbLabelBarOn             =     True
res@pmLabelBarOrthogonalPosF =     0.13

do mmmm = 0,11
    wks2               =  gsn_open_wks("pdf","/data5/2019swh/paint/monthly/hadsst_early_"+years(mmmm))
    plot2              =  gsn_csm_contour_map(wks2,early_sst(mmmm,:,:), res)
    dum2               =  gsn_add_polyline(wks2, plot2 , (/30,120/), (/0,0/), polyres)

    draw(plot2)
    frame(wks2)
    delete(plot2)
end do
;--------------------------------------------晚年--------------------------------------------
plot1 = new(12,graphic)
dum1  = new(12,graphic)
wks1  = gsn_open_wks("pdf","/data5/2019swh/paint/monthly/late_climate_sst")
do mmmm = 0,11
    res@gsnLeftString  =  years(mmmm)
    plot1(mmmm)        =  gsn_csm_contour_map(wks1,late_sst(mmmm,:,:), res)
    dum1(mmmm)         =  gsn_add_polyline(wks1, plot1(mmmm), (/30,120/), (/0,0/), polyres)
end do

pnlres                       =    True
pnlres@gsnPanelMainString    =    "late-year SST (HadISST)"
pnlres@gsnPanelLabelBar      =    True
pnlres@gsnPanelDebug         =    True     ; To get information from panel
pnlres@pmLabelBarWidthF      =    0.55
pnlres@lbLabelFontHeightF    =    0.012
gsn_panel(wks1,plot1,(/3,4/),pnlres)
delete(wks1)
delete(plot1)
delete(dum1)

 
res@lbLabelBarOn             =     True
res@pmLabelBarOrthogonalPosF =     0.13

do mmmm = 0,11
    wks2               =  gsn_open_wks("pdf","/data5/2019swh/paint/monthly/hadsst_late_"+years(mmmm))
    plot2              =  gsn_csm_contour_map(wks2,late_sst(mmmm,:,:), res)
    dum2               =  gsn_add_polyline(wks2, plot2 , (/30,120/), (/0,0/), polyres)

    draw(plot2)
    frame(wks2)
    delete(plot2)
end do

;----------------------------------现在绘制同期海温之差:早年---------------------------------------
res@cnFillPalette         =     "BlueDarkRed18"
res@cnLevels              :=     fspan(-0.5,0.5,21)
res@lbLabelBarOn             =     True
res@pmLabelBarOrthogonalPosF =     0.13
wks1  = gsn_open_wks("pdf","/data5/2019swh/paint/monthly/early_diff_same_period_sst")
res@gsnLeftString  =  "same period diff(early)"
plot1       =  gsn_csm_contour_map(wks1,diff_early, res)
dum1        =  gsn_add_polyline(wks1, plot1, (/30,120/), (/0,0/), polyres)
draw(plot1)
frame(wks1)
delete(wks1)
delete(plot1)
delete(dum1)

;----------------------------------现在绘制同期海温之差:晚年---------------------------------------
res@cnFillPalette         =     "BlueDarkRed18"
res@cnLevels              =     fspan(-0.5,0.5,21)
res@lbLabelBarOn             =     True
res@pmLabelBarOrthogonalPosF =     0.13
wks1  = gsn_open_wks("pdf","/data5/2019swh/paint/monthly/late_diff_same_period_sst")
res@gsnLeftString  =  "same period diff(late)"
plot1       =  gsn_csm_contour_map(wks1,diff_late, res)
dum1        =  gsn_add_polyline(wks1, plot1, (/30,120/), (/0,0/), polyres)
draw(plot1)
frame(wks1)
delete(wks1)
delete(plot1)
delete(dum1)

;
;;----------------------------------现在绘制春季海温之差:早年---------------------------------------
res@cnFillPalette         =     "BlueDarkRed18"
res@cnLevels              =     fspan(-0.5,0.5,21)
res@lbLabelBarOn             =     True
res@pmLabelBarOrthogonalPosF =     0.13
wks1  = gsn_open_wks("pdf","/data5/2019swh/paint/monthly/early_diff_spring_sst")
res@gsnLeftString  =  "spring diff(early)"
plot1       =  gsn_csm_contour_map(wks1,diff_early_spring, res)
dum1        =  gsn_add_polyline(wks1, plot1, (/30,120/), (/0,0/), polyres)
draw(plot1)
frame(wks1)
delete(wks1)
delete(plot1)
delete(dum1)

;
;;----------------------------------现在绘制春季海温之差:晚年---------------------------------------
res@cnFillPalette         =     "BlueDarkRed18"
res@cnLevels              =     fspan(-0.5,0.5,21)
res@lbLabelBarOn             =     True
res@pmLabelBarOrthogonalPosF =     0.13
wks1  = gsn_open_wks("pdf","/data5/2019swh/paint/monthly/late_diff_spring_sst")
res@gsnLeftString  =  "spring diff(late)"
plot1       =  gsn_csm_contour_map(wks1,diff_late_spring, res)
dum1        =  gsn_add_polyline(wks1, plot1, (/30,120/), (/0,0/), polyres)
draw(plot1)
frame(wks1)
delete(wks1)
delete(plot1)
delete(dum1)

end