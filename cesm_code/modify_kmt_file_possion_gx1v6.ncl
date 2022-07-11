;2022-6-7
;处理印度大陆，但是重新做了

begin
    bathy_in  =  "/home/sun/data/cesm/topography_20090204.ieeei4"
    file0     =  "/home/sun/data/cesm/gx1v6_090205.nc"

    setfileoption("bin","ReadByteOrder","BigEndian")
    bath  = fbindirread (bathy_in, 0, -1, "integer")

    bathy  = reshape(bath,(/384,320/))
    bathy2 = bathy 

    latlonf   =  addfile(file0,"r")
    lat       =  latlonf->grid_center_lat
    lon       =  latlonf->grid_center_lon
    imask     =  latlonf->grid_imask


    lat_reshape   = reshape(lat,(/384,320/))
    lon_reshape   = reshape(lon,(/384,320/))
    imask_reshape = reshape(imask,(/384,320/))

    ; range
    lat1      =  0.0
    lat2      =  0.4014257279586958
    lon1      =  1.1344640137963142
    lon2      =  1.5707963267948966

    guess     = 1                ; use zonal means
    is_cyclic = True             ; cyclic [global]
    nscan     = 1500             ; usually much less than this
    eps       = 1.e-2            ; variable dependent
    relc      = 0.6              ; relaxation coefficient
    opt       = 0                ; not used

    bathy_f  =  int2flt(bathy)
    bathy_f@_FillValue = 0.0
    poisson_grid_fill( bathy_f, is_cyclic, guess, nscan, eps, relc, opt) 

    ;change reference bathy2
    do dim1=0,383
        do dim2=0,319
            if (lat_reshape(dim1,dim2) .gt. lat1 .and. lat_reshape(dim1,dim2) .lt. lat2 .and. lon_reshape(dim1,dim2) .gt. lon1 .and. lon_reshape(dim1,dim2) .lt. lon2) then ; 纬向平均
                bathy2(dim1,dim2)  =  1
            end if
        end do
    end do
    bathy2@_FillValue = bathy(0,0)


    ;delete(depth@_FillValue)

    bathy_int = floattointeger(bathy_f)
    bathy_int = where(ismissing(bathy2),0,bathy_int)


    wks  = gsn_open_wks("png","/home/sun/paint/change_land_mask/bathy_gx1v6_possion")            ; send graphics to PNG file
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
    plot = gsn_csm_contour(wks,bathy_int,res)  
    draw(plot)
    frame(wks)
    print(bathy_int(:,110))

    bathy_out    =    "/home/sun/data/cesm/topography_noindian_possion_gx1v6_220612.ieeei4"
    sys       =    systemfunc("rm "+bathy_out)
    setfileoption("bin","WriteByteOrder","BigEndian")
    fbindirwrite(bathy_out, bathy_int)


end