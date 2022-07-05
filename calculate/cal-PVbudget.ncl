;2021/1/9
;本程序主要用于计算PV的budget，上下面的budget可以绘制平面图但是
;东西面和南北面无法绘制，而主要统一起来计算一个值
;1.00000000e+03 9.75000000e+02 9.50000000e+02 9.25000000e+02 9.00000000e+02 8.75000000e+02 8.50000000e+02 8.25000000e+02 8.00000000e+02 7.75000000e+02 7.50000000e+02 7.25000000e+02 7.00000000e+02 6.50000000e+02 6.00000000e+02 5.50000000e+02 5.00000000e+02 4.50000000e+02 4.00000000e+02 3.50000000e+02
;积分到600 14层
;75E-90E 90E-100E 5N-25N 
begin
f1 = addfile("/data5/2019swh/data/potential_temperature.nc","r")
theta = f1->pt

f2 = addfile("/data5/2019swh/data/composite-modeltheta.nc","r")
thetam = f2->theta

f3 = addfile("/data5/2019swh/data/three-dimension-vorticity.nc","r")
vor2_z = f3->z_vorticity
vor2_x = f3->x_vorticity
vor2_y = f3->y_vorticity

f4 = addfile("/data5/2019swh/data/three-dimension-vorticity-pressure.nc","r")
vor3_z = f4->z_vorticity
vor3_x = f4->x_vorticity
vor3_y = f4->y_vorticity

f5 = addfile("/data5/2019swh/data/composite_PS.nc","r")
ps = f5->PS

char_day=(/"D0-30","D0-29","D0-28","D0-27","D0-26","D0-25","D0-24","D0-23","D0-22","D0-21","D0-20","D0-19","D0-18","D0-17","D0-16","D0-15","D0-14","D0-13","D0-12","D0-11","D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10","D0+11","D0+12","D0+13","D0+14","D0+15"/)

jx_bottom  =  thetam(:,32,:,:) *  vor2_x(:,32,:,:)
jy_bottom  =  thetam(:,32,:,:) *  vor2_y(:,32,:,:)   
jz_bottom  =  thetam(:,32,:,:) *  vor2_z(:,32,:,:) 


jx_upper600   =  theta(:,14,:,:)  *  vor3_x(:,14,:,:)
jy_upper600   =  theta(:,14,:,:)  *  vor3_y(:,14,:,:)
jz_upper600   =  theta(:,14,:,:)  *  vor3_z(:,14,:,:)

jx_upper700   =  theta(:,12,:,:)  *  vor3_x(:,12,:,:)
jy_upper700   =  theta(:,12,:,:)  *  vor3_y(:,12,:,:)
jz_upper700   =  theta(:,12,:,:)  *  vor3_z(:,12,:,:)

jx_upper100   =  theta(:,24,:,:)  *  vor3_x(:,24,:,:)
jy_upper100   =  theta(:,24,:,:)  *  vor3_y(:,24,:,:)
jz_upper100   =  theta(:,24,:,:)  *  vor3_z(:,24,:,:)

;垂直面上的收支
deltaz600   =   jz_upper600 - jz_bottom
deltaz700   =   jz_upper700 - jz_bottom
deltaz100_600 = jz_upper100 - jz_upper600
deltaz100_700 = jz_upper100 - jz_upper700

;东西面上的收支
deltax1    =    theta(:,:,:,{90})*vor3_x(:,:,:,{90}) - theta(:,:,:,{75})*vor3_x(:,:,:,{75})
deltax2    =    theta(:,:,:,{100})*vor3_x(:,:,:,{100}) - theta(:,:,:,{90})*vor3_x(:,:,:,{90})
;南北面上的收支
deltay    =    theta(:,:,{25},:)*vor3_y(:,:,{25},:) - theta(:,:,{5},:)*vor3_y(:,:,{5},:)

;赋予单位
deltaz600!0 = "time"
deltaz600!1 = "lat"
deltaz600!2 = "lon"
deltaz600&time = theta&time
deltaz600&lat  = theta&lat
deltaz600&lon  = theta&lon
copy_VarCoords(deltaz600, deltaz700)
copy_VarCoords(deltaz600, deltaz100_600)
;绘制三个面上的收支
res = True
res@gsnDraw               = False
res@gsnFrame              = False
res@cnFillOn              = True     ; turn on color fill
res@cnFillPalette         = "WhiteYellowOrangeRed"
res@cnLineLabelsOn        = True
res@lbLabelBarOn          = False  
res@cnLineLabelsOn        = False
res@gsnRightString        = ""
res@cnLevelSelectionMode = "ExplicitLevels"
res@cnLevels             =  fspan(-1.2, 1.2,13) 
res@cnFillPalette         = "hotcolr_19lev"
res@cnMissingValPerimOn     = True   
res@cnMissingValPerimColor  = "black"
res@cnMissingValFillPattern = 0      
res@cnMissingValFillColor   = "gray" 
tmYROn           = False     ; Turn off right and top tick marks
res@tmXTOn           = False     ; Turn off right and top tick marks

