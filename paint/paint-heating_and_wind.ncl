;2021/3/10
;本代码绘制赤道地区的加热以及纬向垂直剖面流场
;所用资料：jra55的加热资料、风场资料
begin
f1 = addfile("/data/composite3.nc","r")
;f2 = addfile("/data/composite-heating-jra55.nc","r")
f2 = addfile("/data/heating/composite_Q2.nc","r")
char_day=(/"D0-30","D0-29","D0-28","D0-27","D0-26","D0-25","D0-24","D0-23","D0-22","D0-21","D0-20","D0-19","D0-18","D0-17","D0-16","D0-15","D0-14","D0-13","D0-12","D0-11","D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10","D0+11","D0+12","D0+13","D0+14","D0+15"/)


u = f1->uwind
v = f1->vwind
w = f1->OMEGA
w = w*(-60)
u1 = dim_avg_n_Wrap(u(:,:,{-5:5},:),2)
w1 = dim_avg_n_Wrap(w(:,:,{-5:5},:),2)

;q1 = f2->convective
;q2 = f2->radiation
;q3 = f2->diffusion

q = f2->Q2
qm = dim_avg_n_Wrap(q(:,::-1,68:76,:),2)

;绘图
plot = new(15,graphic)

wks = gsn_open_wks("pdf","/picture/paint/day/q2_heating_and_wind")
do day = 15,29
res                 = True                     ; plot mods desired
res@gsnDraw               = False
res@gsnFrame              = False

res@cnLineLabelsOn  = False                ; turn off line labels
res@cnFillOn        = True                 ; turn on color fill
res@cnFillPalette   = "BlueDarkRed18"  ; choose color map
res@lbLabelStride   = 2                    ; every other color
res@vcRefMagnitudeF = 3.0                ; define vector ref mag
res@vcRefLengthF    = 0.045              ; define length of vec ref
res@vcGlyphStyle    = "CurlyVector"      ; turn on curly vectors
res@vcMinDistanceF  = 0.01               ; thin out vectors
res@vcMapDirection  = False
res@gsnRightString        = " "
res@gsnLeftString         = char_day(day)
res@gsnStringFont         = 2
res@tmYLLabelFontHeightF      = 0.024
res@tmXBLabelFontHeightF      = 0.024
res@cnInfoLabelOn         = False

plot(day-15)  = gsn_csm_pres_hgt_vector(wks,qm(day,{1000:200},{30:120}),v(day,{1000:200},{30:120}),w(day,{1000:200},{30:120}),res ) 
end do

pnlres = True
pnlres@gsnPanelMainString = "Q"
pnlres@gsnPanelLabelBar  = True
pnlres@gsnPanelDebug     = True     ; To get information from panel
pnlres@pmLabelBarWidthF  = 0.55
pnlres@lbLabelFontHeightF = 0.012
gsn_panel(wks,plot,(/5,3/),pnlres)

end