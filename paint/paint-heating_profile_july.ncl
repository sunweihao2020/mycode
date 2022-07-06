;2021/2/13
;此代码绘制7月的平均加热廓线
;使用资料：JULY_tdt.nc
begin

char_day=(/"D0-30","D0-29","D0-28","D0-27","D0-26","D0-25","D0-24","D0-23","D0-22","D0-21","D0-20","D0-19","D0-18","D0-17","D0-16","D0-15","D0-14","D0-13","D0-12","D0-11","D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10","D0+11","D0+12","D0+13","D0+14","D0+15"/)

f = addfile("/data/JULY_tdt.nc","r")
tur = f->tur(0,:,{30},{-35})
rad  = f->rad(0,:,{30},{-35})


wks1 = gsn_open_wks("pdf","/picture/heating_profile_L2")
data1 = new((/2,dimsizes(tur&level)/),double)
data1(0,:) = rad
data1(1,:) = tur


res = True
res@trYReverse = True
res@gsnDraw               =False
res@gsnFrame              =False
res@trYReverse = True
res@trXMaxF = 10
res@trXMinF = -10
res@xyLineThicknessF = 1.8
res@xyDashPattern  = 0
res@xyMarkLineMode   = "MarkLines"
res@gsnStringFont = 2.0
res@xyMarkers   = (/4,6,7,11/)
res@xyMarkLineMode = "MarkLines"
res@xyLineColors := (/"blue","red"/)


polyres                   = True
polyres@gsLineColor       = "black"
polyres@gsLineThicknessF  = 1.5
polyres@gsLineDashPattern = 2


plot = gsn_csm_xy(wks1,data1(:,:),tur&level,res)
dum = gsn_add_polyline(wks1, plot, (/0,0/), (/0,1000/), polyres)
draw(plot)
frame(wks1)

;;  ;;===============================
;lgres                       = True   
;lgres@lgMonoLineThickness   = True
;lgres@lgLineThicknessF      = 2.0
;lgres@lgPerimOn             = False                 ; turn off perimeter
;lgres@lgLineLabelStrings    = (/"",""/)             ; no labels in lines
;lgres@lgAutoManage          = False
;lgres@lgLineDashSegLenF     = 0.08
;lgres@lgLabelFontHeightF    = 0.06   
;lgres@lgDashIndexes         = (/0,0/)              ; dash indexes
;lgres@vpHeightF             = 0.12                   ; height of legend (NDC)
;lgres@vpWidthF              = 0.145                  ; width of legend (NDC)
;;lgres@lgLineColors          = (/"red"/)
;lgres@lgLineColors          = (/"black"/)
;
;gsn_legend_ndc(wks1,1,(/" total"/),0.15,0.23,lgres)
;lgres@lgLineColors          = (/"azure4"/)
;gsn_legend_ndc(wks1,1,(/" radiation"/),0.35,0.23,lgres)
;lgres@lgLineColors          = (/"red"/)
;gsn_legend_ndc(wks1,1,(/"  sensible"/),0.55,0.23,lgres)
;lgres@lgLineColors          = (/"blue"/)
;gsn_legend_ndc(wks1,1,(/" moist"/),0.75,0.23,lgres)

end