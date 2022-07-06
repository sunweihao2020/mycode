;2021/4/18
;本代码计算爆发前一个月的Q、流场的平均，并绘制
begin
f1 = addfile("/data5/2019swh/data/composite-Q1-erain.nc","r")
f2 = addfile("/data5/2019swh/data/composite-erain.nc", "r")
f3 = addfile("/data5/2019swh/data/composite_OISST.nc", "r")
f4 = addfile("/data5/2019swh/data/composite-merra2-single.nc","r")
f5 = addfile("/data5/2019swh/data/land_and_ocean.nc","r")

q = f1->Q1(0:29,:,:,:)
u = f2->u(0:29,:,:,:)
v = f2->v(0:29,:,:,:)
sst = f3->SST(0:29,:,:)
t2m = f4->T2M(0:29,:,:)
lsm = short2flt(f5->lsm(0,:,:))

qa = dim_avg_n_Wrap(q, 0)
ua = dim_avg_n_Wrap(u, 0)
va = dim_avg_n_Wrap(v, 0)
ssta = dim_avg_n_Wrap(sst, 0)
t2ma = dim_avg_n_Wrap(t2m, 0)

plot1 = new(2,graphic)
dum1   = new(2,graphic)
wks1 = gsn_open_wks("pdf","/data5/2019swh/paint/day/average_stream_field_low")

plot2 = new(4,graphic)
dum2   = new(4,graphic)
wks2 = gsn_open_wks("pdf","/data5/2019swh/paint/day/average_stream_field_high")

t2ma_land = t2ma
t2ma_land = mask(t2ma,(lsm .gt. 0.1),1)

t2ma_land = t2ma_land - 273.15

res = True
res@gsnDraw               = False
res@gsnFrame              = False
res@cnFillOn              = True     ; turn on color fill
res@cnFillPalette         = "MPL_OrRd"
res@cnLineLabelsOn        = False
res@lbLabelBarOn          = False 
res@mpMinLatF            = -20      ; range to zoom in on
res@mpMaxLatF            =  30.
res@mpMinLonF            =  30.
res@mpMaxLonF            = 120.
res@cnLevelSelectionMode       = "ExplicitLevels" 
res@cnLevels             = fspan(25,30,21)
;res@cnLinesOn = False
res@gsnRightString       = "degC"
res@cnInfoLabelOn = False
res@gsnStringFont         = 2
res@lbLabelBarOn = False
res@tmYLLabelFontHeightF      = 0.024
res@tmXBLabelFontHeightF      = 0.024

stres = True
stres@gsnDraw    = False
stres@gsnFrame   = False
stres@stArrowLengthF     = 0.008  
stres@stLengthCheckCount = 15
stres@stArrowStride      = 1
stres@stMinArrowSpacingF = 0.025
stres@stLineThicknessF   = 1.5
;stres@stLevelSpacingF    = 25
stres@gsnStringFont         = 2
stres@gsnRightString = " "
stres@tmYLLabelFontHeightF      = 0.024
stres@tmXBLabelFontHeightF      = 0.024
stres@stLineStartStride  = 4                    ; default is 2            
stres@stStepSizeF        = 0.001                ; default is dynamic

polyres                   = True
polyres@gsLineColor       = "black"
polyres@gsLineThicknessF  = 2
polyres@gsLineDashPattern = 2
    
res@gsnRightString = "925hPa"
plot1(0) = gsn_csm_contour_map(wks1,ssta,res)
res@gsnRightString = " "
b = gsn_csm_streamline(wks1,ua(3,:,:),va(3,:,:),stres)
overlay(plot1(0),b)
dum1(0) = gsn_add_polyline(wks1, plot1(0), (/30,120/), (/0,0/), polyres)
res@gsnRightString = "850hPa"
plot1(1) = gsn_csm_contour_map(wks1,ssta,res)
res@gsnRightString = " "
b := gsn_csm_streamline(wks1,ua(6,:,:),va(6,:,:),stres)
overlay(plot1(1),b)
dum1(1) = gsn_add_polyline(wks1, plot1(1), (/30,120/), (/0,0/), polyres)


pnlres = True
pnlres@gsnPanelLabelBar  = True
pnlres@gsnPanelDebug     = True     
pnlres@pmLabelBarWidthF  = 0.55
pnlres@lbLabelFontHeightF = 0.012
pnlres@gsnPanelMainString = "streamline & surface temperature"
gsn_panel(wks1,plot1,(/1,2/),pnlres)

;====================绘制热源叠加环流场==================
delete(res@cnFillPalette)
gsn_define_colormap(wks2,"BlueDarkRed18")
res@cnLineLabelsOn        = False
res@cnLevels            := fspan(-5,5,11)
res@cnFillColors        := (/2,3,4,5,6,7,13,14,15,16,17,18/)

res@gsnLeftString = "700hPa"
plot2(0) = gsn_csm_contour_map(wks2,qa(11,:,:),res)
b := gsn_csm_streamline(wks2,ua(11,:,:),va(11,:,:),stres)
overlay(plot2(0),b)
dum2(0) = gsn_add_polyline(wks2, plot2(0), (/30,120/), (/0,0/), polyres)
res@gsnLeftString = "500hPa"
plot2(1) = gsn_csm_contour_map(wks2,qa(15,:,:),res)
b := gsn_csm_streamline(wks2,ua(15,:,:),va(15,:,:),stres)
overlay(plot2(1),b)
dum2(1) = gsn_add_polyline(wks2, plot2(1), (/30,120/), (/0,0/), polyres)
res@gsnLeftString = "200hPa"
plot2(2) = gsn_csm_contour_map(wks2,qa(22,:,:),res)
b := gsn_csm_streamline(wks2,ua(22,:,:),va(22,:,:),stres)
overlay(plot2(2),b)
dum2(2) = gsn_add_polyline(wks2, plot2(2), (/30,120/), (/0,0/), polyres)
res@gsnLeftString = "100hPa"
plot2(3) = gsn_csm_contour_map(wks2,qa(26,:,:),res)
b := gsn_csm_streamline(wks2,ua(26,:,:),va(26,:,:),stres)
overlay(plot2(3),b)
dum2(3) = gsn_add_polyline(wks2, plot2(3), (/30,120/), (/0,0/), polyres)

pnlres = True
pnlres@gsnPanelLabelBar  = True
pnlres@gsnPanelDebug     = True     
pnlres@pmLabelBarWidthF  = 0.55
pnlres@lbLabelFontHeightF = 0.012
pnlres@gsnPanelMainString = "streamline & diabatic heating"
gsn_panel(wks2,plot2,(/2,2/),pnlres)

end