;2021/8/16
;检查cesm输出
begin
f = addfile("/home/sun/10m_all.cam.h1.1979-04-27-00000.nc","r")
t = f->T
res                            = True                ; plot mods desired
res@mpFillOn                   = True               ; turn off gray map
res@cnFillOn              = True
res@cnLinesOn                  = False
res@cnLevelSpacingF       = 4    ; contour spacing
  res@cnFillPalette         = "BlAqGrYeOrRe"
res@cnInfoLabelOn              = False               ; turn off info label
wks = gsn_open_wks("pdf","/home/sun/t")

plot = gsn_csm_contour_map(wks, t(0,30,:,:), res)
end