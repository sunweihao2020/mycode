begin
    bathy_in  =  "/home/sun/data/cesm/topography_20161215.ieeei4"
    file0     =  "/home/sun/data/cesm/gx1v7_151008.nc"
    setfileoption("bin","ReadByteOrder","BigEndian")
    bath  = fbindirread (bathy_in, 0, -1, "integer")

    bathy = reshape(bath,(/384,320/))

    latlonf   =  addfile(file0,"r")
    lat       =  latlonf->grid_center_lat
    lon       =  latlonf->grid_center_lon
    imask     =  latlonf->grid_imask

    lat_reshape   = reshape(lat,(/384,320/))
    lon_reshape   = reshape(lon,(/384,320/))
    imask_reshape = reshape(imask,(/384,320/))

    pi        =  3.141592653

    ; range
    lat1      =  0.13962634015954636
    lat2      =  0.4014257279586958
    lon1      =  1.1344640137963142
    lon2      =  1.5707963267948966


    ;do dim3=0,383
    ;    do dim4=0,319
    ;        if (lat_reshape(dim3,dim4) .gt. lat1 .and. lat_reshape(dim3,dim4) .lt. lat2 .and. lon_reshape(dim3,dim4) .gt. lon1 .and. lon_reshape(dim3,dim4) .lt. lon2) then
    ;            if imask_reshape(dim3,dim4) .eq. 0 then
    ;                bathy(dim3,dim4)  =  40
    ;            end if
    ;        end if
    ;    end do
    ;end do
    ;print(bathy(225,90:130))
   ; print(lat_reshape(:,110))

    wks  = gsn_open_wks("png","kmt")            ; send graphics to PNG file
    cmap = read_colormap_file("BlAqGrYeOrRe")       ; read color data
    res                      = True                 ; plot mods desired
    res@gsnDraw              = False                ; don't draw yet
    res@gsnFrame             = False                ; don't advance frame yet
    res@cnFillOn             = True                 ; turn on color fill
    res@cnLinesOn            = False                ; turn off contour lines
    res@cnLineLabelsOn       = False                ; turn off contour line labels
    ;res@cnFillMode           = "CellFill"
    res@gsnLeftString = "KMT"
    res@gsnRightString = " "
    plot = gsn_csm_contour(wks,bathy(:,:),res)  
    draw(plot)
    frame(wks)

   ; bathy_out    =    "/home/sun/data/cesm/topography_noindian_220606.ieeei4"
   ; sys       =    systemfunc("rm "+bathy_out)
   ; setfileoption("bin","WriteByteOrder","BigEndian")
   ; fbindirwrite(bathy_out, bathy)


end