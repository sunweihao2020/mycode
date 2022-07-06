;2021/10/22
;本代码使用famil来绘制700hPa的流场图，目的在于比对ncl和python画流线图的差异
begin
path = "/home/sun/qomo-data/zhuang_plev/pentad_average/"
f1 = addfile(path+"plev_con_U.nc","r")
f2 = addfile(path+"plev_con_V.nc","r")

u  = f1->u_pen
v  = f2->v_pen

;处理缺测值
u@_FillValue = 999
u@_FillValue = 999

if (any(isnan_ieee(u))) then
    replace_ieeenan(u, u@_FillValue, 0)
    replace_ieeenan(v, v@_FillValue, 0)
end if

;绘制700hPa的

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

plot1 = new(9,graphic)
dum1  = new(9,graphic)

wks   = gsn_open_wks("pdf","/home/sun/paint/python_ncl_stream_compare/compare")
do day = 18,26,1
    stres@gsnRightString     =  "700hPa"
    plot1((day-18)) = gsn_csm_streamline_map(wks,u(day,{700},:,:),v(day,{700},:,:),stres)
    dum1((day-18))  = gsn_add_polyline(wks, plot1((day-18)), (/30,120/), (/0,0/), polyres)
end do

pnlres                    = True
pnlres@gsnPanelMainString = "stream at 700hPa(19-27 pentad)"
pnlres@gsnPanelDebug      = True     ; To get information from panel
pnlres@lbLabelFontHeightF = 0.015
gsn_panel(wks,plot1,(/3,3/),pnlres)
;frame(wks)

end