;2021/5/3
;本代码绘制爆发前夕多层的的温度场来观察温度的变化
;时间跨度-20 ~ 10 五天平均
;多层次

;===========================================绘制多层的水平图==============================================
;begin
;f = addfile("/data5/2019swh/data/composite3.nc","r")
;t = f->T
;
;lev = (/3,6,12,16,22,24/)
;level = (/"925hPa","850hPa","700hPa","500hPa","200hPa","100hPa"/)
;char_5day = (/"D0-30 - D0-26","D0-25 - D0-21","D0-20 - D0-16","D0-15 - D0-11","D0-10 - D0-6","D0-5 - D0-1","D0+1 - D0+5","D0+6 - D0+10"/)
;
;a_t = new((/8,42,361,576/),double)
;
;;先求五天平均
;do xx = 0,7
;    a_t(xx,:,:,:) = dim_avg_n_Wrap(t(xx*5:(xx*5+4),:,:,:), 0)
;end do
;
;res = True
;res@cnFillOn              = True
;res@gsnDraw               = False
;res@gsnFrame              = False
;res@mpMinLatF            = -10 
;res@mpMaxLatF            =  30
;res@mpMinLonF            =  30
;res@mpMaxLonF            =  120
;res@cnFillPalette         = "MPL_seismic"
;res@cnLineLabelsOn        = False
;res@lbLabelBarOn          = False 
;res@cnInfoLabelOn         = False 
;res@cnLinesOn             = True
;res@tmYLLabelFontHeightF      = 0.024
;res@tmXBLabelFontHeightF      = 0.024
;res@mpGeophysicalLineThicknessF  = 1
;res@cnLevelSelectionMode       = "ExplicitLevels" 
;
;polyres                   = True
;polyres@gsLineColor       = "black"
;polyres@gsLineThicknessF  = 1
;polyres@gsLineDashPattern = 2
;
;do ll = 0,5 
;    wks = gsn_open_wks("pdf","/data5/2019swh/paint/day/temperature_at_"+level(ll))
;    plot = new(6,graphic)
;    dum = new(6,graphic)
;
;    min_t = toint(floor(min(a_t(2:7,lev(ll),{-10:30},{30:120}))))
;    max_t = toint(floor(max(a_t(2:7,lev(ll),{-10:30},{30:120}))))
;    res@cnLevels    :=    ispan(min_t,max_t,1)
;    do pen = 2,7
;        res@gsnLeftString = char_5day(pen)
;        plot(pen-2) = gsn_csm_contour_map(wks,a_t(pen,lev(ll),:,:),res)
;        dum(pen-2) = gsn_add_polyline(wks, plot(pen-2), (/30,120/), (/0,0/), polyres)
;    end do
;
;    pnlres = True
;    pnlres@gsnPanelMainString = "temperature at "+level(ll)
;    pnlres@gsnPanelLabelBar  = True
;    pnlres@gsnPanelDebug     = True     ; To get information from panel
;    pnlres@lbLabelFontHeightF = 0.015
;    gsn_panel(wks,plot,(/2,3/),pnlres)
;end do
;
;end

