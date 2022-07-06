;2021/6/15
;本代码绘制纬向-垂直的地转偏差
begin


;;设置
res                                     =       True
res@gsnContourNegLineDashPattern        =       1
res@gsnDraw                             =       False
res@gsnFrame                            =       False
res@gsnAddCyclic                        =       False
res@gsnStringFont                       =       2
res@gsnRightString                      =       "m s-1"

res@tmXBMode                            =       "Explicit"
res@tmXBValues                          =       ispan(60,120,15)
res@tmXBLabels                          =       ispan(60,120,15)
res@tmXBMinorValues                     =       ispan(60,120,1)
res@tmXBLabelFontHeightF                =       0.038

res@cnLineLabelsOn                      =       False
res@cnLevelSelectionMode                =       "ExplicitLevels"
res@cnLevelSpacingF                     =       2.0
res@cnFillOn                            =       True           
res@cnInfoLabelOn                       =       False
res@cnLinesOn                           =       False

res@cnMissingValPerimOn     = True   
res@cnMissingValPerimColor  = "black"
res@cnMissingValFillPattern = 0      
res@cnMissingValFillColor   = "white"

res@lbLabelBarOn                        =       False

;;读取
f1        =       addfile("/data5/2019swh/data/geostrophic_deviation.nc","r")
deviation =    f1->deviation
u         =    f1->u_deviation
v         =    f1->v_deviation
u         =    abs(u)
v         =    abs(v)
copy_VarCoords(deviation, v)
copy_VarCoords(deviation, u)

deviation  =  where(abs(deviation).ge.100,deviation@_FillValue,deviation)

;;读取地形资料
f4              = addfile("/data5/2019swh/liuxl/ERAIN_Geopotential_0.5X0.5.nc","r")
dixing0         = short2flt(f4->z(0,:,:))
dixing          = dixing0/9.8  
copy_VarCoords(dixing0, dixing)
dixing          = dixing/1000 

wks1  =  gsn_open_wks("pdf","/data5/2019swh/paint/day/geostrophic_deviation_lon_level")
wks2  =  gsn_open_wks("pdf","/data5/2019swh/paint/day/geostrophic_u_deviation_lon_level")
wks3  =  gsn_open_wks("pdf","/data5/2019swh/paint/day/geostrophic_v_deviation_lon_level")
gsn_define_colormap(wks1,"temp_diff_18lev")
gsn_define_colormap(wks2,"temp_diff_18lev")
gsn_define_colormap(wks3,"temp_diff_18lev")
    
plot1 =  new(9,graphic)
plot2 =  new(9,graphic)
plot3 =  new(9,graphic)

char_day=(/"D0-30","D0-29","D0-28","D0-27","D0-26","D0-25","D0-24","D0-23","D0-22","D0-21","D0-20","D0-19","D0-18","D0-17","D0-16","D0-15","D0-14","D0-13","D0-12","D0-11","D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10","D0+11","D0+12","D0+13","D0+14","D0+15"/)


do yy = 22,32,2
    res@gsnLeftString     =    char_day(yy)
    res@cnLevels          =    fspan(0,6,7)
    res@cnFillColors      =    (/10,11,12,13,14,15,16,17/)
    plot1((yy-22)/2)  =  gsn_csm_pres_hgt(wks1,deviation(yy,0:22,{10},{60:120}),res)
    plot2((yy-22)/2)  =  gsn_csm_pres_hgt(wks2,u(yy,0:22,{10},{60:120}),res)
    plot3((yy-22)/2)  =  gsn_csm_pres_hgt(wks3,v(yy,0:22,{10},{60:120}),res)
end do

;;绘制地形设置
;绘制地形
res1                        =  True 
res1@gsnDraw                =  False
res1@gsnFrame               =  False
res1@tmXTOn                 =  False
res1@xyLineThicknesses      =  2.                  ; thicker line
res1@tiYAxisString          =  "Topography"   ; axis string
res1@tiYAxisFontColor       =  "black"
res1@xyLineColors           =  "black" 
res1@trYMaxF                =     2.4                 ; axis max
res1@trYMinF                =    0.                    ; axis min
res1@tmXBMode               =  "Explicit" 
res1@tmXBValues             =   ispan(60,120,15)
res1@tmXBLabels             =   ispan(60,120,15)
res1@tmXBMinorValues        =   ispan(60,120,1)
res1@trXMaxF                =  120
res1@trXMinF                =  60
res1@vpWidthF               =  0.6
res1@vpHeightF              =  0.3
res1@tmXBLabelFontHeightF   =  0.025
res1@tmYLLabelFontHeightF   =  0.025
res1@gsnRightString         =   "km"
res1@gsnLeftString          =  "60E-120E" 
res1@gsnRightStringFontHeightF = 0.025

time            = dixing&longitude
time!0          = "lon"
time&lon        = dixing&longitude

do ip = 6,8
    plot1(ip)  = gsn_csm_xy(wks1,time({60:120}),dixing({10},{60:120}),res1) 
    plot2(ip)  = gsn_csm_xy(wks2,time({60:120}),dixing({10},{60:120}),res1) 
    plot3(ip)  = gsn_csm_xy(wks3,time({60:120}),dixing({10},{60:120}),res1) 
end do
    
pnlres = True
pnlres@gsnPanelMainString = "geostrophic deviation"
pnlres@gsnPanelLabelBar  = True
pnlres@gsnPanelDebug     = True     ; To get information from panel
pnlres@pmLabelBarWidthF  = 0.55
pnlres@lbLabelFontHeightF = 0.012
gsn_panel(wks1,plot1,(/3,3/),pnlres)
pnlres@gsnPanelMainString = "geostrophic deviation (u component)"
gsn_panel(wks2,plot2,(/3,3/),pnlres)
pnlres@gsnPanelMainString = "geostrophic deviation (v component)"
gsn_panel(wks3,plot3,(/3,3/),pnlres)


end













