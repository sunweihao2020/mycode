;2021/5/31
;本代码利用计算的基于925hpa的热成风资料
;叠加在925hPa地转风上来试着模拟各层的环流
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

;第一层对应的900hpa
copy_VarCoords(ut, ugt)
copy_VarCoords(vt, vgt)
copy_VarCoords(u, ug)
copy_VarCoords(v, vg)

level = (/900,850,700,500/)
levels = (/"900hPa","850hPa","700hPa","500hPa"/)
char_day=(/"D0-30","D0-29","D0-28","D0-27","D0-26","D0-25","D0-24","D0-23","D0-22","D0-21","D0-20","D0-19","D0-18","D0-17","D0-16","D0-15","D0-14","D0-13","D0-12","D0-11","D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10","D0+11","D0+12","D0+13","D0+14","D0+15"/)


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
vcres@vcRefAnnoString2            = "8 m/s"
vcres@vcRefMagnitudeF             =  8               ; define vector ref mag
vcres@vcRefAnnoFontHeightF        = 0.017
vcres@vcRefAnnoPerimOn            = False

vcres@vcMinDistanceF              = 0.03
vcres@vcGlyphStyle                = "CurlyVector"
vcres@vcLineArrowThicknessF       = 1.8
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
vcres1@vcLineArrowColor           =  "red"
vcres1@gsnLeftString              =  " "
vcres1@gsnRightString             =  " "

vcres1@vcRefAnnoOn                =  True
vcres1@vcRefAnnoFontColor         = "red"

vcres1@vcRefAnnoOrthogonalPosF    = -0.995 
vcres1@vcRefAnnoParallelPosF      = 0.888
;;------------------------------------------

vcres@mpMinLatF                   =  5 
vcres@mpMaxLatF                   =  30.
vcres@mpMinLonF                   = 75.
vcres@mpMaxLonF                   =  110.
vcres@gsnAddCyclic                =  False

;vcres1@vcRefAnnoString1On         =  True
;vcres@vcRefAnnoOrthogonalPosF     = -1.0  
;
;vcres1@vcRefAnnoString2On          = False
;vcres1@vcRefAnnoSide              = "Left"

;;------------------------------------------



do yy = 22,  33
    wks1  =  gsn_open_wks("pdf","/data5/2019swh/paint/day/geostrophic_wind_"+char_day(yy))
    wks2  =  gsn_open_wks("pdf","/data5/2019swh/paint/day/geostrophic_wind_thermal_"+char_day(yy))
    wks3  =  gsn_open_wks("pdf","/data5/2019swh/paint/day/geostrophic_wind&thermal_"+char_day(yy))
    plot1 =  new(4,graphic)
    plot2 =  new(4,graphic)
    plot3 =  new(4,graphic)
    plot4 =  new(4,graphic)
    do ll = 0,3
        vcres@gsnLeftString   =      levels(ll)
        vcres@gsnRightString  =      char_day(yy)
        plot1(ll) = gsn_csm_vector_map(wks1,ug(yy,{level(ll)},:,:),vg(yy,{level(ll)},:,:),vcres)
        plot2(ll) = gsn_csm_vector_map(wks2,ugt(yy,{level(ll)},:,:),vgt(yy,{level(ll)},:,:),vcres)
        plot3(ll) = gsn_csm_vector_map(wks3,ug(yy,{level(ll)},:,:),vg(yy,{level(ll)},:,:),vcres)
        plot4(ll) = gsn_csm_vector(wks3,ugt(yy,{level(ll)},:,:),vgt(yy,{level(ll)},:,:),vcres1)
        overlay(plot3(ll), plot4(ll))

    end do
pnlres                    = True
pnlres@gsnPanelMainString = "geostrophic wind"
pnlres@gsnPanelDebug      = True     ; To get information from panel
pnlres@lbLabelFontHeightF = 0.012
gsn_panel(wks1,plot1,(/2,2/),pnlres)
pnlres@gsnPanelMainString = "geostrophic wind simulated by thermal wind"
gsn_panel(wks2,plot2,(/2,2/),pnlres)
pnlres@gsnPanelMainString = " "
gsn_panel(wks3,plot3,(/2,2/),pnlres)
delete(wks1)
delete(wks2)
delete(wks3)
end do

end