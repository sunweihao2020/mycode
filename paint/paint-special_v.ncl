;2020/11/10 2020/11/13
;所用资料：merra2季风爆发合成分析
;要素 : 计算的强迫惯性风特解的梯度
;level : 925 850
begin
f = addfile("/data5/2019swh/data/special_v_gradient_low.nc", "r")
v1_g = f->v1wind
char_day=(/"D0-15","D0-14","D0-13","D0-12","D0-11","D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10","D0+11","D0+12","D0+13","D0+14","D0+15"/)
v1_g  = where(abs(v1_g) .ge. 10e-4, v1_g@_FillValue, v1_g)
v1_g = v1_g*1E+7*(-1)  ;计算的时候忘记前面的负号了
v1_g  = where(v1_g .le. -6 .and. v1_g .ge. 0, v1_g@_FillValue, v1_g)
s = (/2,7,9,13,16,22,28,32,35,41,42,0/)

do day = 15,45
    wks = gsn_open_wks("pdf","/data5/2019swh/paint/day/specail_vgradient700_"+day)
    gsn_define_colormap(wks,"matlab_hsv")
    res = True
    res@cnFillOn              = True 
    res@cnLinesOn             = False  
    ;res@gsnDraw               = False
    ;res@gsnFrame              = False
    res@cnLevelSelectionMode  =  "ExplicitLevels"
    res@cnLevels              = fspan(-10,0,11)
    res@cnFillColors         = s
    ;res@cnLineColor           =  "red"
    res@gsnLeftString         = char_day(day-15)
    res@cnInfoLabelOn         = False
    res@cnLineThicknessF      = 3
    res@mpFillOn              = False
    ;res@mpFillColor           =  "white"
    res@tiMainString          = "700hPa"
    res@cnLineLabelsOn        = False
    res@cnMissingValPerimOn     = True            ; turn on the missing value perim
    res@cnMissingValPerimColor  = "white"           ; outline the perimeter red
    res@cnMissingValFillPattern = 0               ; choose fill pattern 0 (solid fi
    res@cnMissingValFillColor   = "white"          ; color fill missing areas blue
    res@gsnRightString        = ""
    res@mpMinLatF            =  0 
    res@mpMaxLatF            =  30.
    res@mpMinLonF            =  70.
    res@mpMaxLonF            =  105.
    res@gsnAddCyclic         = False

    plot = gsn_csm_contour_map(wks, v1_g(day,12,{0:20},:), res)

end do

end