;2021/5/6
;本代码使用计算得到的Q2来绘制图像，主要用于检验计算的正确性
;类型，绘制各层的和Q1比一比看看

begin
f1 = addfile("/data5/2019swh/data/heating/composite_Q2.nc","r")
f2 = addfile("/data5/2019swh/data/heating/composite-Q1-merra2.nc","r")
q2 = f1->Q2
q1 = f2->Q1


pens = (/"P0-6","P0-5","P0-4","P0-3","P0-2","P0-1"/)
;==========1.绘制各个高度平面图看一看=============
do pentad = 0,5
wks1 = gsn_open_wks("pdf","/data5/2019swh/paint/day/heating_q1_"+pentad)
wks2 = gsn_open_wks("pdf","/data5/2019swh/paint/day/heating_q2_"+pentad)


gsn_define_colormap(wks1,"BlueDarkRed18")
gsn_define_colormap(wks2,"BlueDarkRed18")

a1 = dim_avg_n_Wrap(q1(pentad*5:(pentad*5+4),:,:,:), 0)
a2 = dim_avg_n_Wrap(q2(pentad*5:(pentad*5+4),:,:,:), 0)
printVarSummary(a1)

res                       = True
res@gsnDraw               = False
res@gsnFrame              = False
res@cnFillOn              = True    
res@cnLineLabelsOn        = False
res@lbLabelsOn            = False
res@lbLabelBarOn          = False
res@cnLevelSelectionMode  = "ExplicitLevels" 
res@cnLevels              = fspan(-10,10,11)
res@cnFillColors          = (/2,3,4,5,6,7,13,14,15,16,17,18/)
 
res@mpMinLatF             = -20  
res@mpMaxLatF             =  30.
res@mpMinLonF             =  30.
res@mpMaxLonF             = 120.
res@gsnAddCyclic          = False
res@gsnRightString        = pens(pentad)
res@gsnStringFont         = 2
res@tmYLLabelFontHeightF  = 0.024
res@tmXBLabelFontHeightF  = 0.024
res@cnInfoLabelOn         = False


plot1 = new(6,graphic)
plot2 = new(6,graphic)

res@gsnLeftString = "925hPa"
plot1(0) = gsn_csm_contour_map(wks1,a1(3 ,:,:),res)
res@gsnLeftString = "850hPa"
plot1(1) = gsn_csm_contour_map(wks1,a1(6 ,:,:),res)
res@gsnLeftString = "700hPa"
plot1(2) = gsn_csm_contour_map(wks1,a1(12,:,:),res)
res@gsnLeftString = "500hPa"
plot1(3) = gsn_csm_contour_map(wks1,a1(16,:,:),res)
res@gsnLeftString = "300hPa"
plot1(4) = gsn_csm_contour_map(wks1,a1(20,:,:),res)
res@gsnLeftString = "200hPa"
plot1(5) = gsn_csm_contour_map(wks1,a1(22,:,:),res)

res@gsnLeftString = "925hPa"
plot2(0) = gsn_csm_contour_map(wks2,a2(3 ,:,:),res)
res@gsnLeftString = "850hPa"
plot2(1) = gsn_csm_contour_map(wks2,a2(6 ,:,:),res)
res@gsnLeftString = "700hPa"
plot2(2) = gsn_csm_contour_map(wks2,a2(12,:,:),res)
res@gsnLeftString = "500hPa"
plot2(3) = gsn_csm_contour_map(wks2,a2(16,:,:),res)
res@gsnLeftString = "300hPa"
plot2(4) = gsn_csm_contour_map(wks2,a2(20,:,:),res)
res@gsnLeftString = "200hPa"
plot2(5) = gsn_csm_contour_map(wks2,a2(22,:,:),res)


pnlres = True
pnlres@gsnPanelMainString = "Q1"
pnlres@gsnPanelLabelBar  = True
pnlres@gsnPanelDebug     = True     ; To get information from panel
pnlres@pmLabelBarWidthF  = 0.55
pnlres@lbLabelFontHeightF = 0.012
gsn_panel(wks1,plot1,(/2,3/),pnlres)
pnlres@gsnPanelMainString = "Q2"
gsn_panel(wks2,plot2,(/2,3/),pnlres)
end do

end