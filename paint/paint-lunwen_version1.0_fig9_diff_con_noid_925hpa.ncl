;2021/11/2
;本代码绘制famil中控制实验与去除印度大陆实验之差
begin
path  =  "/home/sun/qomo-data/zhuang_plev/pentad_average/"

f1    =  addfile(path+"plev_con_U.nc","r")
f2    =  addfile(path+"plev_con_V.nc","r")

f3    =  addfile(path+"plev_id_U.nc","r")
f4    =  addfile(path+"plev_id_V.nc","r")

con_u =  f1->u_pen
con_v =  f2->v_pen

id_u  =  f3->u_pen
id_v  =  f4->v_pen

diff_u  =  con_u - id_u
diff_v  =  con_v - id_v

copy_VarCoords(con_u, diff_u)
copy_VarCoords(con_v, diff_v)

;矢量图设置
vcres                             = True
vcres@gsnDraw                     = False             ; do not draw the plot      
vcres@gsnFrame                    = False            ; so we can draw time stamp
vcres@vcRefAnnoOrthogonalPosF     = -1.35             ; move ref vector up
vcres@vpWidthF                    = 0.6
vcres@vpHeightF                   = 0.55
vcres@gsnAddCyclic                =  False
vcres@vcRefMagnitudeF             = 4               ; define vector ref mag
vcres@vcRefLengthF                = 0.045            ; define length of vec ref
vcres@vcGlyphStyle                = "CurlyVector"    ; turn on curly vectors
vcres@vcMinDistanceF              = 0.02
vcres@vcRefAnnoOrthogonalPosF     = -1.0   
vcres@vcMinDistanceF              = 0.02
vcres@vcLineArrowThicknessF       =  1.5
vcres@mpMinLatF                   =  -15 
vcres@mpMaxLatF                   =  30.
vcres@mpMinLonF                   =  30.
vcres@mpMaxLonF                   =  120.
vcres@tmYLLabelFontHeightF          = 0.024
vcres@tmXBLabelFontHeightF          = 0.024 

polyres                   = True
polyres@gsLineColor       = "black"
polyres@gsLineThicknessF  = 2
polyres@gsLineDashPattern = 2

plot  =  new(6,graphic)
dum   =  new(6,graphic)

wks   =  gsn_open_wks("pdf","/home/sun/paint/lunwen/version1.0/fig9_version1.0_control_and_noid_925")


do yy = 20,22
    vcres@gsnLeftString        =      "Pentad "+flt2string(yy+1)
    vcres@gsnRightString       =      "m/s"
    plot((yy-20)*2)                 =      gsn_csm_vector_map(wks,diff_u(yy,{925},:,:),diff_v(yy,{925},:,:),vcres)
    dum((yy-20)*2)                  =      gsn_add_polyline(wks, plot((yy-20)*2), (/30,120/), (/0,0/), polyres)
end do
do yy = 23,25
    vcres@gsnLeftString        =      "Pentad "+flt2string(yy+1)
    vcres@gsnRightString       =      "m/s"
    plot((yy-22)*2-1)                 =      gsn_csm_vector_map(wks,diff_u(yy,{925},:,:),diff_v(yy,{925},:,:),vcres)
    dum((yy-22)*2-1)                  =      gsn_add_polyline(wks, plot((yy-22)*2-1), (/30,120/), (/0,0/), polyres)
end do
pnlres = True
pnlres@gsnPanelMainString = "diff_wind between CTRL and NO_INDO at 925hPa"
pnlres@gsnPanelDebug     = True
pnlres@lbLabelFontHeightF = 0.012
gsn_panel(wks,plot,(/3,2/),pnlres)


end