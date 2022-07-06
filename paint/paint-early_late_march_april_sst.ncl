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
climate_sst@_FillValue        =  9999
early_sst@_FillValue          =  9999
late_sst@_FillValue           =  9999
diff_early@_FillValue         =  9999
diff_late@_FillValue          =  9999
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


;海温绘图设置
res = True
res@gsnDraw               =     False
res@gsnFrame              =     False
res@gsnAddCyclic          =     False

res@cnLinesOn             =     False   ;!!
res@cnFillOn              =     True     ; turn on color fill
res@cnFillPalette         =     "MPL_OrRd"
res@cnLineLabelsOn        =     False
res@cnLevelSelectionMode  =     "ExplicitLevels" 
res@cnLevels              =     fspan(24,32,17)

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

pnlres = True
pnlres@gsnPanelLabelBar  = True
pnlres@gsnPanelDebug     = True     ; To get information from panel
pnlres@lbLabelFontHeightF = 0.015

;绘制四张图，早晚年的3、4月份
plot  =  new(4,graphic)
wks   =  gsn_open_wks("pdf","/data5/2019swh/paint/monthly/april_march_sst")

res@gsnLeftString        =      "MARCH(early)"
plot(0)                  =      gsn_csm_contour_map(wks,early_sst(2,:,:),res)
dum0                     =      gsn_add_polyline(wks, plot(0), (/30,120/), (/0,0/), polyres)
res@gsnLeftString        =      "APRIL(early)"
plot(1)                  =      gsn_csm_contour_map(wks,early_sst(3,:,:),res)
dum1                     =      gsn_add_polyline(wks, plot(1), (/30,120/), (/0,0/), polyres)
res@gsnLeftString        =      "MARCH(late)"
plot(2)                  =      gsn_csm_contour_map(wks,late_sst(2,:,:),res)
dum2                     =      gsn_add_polyline(wks, plot(2), (/30,120/), (/0,0/), polyres)
res@gsnLeftString        =      "APRIL(late)"
plot(3)                  =      gsn_csm_contour_map(wks,late_sst(3,:,:),res)
dum3                     =      gsn_add_polyline(wks, plot(3), (/30,120/), (/0,0/), polyres)

gsn_panel(wks,plot,(/2,2/),pnlres)

end