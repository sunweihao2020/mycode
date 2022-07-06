;2021/2/1
;此代码绘制北纬10度的80E和100E两点的垂直加热廓线
;使用资料：heating_vertical_profile.nc
;begin
;
;char_day=(/"D0-30","D0-29","D0-28","D0-27","D0-26","D0-25","D0-24","D0-23","D0-22","D0-21","D0-20","D0-19","D0-18","D0-17","D0-16","D0-15","D0-14","D0-13","D0-12","D0-11","D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10","D0+11","D0+12","D0+13","D0+14","D0+15"/)
;
;f = addfile("/data5/2019swh/data/heating_vertical_profile.nc","r")
;;total1 = f->total1
;;total2 = f->total2
;turbulence1 = f->turbulence1
;turbulence2 = f->turbulence2
;radiation1  = f->radiation1
;radiation2  = f->radiation2
;moist1 = f->moist1
;moist2 = f->moist2
;physics1 = f->physics1
;physics2 = f->physics2
;;dynamic1 = f->dynamic1
;;dynamic2 = f->dynamic2
;
;ra_tu_mo1 = turbulence1 + radiation1 + moist1
;ra_tu_mo2 = turbulence2 + radiation2 + moist2
;ra_tu_mo1!0 = "time"
;ra_tu_mo1!1 = "level"
;ra_tu_mo1&time =  physics1&time
;ra_tu_mo1&level = physics1&level
;copy_VarCoords(ra_tu_mo1, ra_tu_mo2)
;;
;data1 = new((/4,61,dimsizes(physics1&level)/),double)
;data2 = new((/4,61,dimsizes(physics1&level)/),double)
;data1(0,:,:) = physics1
;data1(1,:,:) = radiation1
;data1(2,:,:) = turbulence1
;data1(3,:,:) = moist1
;;data1(4,:,:) = ra_tu_mo1
;data2(0,:,:) = physics2
;data2(1,:,:) = radiation2
;data2(2,:,:) = turbulence2
;data2(3,:,:) = moist2
;;data2(4,:,:) = ra_tu_mo2
;
;
;
;
;
;plot1 = new(12,graphic)
;dum1  = new(12,graphic)
;wks1 = gsn_open_wks("pdf","/data5/2019swh/paint/day/heating_profile80")
;
;plot2 = new(12,graphic)
;dum2  = new(12,graphic)
;wks2 = gsn_open_wks("pdf","/data5/2019swh/paint/day/heating_profile100")
;
;res = True
;res@trYReverse = True
;res@gsnDraw               = False
;res@gsnFrame              = False
;
;;res@pmLegendDisplayMode = "Always"
;;res@pmLegendSide = "Top"
;;res@pmLegendParallelPosF   = .80                   ; move units right
;;res@pmLegendOrthogonalPosF = -0.3                  ; more neg = down
;;res@pmLegendWidthF         = 0.12                  ; Change width and
;;res@pmLegendHeightF        = 0.25                  ; height of legend.
;;res@lgLabelFontHeightF     = .02                   ; change font height
;res@lgPerimOn              = False                 ; no box around
;res@trXMaxF = 4
;res@trXMinF = -4
;res@xyLineThicknessF = 1.8
;res@xyDashPattern  = 0
;res@xyMarkLineMode   = "MarkLines"
;res@gsnStringFont = 2.0
;;res@xyMarkers   = (/4,6,7,11,13,16/)
;res@xyMarkers   = (/4,6,7,11/)
;res@xyMarkLineMode = "MarkLines"
;res@xyLineColors := (/"black","azure4","red","blue"/)
;
;;res@xyExplicitLegendLabels = (/"total","radiation","turbulence","moist","dynamic","rad+tur+moi"/)
;
;;gsn_polyline(wks,plot,(/0,0/),(/0,1000/),False)
;res@gsnRightString = "(10N,80E)"
;
;polyres                   = True
;polyres@gsLineColor       = "black"
;polyres@gsLineThicknessF  = 1.5
;polyres@gsLineDashPattern = 2
;
;do day = 10,33,2
;res@gsnLeftString = char_day(day)
;plot1((day-10)/2) = gsn_csm_xy(wks1,data1(:,day,:),physics1&level,res)
;dum1((day-10)/2)  = gsn_add_polyline(wks1, plot1((day-10)/2), (/0,0/), (/0,1000/), polyres)
;plot2((day-10)/2) = gsn_csm_xy(wks2,data2(:,day,:),physics1&level,res)
;dum2((day-10)/2)  = gsn_add_polyline(wks2, plot2((day-10)/2), (/0,0/), (/0,1000/), polyres)
;end do
;
;;;  ;;===============================
;  lgres                       = True   
;  lgres@lgMonoLineThickness   = True
;  lgres@lgLineThicknessF      = 2.0
;  lgres@lgPerimOn             = False                 ; turn off perimeter
;  lgres@lgLineLabelStrings    = (/"",""/)             ; no labels in lines
;  lgres@lgAutoManage          = False
;  lgres@lgLineDashSegLenF     = 0.08
;  lgres@lgLabelFontHeightF    = 0.06   
;  lgres@lgDashIndexes         = (/0,0/)              ; dash indexes
;  lgres@vpHeightF             = 0.12                   ; height of legend (NDC)
;  lgres@vpWidthF              = 0.145                  ; width of legend (NDC)
;  ;lgres@lgLineColors          = (/"red"/)
;
;lgres@lgLineColors          = (/"black"/)
;
;gsn_legend_ndc(wks1,1,(/" total"/),0.15,0.23,lgres)
;gsn_legend_ndc(wks2,2,(/" total"/),0.15,0.23,lgres)
;lgres@lgLineColors          = (/"azure4"/)
;gsn_legend_ndc(wks1,1,(/" radiation"/),0.35,0.23,lgres)
;gsn_legend_ndc(wks1,2,(/" radiation"/),0.35,0.23,lgres)
;lgres@lgLineColors          = (/"red"/)
;gsn_legend_ndc(wks1,1,(/"  sensible"/),0.55,0.23,lgres)
;gsn_legend_ndc(wks1,2,(/"  sensible"/),0.55,0.23,lgres)
;lgres@lgLineColors          = (/"blue"/)
;gsn_legend_ndc(wks1,1,(/" moist"/),0.75,0.23,lgres)
;gsn_legend_ndc(wks1,2,(/" moist"/),0.75,0.23,lgres)
;
;
;
;
;pnlres = True
;pnlres@lgPerimOn             = False
;pnlres@lgAutoManage          = False
;pnlres@lgLineLabelStrings    = (/"",""/)
;pnlres@gsnPanelDebug     = True     ; To get information from panel
;pnlres@gsnPanelMainString = "(10N,80E) vertical heating profile"
;gsn_panel(wks1,plot1,(/5,3/),pnlres)
;pnlres@gsnPanelMainString = "(10N,100E) vertical heating profile"
;gsn_panel(wks2,plot2,(/5,3/),pnlres)
;end


