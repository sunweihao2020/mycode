;2020/12/28
;使用资料：计算出的modelpv合成分析场
;选取层次分别是：500 700 850 地表
begin
f = addfile("/data5/2019swh/data/composite-modelpv.nc","r")
;f = addfile("/data1/MERRA_PV/daily/modellev/pv_MERRA2_modellev_0.5x0.625_monthly_mean_199605.nc","r")
;f = addfile("/data1/other_data/DataUpdate/ERA5/merra2/modelpv/model_pv_19960511.nc","r")

pvv = f->pvv
pvh = f->pvh
allpv = f->all_pv
;allpv = f->pvd
;allpv = allpv*9.8
allpv = allpv*1E+6
pvv = pvv*1E+6
pvh = pvh*1E+6
char_day=(/"D0-30","D0-29","D0-28","D0-27","D0-26","D0-25","D0-24","D0-23","D0-22","D0-21","D0-20","D0-19","D0-18","D0-17","D0-16","D0-15","D0-14","D0-13","D0-12","D0-11","D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10","D0+11","D0+12","D0+13","D0+14","D0+15"/)
level = (/"500hPa","700hPa","850hPa","surface"/)
do ll = 0,3
    do day = 0,45
       wks = gsn_open_wks("pdf", "/data5/2019swh/paint/day/pvh_"+level(ll)+"_"+day)
       ;gsn_define_colormap(wks,"posneg_1")
       res = True
       res@gsnDraw               = False
       res@gsnFrame              = False
       res@cnFillOn              = True     ; turn on color fill
      ; res@cnFillPalette         = "WhiteYellowOrangeRed"
       res@cnLineLabelsOn        = True
       res@gsnLeftString         = char_day(day)
       res@gsnRightString        =  level(ll)  
       res@cnLineLabelsOn        = False
       res@tiMainString          = "Horizontal_PV"
       ;res@cnLevelSpacingF       = 0.2
       res@cnLevelSelectionMode = "ExplicitLevels"
       res@cnLevels             =  fspan(-2, 2, 21) 
       ;res@cnFillColors         = (/2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20/) 
       res@cnFillPalette         = "hotcolr_19lev"
       res@mpMinLatF            =  -10      ; range to zoom in on
       res@mpMaxLatF            =  40.
       res@mpMinLonF            =  30.
       res@mpMaxLonF            =  120.
       ;plot = gsn_csm_contour_map(wks,allpv(day,ll,:,:), res)
       plot = gsn_csm_contour_map(wks,pvh(day,ll,:,:), res)
       polyres                   = True
       polyres@gsLineColor       = "black"
       polyres@gsLineThicknessF  = 5
       polyres@gsLineDashPattern = 2
       dum = gsn_add_polyline(wks, plot, (/30,120/), (/0,0/), polyres)
       draw(plot)
       frame(wks)
end do
end do
end