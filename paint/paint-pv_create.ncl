;2021/1/27
;绘制季风爆发前后地表位涡制造的平面图
;分别热力、动力、以及总制造
;使用资料:/data5/2019swh/data/composite-era5pvcreate.nc
begin
f = addfile("/data5/2019swh/data/composite-era5pvcreate.nc", "r")
j = f->j_all
jd = f->j_dynamic
jt = f->j_thermal


char_day=(/"D0-30","D0-29","D0-28","D0-27","D0-26","D0-25","D0-24","D0-23","D0-22","D0-21","D0-20","D0-19","D0-18","D0-17","D0-16","D0-15","D0-14","D0-13","D0-12","D0-11","D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10","D0+11","D0+12","D0+13","D0+14","D0+15"/)

plot1 = new(15,graphic)
dum1   = new(15,graphic)
plot2 = new(15,graphic)
dum2   = new(15,graphic)
plot3 = new(15,graphic)
dum3   = new(15,graphic)
wks1   = gsn_open_wks("pdf","/data5/2019swh/paint/day/J_all")
wks2   = gsn_open_wks("pdf","/data5/2019swh/paint/day/J_dynamic")
wks3   = gsn_open_wks("pdf","/data5/2019swh/paint/day/J_thermal")

do day = 4,33,2
    res = True
    res@gsnDraw               = False
    res@gsnFrame              = False
    res@cnFillOn              = True     ; turn on color fill
    res@cnFillPalette         = "temp_19lev"
    res@cnLineLabelsOn        = False
    res@lbLabelBarOn          = False 
    res@mpMinLatF            = 0      ; range to zoom in on
    res@mpMaxLatF            =  30.
    res@mpMinLonF            =  30.
    res@mpMaxLonF            = 110.
    res@gsnRightString       = j@units
    res@cnLevelSelectionMode       = "ExplicitLevels" 
    res@cnLevels             := ispan(-5,5,1)
    res@gsnStringFont         = 2
    res@gsnAddCyclic         = False
    res@tmYLLabelFontHeightF      = 0.024
    res@tmXBLabelFontHeightF      = 0.024

    res@gsnLeftString         = char_day(day)
    ;res@tmYLLabelDeltaF = -0.6  ;坐标值跑出去了就调这个
    plot1((day-4)/2) = gsn_csm_contour_map(wks1,j(day,:,:), res)
    plot2((day-4)/2) = gsn_csm_contour_map(wks2,jd(day,:,:), res)
    res@cnLevels             := fspan(-0.05,0.05,11)
    plot3((day-4)/2) = gsn_csm_contour_map(wks3,jt(day,:,:), res)
    
    polyres                   = True
    polyres@gsLineColor       = "black"
    polyres@gsLineThicknessF  = 3
    polyres@gsLineDashPattern = 2
    dum1((day-4)/2) = gsn_add_polyline(wks1, plot1((day-4)/2), (/30,120/), (/0,0/), polyres)
    dum2((day-4)/2) = gsn_add_polyline(wks2, plot2((day-4)/2), (/30,120/), (/0,0/), polyres)
    dum3((day-4)/2) = gsn_add_polyline(wks3, plot3((day-4)/2), (/30,120/), (/0,0/), polyres)

end do

pnlres = True
pnlres@gsnPanelLabelBar  = True
pnlres@gsnPanelDebug     = True     ; To get information from panel
pnlres@pmLabelBarWidthF  = 0.55
pnlres@lbLabelFontHeightF = 0.012
pnlres@gsnPanelMainString = "J"
gsn_panel(wks1,plot1,(/5,3/),pnlres)
pnlres@gsnPanelMainString = "J due to dynamic"
gsn_panel(wks2,plot2,(/5,3/),pnlres)
pnlres@gsnPanelMainString = "J due to thermal"
gsn_panel(wks3,plot3,(/5,3/),pnlres)

end