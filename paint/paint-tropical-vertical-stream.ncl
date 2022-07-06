;2021/4/7
;本代码绘制热带的热源以及垂直的流场
;本代码求取经向平均（-5，5）（-10，10）

begin
f1   = addfile("/data5/2019swh/data/composite3.nc","r")
f2   = addfile("/data5/2019swh/data/heating/composite-heating-jra55.nc","r")
f3   = addfile("/data5/2019swh/data/heating/composite-heating-merra.nc","r")
f4   = addfile("/data5/2019swh/data/heating/composite-Q1-merra2.nc","r")
f5   = addfile("/data5/2019swh/data/heating/composite-Q1-erain.nc","r")

u    = f1->uwind
v    = f1->vwind
w    = f1->OMEGA
q1c  = f2->convective
q1d  = f2->diffusion
q1r  = f2->radiation
q1   = q1c+q1d+q1r
copy_VarCoords(q1c, q1)
q2   = f3->physics
q3   = f4->Q1
q4   = f5->Q1

q1_a = dim_avg_n(q1(:,:,{-10:10},:), 2)
q2_a = dim_avg_n(q2(:,:,{-10:10},:), 2)
q3_a = dim_avg_n(q3(:,:,{-10:10},:), 2)
q4_a = dim_avg_n(q4(:,:,{-10:10},:), 2)

copy_VarCoords(q1(:,:,5,:), q1_a)
copy_VarCoords(q2(:,:,5,:), q2_a)
copy_VarCoords(q3(:,:,5,:), q3_a)
copy_VarCoords(q4(:,:,5,:), q4_a)

ua = dim_avg_n(u(:,:,{-10:10},:), 2)
va = dim_avg_n(v(:,:,{-10:10},:), 2)
wa = dim_avg_n(w(:,:,{-10:10},:), 2)

copy_VarCoords(u(:,:,5,:), ua)
copy_VarCoords(v(:,:,5,:), va)
copy_VarCoords(w(:,:,5,:), wa)

wa = wa*(60)
char_day=(/"D0-30","D0-29","D0-28","D0-27","D0-26","D0-25","D0-24","D0-23","D0-22","D0-21","D0-20","D0-19","D0-18","D0-17","D0-16","D0-15","D0-14","D0-13","D0-12","D0-11","D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10","D0+11","D0+12","D0+13","D0+14","D0+15"/)


res                            = True                                     ; plot mods desired
res@gsnDraw                    = False
res@gsnFrame                   = False
res@lbLabelBarOn               = False   
res@lbLabelsOn                 = False
res@trYReverse                 = True                             

res@cnFillOn                   = True                ; turn on color fill
res@cnFillPalette              = "BlueDarkRed18" ; choose color map
res@cnLineLabelsOn             = False               ; turn off line labels
;res@lbLabelStride             = 2                   ; label every other box
res@cnLevelSelectionMode       = "ExplicitLevels" 
res@cnLevels                   = ispan(-8,8,1)
res@cnMissingValPerimOn        = True            ; turn on the missing value perimeter
;res@gsnLeftString             = char_day(iday-15)
res@cnLinesOn                  = False
res@cnInfoLabelOn              = False
res@cnMissingValPerimColor     = "black"           ; outline the perimeter red
res@cnMissingValFillPattern    = 0               ; choose fill pattern 0 (solid fill) 
res@cnMissingValFillColor      = "black"          ; color fill missing areas blue

res@stLevelSelectionMode       =  "ManualLevels"
;res@stLevelSpacingF           =  8
res@stMinLineSpacingF          = 0.005
res@stMinArrowSpacingF         = 0.5
res@stMinArrowSpacingF         = 0.02             ; arrow spacing.
res@stArrowLengthF             = 0.008             ; arrow length
res@stMinDistanceF             = 0.05

res@tmXBLabelFontHeightF       = 0.030
res@tmYLLabelFontHeightF       = 0.030
res@gsnPresHgtHeightLabelOn    = False 
res@tmXBMode                   = "Explicit"
res@tmXBValues                 = (/30,60,90,120/)
res@tmXBLabels                 = (/"30","60","90","120"/)
res@gsnRightString             = "K day-1"
res@gsnRightStringFontHeightF  = 0.032
res@gsnLeftStringFontHeightF   = 0.032

wks1  = gsn_open_wks("pdf", "/data5/2019swh/paint/day/tropical_stream_q1")
wks2  = gsn_open_wks("pdf", "/data5/2019swh/paint/day/tropical_stream_q2")
wks3  = gsn_open_wks("pdf", "/data5/2019swh/paint/day/tropical_stream_q3")
wks4  = gsn_open_wks("pdf", "/data5/2019swh/paint/day/tropical_stream_q4")

plot1 = new(15,graphic)
plot2 = new(15,graphic)
plot3 = new(15,graphic)
plot4 = new(15,graphic)
do day=16,30
res@gsnLeftString            = char_day(day)
plot1(day-16)  = gsn_csm_pres_hgt_streamline(wks1,q1_a(day,{1000:200},{30:120}),va(day,{1000:200},{30:120}),wa(day,{1000:200},{30:120}),res )  
plot2(day-16)  = gsn_csm_pres_hgt_streamline(wks2,q2_a(day,{1000:200},{30:120}),va(day,{1000:200},{30:120}),wa(day,{1000:200},{30:120}),res )
plot3(day-16)  = gsn_csm_pres_hgt_streamline(wks3,q3_a(day,{1000:200},{30:120}),va(day,{1000:200},{30:120}),wa(day,{1000:200},{30:120}),res )
plot4(day-16)  = gsn_csm_pres_hgt_streamline(wks4,q4_a(day,{1000:200},{30:120}),va(day,{1000:200},{30:120}),wa(day,{1000:200},{30:120}),res )
end do

pnlres                       = True
pnlres@gsnPanelLabelBar      = True
pnlres@gsnPanelDebug         = True    
pnlres@pmLabelBarWidthF      = 0.55
pnlres@lbLabelFontHeightF    = 0.012
pnlres@gsnPanelMainString    = "Q1(jra55) & stream"
gsn_panel(wks1,plot1,(/3,5/),pnlres)
pnlres@gsnPanelMainString    = "Q1(MERRA2) & stream"
gsn_panel(wks2,plot2,(/3,5/),pnlres)
pnlres@gsnPanelMainString    = "Q1(erain) & stream"
gsn_panel(wks3,plot3,(/3,5/),pnlres)
pnlres@gsnPanelMainString    = "Q1(MERRA2) & stream"
gsn_panel(wks4,plot4,(/3,5/),pnlres)

end
