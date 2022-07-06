;2021/12/20
;merra2合成分析资料
;沿10-15N做剖面看经向风分量
;层次：30-120E 地面到高层
begin
path = "/home/sun/qomo-data/"
f = addfile(path+"composite3.nc","r")
v = f->vwind
char_day=(/"D0-15","D0-14","D0-13","D0-12","D0-11","D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10","D0+11","D0+12","D0+13","D0+14","D0+15"/)

path2 =  "/home/sun/paint/lunwen/version1.0/"
do day = 15,35
    wks = gsn_open_wks("pdf", path2+"/lunwen_version1.0_fig6_along10N_V_"+day)
    res                      = True                  ; plot mods desired
    res@tiMainString         = "vwind(10N)"        ; title
    res@cnLineLabelsOn       = False
    res@gsnContourZeroLineThicknessF = 5 	          ; doubles thickness of zero contour
    res@gsnContourNegLineDashPattern = 1 		  ; sets negative contours to dash pattern 1
    res@cnLevelSelectionMode = "ManualLevels"        ; manual contour levels
    res@cnLevelSpacingF      = 2.0                   ; contour interval
    res@cnMinLevelValF       = -50.                  ; min level
    res@cnMaxLevelValF       =  50.                  ; max level
    res@cnLineLabelsOn       = True                  ; turn on line labels
    res@cnFillOn             = True                  ; turn on color fill
    res@cnFillPalette        = "BlWhRe"              ; set color map
    res@gsnLeftString        = char_day(day-15)
    res@gsnRightString       = "m s-1"
    res@tmXBMode             = "Explicit"
    res@tmXBValues           = ispan(30,120,15)
    res@tmXBLabels           = ispan(30,120,15)
    res@tmXBMinorValues      = ispan(30,120,1)
    res@tmXBLabelFontHeightF = 0.038
    res@cnMissingValPerimOn     = True            ; turn on the missing value perim
    res@cnMissingValPerimColor  = "black"           ; outline the perimeter red
    res@cnMissingValFillPattern = 0               ; choose fill pattern 0 (solid fi
    res@cnMissingValFillColor   = "white"          ; color fill missing areas blue
    plot = gsn_csm_pres_hgt(wks,v(day,0:22,{10},{30:120}),res)
end do
end


