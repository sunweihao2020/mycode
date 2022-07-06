;2021/9/16
;本代码绘制模式里面的海温驱动数据看看
;我怀疑里面没有缺测
begin
file1 = addfile("/data5/2019swh/data/domain/sst_HadOIBl_bc_1x1_1850_2017_c180507.nc","r")
sst1 = file1->SST_cpl(10,:,:)
sst2 = file1->SST_cpl_prediddle(10,:,:)

res = True
;res@gsnDraw               =     False
;res@gsnFrame              =     False
;res@gsnAddCyclic          =     False

res@cnFillOn              =     True     ; turn on color fill
res@cnFillPalette         =     "cmp_b2r"
res@cnLineLabelsOn        =     False
res@cnLevelSelectionMode  =     "ExplicitLevels" 
res@cnLevels              =     fspan(0,32,33)

;res@mpMinLatF             =     -10      ; range to zoom in on
;res@mpMaxLatF             =      30.
;res@mpMinLonF             =      30.
;res@mpMaxLonF             =     120.

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

wks1       =  gsn_open_wks("pdf","/data5/2019swh/paint/model_sst1")
plot1      =  gsn_csm_contour_map(wks1,sst1, res)

wks2       =  gsn_open_wks("pdf","/data5/2019swh/paint/model_sst2")
plot2      =  gsn_csm_contour_map(wks2,sst2, res)

end