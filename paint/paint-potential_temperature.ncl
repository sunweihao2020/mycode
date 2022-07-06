;2020/11/12
;merra2合成分析资料
;计算相当位温和位温
;多层次
begin
f = addfile("/data5/2019swh/data/composite_equivalent_tem.nc","r")
;ff = addfile("/data5/2019swh/data/composite3.nc","r")
;t   = ff->T

;pt1 = f->pt
pt = f->theate_e
;pt_a = dim_avg_n(pt1(:,:,:,400:416), 3)
;pt_a!0 = "time"
;pt_a!1 = "level"
;pt_a!2 = "lat"
;pt_a&time = pt1&time
;pt_a&level = pt1&level
;pt_a&lat  =  pt1&lat
char_day=(/"D0-15","D0-14","D0-13","D0-12","D0-11","D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10","D0+11","D0+12","D0+13","D0+14","D0+15"/)
lev = (/3,6,16,22/)
level = (/"925","850","500","200"/)
longitudes  = (/416,420,424,428,432,436,440,444,448,452/)
char_lon    = (/"80E","82.5E","85E","87.5E","90E","92.5E","95E","97.5E","100E","102.5E"/)
;=====================================平面图============================================
do z=0,3
    do day = 15,45
        wks = gsn_open_wks("png","/data5/2019swh/paint/day/"+level(z)+"pt2_field_"+day)
        res = True
        res@cnFillOn              = False 
        res@cnLinesOn             = True  
        ;res@gsnDraw               = False
        ;res@gsnFrame              = False
        ;res@cnLevelSelectionMode  =  "ExplicitLevels"
        res@cnLevelSpacingF       = 1
        res@cnSmoothingOn         = True
        res@cnSmoothingDistanceF  = 0.006
        res@cnInfoLabelOn         = False
        res@cnLineThicknessF      = 2
        res@cnLineLabelsOn        = True
        res@cnMissingValPerimOn     = True            ; turn on the missing value perim
        res@cnMissingValPerimColor  = "black"           ; outline the perimeter red
        res@cnMissingValFillPattern = 0               ; choose fill pattern 0 (solid fi
        res@cnMissingValFillColor   = "gray"          ; color fill missing areas blue
        res@gsnRightString        = ""
        res@mpMinLatF            = -10 
        res@mpMaxLatF            =  30.
        res@mpMinLonF            =  30.
        res@mpMaxLonF            =  120.

        res@gsnLeftString       = char_day(day-15)
        res@tiMainString        = "potential temperature"
        plot = gsn_csm_contour_map(wks, pt2(day,lev(z),:,:), res)
    end do
end do
end
;
;======================================垂直剖面图===============================
;这里先5度一平均
;do ll = 0,9
;    do day = 15,35
;        wks = gsn_open_wks("png","/data5/2019swh/paint/day/theate_vertical_field_"+char_lon(ll)+"_"+day)
;        res   = True
;        res@gsnDraw     = False                                
;        res@gsnFrame     =  False
;        res@tiMainString    =  "theate_e " + char_lon(ll)
;        res@gsnLeftString   =  char_day(day-15)
;        ;res@cnLevelSpacingF       = 2
;        ;res@gsnRightString        =  "10~S~-6~N~"
;        res@cnLevelSelectionMode = "ExplicitLevels" 
;        res@cnLevels             =  ispan(268, 352, 2)
;        res@cnFillColor         = (/0/)
;        res@cnFillOn        = False
;        res@cnLineLabelsOn  = True
;        res@cnLineLabelBackgroundColor = -1
;        res@gsnRightString        = ""
;        res@cnMissingValPerimOn     = True            ; turn on the missing value perimete
;        res@cnMissingValPerimColor  = "blue"           ; outline the perimeter red
;        res@cnMissingValFillScaleF  = 3
;        res@cnMissingValFillPattern = 0               ; choose fill pattern 0 (solid fill)
;        res@cnMissingValFillColor   = "gray"          ; color fill missing areas blue
;        plot = gsn_csm_pres_hgt(wks,pt2(day,0:22,{-10:40},longitudes(ll)) , res)
;        polyres                   = True
;        polyres@gsLineColor       = "black"
;        polyres@gsLineThicknessF  = 5
;        polyres@gsLineDashPattern = 2
;        dum = gsn_add_polyline(wks, plot, (/0,0/), (/1000,100/), polyres)
;        draw(plot) ;delete(dum)
;        frame(wks)
;    end do
;end do
;end