;====================================分割线==========================
;2021/4/12
;此代码绘制北纬15度的80E和100E两点的垂直加热廓线
;使用资料：heating_vertical_profile.nc
;begin
;
;char_day=(/"D0-30","D0-29","D0-28","D0-27","D0-26","D0-25","D0-24","D0-23","D0-22","D0-21","D0-20","D0-19","D0-18","D0-17","D0-16","D0-15","D0-14","D0-13","D0-12","D0-11","D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10","D0+11","D0+12","D0+13","D0+14","D0+15"/)
;
;f = addfile("/data5/2019swh/data/heating_vertical_profile.nc","r")
;;total1 = f->total1
;;total2 = f->total2
;turbulence1 = f->turbulence1
;turbulence2 = f->turbulence2
;radiation1  = f->radiation1
;radiation2  = f->radiation2
;moist1 = f->moist1
;moist2 = f->moist2
;physics1 = f->physics1
;physics2 = f->physics2
;;dynamic1 = f->dynamic1
;;dynamic2 = f->dynamic2
;
;ra_tu_mo1 = turbulence1 + radiation1 + moist1
;ra_tu_mo2 = turbulence2 + radiation2 + moist2
;ra_tu_mo1!0 = "time"
;ra_tu_mo1!1 = "level"
;ra_tu_mo1&time =  physics1&time
;ra_tu_mo1&level = physics1&level
;copy_VarCoords(ra_tu_mo1, ra_tu_mo2)
;;
;data1 = new((/4,61,dimsizes(physics1&level)/),double)
;data2 = new((/4,61,dimsizes(physics1&level)/),double)
;data1(0,:,:) = physics1
;data1(1,:,:) = radiation1
;data1(2,:,:) = turbulence1
;data1(3,:,:) = moist1
;;data1(4,:,:) = ra_tu_mo1
;data2(0,:,:) = physics2
;data2(1,:,:) = radiation2
;data2(2,:,:) = turbulence2
;data2(3,:,:) = moist2
;;data2(4,:,:) = ra_tu_mo2
;
;
;
;
;
;plot1 = new(12,graphic)
;dum1  = new(12,graphic)
;wks1 = gsn_open_wks("pdf","/data5/2019swh/paint/day/heating_profile80")
;
;plot2 = new(12,graphic)
;dum2  = new(12,graphic)
;wks2 = gsn_open_wks("pdf","/data5/2019swh/paint/day/heating_profile100")
;
;res = True
;res@trYReverse = True
;res@gsnDraw               = False
;res@gsnFrame              = False
;
;;res@pmLegendDisplayMode = "Always"
;;res@pmLegendSide = "Top"
;;res@pmLegendParallelPosF   = .80                   ; move units right
;;res@pmLegendOrthogonalPosF = -0.3                  ; more neg = down
;;res@pmLegendWidthF         = 0.12                  ; Change width and
;;res@pmLegendHeightF        = 0.25                  ; height of legend.
;;res@lgLabelFontHeightF     = .02                   ; change font height
;res@lgPerimOn              = False                 ; no box around
;res@trXMaxF = 4
;res@trXMinF = -4
;res@xyLineThicknessF = 1.8
;res@xyDashPattern  = 0
;res@xyMarkLineMode   = "MarkLines"
;res@gsnStringFont = 2.0
;;res@xyMarkers   = (/4,6,7,11,13,16/)
;res@xyMarkers   = (/4,6,7,11/)
;res@xyMarkLineMode = "MarkLines"
;res@xyLineColors := (/"black","azure4","red","blue"/)
;
;;res@xyExplicitLegendLabels = (/"total","radiation","turbulence","moist","dynamic","rad+tur+moi"/)
;
;;gsn_polyline(wks,plot,(/0,0/),(/0,1000/),False)
;res@gsnRightString = "(10N,80E)"
;
;polyres                   = True
;polyres@gsLineColor       = "black"
;polyres@gsLineThicknessF  = 1.5
;polyres@gsLineDashPattern = 2
;
;do day = 10,33,2
;res@gsnLeftString = char_day(day)
;plot1((day-10)/2) = gsn_csm_xy(wks1,data1(:,day,:),physics1&level,res)
;dum1((day-10)/2)  = gsn_add_polyline(wks1, plot1((day-10)/2), (/0,0/), (/0,1000/), polyres)
;plot2((day-10)/2) = gsn_csm_xy(wks2,data2(:,day,:),physics1&level,res)
;dum2((day-10)/2)  = gsn_add_polyline(wks2, plot2((day-10)/2), (/0,0/), (/0,1000/), polyres)
;end do
;
;;;  ;;===============================
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
;
;lgres@lgLineColors          = (/"black"/)
;
;gsn_legend_ndc(wks1,1,(/" total"/),0.15,0.23,lgres)
;gsn_legend_ndc(wks2,2,(/" total"/),0.15,0.23,lgres)
;lgres@lgLineColors          = (/"azure4"/)
;gsn_legend_ndc(wks1,1,(/" radiation"/),0.35,0.23,lgres)
;gsn_legend_ndc(wks1,2,(/" radiation"/),0.35,0.23,lgres)
;lgres@lgLineColors          = (/"red"/)
;gsn_legend_ndc(wks1,1,(/"  sensible"/),0.55,0.23,lgres)
;gsn_legend_ndc(wks1,2,(/"  sensible"/),0.55,0.23,lgres)
;lgres@lgLineColors          = (/"blue"/)
;gsn_legend_ndc(wks1,1,(/" moist"/),0.75,0.23,lgres)
;gsn_legend_ndc(wks1,2,(/" moist"/),0.75,0.23,lgres)
;
;
;
;
;pnlres = True
;pnlres@lgPerimOn             = False
;pnlres@lgAutoManage          = False
;pnlres@lgLineLabelStrings    = (/"",""/)
;pnlres@gsnPanelDebug     = True     ; To get information from panel
;pnlres@gsnPanelMainString = "(10N,80E) vertical heating profile"
;gsn_panel(wks1,plot1,(/5,3/),pnlres)
;pnlres@gsnPanelMainString = "(10N,100E) vertical heating profile"
;gsn_panel(wks2,plot2,(/5,3/),pnlres)
;end


