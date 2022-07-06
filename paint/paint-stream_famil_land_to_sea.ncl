;2021/9/21
;本代码绘制famil实验中的结果
;画一到六月
begin
f1_u = addfile("/data5/2019swh/data/zhuang_plev/plev_monthly_con_U.nc","r")
f2_u = addfile("/data5/2019swh/data/zhuang_plev/plev_monthly_ic_U.nc","r")
f3_u = addfile("/data5/2019swh/data/zhuang_plev/plev_monthly_id_U.nc","r")
f4_u = addfile("/data5/2019swh/data/zhuang_plev/plev_monthly_icid_U.nc","r")
f1_v = addfile("/data5/2019swh/data/zhuang_plev/plev_monthly_con_V.nc","r")
f2_v = addfile("/data5/2019swh/data/zhuang_plev/plev_monthly_ic_V.nc","r")
f3_v = addfile("/data5/2019swh/data/zhuang_plev/plev_monthly_id_V.nc","r")
f4_v = addfile("/data5/2019swh/data/zhuang_plev/plev_monthly_icid_V.nc","r")

u1  = f1_u->U
u2  = f2_u->U
u3  = f3_u->U
u4  = f4_u->U
v1  = f1_v->V
v2  = f2_v->V
v3  = f3_v->V
v4  = f4_v->V

u1@_FillValue    =    9999
u2@_FillValue    =    9999
u3@_FillValue    =    9999
u4@_FillValue    =    9999
v1@_FillValue    =    9999
v2@_FillValue    =    9999
v3@_FillValue    =    9999
v4@_FillValue    =    9999

if (any(isnan_ieee(u1))) then
    replace_ieeenan(u1, u1@_FillValue, 0)
    replace_ieeenan(v1, v1@_FillValue, 0)
end if

if (any(isnan_ieee(u2))) then
    replace_ieeenan(u2, u2@_FillValue, 0)
    replace_ieeenan(v2, v2@_FillValue, 0)
end if

if (any(isnan_ieee(u3))) then
    replace_ieeenan(u3, u3@_FillValue, 0)
    replace_ieeenan(v3, v3@_FillValue, 0)
end if

if (any(isnan_ieee(u4))) then
    replace_ieeenan(u4, u4@_FillValue, 0)
    replace_ieeenan(v4, v4@_FillValue, 0)
end if

char_mon  =  (/"Jan","Feb","March","April","May","June"/)
level     =  (/925,850,700,500,200,150/)

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

stres@gsnStringFont             = 1.5
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

plot1 = new(6,graphic)
dum1  = new(6,graphic)
plot2 = new(6,graphic)
dum2  = new(6,graphic)
plot3 = new(6,graphic)
dum3  = new(6,graphic)
plot4 = new(6,graphic)
dum4  = new(6,graphic)
wks1  = gsn_open_wks("pdf","/data5/2019swh/paint/day/control_stream")
wks2  = gsn_open_wks("pdf","/data5/2019swh/paint/day/ic_stream")
wks3  = gsn_open_wks("pdf","/data5/2019swh/paint/day/id_stream")
wks4  = gsn_open_wks("pdf","/data5/2019swh/paint/day/icid_stream")

do mm = 0,5
    wks1  = gsn_open_wks("pdf","/data5/2019swh/paint/day/control_stream"+level(mm))
    wks2  = gsn_open_wks("pdf","/data5/2019swh/paint/day/ic_stream"+level(mm))
    wks3  = gsn_open_wks("pdf","/data5/2019swh/paint/day/id_stream"+level(mm))
    wks4  = gsn_open_wks("pdf","/data5/2019swh/paint/day/icid_stream"+level(mm))
    do month = 0,5
        stres@gsnLeftString      = char_mon(month)
        stres@gsnRightString     =  "control"
        plot1(month)  = gsn_csm_streamline_map(wks1,u1(month,{level(mm)},:,:),v1(month,{level(mm)},:,:),stres)
        dum1(month)   = gsn_add_polyline(wks1, plot1(month), (/30,120/), (/0,0/), polyres)
        stres@gsnRightString     =  "No Indo-China"
        plot2(month)  = gsn_csm_streamline_map(wks2,u2(month,{level(mm)},:,:),v2(month,{level(mm)},:,:),stres)
        dum2(month)   = gsn_add_polyline(wks2, plot2(month), (/30,120/), (/0,0/), polyres)
        stres@gsnRightString     =  "No India"
        plot3(month)  = gsn_csm_streamline_map(wks3,u3(month,{level(mm)},:,:),v3(month,{level(mm)},:,:),stres)
        dum3(month)   = gsn_add_polyline(wks3, plot3(month), (/30,120/), (/0,0/), polyres)
        stres@gsnRightString     =  "No IC and ID"
        plot4(month)  = gsn_csm_streamline_map(wks4,u4(month,{level(mm)},:,:),v4(month,{level(mm)},:,:),stres)
        dum4(month)   = gsn_add_polyline(wks4, plot4(month), (/30,120/), (/0,0/), polyres)
    end do
    pnlres                    = True
    pnlres@gsnPanelMainString = "stream at "+tostring(level(mm))+"hPa"
    pnlres@gsnPanelDebug      = True     ; To get information from panel
    pnlres@lbLabelFontHeightF = 0.015

    gsn_panel(wks1,plot1,(/2,3/),pnlres)
    gsn_panel(wks2,plot2,(/2,3/),pnlres)
    gsn_panel(wks3,plot3,(/2,3/),pnlres)
    gsn_panel(wks4,plot4,(/2,3/),pnlres)
end do

end