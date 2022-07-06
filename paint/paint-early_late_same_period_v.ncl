;2021/9/9
;本代码根据早年晚年的同期3、4月份风场，绘制v的偏差图
begin
f  =  addfile("/data5/2019swh/data/same_period_wind_earlylate.nc","r")
v3ewind  =  f->v3ewind
v3lwind  =  f->v3lwind
v4ewind  =  f->v4ewind
v4lwind  =  f->v4lwind
u3ewind  =  f->u3ewind
u3lwind  =  f->u3lwind
u4ewind  =  f->u4ewind
u4lwind  =  f->u4lwind

v3ewind@_FillValue  =  999
v4ewind@_FillValue  =  999
u3ewind@_FillValue  =  999
u4ewind@_FillValue  =  999
v3lwind@_FillValue  =  999
v4lwind@_FillValue  =  999
u3lwind@_FillValue  =  999
u4lwind@_FillValue  =  999
if (any(isnan_ieee(v3ewind))) then
  replace_ieeenan(v3ewind, v3ewind@_FillValue, 0)
  replace_ieeenan(v4ewind, v4ewind@_FillValue, 0)
  replace_ieeenan(u3ewind, u3ewind@_FillValue, 0)
  replace_ieeenan(u4ewind, u4ewind@_FillValue, 0)
  replace_ieeenan(v3lwind, v3lwind@_FillValue, 0)
  replace_ieeenan(v4lwind, v4lwind@_FillValue, 0)
  replace_ieeenan(u3lwind, u3lwind@_FillValue, 0)
  replace_ieeenan(u4lwind, u4lwind@_FillValue, 0)
end if

v3_diff  =  v3ewind
v4_diff  =  v4ewind
u3_diff  =  v3ewind
u4_diff  =  v4ewind

v3_diff  =  v3lwind - v3ewind
v4_diff  =  v4lwind - v4ewind
u3_diff  =  u3lwind - u3ewind
u4_diff  =  u4lwind - u4ewind

vcres = True
vcres@gsnDraw                   = False            ; do not draw the plot      
vcres@gsnFrame                  = False           ; so we can draw time stamp
vcres@vcRefAnnoOrthogonalPosF   = -1.35             ; move ref vector up
vcres@vpWidthF                  = 0.6
vcres@vpHeightF                 = 0.55
;vcres@gsnAddCyclic              =  False
vcres@vcRefMagnitudeF           = 5            ; define vector ref mag
vcres@vcRefLengthF              = 0.045            ; define length of vec ref
vcres@vcGlyphStyle              = "FillArrow"    ; turn on curly vectors
vcres@vcMinDistanceF            = 0.017
vcres@vcRefAnnoOrthogonalPosF   = -1.0
vcres@gsnRightString            = ""    
vcres@vcMinDistanceF            = 0.02
vcres@gsnLeftString             = ""
vcres@mpMinLatF                 =  -10 
vcres@mpMaxLatF                 =  30.
vcres@mpMinLonF                 =  30.
vcres@mpMaxLonF                 =  120.


polyres                   = True
polyres@gsLineColor       = "black"
polyres@gsLineThicknessF  = 1
polyres@gsLineDashPattern = 2

wks1  =  gsn_open_wks("pdf","/data5/2019swh/paint/day/early_march_vdiff")
wks2  =  gsn_open_wks("pdf","/data5/2019swh/paint/day/early_april_vdiff")
plot1 =  gsn_csm_vector_map(wks1,u3_diff(3,:,:),v3_diff(3,:,:),vcres)
plot2 =  gsn_csm_vector_map(wks2,u4_diff(3,:,:),v4_diff(3,:,:),vcres)
dum1  =  gsn_add_polyline(wks1, plot1,(/30,120/), (/0,0/), polyres)
dum2  =  gsn_add_polyline(wks2, plot2,(/30,120/), (/0,0/), polyres)

draw(plot1)
draw(plot2)
frame(wks1)
frame(wks2)
end