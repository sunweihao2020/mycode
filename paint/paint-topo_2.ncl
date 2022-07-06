;2021/9/6
;绘制原始地形
begin
f0 = addfile("/data5/2019swh/data/topo_200m_plateau.nc","r")
phis0 = f0->PHIS
phis0 = phis0/9.8

res = True
res@mpMinLatF            = -15      ; range to zoom in on
res@mpMaxLatF            =  70.
res@mpMinLonF            =  30.
res@mpMaxLonF            = 120.
res@cnFillOn             = True
res@cnLinesOn            = False
res@cnFillPalette        = "cmocean_amp"
res@cnLevelSelectionMode       = "ExplicitLevels" 
res@cnLevels             = ispan(0,7000,200)
res@cnLineLabelsOn       = False
res@lbLabelBarOn         = True


wks5 = gsn_open_wks("pdf","/data5/2019swh/paint/day/topo_200m")
plot5 = gsn_csm_contour_map(wks5,phis0,res)
end