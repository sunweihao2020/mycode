begin
f = addfile("/home/sun/data/cesm/b1850m_test_indian4.mom6.hm_0001_01.nc","r")
s = f->tos
    wks  = gsn_open_wks("png","sst")            ; send graphics to PNG file
    cmap = read_colormap_file("BlAqGrYeOrRe")       ; read color data
    res                      = True                 ; plot mods desired
    res@gsnDraw              = False                ; don't draw yet
    res@gsnFrame             = False                ; don't advance frame yet
    res@cnFillOn             = True                 ; turn on color fill
    res@cnLinesOn            = False                ; turn off contour lines
    res@cnLineLabelsOn       = False                ; turn off contour line labels
    ;res@cnFillMode           = "CellFill"
    res@gsnLeftString = "Sea surface temperature"
    res@gsnRightString = " "
    plot = gsn_csm_contour(wks,s(0,:,:),res)  
    draw(plot)
    frame(wks)

end