;====================================分割线==========================
;2021/4/12
;此代码绘制北纬15度的80E和100E两点的垂直加热廓线
;使用资料：heating_vertical_profile.nc
begin

char_day=(/"D0-30","D0-29","D0-28","D0-27","D0-26","D0-25","D0-24","D0-23","D0-22","D0-21","D0-20","D0-19","D0-18","D0-17","D0-16","D0-15","D0-14","D0-13","D0-12","D0-11","D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10","D0+11","D0+12","D0+13","D0+14","D0+15"/)
pens = (/"P0-6","P0-5","P0-4","P0-3","P0-2","P0-1"/)

f = addfile("/data5/2019swh/data/heating_vertical_profile.nc","r")
;total1 = f->total1
;total2 = f->total2
turbulence1 = f->turbulence1
turbulence2 = f->turbulence2
radiation1  = f->radiation1
radiation2  = f->radiation2
moist1 = f->moist1
moist2 = f->moist2
physics1 = f->physics1
physics2 = f->physics2
;dynamic1 = f->dynamic1
;dynamic2 = f->dynamic2

ra_tu_mo1 = turbulence1 + radiation1 + moist1
ra_tu_mo2 = turbulence2 + radiation2 + moist2
ra_tu_mo1!0 = "time"
ra_tu_mo1!1 = "level"
ra_tu_mo1&time =  physics1&time
ra_tu_mo1&level = physics1&level
copy_VarCoords(ra_tu_mo1, ra_tu_mo2)
;
data1 = new((/4,61,dimsizes(physics1&level)/),double)
data2 = new((/4,61,dimsizes(physics1&level)/),double)
data1(0,:,:) = physics1
data1(1,:,:) = radiation1
data1(2,:,:) = turbulence1
data1(3,:,:) = moist1
;data1(4,:,:) = ra_tu_mo1
data2(0,:,:) = physics2
data2(1,:,:) = radiation2
data2(2,:,:) = turbulence2
data2(3,:,:) = moist2
;data2(4,:,:) = ra_tu_mo2





