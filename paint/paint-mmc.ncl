begin
a = addfile("/data5/2019swh/data/streamfunction.nc", "r")
aa = addfile("/data5/2019swh/data/mean_pentad_multilayer_0924.nc","r")
aaa = addfile("/data5/2019swh/data/mean_pentad_vwt_0926.nc","r") 
mpsi = a->MPSI
mp = new((/13,32,361/),double)
mp(:,0:30,:) = mpsi(:,:,:)
mp(:,31,:)   = mp@_FillValue
mp&lev(31)   = 100000
t = aaa->T


char_pen=(/"p22","p23","p24","p25","p26","p27","p28","p29","p30","p31","p32","p33","p34"/)

do ipen = 1,13
    wks = gsn_open_wks("png", "/data5/2019swh/paint/pentad/streamfunction_"+ipen)
    ;wks = gsn_open_wks("png", "/data5/2019swh/paint/pentad/test")
    res0  = True
    res0@gsnDraw      =  False                   ; do not draw the plot
    res0@gsnFrame     =  False
    res0@cnLevelSelectionMode       = "ExplicitLevels" 
    res0@cnLevels             = (/16600/)
    res0@cnFillColors         =(/"white","gray"/)
    res0@cnLinesOn      = False
    res0@cnInfoLabelOn = False
    res0@cnLineLabelsOn = False
    res0@cnFillOn      = True
    res0@lbLabelBarOn                   = False
    res0@gsnRightString = ""
    res0@cnMissingValPerimOn     = True    
    res0@cnMissingValPerimColor  = "black"  
    res0@cnMissingValFillPattern = 0       
    res0@cnMissingValFillColor   = "black"  
    plot0 = gsn_csm_pres_hgt(wks,t(1,0:24,:),res0)
     


    res   = True                                     ; plot mods desired
    res@gsnDraw = False
    res@gsnFrame= False
    res@gsnLeftString         = char_pen(ipen-1) 
    res@gsnRightString        = " "
    res@tiMainString          = "streamfunction"
    res@cnLevelSpacingF = 1                        ; contour level spacing
    res@cnLevelSelectionMode       = "ExplicitLevels" 
    res@cnLevels             = ispan(-400,400,40)
    res@gsnContourZeroLineThicknessF = 0 	          ; doubles thickness of zero contour
    res@gsnContourNegLineDashPattern = 1 		  ; sets negative contours to dash pattern 1
    res@cnFillOn        = True
    res@cnLineLabelsOn  = True
    res@cnLineLabelInterval = 3
    res@cnLineLabelBackgroundColor = -1
    res@cnFillPalette         = "temp_19lev"
    
    ;res@cnMissingValPerimOn     = True            ; turn on the missing value perimeter
    ;res@cnMissingValPerimColor  = "gray"           ; outline the perimeter red
    ;res@cnMissingValFillPattern = 0               ; choose fill pattern 0 (solid fill) 
    ;res@cnMissingValFillColor   = "gray"          ; color fill missing areas blue


   
    plot1  = gsn_csm_pres_hgt(wks, mp(ipen-1,7:,:), res )
    overlay(plot0, plot1)
    draw(plot0)
    frame(wks)

end do
end
