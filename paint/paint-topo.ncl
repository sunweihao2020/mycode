;2021/8/17
;绘制更改后的地形
begin
f1 = addfile("/data5/2019swh/data/topo_1m_all.nc","r")
f2 = addfile("/data5/2019swh/data/topo_1m_india.nc","r")
f3 = addfile("/data5/2019swh/data/topo_1m_indo.nc","r")
f4 = addfile("/data5/2019swh/data/topo_1m_sealand.nc","r")
f0 = addfile("/data5/2019swh/data/fv_0.9x1.25_nc3000_Nsw042_Nrs008_Co060_Fi001_ZR_sgh30_24km_GRNL_c170103.nc","r")

phis1 = f1->PHIS
phis2 = f2->PHIS
phis3 = f3->PHIS
phis4 = f4->PHIS
phis0 = f0->PHIS

res = True
res@mpMinLatF            = -60      ; range to zoom in on
res@mpMaxLatF            =  60.
res@mpMinLonF            =  30.
res@mpMaxLonF            = 180.
res@cnFillOn             = True
res@cnLinesOn            = False
res@cnFillPalette        = "cmocean_amp"
res@cnLevelSpacingF      = 500
res@cnLineLabelsOn       = False
res@lbLabelBarOn         = False
wks1 = gsn_open_wks("pdf","/data5/2019swh/paint/day/topo_all")
wks2 = gsn_open_wks("pdf","/data5/2019swh/paint/day/topo_india")
wks3 = gsn_open_wks("pdf","/data5/2019swh/paint/day/topo_indo")
wks4 = gsn_open_wks("pdf","/data5/2019swh/paint/day/topo_sealand")
wks5 = gsn_open_wks("pdf","/data5/2019swh/paint/day/topo_complete")
plot1 = gsn_csm_contour_map(wks1,phis1,res)
plot2 = gsn_csm_contour_map(wks2,phis2,res)
plot3 = gsn_csm_contour_map(wks3,phis3,res)
plot4 = gsn_csm_contour_map(wks4,phis4,res)
plot5 = gsn_csm_contour_map(wks5,phis0,res)
end