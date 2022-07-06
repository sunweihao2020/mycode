;2021/3/1
;此代码绘制北纬10度的80E和100E两点的垂直加热廓线(JRA55)
;使用资料：composite-heating-jra55.nc
;位置64-80E 80-100E   64-10N
begin
char_day=(/"D0-30","D0-29","D0-28","D0-27","D0-26","D0-25","D0-24","D0-23","D0-22","D0-21","D0-20","D0-19","D0-18","D0-17","D0-16","D0-15","D0-14","D0-13","D0-12","D0-11","D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10","D0+11","D0+12","D0+13","D0+14","D0+15"/)

f = addfile("/data/composite-heating-jra55.nc","r")
adiabatic = f->adiabatic
convective = f->convective
condensation = f->condensation
radiation = f->radiation
diffusion = f->diffusion

ra_tu_mo = diffusion + radiation + convective

ra_tu_mo!0 = "time"
ra_tu_mo!1 = "level"
ra_tu_mo!2 = "lat"
ra_tu_mo!3 = "lon"
ra_tu_mo&time =  adiabatic&time
ra_tu_mo&level = adiabatic&level
ra_tu_mo&lat = adiabatic&lat
ra_tu_mo&lon = adiabatic&lon

;
data1 = new((/4,35,37,145,288/),double)
data1(0,:,:,:,:) = convective
data1(1,:,:,:,:) = ra_tu_mo
data1(2,:,:,:,:) = radiation
data1(3,:,:,:,:) = diffusion






plot1 = new(12,graphic)
dum1  = new(12,graphic)
wks1 = gsn_open_wks("pdf","/picture/paint/day/jra55_heating_profile80")

plot2 = new(12,graphic)
dum2  = new(12,graphic)
wks2 = gsn_open_wks("pdf","/picture/paint/day/jra55_heating_profile100")

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
res@trXMaxF = 8
res@trXMinF = -8
res@xyLineThicknessF = 1.8
res@xyDashPattern  = 0
res@xyMarkLineMode   = "MarkLines"
res@gsnStringFont = 2.0

res@xyMarkers   = (/6,7,11,13/)
res@xyMarkLineMode = "MarkLines"
res@xyLineColors := (/"blue","black","azure4","red"/)

;res@xyExplicitLegendLabels = (/"total","radiation","turbulence","moist","dynamic","rad+tur+moi"/)

;gsn_polyline(wks,plot,(/0,0/),(/0,1000/),False)
res@gsnRightString := "(10N,80E)"

polyres                   = True
polyres@gsLineColor       = "black"
polyres@gsLineThicknessF  = 1.5
polyres@gsLineDashPattern = 2

do day = 20,31,1
res@gsnLeftString = char_day(day)
plot1(day-20) = gsn_csm_xy(wks1,data1(:,day-20,:,64,64),adiabatic&level,res)
dum1(day-20)  = gsn_add_polyline(wks1, plot1(day-20), (/0,0/), (/0,1000/), polyres)

res@gsnRightString := "(10N,100E)"
plot2(day-20) = gsn_csm_xy(wks2,data1(:,day-20,:,64,80),adiabatic&level,res)
dum2(day-20)  = gsn_add_polyline(wks2, plot2(day-20), (/0,0/), (/0,1000/), polyres)
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

lgres@lgLineColors          = (/"blue"/)
gsn_legend_ndc(wks1,1,(/" convective"/),0.05,0.12,lgres)
gsn_legend_ndc(wks2,1,(/" convective"/),0.05,0.12,lgres)
lgres@lgLineColors          = (/"black"/)
gsn_legend_ndc(wks1,1,(/"  rad+diff+conve"/),0.25,0.12,lgres)
gsn_legend_ndc(wks2,1,(/"  rad+diff+conve"/),0.25,0.12,lgres)
lgres@lgLineColors          = (/"azure4"/)
gsn_legend_ndc(wks1,1,(/" radiation"/),0.45,0.12,lgres)
gsn_legend_ndc(wks2,1,(/" radiation"/),0.45,0.12,lgres)
lgres@lgLineColors          = (/"red"/)
gsn_legend_ndc(wks1,1,(/" vertical_diffusion"/),0.65,0.12,lgres)
gsn_legend_ndc(wks2,1,(/" vertical_diffusion"/),0.65,0.12,lgres)




pnlres = True
pnlres@lgPerimOn             = False
pnlres@lgAutoManage          = False
pnlres@lgLineLabelStrings    = (/"",""/)
pnlres@gsnPanelDebug     = True     ; To get information from panel
pnlres@gsnPanelMainString = "(10N,80E) vertical heating profile"
gsn_panel(wks1,plot1,(/3,4/),pnlres)
pnlres@gsnPanelMainString = "(10N,100E) vertical heating profile"
gsn_panel(wks2,plot2,(/3,4/),pnlres)
end