plot1 = new(6,graphic)
dum1  = new(6,graphic)
wks1 = gsn_open_wks("pdf","/data5/2019swh/paint/day/heating_profile80_10N")

plot2 = new(6,graphic)
dum2  = new(6,graphic)
wks2 = gsn_open_wks("pdf","/data5/2019swh/paint/day/heating_profile100_10N")

res = True
res@trYReverse = True
res@gsnDraw               = False
res@gsnFrame              = False

;res@pmLegendDisplayMode = "Always"
;res@pmLegendSide = "Top"
;res@pmLegendParallelPosF   = .80                   ; move units right
;res@pmLegendOrthogonalPosF = -0.3                  ; more neg = down
;res@pmLegendWidthF         = 0.12                  ; Change width and
;res@pmLegendHeightF        = 0.25                  ; height of legend.
;res@lgLabelFontHeightF     = .02                   ; change font height
res@lgPerimOn              = False                 ; no box around
res@trXMaxF = 6
res@trXMinF = -4
res@xyLineThicknessF = 1.8
res@xyDashPattern  = 0
res@xyMarkLineMode   = "MarkLines"
res@gsnStringFont = 2.0
;res@xyMarkers   = (/4,6,7,11,13,16/)
res@xyMarkers   = (/4,6,7,11/)
res@xyMarkLineMode = "MarkLines"
res@xyLineColors := (/"black","azure4","red","blue"/)

