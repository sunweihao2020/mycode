;2020/11/14
;merra2季风爆发合成资料
;计算绝对角动量M 用于诊断对称不稳定
begin
f1 = addfile("/data5/2019swh/data/ugvg.nc", "r")
f2 = addfile("/data5/2019swh/data/potential_temperature.nc","r")
ug    = f1->ug
lat   = f1->lat
pt1 = f2->pt
f = coriolis_param(lat)
fy = f*lat
m = ug
do t = 0,60
    do lev = 0,41
        do lon = 0,575
            m(t,lev,:,lon) = fy-ug(t,lev,:,lon)
        end do
    end do
end do
ptm = dim_avg_n_Wrap(pt1(:,:,:,432:440), 3)
mm  = dim_avg_n_Wrap(m(:,:,:,432:440), 3)
char_day=(/"D0-15","D0-14","D0-13","D0-12","D0-11","D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10","D0+11","D0+12","D0+13","D0+14","D0+15"/)
longitudes  = (/416,420,424,428,432,436,440,444,448,452/)
char_lon    = (/"80E","82.5E","85E","87.5E","90E","92.5E","95E","97.5E","100E","102.5E"/)


do day = 15,35
    wks = gsn_open_wks("pdf","/data5/2019swh/paint/day/SI_field_"+day)
    res   = True
    res@gsnDraw     = False                                
    res@gsnFrame     =  False
    res@tiMainString    =  "PT & M(90-95E))"
    res@gsnLeftString   =  char_day(day-15)
    ;res@gsnRightString        =  "10~S~-6~N~"
    res@cnLevelSelectionMode = "ExplicitLevels" 
    res@cnLevels             =  ispan(268, 352, 4)
    res@cnFillOn        = False
    res@cnLineLabelsOn  = True
    res@cnLineColor            = "red"
    res@cnLineThicknessF       = 3
    res@cnInfoLabelOn         = False
    res@cnLineLabelBackgroundColor = -1
    res@gsnRightString        = ""
    res@cnMissingValPerimOn     = True            ; turn on the missing value perimete
    res@cnMissingValPerimColor  = "blue"           ; outline the perimeter red
    res@cnMissingValFillPattern = 0               ; choose fill pattern 0 (solid fill)
    res@cnMissingValFillColor   = "gray"          ; color fill missing areas blue
    plot = gsn_csm_pres_hgt(wks,ptm(day,0:16,{0:30}) , res)
    res@cnFillOn             = False
    res@cnLevelSelectionMode    = "AutomaticLevels"
    res@cnLineColor            = "black"
    res@cnMissingValPerimOn     = False
    plot2 = gsn_csm_pres_hgt(wks,mm(day,0:16,{5:30}), res)
    overlay(plot, plot2)
    draw(plot)
    frame(wks)
end do


end