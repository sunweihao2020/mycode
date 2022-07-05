;这里画925、850、700、500、100的 在lev中分别对应3、7、12、16、24
;这波啊，这波计算一下vorticity
begin
a = addfile("/data5/2019swh/data/mean_pentad_multilayer_0924.nc","r")
u = a->uwind
v = a->vwind
lon = a->lon
lat = a->lat
lev = a->level

levs = (/3,7,12,16,24/)
vorticity = new((/13,5,361,576/),double)
vorticity!2 = "lat"
vorticity!3 = "lon"
vorticity&lat = lat
vorticity&lon = lon
char_pen=(/"p22","p23","p24","p25","p26","p27","p28","p29","p30","p31","p32","p33","p34"/)
ll = (/"925hPa","850hPa","700hPa","500hPa","100hPa"/)

do ipen=1,13
    do level =0,4
        vorticity(ipen-1,level,:,:) = uv2vr_cfd(u(ipen-1,levs(level),:,:), v(ipen-1,levs(level),:,:), lat, lon, 2)
        wks = gsn_open_wks("png", "/data5/2019swh/paint/pentad/absolute_vorticity_"+lev(levs(level))+"_"+ipen)
        do lat1=0,360,1
            vorticity(ipen-1,level,lat1,:) = vorticity(ipen-1,level,lat1,:) + coriolis_param(lat(lat1))
        end do
        vorticity = vorticity*1E+5
        res     =   True
        res@gsnDraw               = False
        res@gsnFrame              = False
        res@mpMinLatF            = -30 
        res@mpMaxLatF            =  60.
        res@mpMinLonF            =  30.
        res@mpMaxLonF            = 150.
        res@gsnLeftString         = char_pen(ipen-1) 
        res@gsnRightString        = "10~S~-5~N~"+" s~S~-1~N~"
        res@tiMainString          = ll(level)+" absolute vorticity"
        res@gsnContourZeroLineThicknessF = 7.
        res@cnLevelSelectionMode  =  "ExplicitLevels"
        res@gsnContourNegLineDashPattern = 1 
        res@cnFillOn        = True
        res@cnLineLabelsOn  = False
        res@cnLineLabelInterval = 3
        res@cnLineLabelBackgroundColor = -1
        res@cnFillPalette         = "BlAqGrYeOrRe"
        res@cnMissingValPerimOn     = True            ; turn on the missing value perim
        res@cnMissingValPerimColor  = "gray"           ; outline the perimeter red
        res@cnMissingValFillPattern = 0               ; choose fill pattern 0 (solid fi
        res@cnMissingValFillColor   = "gray"          ; color fill missing areas blue
        plot  = gsn_csm_contour_map(wks, vorticity(ipen-1,level,:,:), res)

        polyres                   = True
        polyres@gsLineColor       = "black"
        polyres@gsLineThicknessF  = 5
        polyres@gsLineDashPattern = 2
        dum = gsn_add_polyline(wks, plot, (/30,150/), (/0,0/), polyres)

        draw(plot)
        frame(wks)

    end do
end do
end