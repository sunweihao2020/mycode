;2021/11/30
;本代码绘制等theta面叠加垂直运动的流线图
begin
f  =  addfile("/home/sun/data/for_lunwen_fig2.nc","r")

u  =  f->uwind
v  =  f->vwind
omega  =  f->omega
theta  =  f->theta

;处理nan
u@_FillValue  =  9999
if (any(isnan_ieee(u))) then
    replace_ieeenan (u, u@_FillValue, 0)
    replace_ieeenan (v, u@_FillValue, 0)
    replace_ieeenan (omega, u@_FillValue, 0)
    replace_ieeenan (theta, u@_FillValue, 0)
end if

; 画图
wks  =  gsn_open_wks("pdf","/home/sun/paint/lunwen/fig2_vertical_lon_potential_tem_motion")

res   = True
res@gsnDraw     = False                                
res@gsnFrame     =  False
res@cnLevelSelectionMode = "ExplicitLevels" 
res@cnLevels             =  ispan(296, 352, 2)
res@cnFillOn        = True
res@cnLineLabelsOn  = True
res@cnLineLabelBackgroundColor = -1
res@cnInfoLabelOn         = False
res@gsnStringFont         = 2
res@cnLineLabelDensityF   = 1
;res@cnFillPalette         = "cmocean_amp"
res@cnLineLabelFontThicknessF = 1
res@cnLineLabelFont       = 2.5
res@tmYLLabelFontHeightF      = 0.024
res@tmXBLabelFontHeightF      = 0.024
res@gsnRightString        = "K"
res@cnMissingValPerimOn     = True    
res@cnMissingValPerimColor  = "black" 
res@cnMissingValFillPattern = 0       
res@cnMissingValFillColor   = "gray"  

res@vcRefMagnitudeF = 5                ; define vector ref mag
res@vcRefLengthF    = 0.021              ; define length of vec ref
;res@vcGlyphStyle    = "CurlyVector"      ; turn on curly vectors
res@vcMinDistanceF  = 0.01               ; thin out vectors
res@vcMapDirection  = False          

plot1 = gsn_csm_pres_hgt_vector(wks,theta({1000:150},{50:}),u({1000:150},{50:}),omega({1000:150},{50:}),res )  

draw(plot1)
frame(wks)
end
