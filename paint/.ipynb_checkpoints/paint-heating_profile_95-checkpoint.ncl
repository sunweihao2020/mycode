;2021/6/7
;本代码绘制95E逐侯的加热廓线
begin
f  =  addfile("/data5/2019swh/data/composite-heating-merra.nc","r")
physics      = f->physics(:,:,{10},{95})
turbulence = f->turbulence(:,:,{10},{95})
moist      = f->moist(:,:,{10},{95})
radiation  = f->radiation(:,:,{10},{95})
ta_tu_mo   = turbulence + moist + radiation
pens = (/"P0-6","P0-5","P0-4","P0-3","P0-2","P0-1"/)


data1 = new((/4,61,dimsizes(physics&level)/),double)
data1(0,:,:) = physics
data1(1,:,:) = radiation
data1(2,:,:) = turbulence
data1(3,:,:) = moist

plot = new(6,graphic)
dum  = new(6,graphic)
wks  = gsn_open_wks("pdf","/data5/2019swh/paint/day/heating_profile95")

res = True
res@gsnDraw               = False
res@gsnFrame              = False
res@gsnRightString        = "(10N,95E)"

res@trXMaxF          =    6
res@trXMinF          =    -4
res@trYReverse       =    True

res@tmYLLabelFontHeightF      = 0.024
res@tmXBLabelFontHeightF      = 0.024

res@xyLineThicknessF =    1.8
res@xyDashPattern    =    0
res@xyMarkLineMode   =    "MarkLines"
res@xyMarkers        =    (/4,6,7,11/)
res@xyLineColors    :=    (/"black","azure4","red","blue"/)

res@lgPerimOn              = False  

polyres                   = True
polyres@gsLineColor       = "black"
polyres@gsLineThicknessF  = 1.5
polyres@gsLineDashPattern = 2

do day = 0,5
res@gsnLeftString = pens(day)
plot(day) = gsn_csm_xy(wks,dim_avg_n_Wrap(data1(:,day*5:(day*5+5),:),1),physics&level,res)
dum(day)  = gsn_add_polyline(wks, plot(day), (/0,0/), (/0,1000/), polyres)
end do

lgres                       = True   
lgres@lgMonoLineThickness   = True
lgres@lgLineThicknessF      = 2.0
lgres@lgPerimOn             = False              
lgres@lgLineLabelStrings    = (/"",""/)          
lgres@lgAutoManage          = False
lgres@lgLineDashSegLenF     = 0.08
lgres@lgLabelFontHeightF    = 0.06   
lgres@lgDashIndexes         = (/0,0/)     

lgres@vpHeightF             = 0.12                  
lgres@vpWidthF              = 0.145    

lgres@lgLineColors          = (/"black"/)
gsn_legend_ndc(wks,1,(/" total"/),0.15,0.15,lgres)
lgres@lgLineColors          = (/"azure4"/)
gsn_legend_ndc(wks,1,(/" radiation"/),0.35,0.15,lgres)
lgres@lgLineColors          = (/"red"/)
gsn_legend_ndc(wks,1,(/"  sensible"/),0.55,0.15,lgres)
lgres@lgLineColors          = (/"blue"/)
gsn_legend_ndc(wks,1,(/" moist"/),0.75,0.15,lgres)

pnlres = True
pnlres@lgPerimOn             = False
pnlres@lgAutoManage          = False
pnlres@lgLineLabelStrings    = (/"",""/)
pnlres@gsnPanelDebug     = True  
pnlres@gsnPanelMainString = "(10N,95E) vertical heating profile"
gsn_panel(wks,plot,(/2,3/),pnlres)
end
