;2021/6/22
;本代码计算并绘制地转偏差
;该地转偏差是基于实际风和热成风叠加在925hPa的地转风所得到的
begin
f1  =  addfile("/data5/2019swh/data/composite3.nc","r")
u0  =  f1->uwind
v0  =  f1->vwind

f2  =  addfile("/data5/2019swh/data/thermal_wind_925hpa.nc","r")
ut  =  f2->thermal_u
vt  =  f2->thermal_v

f3  =  addfile("/data5/2019swh/data/ugvg.nc","r")
ug  =  f3->ug
vg  =  f3->vg

u925  =  ug(:,{925},:,:)
v925  =  vg(:,{925},:,:)

ugt =  ut
vgt =  vt

do ll = 0,37
    ugt(:,ll,:,:)  =  ut(:,ll,:,:) + u925
    vgt(:,ll,:,:)  =  vt(:,ll,:,:) + v925
end do

;把热成风的那部分实际风截取出来
u1  =  u0(:,4:,:,:)
v1  =  v0(:,4:,:,:)

u_deviation  =  u1 - ugt
v_deviation  =  v1 - vgt

copy_VarCoords(ugt, u_deviation)
copy_VarCoords(vgt, v_deviation)

char_day=(/"D0-30","D0-29","D0-28","D0-27","D0-26","D0-25","D0-24","D0-23","D0-22","D0-21","D0-20","D0-19","D0-18","D0-17","D0-16","D0-15","D0-14","D0-13","D0-12","D0-11","D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10","D0+11","D0+12","D0+13","D0+14","D0+15"/)
level = (/900,850,700,500,300,200/)
levels = (/"900hPa","850hPa","700hPa","500hPa","300hPa","200hPa"/)

;计算地转偏差的模
deviation  =  sqrt(u_deviation^2+v_deviation^2)
copy_VarCoords(u_deviation, deviation)

;关于地转偏差的设置
res1                       = True
res1@cnFillOn              = True   ; turn on color fill
res1@gsnDraw               = False
res1@gsnFrame              = False
res1@gsnAddCyclic          = False
res1@gsnStringFont         = 2
res1@gsnRightString        = "m s-1" 

res1@mpMinLatF            =  5 
res1@mpMaxLatF            =  30.
res1@mpMinLonF            =  60.
res1@mpMaxLonF            =  120.


res1@cnInfoLabelOn         = False 
res1@cnLinesOn             = False 
res1@cnLevelSelectionMode       = "ExplicitLevels" 
res1@cnLevels              = fspan(-10,10,11)

res1@vpWidthF              = 0.6
res1@vpHeightF             = 0.55



;绘制地转偏差矢量的设置
vcres                         = True
vcres@gsnDraw                 = False             ; do not draw the plot      
vcres@gsnFrame                = False            ; so we can draw time stamp
vcres@vpWidthF              = 0.6
vcres@vpHeightF             = 0.55
vcres@gsnAddCyclic            =  False
vcres@vcRefMagnitudeF         = 5            ; define vector ref mag
vcres@vcRefLengthF            = 0.045            ; define length of vec ref
vcres@vcGlyphStyle            = "LineArrow"    ; turn on curly vectors
vcres@vcMinDistanceF          = 0.017
vcres@vcRefAnnoOrthogonalPosF = -1.0
vcres@gsnRightString          = ""    
vcres@vcMinDistanceF          = 0.02
vcres@vcRefLengthF               = 0.03
vcres@gsnLeftString           = ""
vcres@vcLineArrowThicknessF   = 1.5


do yy = 22,33
    wks  =  gsn_open_wks("pdf","/data5/2019swh/paint/day/geostrophic_deviation_abs_"+char_day(yy))
    gsn_define_colormap(wks,"temp_diff_18lev")
    plot1 =  new(6,graphic)
    plot2 =  new(6,graphic)
    do ll = 0,5
        res1@gsnLeftString   =      levels(ll)
        res1@gsnRightString  =      char_day(yy)
        plot1(ll) = gsn_csm_contour_map(wks, deviation(yy,{level(ll)},:,:), res1)
        ;plot2(ll) = gsn_csm_vector(wks, u_deviation(yy,{level(ll)},:,:), v_deviation(yy,{level(ll)},:,:), vcres)
        ;overlay(plot1(ll), plot2(ll))
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