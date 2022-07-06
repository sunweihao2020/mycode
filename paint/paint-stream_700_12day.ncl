;2021/6/5
;本代码选取-12~2天来绘制700hPa的流线图
begin
f1 = addfile("/data5/2019swh/data/composite3.nc","r")
u  = f1->uwind
v  = f1->vwind
char_day=(/"D0-30","D0-29","D0-28","D0-27","D0-26","D0-25","D0-24","D0-23","D0-22","D0-21","D0-20","D0-19","D0-18","D0-17","D0-16","D0-15","D0-14","D0-13","D0-12","D0-11","D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10","D0+11","D0+12","D0+13","D0+14","D0+15"/)

;sf = u
;vp = u
;sfvp2uvf (sf,vp, u,v)
;printVarSummary(sf)
;;------------------------------
stres                           = True
stres@gsnDraw                   = False
stres@gsnFrame                  = False
stres@stArrowLengthF            = 0.009  
stres@stArrowStride             = 4
stres@stMinArrowSpacingF        = 0.025
stres@stLineThicknessF          = 0.9
stres@stMinDistanceF            = 0.06
stres@stMinLineSpacingF         = 0.005

stres@stLevelSelectionMode      = "ManualLevels"
stres@stMinLevelValF            = -50
stres@stMaxLevelValF            = 50
stres@stLevelSpacingF           = 1.5

stres@gsnStringFont             = 2
stres@gsnRightString            = " "

stres@tmYLLabelFontHeightF      = 0.024
stres@tmXBLabelFontHeightF      = 0.024
stres@stLineStartStride         = 20                 

stres@mpMinLatF            = -20      ; range to zoom in on
stres@mpMaxLatF            =  30.
stres@mpMinLonF            =  30.
stres@mpMaxLonF            = 120.

polyres                   = True
polyres@gsLineColor       = "black"
polyres@gsLineThicknessF  = 1
polyres@gsLineDashPattern = 2

plot1 = new(8,graphic)
dum1  = new(8,graphic)
;wks   = gsn_open_wks("pdf","/data5/2019swh/paint/day/700hpa_12day_stream")
wks   = gsn_open_wks("pdf","/data5/2019swh/paint/day/925hpa_12day_stream")
do day = 18,32,2
    stres@gsnLeftString      = char_day(day)
    stres@gsnRightString     =  "925hPa"
    plot1((day-18)/2) = gsn_csm_streamline_map(wks,u(day,{925},:,:),v(day,{925},:,:),stres)
    dum1((day-18)/2)  = gsn_add_polyline(wks, plot1((day-18)/2), (/30,120/), (/0,0/), polyres)
end do

    pnlres                    = True
    pnlres@gsnPanelMainString = "stream at 925hPa"
    pnlres@gsnPanelDebug      = True     ; To get information from panel
    pnlres@lbLabelFontHeightF = 0.015
    gsn_panel(wks,plot1,(/4,2/),pnlres)

    ;frame(wks)

end
