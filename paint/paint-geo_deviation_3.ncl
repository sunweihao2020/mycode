;2021/6/23
;本代买绘制地转偏差标量与矢量图
;主要是与2作对比，之前绘制的总是有问题
;不知道为啥= =，但是2那个就是有问题
begin
f1  =  addfile("/data5/2019swh/data/thermal_wind_925hpa.nc", "r")
f2 = addfile("/data5/2019swh/data/composite3.nc","r")
u  =  f2->uwind
v  =  f2->vwind
h  =  f2->H

uv =  z2geouv(h, h&lat, h&lon, 1)

ug =  uv(0,:,:,:,:)
vg =  uv(1,:,:,:,:)

ut =  f1->thermal_u
vt =  f1->thermal_v

u0 =  ug(:,3,:,:)
v0 =  vg(:,3,:,:)

ugt  =  ut
vgt  =  vt
do ll = 0,37
    ugt(:,ll,:,:)  =  ut(:,ll,:,:) + u0
    vgt(:,ll,:,:)  =  vt(:,ll,:,:) + v0
end do

do ll = 0,37
    u(:,ll,:,:)    =  where(ismissing(u0),0,u(:,ll,:,:))
    v(:,ll,:,:)    =  where(ismissing(v0),0,v(:,ll,:,:))
end do

;第一层对应的900hpa
copy_VarCoords(ut, ugt)
copy_VarCoords(vt, vgt)
copy_VarCoords(u, ug)
copy_VarCoords(v, vg)

char_day=(/"D0-30","D0-29","D0-28","D0-27","D0-26","D0-25","D0-24","D0-23","D0-22","D0-21","D0-20","D0-19","D0-18","D0-17","D0-16","D0-15","D0-14","D0-13","D0-12","D0-11","D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10","D0+11","D0+12","D0+13","D0+14","D0+15"/)
level = (/900,850,700,500,300,200/)
levels = (/"900hPa","850hPa","700hPa","500hPa","300hPa","200hPa"/)

u1  =  u(:,4:,:,:)
v1  =  v(:,4:,:,:)

u_deviation  =  u1 - ugt
v_deviation  =  v1 - vgt

copy_VarCoords(ugt, u_deviation)
copy_VarCoords(vgt, v_deviation)

deviation  =  sqrt(u_deviation^2+v_deviation^2)
copy_VarCoords(u_deviation, deviation)

res1                       = True
res1@cnFillOn              = True   ; turn on color fill
res1@gsnDraw               = False
res1@gsnFrame              = False
res1@gsnAddCyclic          = False
res1@gsnStringFont         = 4
res1@gsnRightString        = "m s-1" 
res1@gsnStringFontHeightF  = 0.024

res1@lbLabelBarOn          = False

res1@mpMinLatF            =  5 
res1@mpMaxLatF            =  30.
res1@mpMinLonF            =  60.
res1@mpMaxLonF            =  120.

res1@tmYLLabelFontHeightF        = 0.020
res1@tmXBLabelFontHeightF        = 0.020


res1@cnInfoLabelOn         = False 
res1@cnLinesOn             = False 
res1@cnLineLabelsOn        = False
res1@cnLevelSelectionMode  = "ExplicitLevels" 
res1@cnLevels              = fspan(0,10,6)
res1@cnFillColors          = (/0,2,30,100,145,170,193,226/)

res1@vpWidthF              = 0.6
res1@vpHeightF             = 0.55



;绘制地转偏差矢量的设置
vcres                             = True
vcres@gsnDraw                     = False             ; do not draw the plot      
vcres@gsnFrame                    = False            ; so we can draw time stamp
vcres@vpWidthF                    = 0.6
vcres@vpHeightF                   = 0.55

vcres@vcRefAnnoOn                 = True
vcres@vcRefLengthF                = 0.04            ; define length of vec ref
vcres@vcRefAnnoOrthogonalPosF     = -0.995   
vcres@vcRefAnnoString1On          = False       
;vcres@vcRefAnnoString1            = "8 m/s"
vcres@vcRefAnnoString2On          = True 
vcres@vcRefAnnoString2            = "10 m/s"
vcres@vcRefMagnitudeF             =  10              ; define vector ref mag
vcres@vcRefAnnoFontHeightF        = 0.017
vcres@vcRefAnnoPerimOn            = False

vcres@vcMinDistanceF              = 0.03
vcres@vcGlyphStyle                = "CurlyVector"
vcres@vcLineArrowThicknessF       = 1.5
vcres@vcLineArrowHeadMaxSizeF     = 0.025
vcres@vcLineArrowHeadMinSizeF     = 0.004
vcres@vcMinFracLengthF            = 0.2
    ; turn on curly vectors
vcres@tmYLLabelFontHeightF        = 0.024
vcres@tmXBLabelFontHeightF        = 0.024
vcres@tmXTOn                      = False
vcres@tmYROn                      = False
;;----------------------------------------
vcres1                            =  vcres
vcres1@vcLineArrowColor           =  "black"
vcres1@gsnLeftString              =  " "
vcres1@gsnRightString             =  " "

vcres1@vcRefAnnoOn                =  True
vcres1@vcRefAnnoFontColor         = "black"

vcres1@vcRefAnnoOrthogonalPosF    = -0.995 
vcres1@vcRefAnnoParallelPosF      = 0.888

do yy = 22,33
    wks  =  gsn_open_wks("pdf","/data5/2019swh/paint/day/geostrophic_deviation_abs_"+char_day(yy))
    gsn_define_colormap(wks,"cmocean_amp")
    plot1 =  new(6,graphic)
    plot2 =  new(6,graphic)
    do ll = 0,5
        res1@gsnLeftString   =      levels(ll)
        res1@gsnRightString  =      char_day(yy)
        plot1(ll) = gsn_csm_contour_map(wks, deviation(yy,{level(ll)},:,:), res1)
        plot2(ll) = gsn_csm_vector(wks, u_deviation(yy,{level(ll)},:,:), v_deviation(yy,{level(ll)},:,:), vcres1)
        overlay(plot1(ll), plot2(ll))
    end do
    pnlres = True
    pnlres@gsnPanelMainString = "geostrophic deviation"
    pnlres@gsnPanelLabelBar  = True
    pnlres@gsnPanelDebug     = True     ; To get information from panel
    pnlres@pmLabelBarWidthF  = 0.55
    pnlres@lbLabelFontHeightF = 0.012
    gsn_panel(wks,plot1,(/2,3/),pnlres)
end do

end