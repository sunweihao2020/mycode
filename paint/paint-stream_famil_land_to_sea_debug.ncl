;2021/9/21
;针对前一版本的debug
begin
f1_u = addfile("/data5/2019swh/data/zhuang_plev/plev_con_U.nc","r")
f2_u = addfile("/data5/2019swh/data/zhuang_plev/plev_ic_U.nc","r")
f3_u = addfile("/data5/2019swh/data/zhuang_plev/plev_id_U.nc","r")
f4_u = addfile("/data5/2019swh/data/zhuang_plev/plev_icid_U.nc","r")
f1_v = addfile("/data5/2019swh/data/zhuang_plev/plev_con_V.nc","r")
f2_v = addfile("/data5/2019swh/data/zhuang_plev/plev_ic_V.nc","r")
f3_v = addfile("/data5/2019swh/data/zhuang_plev/plev_id_V.nc","r")
f4_v = addfile("/data5/2019swh/data/zhuang_plev/plev_icid_V.nc","r")

u1  = f1_u->U
u2  = f2_u->U
u3  = f3_u->U
u4  = f4_u->U
v1  = f1_v->V
v2  = f2_v->V
v3  = f3_v->V
v4  = f4_v->V

day   =   150
level =   700

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
stres@mpMaxLatF            =  60.
stres@mpMinLonF            =  30.
stres@mpMaxLonF            = 120.

polyres                   = True
polyres@gsLineColor       = "black"
polyres@gsLineThicknessF  = 1
polyres@gsLineDashPattern = 2

plot = new(4,graphic)
dum  = new(4,graphic)

wks  = gsn_open_wks("pdf","/data5/2019swh/paint/day/test_stream")

stres@gsnLeftString  =  "con"
plot(0)  =  gsn_csm_streamline_map(wks,u1(day,{level},:,:),v1(day,{level},:,:),stres)
stres@gsnLeftString  =  "ic"
plot(1)  =  gsn_csm_streamline_map(wks,u2(day,{level},:,:),v2(day,{level},:,:),stres)
stres@gsnLeftString  =  "id"
plot(2)  =  gsn_csm_streamline_map(wks,u3(day,{level},:,:),v3(day,{level},:,:),stres)
stres@gsnLeftString  =  "icid"
plot(3)  =  gsn_csm_streamline_map(wks,u4(day,{level},:,:),v4(day,{level},:,:),stres)

pnlres                    = True
pnlres@gsnPanelMainString = "stream at 925hPa"
pnlres@gsnPanelDebug      = True     ; To get information from panel
pnlres@lbLabelFontHeightF = 0.015
gsn_panel(wks,plot,(/2,2/),pnlres)

end