;=====================绘制平面差分图==========================
;res@mpMinLatF            =  -10      ; range to zoom in on
;res@mpMaxLatF            =  30.
;res@mpMinLonF            =  30.
;res@mpMaxLonF            =  120.
;plot1 = new(15,graphic)
;plot2 = new(15,graphic)
;plot3 = new(15,graphic)
;wks1 = gsn_open_wks("pdf", "/data5/2019swh/paint/day/0-600")
;wks2 = gsn_open_wks("pdf", "/data5/2019swh/paint/day/0-700")
;wks3 = gsn_open_wks("pdf", "/data5/2019swh/paint/day/600-100")
;do day = 0,14,1
;    ;wks1 = gsn_open_wks("pdf", "/data5/2019swh/paint/day/0-600_"+day)
;    ;wks2 = gsn_open_wks("pdf", "/data5/2019swh/paint/day/0-700_"+day)
;    ;wks3 = gsn_open_wks("pdf", "/data5/2019swh/paint/day/600-100_"+day)
;    res@gsnCenterString = char_day(day*2+1)
;    d1   = deltaz600(day*2+1,:,:) - deltaz600(0,:,:)
;    d2   = deltaz700(day*2+1,:,:) - deltaz700(0,:,:)
;    d3   = deltaz100_600(day*2+1,:,:) - deltaz100_600(0,:,:)
;    d1!0   =  "lat"
;    d1!1   =  "lon"
;    d1&lat = deltaz600&lat
;    d1&lon = deltaz600&lon
;    copy_VarCoords(d1, d2)
;    copy_VarCoords(d2, d3)
;    plot1(day) = gsn_csm_contour_map(wks1,d1(:,:), res)
;    plot2(day) = gsn_csm_contour_map(wks2,d2(:,:), res)
;    plot3(day) = gsn_csm_contour_map(wks3,d3(:,:), res)
;
;end do
;pnlres = True
;pnlres@gsnPanelMainString   = "vertical PV budget"
;pnlres@gsnPanelLabelBar  = True
;;pnlres@gsnPanelDebug     = True     ; To get information from panel
;gsn_panel(wks1,plot1,(/3,5/),pnlres)
;gsn_panel(wks2,plot2,(/3,5/),pnlres)
;gsn_panel(wks3,plot3,(/3,5/),pnlres)
;
;====================绘制东西差分图===========================
;plot1 = new(15,graphic)
;plot2 = new(15,graphic)
;wks1 = gsn_open_wks("pdf", "/data5/2019swh/paint/day/75-90E")
;wks2 = gsn_open_wks("pdf", "/data5/2019swh/paint/day/90-100E")
;do day=0,14
;
;    res@gsnCenterString = char_day(day*2+1)
;    res@gsnLeftString = "75-90E"
;    d1   = deltax1(day*2+1,:,:) - deltax1(0,:,:)
;    d2   = deltax2(day*2+1,:,:) - deltax2(0,:,:)
;
;    d1!0   =  "level"
;    d1!1   =  "lat"
;    d1&level = vor3_x&level
;    d1&lat   = vor3_x&lat
;    copy_VarCoords(d1, d2)
;    
;    plot1(day) = gsn_csm_pres_hgt(wks1,d1(0:24,{0:30}),res)
;    res@gsnLeftString = "90-100E"
;    plot2(day) = gsn_csm_pres_hgt(wks2,d2(0:24,{0:30}),res)
;
;end do
;pnlres = True
;pnlres@gsnPanelMainString   = "W-E PV budget"
;pnlres@gsnPanelLabelBar  = True
;gsn_panel(wks1,plot1,(/3,5/),pnlres)
;gsn_panel(wks2,plot2,(/3,5/),pnlres)
;===================绘制南北差分图=============================
plot1 = new(15,graphic)
wks1 = gsn_open_wks("pdf", "/data5/2019swh/paint/day/5-25")

do day=11,25
    res@gsnCenterString = char_day(day)
    res@gsnLeftString = "5-25E"
    d1   = deltay(day,:,:) - deltay(10,:,:)

    d1!0   =  "level"
    d1!1   =  "lon"
    d1&level = vor3_x&level
    d1&lon   = vor3_x&lon
    
    plot1(day-11) = gsn_csm_pres_hgt(wks1,d1(0:20,{30:120}),res)
end do
pnlres = True
pnlres@gsnPanelMainString   = "N-S PV budget"
pnlres@gsnPanelLabelBar  = True
gsn_panel(wks1,plot1,(/3,5/),pnlres)

end
