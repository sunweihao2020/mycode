;2021/4/19
;所用资料：merra2季风爆发的合成分析
;要素：风场、散度
;层次：多层次
begin
f = addfile("/data5/2019swh/data/composite3.nc","r")
ff = addfile("/data5/2019swh/data/div_vor.nc","r")
u = f->uwind
v = f->vwind
div = ff->div


char_day=(/"D0-30","D0-29","D0-28","D0-27","D0-26","D0-25","D0-24","D0-23","D0-22","D0-21","D0-20","D0-19","D0-18","D0-17","D0-16","D0-15","D0-14","D0-13","D0-12","D0-11","D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10","D0+11","D0+12","D0+13","D0+14","D0+15"/)
lev = (/3,6,12,16,22,24/)
level = (/"925hPa","850hPa","700hPa","500hPa","200hPa","100hPa"/)

res = True
res@cnFillOn              = True
res@gsnDraw               = False
res@gsnFrame              = False
res@mpMinLatF            = -20 
res@mpMaxLatF            =  30.
res@mpMinLonF            =  30.
res@mpMaxLonF            =  120.
res@cnFillPalette         = "BlueDarkRed18"
res@cnLineLabelsOn        = False
res@cnInfoLabelOn         = False 
res@vpWidthF              = 0.6
res@cnLinesOn             = False
res@vpHeightF             = 0.55
res@mpGeophysicalLineThicknessF  = 1
res@cnLevelSelectionMode       = "ExplicitLevels" 
res@cnLevels             = ispan(-8,8,2)
res@lbLabelBarOn = False
res@tmYLLabelFontHeightF      = 0.024
res@tmXBLabelFontHeightF      = 0.024
res@gsnRightString = "10~S~-6~N~ s~S~-1~n~"
res@gsnStringFont = 2

stres = True
stres@gsnDraw    = False
stres@gsnFrame   = False
stres@stArrowLengthF     = 0.008  
stres@stLengthCheckCount = 15
stres@stArrowStride      = 1
stres@stMinArrowSpacingF = 0.025
stres@stLineThicknessF   = 0.7
;stres@stLevelSpacingF    = 25
stres@gsnStringFont         = 2
stres@gsnRightString = " "
stres@tmYLLabelFontHeightF      = 0.024
stres@tmXBLabelFontHeightF      = 0.024
stres@stLineStartStride  = 20                    ; default is 2            
stres@stStepSizeF        = 0.001                ; default is dynamic

polyres                   = True
polyres@gsLineColor       = "black"
polyres@gsLineThicknessF  = 1
polyres@gsLineDashPattern = 2


do ll = 0,5
plot1 = new(15,graphic)
dum1  = new(15,graphic)
wks1 = gsn_open_wks("pdf","/data5/2019swh/paint/day/stream_field_"+level(ll))

do day = 16,30
    res@gsnLeftString = char_day(day)
    plot1(day-16) = gsn_csm_contour_map(wks1,div(day,lev(ll),:,:),res)

    a = gsn_csm_streamline(wks1,u(day,lev(ll),:,:),v(day,lev(ll),:,:),stres)
    overlay(plot1(day-16),a)
    dum1(day-16) = gsn_add_polyline(wks1, plot1(day-16), (/30,120/), (/0,0/), polyres)
  


end do
    pnlres = True
    pnlres@gsnPanelMainString = "wind at "+level(ll)+" & divergence"
    pnlres@gsnPanelLabelBar  = True
    pnlres@gsnPanelDebug     = True     ; To get information from panel
    pnlres@lbLabelFontHeightF = 0.015
    gsn_panel(wks1,plot1,(/5,3/),pnlres)

    ;frame(wks)
end do
end