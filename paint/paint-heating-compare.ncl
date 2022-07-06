;2021/4/2                                              ;2021/4/3
;本代码使用文件路径:/data5/2019swh/data/heating         ;做以下修改：求候平均，然后逐层画图
;本代码使用两个视热源，两个模式提供数据，来进行互相验证   ;
begin
f1 = addfile("/data5/2019swh/data/heating/composite-heating-jra55.nc","r")
f2 = addfile("/data5/2019swh/data/heating/composite-heating-merra.nc","r")
f3 = addfile("/data5/2019swh/data/heating/composite-Q1-erain.nc","r")
f4 = addfile("/data5/2019swh/data/heating/composite-Q1-merra2.nc","r")

;=========把模式提供数据求个和================
q1 = f1->convective
q2 = f1->radiation
q3 = f1->diffusion
q_jra55 = q1+q2+q3
copy_VarCoords(q1, q_jra55)
q_merra = f2->physics

delete(q1)
delete(q2)
delete(q3)

q1 = f3->Q1
q2 = f4->Q1

pens = (/"P0-6","P0-5","P0-4","P0-3","P0-2","P0-1"/)
;==========1.绘制各个高度平面图看一看=============
do pentad = 0,5
wks1 = gsn_open_wks("pdf","/data5/2019swh/paint/day/heating1_"+pentad)
wks2 = gsn_open_wks("pdf","/data5/2019swh/paint/day/heating2_"+pentad)
wks3 = gsn_open_wks("pdf","/data5/2019swh/paint/day/heating3_"+pentad)
wks4 = gsn_open_wks("pdf","/data5/2019swh/paint/day/heating4_"+pentad)

gsn_define_colormap(wks1,"BlueDarkRed18")
gsn_define_colormap(wks2,"BlueDarkRed18")
gsn_define_colormap(wks3,"BlueDarkRed18")
gsn_define_colormap(wks4,"BlueDarkRed18")

a1 = dim_avg_n(q_jra55(pentad*5:(pentad*5+4),:,:,:), 0)
a2 = dim_avg_n(q_merra(pentad*5:(pentad*5+4),:,:,:), 0)
a3 = dim_avg_n(q1(pentad*5:(pentad*5+4),:,:,:), 0)
a4 = dim_avg_n(q2(pentad*5:(pentad*5+4),:,:,:), 0)

a1!0 = "level"
a1!1 = "lat"
a1!2 = "lon"
a1&level = q_jra55&level
a1&lat = q_jra55&lat
a1&lon = q_jra55&lon

a2!0 = "level"
a2!1 = "lat"
a2!2 = "lon"
a2&level = q_merra&level
a2&lat = q_merra&lat
a2&lon = q_merra&lon

a3!0 = "level"
a3!1 = "lat"
a3!2 = "lon"
a3&level = q1&level
a3&lat =   q1&lat
a3&lon =   q1&lon

a4!0 = "level"
a4!1 = "lat"
a4!2 = "lon"
a4&level = q2&level
a4&lat   = q2&lat
a4&lon   = q2&lon

res = True
res@gsnDraw               = False
res@gsnFrame              = False
res@cnFillOn              = True     ; turn on color fill
res@cnLineLabelsOn        = False
res@lbLabelsOn            = False
res@lbLabelBarOn          = False
res@cnLevelSelectionMode       = "ExplicitLevels" 
res@cnLevels             = fspan(-10,10,11)
res@cnFillColors         = (/2,3,4,5,6,7,13,14,15,16,17,18/)

res@mpMinLatF            = -20      ; range to zoom in on
res@mpMaxLatF            =  30.
res@mpMinLonF            =  30.
res@mpMaxLonF            = 110.
res@gsnAddCyclic         = False
res@gsnRightString       = pens(pentad)
res@gsnStringFont         = 2
res@tmYLLabelFontHeightF      = 0.024
res@tmXBLabelFontHeightF      = 0.024
res@cnInfoLabelOn         = False
;plot(day-15) = gsn_csm_contour_map(wks,qm(day,:,:), res)  

plot1 = new(6,graphic)
plot2 = new(6,graphic)
plot3 = new(6,graphic)
plot4 = new(6,graphic)

res@gsnLeftString = "925hPa"
plot1(0) = gsn_csm_contour_map(wks1,a1(33,:,:),res)
res@gsnLeftString = "850hPa"
plot1(1) = gsn_csm_contour_map(wks1,a1(30,:,:),res)
res@gsnLeftString = "700hPa"
plot1(2) = gsn_csm_contour_map(wks1,a1(25,:,:),res)
res@gsnLeftString = "500hPa"
plot1(3) = gsn_csm_contour_map(wks1,a1(21,:,:),res)
res@gsnLeftString = "300hPa"
plot1(4) = gsn_csm_contour_map(wks1,a1(17,:,:),res)
res@gsnLeftString = "200hPa"
plot1(5) = gsn_csm_contour_map(wks1,a1(14,:,:),res)

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

res@gsnLeftString = "925hPa"
plot3(0) = gsn_csm_contour_map(wks3,a3(3 ,:,:),res)
res@gsnLeftString = "850hPa"
plot3(1) = gsn_csm_contour_map(wks3,a3(6 ,:,:),res)
res@gsnLeftString = "700hPa"
plot3(2) = gsn_csm_contour_map(wks3,a3(11,:,:),res)
res@gsnLeftString = "500hPa"
plot3(3) = gsn_csm_contour_map(wks3,a3(15,:,:),res)
res@gsnLeftString = "300hPa"
plot3(4) = gsn_csm_contour_map(wks3,a3(19,:,:),res)
res@gsnLeftString = "200hPa"
plot3(5) = gsn_csm_contour_map(wks3,a3(22,:,:),res)

res@gsnLeftString = "925hPa"
plot4(0) = gsn_csm_contour_map(wks4,a4(3 ,:,:),res)
res@gsnLeftString = "850hPa"
plot4(1) = gsn_csm_contour_map(wks4,a4(6 ,:,:),res)
res@gsnLeftString = "700hPa"
plot4(2) = gsn_csm_contour_map(wks4,a4(11,:,:),res)
res@gsnLeftString = "500hPa"
plot4(3) = gsn_csm_contour_map(wks4,a4(15,:,:),res)
res@gsnLeftString = "300hPa"
plot4(4) = gsn_csm_contour_map(wks4,a4(19,:,:),res)
res@gsnLeftString = "200hPa"
plot4(5) = gsn_csm_contour_map(wks4,a4(22,:,:),res)

pnlres = True
pnlres@gsnPanelMainString = "Q"
pnlres@gsnPanelLabelBar  = True
pnlres@gsnPanelDebug     = True     ; To get information from panel
pnlres@pmLabelBarWidthF  = 0.55
pnlres@lbLabelFontHeightF = 0.012
gsn_panel(wks1,plot1,(/2,3/),pnlres)
gsn_panel(wks2,plot2,(/2,3/),pnlres)
gsn_panel(wks3,plot3,(/2,3/),pnlres)
gsn_panel(wks4,plot4,(/2,3/),pnlres)
end do

end