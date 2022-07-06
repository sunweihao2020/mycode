;计算绝对涡度平流
;2021、3、12
begin
f = addfile("/data5/2019swh/data/composite-divvor.nc","r")

v = f->v_vor_gradient
u = f->u_vor_gradient
v = v*1E+5
u = u*1E+4
char_day=(/"D0-30","D0-29","D0-28","D0-27","D0-26","D0-25","D0-24","D0-23","D0-22","D0-21","D0-20","D0-19","D0-18","D0-17","D0-16","D0-15","D0-14","D0-13","D0-12","D0-11","D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10","D0+11","D0+12","D0+13","D0+14","D0+15"/)
plot = new(12,graphic)
dum  = new(12,graphic)
vm = v(:,12,:,:)
wks = gsn_open_wks("pdf","/data5/2019swh/paint/day/wind_vor_gradientu")
;gsn_define_colormap(wks,"BlueDarkRed18")

do day = 18,29
    res = True
    res@gsnDraw               = False
    res@gsnFrame              = False
    res@cnFillOn              = True     ; turn on color fill
    res@cnLineLabelsOn        = False
    res@lbLabelsOn            = False
    res@lbLabelBarOn          = False
    
    res@cnLevelSelectionMode       = "ExplicitLevels" 
    res@cnLevels             = fspan(-5,5,11)
    res@cnFillPalette = "BlueDarkRed18"
    ;res@cnFillColors         = (/2,15,30,50,60,90,100,144,173,190,200,220/)
    ;res@cnLevelSpacingF = 1
    res@mpMinLatF            = 0      ; range to zoom in on
    res@mpMaxLatF            =  30.
    res@mpMinLonF            =  60.
    res@mpMaxLonF            = 100.
    
    res@gsnRightString        = " "
    res@gsnLeftString         = char_day(day)
    res@gsnStringFont         = 2
    res@tmYLLabelFontHeightF      = 0.024
    res@tmXBLabelFontHeightF      = 0.024
    ;res@tmYLLabelDeltaF = -0.6  ;坐标值跑出去了就调这个

    res@cnInfoLabelOn         = False
    plot(day-18) = gsn_csm_contour_map(wks,vm(day,:,:), res)  
  
    polyres                   = True
    polyres@gsLineColor       = "black"
    polyres@gsLineThicknessF  = 3
    polyres@gsLineDashPattern = 2
    dum(day-18) = gsn_add_polyline(wks, plot(day-18), (/30,120/), (/0,0/), polyres)
    
end do

pnlres = True
pnlres@gsnPanelMainString = "v * vorticity gradient"
pnlres@gsnPanelLabelBar  = True
pnlres@gsnPanelDebug     = True     ; To get information from panel
pnlres@pmLabelBarWidthF  = 0.55
pnlres@lbLabelFontHeightF = 0.012
gsn_panel(wks,plot,(/3,4/),pnlres)
;frame(wks)

end