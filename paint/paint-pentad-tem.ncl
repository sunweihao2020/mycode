;2021/1/18
;使用资料：merra2_singlelayer_0924.nc
;绘制变量：地表2m温度
begin

f = addfile("/data5/2019swh/data/merra2_singlelayer_0924.nc","r")
f2 = addfile("/data5/2019swh/data/land_ocean_merra.nc","r")
lsm = f2->FRLAND(0,:,:)
t = f->T2M
char_pen=(/"p22","p23","p24","p25","p26","p27","p28","p29","p30","p31","p32","p33","p34"/)

plot1 = new(4,graphic)
plot2 = new(4,graphic)
wks = gsn_open_wks("pdf","/data5/2019swh/paint/pentad/2m_temperature")
do ipen = 0,3
    land = t(ipen,:,:)
    land = mask(t(ipen,:,:),(lsm .gt. 0.1),1)
    res = True
    res@gsnDraw      =  False                   ; do not draw the plot
    res@gsnFrame     =  False
    res@cnLinesOn    = False
    res@mpMinLatF            = -10
    res@mpMaxLatF            = 30
    res@mpMinLonF            = 30
    res@mpMaxLonF            = 120
    res@gsnLeftString         = char_pen(ipen)
    res@cnLineLabelsOn        = False
    res@cnFillOn              = True     ; turn on color fill
    res@cnLevelSelectionMode       = "ExplicitLevels" 
    res@cnLevels             = ispan(270,310,4)
    res@lbLabelBarOn         = False
    res@gsnStringFont         = 2
    res@tmYLLabelFontHeightF      = 0.024
    res@tmXBLabelFontHeightF      = 0.024
    res@gsnRightString        = "K"
    res@cnInfoLabelOn              = False
    res@cnMissingValPerimOn     = True            ; turn on the missing value perimeter
    res@cnMissingValPerimColor  = "black"           ; outline the perimeter red
    res@cnMissingValFillPattern = 0               ; choose fill pattern 0 (solid fill) 
    res@cnMissingValFillColor   = "white"          ; color fill missing areas blue
    plot1(ipen) = gsn_csm_contour_map(wks,land,res)
    
    polyres                   = True
    polyres@gsLineColor       = "black"
    polyres@gsLineThicknessF  = 3
    polyres@gsLineDashPattern = 2
    plot2(ipen) = gsn_add_polyline(wks, plot1(ipen), (/30,120/), (/0,0/), polyres)
end do
pnlres = True
pnlres@gsnPanelMainString = "2m temperature"
pnlres@gsnPanelLabelBar  = True
pnlres@gsnPanelDebug     = True     ; To get information from panel
pnlres@pmLabelBarWidthF  = 0.55
pnlres@lbLabelFontHeightF = 0.012
gsn_panel(wks,plot1,(/2,2/),pnlres)
end


