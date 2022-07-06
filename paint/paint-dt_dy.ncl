;2021/6/22
;本代码绘制温度的水平梯度，来看正负情况
begin
f = addfile("/data5/2019swh/data/composite-tem_advection.nc","r")
ty = f->dt_dy

ty_a  =  dim_avg_n_Wrap(ty(:,:,:,{90:93}), 3)
ty_a  =  ty_a*1E+6
char_day=(/"D0-30","D0-29","D0-28","D0-27","D0-26","D0-25","D0-24","D0-23","D0-22","D0-21","D0-20","D0-19","D0-18","D0-17","D0-16","D0-15","D0-14","D0-13","D0-12","D0-11","D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10","D0+11","D0+12","D0+13","D0+14","D0+15"/)


res = True
res@gsnDraw               = False
res@gsnFrame              = False
res@cnFillOn              = True     
res@cnLineLabelsOn        = False
res@lbLabelBarOn          = False
res@cnLinesOn             = True
res@cnLevelSelectionMode  = "ExplicitLevels" 
res@cnFillPalette         = "BlRe"
res@gsnRightString        = "1E+6 K m-1"
res@cnInfoLabelOn = False
res@gsnStringFont         = 2
res@tmYLLabelFontHeightF      = 0.024
res@tmXBLabelFontHeightF      = 0.024
res@cnLevels              = ispan(-16,16,2)
plot                      =  new(12,graphic)
wks                       = gsn_open_wks("pdf","/data5/2019swh/paint/day/dtdy")

do dd = 22,33
res@gsnLeftString = char_day(dd)
    plot(dd-22) = gsn_csm_pres_hgt(wks, ty_a(dd,{1000:200},{0:40}), res )
end do

pnlres = True
pnlres@gsnPanelMainString = " temperature gradient"
pnlres@gsnPanelLabelBar  = True
pnlres@gsnPanelDebug     = True     ; To get information from panel
pnlres@pmLabelBarWidthF  = 0.55
pnlres@lbLabelFontHeightF = 0.012
gsn_panel(wks,plot,(/3,4/),pnlres)


end