;2021/2/5
;绘制两个经向垂直剖面的位势高度场
;使用资料:/data/composite3
;纬向平均： 70-80  95-105
begin
f = addfile("/data/composite3.nc","r")
h = f->H
h1 = dim_avg_n(h(:,:,:,{70:80}), 3)
h2 = dim_avg_n(h(:,:,:,{95:105}), 3)
h1!0 = "time"
h1!1 = "level"
h1!2 = "lat"
h1&time = h&time
h1&level  =  h&level
h1&lat = h&lat
copy_VarCoords(h1, h2)

plot1  = new(15,graphic)
dum1   = new(15,graphic)
plot2  = new(15,graphic)
dum2   = new(15,graphic)
wks1 = gsn_open_wks("pdf","/picture/paint/day/H_1")
wks2 = gsn_open_wks("pdf","/picture/paint/day/H_2")

char_day=(/"D0-30","D0-29","D0-28","D0-27","D0-26","D0-25","D0-24","D0-23","D0-22","D0-21","D0-20","D0-19","D0-18","D0-17","D0-16","D0-15","D0-14","D0-13","D0-12","D0-11","D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10","D0+11","D0+12","D0+13","D0+14","D0+15"/)


res = True
res@cnFillOn              = False 
res@cnLinesOn             = True  
res@gsnDraw               = False
res@gsnFrame              = False
;res@cnLevelSelectionMode  =  "ExplicitLevels"
;res@cnLevelSpacingF       = 1
res@cnSmoothingOn         = True
res@cnSmoothingDistanceF  = 0.006
res@cnInfoLabelOn         = False
res@cnLineThicknessF      = 2
res@cnLineLabelsOn        = True
res@cnMissingValPerimOn     = True            ; turn on the missing value perim
res@cnMissingValPerimColor  = "black"           ; outline the perimeter red
res@cnMissingValFillPattern = 0               ; choose fill pattern 0 (solid fi
res@cnMissingValFillColor   = "gray"          ; color fill missing areas blue
res@gsnRightString        = ""



do day = 16,30
res@gsnLeftString       = char_day(day-16)
res@gsnRightString      = "70E-80E"
plot1(day-16) = gsn_csm_pres_hgt(wks1,h1(day,0:22,{-10:35}),res)
res@gsnRightString      = "95E-105E"
plot2(day-16) = gsn_csm_pres_hgt(wks2,h2(day,0:22,{-10:35}),res)

polyres                   = True
polyres@gsLineColor       = "black"
polyres@gsLineThicknessF  = 2
polyres@gsLineDashPattern = 2
dum1(day-16) = gsn_add_polyline(wks1, plot1(day-16), (/0,0/), (/1000,100/), polyres)
dum2(day-16) = gsn_add_polyline(wks2, plot2(day-16), (/0,0/), (/1000,100/), polyres)
end do
pnlres = True
pnlres@gsnPanelMainString = "geopotential height"
pnlres@gsnPanelLabelBar  = True
pnlres@gsnPanelDebug     = True     ; To get information from panel
pnlres@pmLabelBarWidthF  = 0.55
pnlres@lbLabelFontHeightF = 0.012
gsn_panel(wks1,plot1,(/5,3/),pnlres)
gsn_panel(wks2,plot2,(/5,3/),pnlres)

end




