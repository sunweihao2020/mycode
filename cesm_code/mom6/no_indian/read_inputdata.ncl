begin
    file0  =  "/home/sun/mydown/model_input/b1850/topography_20190315.ieeei4"
    file1     =  "/home/sun/mydown/model_input/b1850/horiz_grid_20190315.ieeer8"
    setfileoption("bin","ReadByteOrder","BigEndian")
    bath  = fbindirread (file0, 0, -1, "integer")
    bathy = reshape(bath,(/458,540/))
    ; print
    ;printVarSummary(grid)
    wks  = gsn_open_wks("png","/home/sun/paint/change_land_mask/t66_kmt")            ; send graphics to PNG file
    cmap = read_colormap_file("BlAqGrYeOrRe")       ; read color data
    res                      = True                 ; plot mods desired
    res@gsnDraw              = False                ; don't draw yet
    res@gsnFrame             = False                ; don't advance frame yet
    res@cnFillOn             = True                 ; turn on color fill
    res@cnLinesOn            = False                ; turn off contour lines
    res@cnLineLabelsOn       = False                ; turn off contour line labels
    plot = gsn_csm_contour(wks,bathy,res)  
    draw(plot)
    frame(wks)
    

end
