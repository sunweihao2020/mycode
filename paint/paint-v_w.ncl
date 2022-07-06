;2020/12/29
;对于合成分析资料绘制
;选取了三个经度范围77.5-80（412-416）80-82.5（416-420） 92.5-97.5（436-444）
begin
f = addfile("/data5/2019swh/data/composite3.nc","r")
v = f->vwind
w = f->OMEGA
w = w*(-60)
v1 = dim_avg_n(v(:,:,:,400:416), 3)
v1!0 = "time"
v1!1 = "level"
v1!2 = "lat"
v1&time = v&time
v1&level = v&level
v1&lat = v&lat
w1 = dim_avg_n(w(:,:,:,400:416), 3)
v2 = dim_avg_n(v(:,:,:,440:456), 3)
w2 = dim_avg_n(w(:,:,:,440:456), 3)
copy_VarCoords(v1, w1)
copy_VarCoords(v1, w2)
copy_VarCoords(v1, v2)


plot1 = new(15,graphic)
dum1 = new(15,graphic)
plot2 = new(15,graphic)
dum2 = new(15,graphic)

char_day=(/"D0-30","D0-29","D0-28","D0-27","D0-26","D0-25","D0-24","D0-23","D0-22","D0-21","D0-20","D0-19","D0-18","D0-17","D0-16","D0-15","D0-14","D0-13","D0-12","D0-11","D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10","D0+11","D0+12","D0+13","D0+14","D0+15"/)
wks1 = gsn_open_wks("pdf", "/data5/2019swh/paint/day/vertical3_wind1")
wks2 = gsn_open_wks("pdf", "/data5/2019swh/paint/day/vertical3_wind2")

do day = 4,33,2
    res = True
    res@gsnDraw     = False                                ; plot mods desired
    res@gsnFrame     =  False
    
    res@cnLineLabelsOn  = False                ; turn off line labels
    res@cnFillOn        = True                 ; turn on color fill
    res@cnFillPalette   = "CBR_coldhot"  ; choose color map
    res@cnLevelSelectionMode = "ExplicitLevels" 
    res@cnLevels             =  ispan(-6, 6, 1)
    res@gsnLeftString        = char_day(day)
    res@vcRefMagnitudeF = 5                ; define vector ref mag
    res@vcRefLengthF    = 0.045              ; define length of vec ref
    res@vcLineArrowThicknessF = 1
    res@vcGlyphStyle    = "FillArrow"      ; turn on curly vectors
    res@vcMinDistanceF  = 0.04               ; thin out vectors
    res@vcMapDirection  = False
    
    plot1((day-4)/2)  = gsn_csm_pres_hgt_vector(wks1,v1(day,0:12,{-30:60}),v1(day,0:25,{-30:60}),w1(day,0:25,{-30:60}),res )  
    plot2((day-4)/2)  = gsn_csm_pres_hgt_vector(wks2,v2(day,0:12,{-30:60}),v2(day,0:25,{-30:60}),w2(day,0:25,{-30:60}),res )  
    polyres                   = True
    polyres@gsLineColor       = "black"
    polyres@gsLineThicknessF  = 5
    polyres@gsLineDashPattern = 2
    dum1((day-4)/2) = gsn_add_polyline(wks1, plot1((day-4)/2), (/0,0/), (/1000,700/), polyres)
    dum2((day-4)/2) = gsn_add_polyline(wks2, plot2((day-4)/2), (/0,0/), (/1000,700/), polyres)

end do

pnlres = True
pnlres@gsnPanelMainString = "vertical v-w"
pnlres@gsnPanelLabelBar  = False
pnlres@gsnPanelDebug     = True     ; To get information from panel
pnlres@pmLabelBarWidthF  = 0.55
pnlres@lbLabelFontHeightF = 0.012
gsn_panel(wks1,plot1,(/3,5/),pnlres)
gsn_panel(wks2,plot2,(/3,5/),pnlres)

end