;res@xyExplicitLegendLabels = (/"total","radiation","turbulence","moist","dynamic","rad+tur+moi"/)

;gsn_polyline(wks,plot,(/0,0/),(/0,1000/),False)
res@gsnRightString = "(10N,80E)"

polyres                   = True
polyres@gsLineColor       = "black"
polyres@gsLineThicknessF  = 1.5
polyres@gsLineDashPattern = 2

do day = 0,5
res@gsnLeftString = pens(day)
plot1(day) = gsn_csm_xy(wks1,dim_avg_n_Wrap(data1(:,day*5:(day*5+5),:),1),physics1&level,res)
dum1(day)  = gsn_add_polyline(wks1, plot1(day), (/0,0/), (/0,1000/), polyres)
plot2(day) = gsn_csm_xy(wks2,dim_avg_n_Wrap(data2(:,day*5:(day*5+5),:),1),physics1&level,res)
dum2(day)  = gsn_add_polyline(wks2, plot2(day), (/0,0/), (/0,1000/), polyres)
end do

;;  ;;===============================
lgres                       = True   
lgres@lgMonoLineThickness   = True
lgres@lgLineThicknessF      = 2.0
lgres@lgPerimOn             = False                 ; turn off perimeter
lgres@lgLineLabelStrings    = (/"",""/)             ; no labels in lines
lgres@lgAutoManage          = False
lgres@lgLineDashSegLenF     = 0.08
lgres@lgLabelFontHeightF    = 0.06   
lgres@lgDashIndexes         = (/0,0/)              ; dash indexes
lgres@vpHeightF             = 0.12                   ; height of legend (NDC)
lgres@vpWidthF              = 0.145                  ; width of legend (NDC)
;lgres@lgLineColors          = (/"red"/)

lgres@lgLineColors          = (/"black"/)

gsn_legend_ndc(wks1,1,(/" total"/),0.15,0.15,lgres)
gsn_legend_ndc(wks2,1,(/" total"/),0.15,0.15,lgres)
lgres@lgLineColors          = (/"azure4"/)
gsn_legend_ndc(wks1,1,(/" radiation"/),0.35,0.15,lgres)
gsn_legend_ndc(wks2,1,(/" radiation"/),0.35,0.15,lgres)
lgres@lgLineColors          = (/"red"/)
gsn_legend_ndc(wks1,1,(/"  sensible"/),0.55,0.15,lgres)
gsn_legend_ndc(wks2,1,(/"  sensible"/),0.55,0.15,lgres)
lgres@lgLineColors          = (/"blue"/)
gsn_legend_ndc(wks1,1,(/" moist"/),0.75,0.15,lgres)
gsn_legend_ndc(wks2,1,(/" moist"/),0.75,0.15,lgres)




pnlres = True
pnlres@lgPerimOn             = False
pnlres@lgAutoManage          = False
pnlres@lgLineLabelStrings    = (/"",""/)
pnlres@gsnPanelDebug     = True     ; To get information from panel
pnlres@gsnPanelMainString = "(10N,80E) vertical heating profile"
gsn_panel(wks1,plot1,(/2,3/),pnlres)
pnlres@gsnPanelMainString = "(10N,100E) vertical heating profile"
gsn_panel(wks2,plot2,(/2,3/),pnlres)
end