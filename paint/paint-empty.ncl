;2021/3/8
;此代码绘制一张空地图
begin

wks  = gsn_open_wks("pdf","/picture/paint/maponly")

res                             = True
res@mpFillOn                    = False        ; turn off gray fill
res@mpOutlineBoundarySets       = "National"   ; turn on country boundaries
res@mpGeophysicalLineColor      = "black"       ; color of cont. outlines
res@mpGeophysicalLineThicknessF = 1.5          ; thickness of outlines
res@mpMaxLatF                   = 30           ; choose subregion           
res@mpMinLatF                   = -30
res@mpMaxLonF                   = 150
res@mpMinLonF                   = 30
plot = gsn_csm_map(wks,res)                 ; draw map

end