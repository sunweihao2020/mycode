;2020/11/1
;所用资料：merra2季风爆发合成分析
;要素：位势高度，风场，散度场
;level : 925 850 500 200
begin
f = addfile("/data5/2019swh/data/composite3.nc","r")
ff = addfile("/data5/2019swh/data/div_vor.nc","r")
h = f->H
u = f->uwind
v = f->vwind
div = ff->div

char_day=(/"D0-15","D0-14","D0-13","D0-12","D0-11","D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10","D0+11","D0+12","D0+13","D0+14","D0+15"/)
lev = (/3,6,12,16,22,24/)
level = (/"925hPa","850hPa","700hPa","500hPa","200hPa","100hPa"/)

do z=0,5
    do day = 15,16
        wks = gsn_open_wks("png","/data5/2019swh/paint/day/"+level(z)+"height_field_"+day)
        res = True
        res@cnFillOn              = False 
        res@cnLinesOn             = True  
        ;res@gsnDraw               = False
        ;res@gsnFrame              = False
        res@cnLevelSelectionMode  =  "ExplicitLevels"
        res@cnLineColor           =  "red"
        res@cnInfoLabelOn         = False
        res@cnLevelSpacingF       = 4
        res@cnLineThicknessF      = 3
        res@cnLineLabelsOn        = True
        res@cnMissingValPerimOn     = True            ; turn on the missing value perim
        res@cnMissingValPerimColor  = "black"           ; outline the perimeter red
        res@cnMissingValFillPattern = 0               ; choose fill pattern 0 (solid fi
        res@cnMissingValFillColor   = "white"          ; color fill missing areas blue
        res@gsnRightString        = ""
        res@mpMinLatF            = -10 
        res@mpMaxLatF            =  30.
        res@mpMinLonF            =  30.
        res@mpMaxLonF            =  120.

        plot = gsn_csm_contour_map(wks, h(day,lev(z),:,:), res)
    end do
end do
end