;==============================绘制一下垂直剖面图=============================
;load "/data5/2019swh/mycode/calculate/add_TP.ncl"
;begin
;f = addfile("/data5/2019swh/data/composite3.nc","r")
;t = f->T
;u = f->uwind
;char_5day = (/"D0-30 - D0-26","D0-25 - D0-21","D0-20 - D0-16","D0-15 - D0-11","D0-10 - D0-6","D0-5 - D0-1","D0+1 - D0+5","D0+6 - D0+10"/)
;;
;a_t = new((/8,42,361,576/),double)
;a_u = new((/8,42,361,576/),double)
;;
;;先求五天平均
;do xx = 0,7
;    a_t(xx,:,:,:) = dim_avg_n_Wrap(t(xx*5:(xx*5+4),:,:,:), 0)
;    a_u(xx,:,:,:) = dim_avg_n_Wrap(u(xx*5:(xx*5+4),:,:,:), 0)
;end do
;u_a = dim_avg_n_Wrap(a_u(:,:,:,{90:95}), 3)
;t_a = dim_avg_n_Wrap(a_t(:,:,:,{90:95}), 3)
;
;min_u = toint(floor(min(u_a(2:7,{1000:200},{-10:40}))))
;max_u = toint(floor(max(u_a(2:7,{1000:200},{-10:40}))))
;
;
;res = True
;res@gsnDraw               = False
;res@gsnFrame              = False
;res@cnFillOn              = True     
;res@cnLineLabelsOn        = False
;res@lbLabelBarOn          = False
;res@cnLinesOn             = False
;res@cnFillPalette         = "BlueDarkRed18"
;res@cnLevelSelectionMode       = "ExplicitLevels" 
;res@cnLevels    :=    fspan(-10,10,11)
;res@gsnRightString       = "m/s"
;
;res@gsnStringFont         = 2
;res@tmYLLabelFontHeightF      = 0.024
;res@tmXBLabelFontHeightF      = 0.024
;res@cnInfoLabelOn         = False
;
;res1 = True
;res1@gsnDraw               = False
;res1@gsnFrame              = False
;res1@cnFillOn              = False     
;res1@cnLineLabelsOn        = False
;res1@lbLabelsOn            = False
;res1@lbLabelBarOn          = False
;res1@cnLinesOn             = True
;res1@cnLevelSpacingF       = 2
;res1@cnInfoLabelOn         = False
;res1@gsnRightString        =  " "
;
;plot1 = new(6,graphic)
;dum1 = new(6,graphic)
;
;wks1 = gsn_open_wks("pdf","/data5/2019swh/paint/day/u_tem_latlev")
;
;
;do day = 2,7
;res@gsnLeftString = char_5day(day)
;plot1(day-2) = gsn_csm_pres_hgt(wks1, u_a(day,{1000:200},{-10:40}), res )
;a = gsn_csm_pres_hgt(wks1, t_a(day,{1000:200},{-10:40}),res1)
;overlay(plot1(day-2),a)
;dum1(day-2) = overlay_x_latitude(wks1,plot1(day-2),93,"black")
;end do
;
;pnlres = True
;pnlres@gsnPanelMainString = "u-wind & temperature"
;pnlres@gsnPanelLabelBar  = True
;pnlres@gsnPanelDebug     = True     ; To get information from panel
;pnlres@pmLabelBarWidthF  = 0.55
;pnlres@lbLabelFontHeightF = 0.012
;gsn_panel(wks1,plot1,(/2,3/),pnlres)
;
;
;end

;==============================2021/5/4==========================
;绘制爆发后一侯减去前一候的值，共计三张
load "/data5/2019swh/mycode/calculate/add_TP.ncl"
begin
f = addfile("/data5/2019swh/data/composite3.nc","r")
t = f->T
u = f->uwind
char_pen = (/"P0-3 - P0-2","P0-2 - P0-1","P0-1 - P0+1"/)
a_t = new((/8,42,361,576/),double)
a_u = new((/8,42,361,576/),double)
;先求五天平均
do xx = 0,7
    a_t(xx,:,:,:) = dim_avg_n_Wrap(t(xx*5:(xx*5+4),:,:,:), 0)
    a_u(xx,:,:,:) = dim_avg_n_Wrap(u(xx*5:(xx*5+4),:,:,:), 0)
end do
u_a = dim_avg_n_Wrap(a_u(:,:,:,{90:95}), 3)
t_a = dim_avg_n_Wrap(a_t(:,:,:,{90:95}), 3)
min_u = toint(floor(min(u_a(2:7,{1000:200},{-10:40}))))
max_u = toint(floor(max(u_a(2:7,{1000:200},{-10:40}))))

delta_t = new((/3,42,361/),double)
delta_t(0,:,:) = t_a(4,:,:) - t_a(3,:,:)
delta_t(1,:,:) = t_a(5,:,:) - t_a(4,:,:)
delta_t(2,:,:) = t_a(6,:,:) - t_a(5,:,:)
copy_VarCoords(t_a(0:2,:,:), delta_t)


res = True
res@gsnDraw               = False
res@gsnFrame              = False
res@cnFillOn              = True     
res@cnLineLabelsOn        = False
res@lbLabelBarOn          = False
res@cnLinesOn             = True
res@cnLevelSelectionMode       = "ExplicitLevels" 
res@cnFillPalette         = "GMT_polar"
res@gsnRightString       = "K"
res@gsnStringFont         = 2
res@tmYLLabelFontHeightF      = 0.024
res@tmXBLabelFontHeightF      = 0.024
res@cnLevels              = fspan(-2,2,17)

wks1 = gsn_open_wks("pdf","/data5/2019swh/paint/day/delta_t")
plot = new(3,graphic)


do ll = 0,2

plot(ll) = gsn_csm_pres_hgt(wks1, delta_t(ll,{1000:200},{-10:40}), res )
end do

pnlres = True
pnlres@gsnPanelMainString = " temperature difference"
pnlres@gsnPanelLabelBar  = True
pnlres@gsnPanelDebug     = True     ; To get information from panel
pnlres@pmLabelBarWidthF  = 0.55
pnlres@lbLabelFontHeightF = 0.012
gsn_panel(wks1,plot,(/1,3/),pnlres)


end