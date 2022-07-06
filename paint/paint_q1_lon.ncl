;2021/4/26
;本代码绘制90E~95E纬向平均的经向垂直剖面图
;使用merra2以及erain的资料场反算出来各画一下
load "/data5/2019swh/mycode/calculate/add_TP.ncl"
begin
f1 = addfile("/data5/2019swh/data/heating/composite-Q1-erain.nc","r")
f2 = addfile("/data5/2019swh/data/heating/composite-Q1-merra2.nc","r")
q1 = f1->Q1
q2 = f2->Q1
char_day=(/"D0-30","D0-29","D0-28","D0-27","D0-26","D0-25","D0-24","D0-23","D0-22","D0-21","D0-20","D0-19","D0-18","D0-17","D0-16","D0-15","D0-14","D0-13","D0-12","D0-11","D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10","D0+11","D0+12","D0+13","D0+14","D0+15"/)

q1_a = dim_avg_n_Wrap(q1(:,:,:,{90:95}), 3)
q2_a = dim_avg_n_Wrap(q2(:,:,:,{90:95}), 3)

res = True
res@gsnDraw               = False
res@gsnFrame              = False
res@cnFillOn              = True     
res@cnLineLabelsOn        = False
res@lbLabelsOn            = False
res@lbLabelBarOn          = False
res@cnLevelSelectionMode       = "ExplicitLevels" 
res@cnLevels             = fspan(-10,10,11)
res@cnFillColors         = (/2,3,4,5,6,7,13,14,15,16,17,18/)
res@gsnRightString       = "K/day"


res@gsnStringFont         = 2
res@tmYLLabelFontHeightF      = 0.024
res@tmXBLabelFontHeightF      = 0.024
res@cnInfoLabelOn         = False

plot1 = new(15,graphic)
dum1 = new(15,graphic)
plot2 = new(15,graphic)
dum2 = new(15,graphic)
wks1 = gsn_open_wks("pdf","/data5/2019swh/paint/day/q1_lat_pres_erain")
wks2 = gsn_open_wks("pdf","/data5/2019swh/paint/day/q1_lat_pres_merra2")

gsn_define_colormap(wks1,"BlueDarkRed18")
gsn_define_colormap(wks2,"BlueDarkRed18")

do day = 16,30
res@gsnLeftString = char_day(day)
plot1(day-16) = gsn_csm_pres_hgt(wks1, q1_a(day,{1000:100},{-10:40}), res )
dum1(day-16) = overlay_x_latitude(wks1,plot1(day-16),93,"black")
plot2(day-16) = gsn_csm_pres_hgt(wks2, q2_a(day,{1000:100},{-10:40}), res )
dum2(day-16) = overlay_x_latitude(wks2,plot2(day-16),93,"black")
end do

pnlres = True
pnlres@gsnPanelMainString = "Q1 (erain)"
pnlres@gsnPanelLabelBar  = True
pnlres@gsnPanelDebug     = True     ; To get information from panel
pnlres@pmLabelBarWidthF  = 0.55
pnlres@lbLabelFontHeightF = 0.012
gsn_panel(wks1,plot1,(/3,5/),pnlres)
pnlres@gsnPanelMainString = "Q1 (MERRA2)"
gsn_panel(wks2,plot2,(/3,5/),pnlres)

end