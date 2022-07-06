;2021/8/16
;本代码给出晚年-早年的风场图，分别是u的平面图以及v的纬向垂直剖面图
begin
path = "/data5/2019swh/data/"
f1 = addfile(path+"early-year-composite.nc","r")
f2 = addfile(path+"late-year-composite.nc", "r")

u1 = f1->u
u2 = f2->u
v1 = f1->v
v2 = f2->v

diff_u = u2 - u1
diff_v = v2 - v1
copy_VarCoords(u1, diff_u)
copy_VarCoords(v1, diff_v)
diff_u_average  =  dim_avg_n_Wrap(diff_u(20:35,:,:,:), 0)
diff_v_average  =  dim_avg_n_Wrap(diff_v(20:35,:,:,:), 0)

char_day=(/"D0-30","D0-29","D0-28","D0-27","D0-26","D0-25","D0-24","D0-23","D0-22","D0-21","D0-20","D0-19","D0-18","D0-17","D0-16","D0-15","D0-14","D0-13","D0-12","D0-11","D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10","D0+11","D0+12","D0+13","D0+14","D0+15"/)
;lev = (/3,6,12,16,22,24/)
lev = (/3,6/)
level = (/"925hPa","850hPa"/)
;level = (/"925hPa","850hPa","700hPa","500hPa","200hPa","100hPa"/)
lat = (/0,10/)

res = True
res@cnFillOn              = True 
res@cnLinesOn             = True  
res@gsnDraw               = False
res@gsnFrame              = False

res@cnLevelSelectionMode  =  "ExplicitLevels"
;res@cnInfoLabelOn         = False
res@cnLevelSpacingF       = 2
res@cnLineThicknessF      = 1.5
res@cnLineLabelsOn        = True
res@cnLevels              = ispan(0,6,1)
res@cnFillColors         = (/10,11,12,13,14,15,16,17/)

res@lbLabelBarOn          = True
res@lbLabelFontHeightF    = 0.013

res@pmLabelBarHeightF     = 0.08
res@pmLabelBarWidthF      = 0.8
res@pmLabelBarOrthogonalPosF  =  0.1
;res@gsnRightString        = ""

res@tmYLLabelFontHeightF  = 0.024
res@tmXBLabelFontHeightF  = 0.024

res@mpMinLatF            = -10 
res@mpMaxLatF            =  30.
res@mpMinLonF            =  30.
res@mpMaxLonF            =  120.

res@cnMissingValPerimOn     = True            ; turn on the missing value perim
res@cnMissingValPerimColor  = "black"           ; outline the perimeter red
res@cnMissingValFillPattern = 0               ; choose fill pattern 0 (solid fi
res@cnMissingValFillColor   = "white"          ; color fill missing areas blue

polyres                   = True
polyres@gsLineColor       = "black"
polyres@gsLineThicknessF  = 1
polyres@gsLineDashPattern = 2

;------------------------------绘制逐日的差值图 2021/8/16------------------------------------------------------
;do ll = 0,1
;plot1  =  new(16,graphic)
;dum1   =  new(16,graphic)
;plot2  =  new(16,graphic)
;dum2   =  new(16,graphic)
;
;wks1   =  gsn_open_wks("pdf","/data5/2019swh/paint/day/late_early_wind_diff_u"+level(ll))
;wks2   =  gsn_open_wks("pdf","/data5/2019swh/paint/day/late_early_wind_diff_v"+level(ll))
;gsn_define_colormap(wks1,"BlueDarkRed18")
;gsn_define_colormap(wks2,"BlueDarkRed18")
;
;res@gsnRightString          =      level(ll)
;    do day = 4,34,2
;        res@gsnLeftString   =      char_day(day)
;        plot1((day-4)/2)      =      gsn_csm_contour_map(wks1,diff_u(day,lev(ll),:,:),res)
;        plot2((day-4)/2)      =      gsn_csm_contour_map(wks2,diff_v(day,lev(ll),:,:),res)
;        dum1((day-4)/2)       =      gsn_add_polyline(wks1, plot1((day-4)/2), (/30,120/), (/0,0/), polyres)
;        dum2((day-4)/2)       =      gsn_add_polyline(wks2, plot2((day-4)/2), (/30,120/), (/0,0/), polyres)
;    end do
;
;pnlres = True
;pnlres@gsnPanelMainString     =      "diff_u between late and early at "+level(ll)
;pnlres@gsnPanelLabelBar  = True
;pnlres@gsnPanelDebug     = True     ; To get information from panel
;pnlres@pmLabelBarWidthF  = 0.55
;pnlres@lbLabelFontHeightF = 0.012
;gsn_panel(wks1,plot1,(/4,4/),pnlres)
;delete(wks1)
;pnlres@gsnPanelMainString     =      "diff_v between late and early at "+level(ll)
;gsn_panel(wks2,plot2,(/4,4/),pnlres)
;delete(wks2)
;end do
;-------------------------------------------------------------------------------------------------------------

;-----------------------------------------绘制平均------------------------------------------------------------
;do ll = 0,1
;
;wks1   =  gsn_open_wks("pdf","/data5/2019swh/paint/day/late_early_average_wind_diff_u"+level(ll))
;wks2   =  gsn_open_wks("pdf","/data5/2019swh/paint/day/late_early_average_wind_diff_v"+level(ll))
;gsn_define_colormap(wks1,"BlueDarkRed18")
;gsn_define_colormap(wks2,"BlueDarkRed18")
;
;res@gsnRightString          =      level(ll)
;res@tiMainString            =      "diff_u between late and early at "+level(ll)
;plot1                       =      gsn_csm_contour_map(wks1,diff_u_average(lev(ll),:,:),res)
;res@tiMainString            =      "diff_v between late and early at "+level(ll)
;plot2                       =      gsn_csm_contour_map(wks2,diff_v_average(lev(ll),:,:),res)
;dum1                        =      gsn_add_polyline(wks1, plot1, (/30,120/), (/0,0/), polyres)
;dum2                        =      gsn_add_polyline(wks2, plot2, (/30,120/), (/0,0/), polyres)
;
;draw(plot1)
;draw(plot2)
;frame(wks1)
;frame(wks2)
;
;end do
;------------------------------------------------------------------------------------------------------------

;---------------------------------------绘制纬向垂直剖面图-----------------------------------------------------
do ll = 0,1
    wks1   =  gsn_open_wks("pdf","/data5/2019swh/paint/day/early_late_v_diff_lat+"+lat(ll))
    gsn_define_colormap(wks1,"BlueDarkRed18")
    res@gsnRightString          =      lat(ll)
    plot1                       =      gsn_csm_pres_hgt(wks1,diff_v_average({1000:200},{lat(ll)},{30:120}),res)
    draw(plot1)
    frame(wks1)
end do

end