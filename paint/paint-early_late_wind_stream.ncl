;2021/8/15
;本代码使用早年晚年合成的数据绘制环流场
;本代码为流线图，另有矢量图版本
begin
path = "/data5/2019swh/data/"
f1 = addfile(path+"early-year-composite.nc","r")
f2 = addfile(path+"late-year-composite.nc", "r")

u1 = f1->u
u2 = f2->u
v1 = f1->v
v2 = f2->v

char_day=(/"D0-30","D0-29","D0-28","D0-27","D0-26","D0-25","D0-24","D0-23","D0-22","D0-21","D0-20","D0-19","D0-18","D0-17","D0-16","D0-15","D0-14","D0-13","D0-12","D0-11","D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10","D0+11","D0+12","D0+13","D0+14","D0+15"/)
lev = (/3,6,12,16,22,24/)
level = (/"925hPa","850hPa","700hPa","500hPa","200hPa","100hPa"/)

stres                           = True
stres@gsnDraw                   = False
stres@gsnFrame                  = False
;stres@stArrowLengthF            = 0.009  
;stres@stArrowStride             = 4
;stres@stMinArrowSpacingF        = 0.05
stres@stLineThicknessF          = 0.9
stres@stMinDistanceF            = 0.07
;stres@stMinLineSpacingF         = 0.05
;
;stres@stLevelSelectionMode      = "ManualLevels"
;stres@stMinLevelValF            = -50
;stres@stMaxLevelValF            = 50
;stres@stLevelSpacingF           = 1.5
;
;stres@gsnStringFont             = 2
;stres@gsnRightString            = " "
;
stres@tmYLLabelFontHeightF      = 0.024
stres@tmXBLabelFontHeightF      = 0.024
;stres@stLineStartStride         = 20                 
;
stres@mpMinLatF            = -10      ; range to zoom in on
stres@mpMaxLatF            =  30.
stres@mpMinLonF            =  30.
stres@mpMaxLonF            = 120.

;stres@tiMainString       = "Streamlines"            ; titlest
stres@stArrowLengthF     = 0.004                    ; size of the arrows.
stres@stMinArrowSpacingF = 0.01                    ; arrow spacing.
stres@stArrowStride      = 5                        ; arrows start every third 设置的值大，箭头就少
stres@stArrowLengthF     = 0.015

polyres                   = True
polyres@gsLineColor       = "black"
polyres@gsLineThicknessF  = 1
polyres@gsLineDashPattern = 2

do ll = 0,5
plot1  =  new(16,graphic)
dum1   =  new(16,graphic)
plot2  =  new(16,graphic)
dum2   =  new(16,graphic)

wks1   =  gsn_open_wks("pdf","/data5/2019swh/paint/day/early_stream"+level(ll))
wks2   =  gsn_open_wks("pdf","/data5/2019swh/paint/day/late_stream"+level(ll))

stres@gsnRightString          =      level(ll)
    do day = 4,34,2
        stres@gsnLeftString   =      char_day(day)
        plot1((day-4)/2)      =      gsn_csm_streamline_map(wks1,u1(day,lev(ll),:,:),v1(day,lev(ll),:,:),stres)
        plot2((day-4)/2)      =      gsn_csm_streamline_map(wks2,u2(day,lev(ll),:,:),v2(day,lev(ll),:,:),stres)
        dum1((day-4)/2)       =      gsn_add_polyline(wks1, plot1((day-4)/2), (/30,120/), (/0,0/), polyres)
        dum2((day-4)/2)       =      gsn_add_polyline(wks2, plot2((day-4)/2), (/30,120/), (/0,0/), polyres)
    end do

pnlres = True
pnlres@gsnPanelMainString     =      "early year composite stream at "+level(ll)
pnlres@gsnPanelDebug          =      True     ; To get information from panel
gsn_panel(wks1,plot1,(/4,4/),pnlres)
delete(wks1)
pnlres@gsnPanelMainString     =      "late year composite stream at "+level(ll)
gsn_panel(wks2,plot2,(/4,4/),pnlres)
delete(wks2)
end do
end