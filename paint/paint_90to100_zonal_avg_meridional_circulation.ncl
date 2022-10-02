;2022/7/1
;本代码绘制90-100E平均的经向-垂直环流场

begin
f0   = addfile("/home/sun/data/model_data/climate/b1850_control_atmospheric_monthly_average.nc","r")


avg_v      =  f0->avg_v
avg_omega  =  f0->avg_omega
avg_temg   =  f0->avg_t_gradient ; 0-29 30 31-60

;处理nan
avg_v@_FillValue  =  9999
avg_omega@_FillValue    =  9999
avg_temg@_FillValue     =  9999

if (any(isnan_ieee(avg_v))) then
  replace_ieeenan (avg_v, avg_v@_FillValue, 0)
  replace_ieeenan (avg_omega, avg_omega@_FillValue, 0)
  replace_ieeenan (avg_temg, avg_temg@_FillValue, 0)
end if

res                            = True             
res@gsnDraw                    = False
res@gsnFrame                   = False
res@lbLabelBarOn               = False   
res@lbLabelsOn                 = False
res@trYReverse                 = True                             

res@cnFillOn                   = True                ; turn on color fill
res@cnFillPalette              = "BlueDarkRed18" ; choose color map
res@cnLineLabelsOn             = False               ; turn off line labels
res@cnLevelSelectionMode       = "ExplicitLevels" 
res@cnLevels                   = fspan(-2,2,11)
res@cnMissingValPerimOn        = True            ; turn on the missing value perimeter
;res@gsnLeftString              = "D0"+
res@cnLinesOn                  = False
res@cnInfoLabelOn              = False

res@cnMissingValPerimColor     = "black"  
res@cnMissingValFillPattern    = 0        
res@cnMissingValFillColor      = "black"  

res@stLevelSelectionMode       =  "ManualLevels"
;res@stLevelSpacingF           =  8
;res@stMinLineSpacingF          = 0.005
;res@stMinArrowSpacingF         = 0.5
;res@stMinArrowSpacingF         = 0.02             ; arrow spacing.
res@stArrowLengthF             = 0.008             ; arrow length
res@stArrowStride              = 3
;res@stMinDistanceF             = 0.05

res@tmXBLabelFontHeightF       = 0.030
res@tmYLLabelFontHeightF       = 0.030
res@gsnPresHgtHeightLabelOn    = False 
res@tmXBMode                   = "Explicit"
res@tmXBValues                 = (/-10,0,10,20,30,40/)
res@tmXBLabels                 = (/"10S","EQ","10N","20N","30N","40N"/)

wks1  = gsn_open_wks("pdf", "/home/sun/paint/meridional_tem_gradient_circulation/meridional_circulation_d0tod+8")


plot1 = new(9,graphic)

avg_temg  =  avg_temg*1e5

do day=30,38
res@gsnLeftString            = "D0"+(day-30)
plot1(day-30)  = gsn_csm_pres_hgt_streamline(wks1,avg_temg(day,{1000:200},{-10:40}),avg_v(day,{1000:200},{-10:40}),avg_omega(day,{1000:200},{-10:40})*-3,res )  
end do

pnlres                       = True
pnlres@gsnPanelLabelBar      = True
pnlres@gsnPanelDebug         = True    
pnlres@pmLabelBarWidthF      = 0.55
pnlres@lbLabelFontHeightF    = 0.012
pnlres@gsnPanelMainString    = "temp gradient(shading)"
gsn_panel(wks1,plot1,(/3,3/),pnlres)


end
