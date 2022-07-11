begin
    f1  =  addfile("/home/sun/data/cesm/domain.lnd.fv0.9x1.25_gx1v6.090309.nc","r")
    f2  =  addfile("/home/sun/data/cesm/domain.lnd.fv09_125_gx1v6_noindian.220610.nc","r")
    xc1 =  f1->xc
    xc2 =  f2->xc

    mask2  =  f2->frac
    print(xc1(10,:))
    print(xc2(10,:))
    wks  = gsn_open_wks("png","/home/sun/paint/change_land_mask/mask")            ; send graphics to PNG file
    cmap = read_colormap_file("BlAqGrYeOrRe")       ; read color data
    res                      = True                 ; plot mods desired
    res@gsnDraw              = False                ; don't draw yet
    res@gsnFrame             = False                ; don't advance frame yet
    res@cnFillOn             = True                 ; turn on color fill
    res@cnLinesOn            = False                ; turn off contour lines
    res@cnLineLabelsOn       = False                ; turn off contour line labels
    res@gsnRightString = " "
    plot = gsn_csm_contour(wks,mask2,res)  
    draw(plot)
    frame(wks)
    ;print(f1)
end