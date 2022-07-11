;2021/8/2
;绘制查看地形数据
begin
f = addfile("/home/sun/inputdata/topo_cancel_seeland.nc","r")
phis = f->PHIS
frac = f->LANDFRAC

;printMinMax(frac, False)
;绘制地形看看
res                       = True
res@cnFillOn              = True     ; turn on color fill
res@cnFillPalette         = "cmocean_amp"
;res@cnLineLabelsOn        = False
;res@mpMinLatF            = -10      ; range to zoom in on
;res@mpMaxLatF            =  30.
;res@mpMinLonF            =  30.
;res@mpMaxLonF            = 120.
res@lbLabelBarOn           = True
res@cnLinesOn             = True
;res@gsnRightString        = "units:degC"
;res@gsnStringFont         = 3
;res@tmYLLabelFontHeightF      = 0.05
;res@tmXBLabelFontHeightF      = 0.05


wks1 = gsn_open_wks("pdf","/home/sun/picture/topo3")
plot1 = gsn_csm_contour_map(wks1,phis, res)

end