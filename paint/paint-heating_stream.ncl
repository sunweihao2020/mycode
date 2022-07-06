;2020/12/3
;使用资料：合成分析热源 垂直流场
;本代码绘制纬向平均的热源、垂直流场合成图
begin 
f = addfile("/data5/2019swh/data/composite3.nc","r")
v = f->vwind
omega = f->OMEGA
omega = omega*(-100)
ff = addfile("/data5/2019swh/data/composite_Q1.nc","r")
q1 = ff->all_heating
;q1_a = dim_avg_n(q1(:,:,:,480:496), 3)
;v1_a = dim_avg_n(v(:,:,:,480:496), 3)
;o1_a = dim_avg_n(omega(:,:,:,480:496), 3)
q1_a = dim_avg_n(q1(:,:,:,400:416), 3)
v1_a = dim_avg_n(v(:,:,:,400:416), 3)
o1_a = dim_avg_n(omega(:,:,:,400:416), 3)
q1_a!0 = "time"
q1_a!1 = "level"
q1_a!2 = "lat"
q1_a&time = v&time
q1_a&level = v&level
q1_a&lat  =  v&lat
copy_VarCoords(q1_a, v1_a)
copy_VarCoords(q1_a, o1_a)
q1_a = q1_a*10
char_day=(/"D0-15","D0-14","D0-13","D0-12","D0-11","D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10","D0+11","D0+12","D0+13","D0+14","D0+15"/)

do day = 15,45
    
    wks = gsn_open_wks("pdf", "/data5/2019swh/paint/day/vertival_heating_"+day)
    gsn_define_colormap(wks,"MPL_OrRd")
    res   = True
    res@gsnDraw     = False                                ; plot mods desired
    res@gsnFrame     =  False
    res@tiMainString    =  "heating (70-80E)"
    res@gsnLeftString   =  char_day(day-15)
    res@gsnContourZeroLineThicknessF = 1
    res@gsnContourNegLineDashPattern = 1
    ;res@cnLevelSpacingF       =0.1
    ;res@gsnRightString        =  "10~S~-6~N~"
    res@cnFillOn        = True
    res@cnLevelSelectionMode       = "ExplicitLevels" 
    res@cnLevels             = fspan(-5,5,11)

    res@cnFillColors         = (/0,4,17,25,33,40,50,60,81,99,120,129/) ;
    res@gsnRightString        = ""
    res@cnMissingValPerimOn     = True            ; turn on the missing value perimeter
    res@cnMissingValPerimColor  = "black"           ; outline the perimeter red
    res@cnMissingValFillPattern = 0               ; choose fill pattern 0 (solid fill) 
    res@cnMissingValFillColor   = "black"          ; color fill missing areas blue

    plot = gsn_csm_pres_hgt(wks,q1_a(day,0:24,{-10:40}) , res)
    polyres                   = True
    polyres@gsLineColor       = "black"
    polyres@gsLineThicknessF  = 5
    polyres@gsLineDashPattern = 2
    dum = gsn_add_polyline(wks, plot, (/0,0/), (/1000,100/), polyres)

    draw(plot) ;delete(dum)
    frame(wks)
end do
end