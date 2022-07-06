;2021/4/18
;本代码计算爆发前一个月的Q、流场的平均，并绘制
begin
f1    = addfile("/data5/2019swh/data/composite-Q1-erain.nc","r")
f2    = addfile("/data5/2019swh/data/composite-erain.nc", "r")
f3    = addfile("/data5/2019swh/data/composite_OISST.nc", "r")
f4    = addfile("/data5/2019swh/data/composite-merra2-single.nc","r")
f5    = addfile("/data5/2019swh/data/land_and_ocean.nc","r")

q     = f1->Q1(0:29,:,:,:)
u     = f2->u(0:29,:,:,:)
v     = f2->v(0:29,:,:,:)
sst   = f3->SST(0:29,:,:)
t2m   = f4->T2M(0:29,::-1,:)
lsm   = short2flt(f5->lsm(0,:,:))

qa    = dim_avg_n_Wrap(q, 0)
ua    = dim_avg_n_Wrap(u, 0)
va    = dim_avg_n_Wrap(v, 0)
ssta  = dim_avg_n_Wrap(sst, 0)
t2ma  = dim_avg_n_Wrap(t2m, 0)
printVarSummary(ssta)
printVarSummary(t2ma)
printVarSummary(lsm)
;;print(t2ma&lat)
;print(ssta&lon)

t2ma   = lonFlip(t2ma)
printVarSummary(t2ma)
;exit

plot1     = new(2,graphic)
dum1      = new(2,graphic)
wks1      = gsn_open_wks("pdf","/data5/2019swh/paint/day/liuxl_average_stream_field_low")

plot2     = new(4,graphic)
dum2      = new(2,graphic)
;wks2 = gsn_open_wks("pdf","/data5/2019swh/paint/day/average_stream_field_high")

t2ma_land = t2ma  
t2ma_land = t2ma - 273.15
;t2ma_land = mask(t2ma,(lsm .gt. 0.1),1)

printVarSummary(t2ma_land)
printMinMax(t2ma_land, False)
t2ma_land = where(lsm.lt.0.5, -999, t2ma_land)  ;   海上的数值设置为0
printMinMax(t2ma_land, False)

print(t2ma_land({10:25},{70:88}))
printMinMax(t2ma_land({10:25},{70:88}), False)
printMinMax(ssta({-10:10},{55:60}), False)

exit
;--------------------------------------------

;--------------------------------------------

res                             = True
res@gsnDraw                     = False
res@gsnFrame                    = False
tres                            = res

res@mpMinLatF                   = -20      ; range to zoom in on
res@mpMaxLatF                   =  30.
res@mpMinLonF                   =  30.
res@mpMaxLonF                   = 120.


res@cnLevelSelectionMode        = "ExplicitLevels" 
res@cnLevels                    = fspan(18,36,21)
res@cnFillOn                    = True     ; turn on color fill
res@cnFillPalette               = "MPL_OrRd"
res@cnLineLabelsOn              = False
res@cnInfoLabelOn               = False

res@gsnRightString              = "degC"

res@lbLabelBarOn                = True
res@lbOrientation               = "horizontal"

res@tmYLLabelFontHeightF        = 0.024
res@tmXBLabelFontHeightF        = 0.024
res@pmLabelBarHeightF           = 0.06
res@pmLabelBarWidthF            = 0.7
res@pmLabelBarOrthogonalPosF    = 0.17

res@gsnRightString              = "SSTA + Ta_2m"
plot1(0)                        = gsn_csm_contour_map(wks1,ssta,res)
res@gsnRightString              = " "

;;------------------------------------------------------
;;------------------------------------------------------
cmap                            = read_colormap_file("MPL_OrRd")
cmap(0:1,3)                     = 0.0    ; Make first two blue colors fully transparent

tres@cnFillPalette              = cmap
tres@cnLevelSelectionMode       = "ExplicitLevels" 
tres@cnLevels                   = fspan(18,36,21)
tres@cnFillOn                   = True  
tres@cnLinesOn                  = False
tres@gsnRightString             = "  "
tres@lbLabelBarOn               = True
tres@lbOrientation              = "vertical"
;plot_s                          = gsn_csm_contour_map(wks1,t2ma_land,tres)
plot_s                          = gsn_csm_contour(wks1,t2ma_land,tres)


polyres                         = True
polyres@gsLineColor             = "black"
polyres@gsLineThicknessF        = 2
polyres@gsLineDashPattern       = 2

dum1(0) = gsn_add_polyline(wks1, plot1(0), (/30,120/), (/0,0/), polyres)

overlay(plot1(0), plot_s)
draw(plot1(0))

;draw(plot_s)

end