;2021/3/8
;使用资料：composite-heating-pentadjra55.nc
;三个点位置(75,80,100)
;begin
;f = addfile("/data/composite-pentad-jra55heating.nc","r")
;char_pen=(/"P0-6","P0-5","P0-4","P0-3","P0-2","P0-1"/)
;convective = f->convective
;total = f->total
;radiation = f->radiation
;diffusion = f->diffusion
;
;data1 = new((/4,6,37,145,288/),double)
;data1(0,:,:,:,:) = convective
;data1(2,:,:,:,:) = radiation
;data1(3,:,:,:,:) = diffusion
;data1(1,:,:,:,:) = total
;
;plot1 = new(6,graphic)
;dum1  = new(6,graphic)
;wks1 = gsn_open_wks("pdf","/picture/paint/day/jra55_heating_profile75")
;
;plot2 = new(6,graphic)
;dum2  = new(6,graphic)
;wks2 = gsn_open_wks("pdf","/picture/paint/day/jra55_heating_profile85")
;
;plot3 = new(6,graphic)
;dum3  = new(6,graphic)
;wks3 = gsn_open_wks("pdf","/picture/paint/day/jra55_heating_profile100")
;
;plot4 = new(6,graphic)
;dum4  = new(6,graphic)
;wks4 = gsn_open_wks("pdf","/picture/paint/day/jra55_heating_profile70")
;
;res = True
;res@trYReverse = True
;res@gsnDraw               = False
;res@gsnFrame              = False
;
;res@lgPerimOn              = False                 
;res@trXMaxF = 8
;res@trXMinF = -8
;res@xyLineThicknessF = 1.8
;res@xyDashPattern  = 0
;res@xyMarkLineMode   = "MarkLines"
;res@gsnStringFont = 2.0
;res@xyMarkers   = (/6,7,11,13/)
;res@xyMarkLineMode = "MarkLines"
;res@xyLineColors := (/"blue","black","azure4","red"/)
;res@gsnRightString := "(10N,75E)"
;polyres                   = True
;polyres@gsLineColor       = "black"
;polyres@gsLineThicknessF  = 1.5
;polyres@gsLineDashPattern = 2
;
;do day = 0,5,1
;res@gsnLeftString = char_pen(day)
;plot1(day) = gsn_csm_xy(wks1,data1(:,day,:,{20},{75}),convective&level,res)
;dum1(day)  = gsn_add_polyline(wks1, plot1(day), (/0,0/), (/0,1000/), polyres)
;res@gsnRightString := "(10N,85E)"
;plot2(day) = gsn_csm_xy(wks2,data1(:,day,:,{20},{85}),convective&level,res)
;dum2(day)  = gsn_add_polyline(wks2, plot2(day), (/0,0/), (/0,1000/), polyres)
;res@gsnRightString := "(10N,100E)"
;plot3(day) = gsn_csm_xy(wks3,data1(:,day,:,{20},{100}),convective&level,res)
;dum3(day)  = gsn_add_polyline(wks3, plot3(day), (/0,0/), (/0,1000/), polyres)
;res@gsnRightString := "(10N,70E)"
;plot4(day) = gsn_csm_xy(wks4,data1(:,day,:,{20},{70}),convective&level,res)
;dum4(day)  = gsn_add_polyline(wks4, plot4(day), (/0,0/), (/0,1000/), polyres)
;end do
;
;lgres                       = True   
;lgres@lgMonoLineThickness   = True
;lgres@lgLineThicknessF      = 2.0
;lgres@lgPerimOn             = False           
;lgres@lgLineLabelStrings    = (/"",""/)       
;lgres@lgAutoManage          = False
;lgres@lgLineDashSegLenF     = 0.08
;lgres@lgLabelFontHeightF    = 0.06   
;lgres@lgDashIndexes         = (/0,0/)         
;lgres@vpHeightF             = 0.12            
;lgres@vpWidthF              = 0.145           
;
;lgres@lgLineColors          = (/"blue"/)
;gsn_legend_ndc(wks1,1,(/" convective"/),0.05,0.12,lgres)
;gsn_legend_ndc(wks2,1,(/" convective"/),0.05,0.12,lgres)
;gsn_legend_ndc(wks3,1,(/" convective"/),0.05,0.12,lgres)
;gsn_legend_ndc(wks4,1,(/" convective"/),0.05,0.12,lgres)
;lgres@lgLineColors          = (/"black"/)
;gsn_legend_ndc(wks1,1,(/"  rad+diff+conve"/),0.25,0.12,lgres)
;gsn_legend_ndc(wks2,1,(/"  rad+diff+conve"/),0.25,0.12,lgres)
;gsn_legend_ndc(wks3,1,(/"  rad+diff+conve"/),0.25,0.12,lgres)
;gsn_legend_ndc(wks4,1,(/"  rad+diff+conve"/),0.25,0.12,lgres)
;lgres@lgLineColors          = (/"azure4"/)
;gsn_legend_ndc(wks1,1,(/" radiation"/),0.45,0.12,lgres)
;gsn_legend_ndc(wks2,1,(/" radiation"/),0.45,0.12,lgres)
;gsn_legend_ndc(wks3,1,(/" radiation"/),0.45,0.12,lgres)
;gsn_legend_ndc(wks4,1,(/" radiation"/),0.45,0.12,lgres)
;lgres@lgLineColors          = (/"red"/)
;gsn_legend_ndc(wks1,1,(/" vertical_diffusion"/),0.65,0.12,lgres)
;gsn_legend_ndc(wks2,1,(/" vertical_diffusion"/),0.65,0.12,lgres)
;gsn_legend_ndc(wks3,1,(/" vertical_diffusion"/),0.65,0.12,lgres)
;gsn_legend_ndc(wks4,1,(/" vertical_diffusion"/),0.65,0.12,lgres)
;
;pnlres = True
;pnlres@lgPerimOn             = False
;pnlres@lgAutoManage          = False
;pnlres@lgLineLabelStrings    = (/"",""/)
;pnlres@gsnPanelDebug     = True     ; To get information from panel
;pnlres@gsnPanelMainString = "(10N,75E) vertical heating profile"
;gsn_panel(wks1,plot1,(/2,3/),pnlres)
;pnlres@gsnPanelMainString = "(10N,85E) vertical heating profile"
;gsn_panel(wks2,plot2,(/2,3/),pnlres)
;pnlres@gsnPanelMainString = "(10N,100E) vertical heating profile"
;gsn_panel(wks3,plot3,(/2,3/),pnlres)
;pnlres@gsnPanelMainString = "(10N,70E) vertical heating profile"
;gsn_panel(wks4,plot4,(/2,3/),pnlres)
;end