;;;这波啊，这波是求个月平均各层温度场
begin
f = addfile("/data5/2019swh/data/mean_merra2_multilayer_0921.nc","r")
t = f->T
char_mon=(/"Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"/)
plevs   = (/3,6,22,24/)
plev    = (/"925hpa","850hpa","500hpa","100hpa"/)

do p=3,3
    do mon=0,11
    wks = gsn_open_wks("png","/data5/2019swh/paint/climatemean/temperature_"+plev(p)+"_"+(mon+1))
    res = True
    ;res@gsnDraw      =  False                   ; do not draw the plot
    ;res@gsnFrame     =  False
    res@cnLinesOn    = True
    res@mpCenterLonF               = 90
   ; res@mpMinLatF            = -30
   ; res@mpMaxLatF            = 60
   ; res@mpMinLonF            = 30
   ; res@mpMaxLonF            = 160
    res@gsnCenterString        = plev(p)+"  temperature field"
    res@gsnLeftString         = char_mon(mon)
    res@cnLineLabelsOn        = True
    res@gsnMaximize           = True     ; Make plot fit the frame
    res@cnFillOn              = True     ; turn on color fill
    res@cnLevelSelectionMode       = "ExplicitLevels" 
    res@cnLevels             = ispan(-90,-40,4) 
    res@cnInfoLabelOn              = False
    res@cnMinLevelValF             = 1000
    res@gsnRightString             = "units:degC"
    res@cnMissingValPerimOn     = True            ; turn on the missing value perimeter
    res@cnMissingValPerimColor  = "black"           ; outline the perimeter red
    res@cnMissingValFillPattern = 0               ; choose fill pattern 0 (solid fill) 
    res@cnMissingValFillColor   = "black"          ; color fill missing areas blue
    plot1 = gsn_csm_contour_map(wks,t(mon,plevs(p),:,:)-273.15,res)  
    end do
end do
end