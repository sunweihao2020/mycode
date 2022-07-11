begin
    bathy_in  =  "/home/sun/data/cesm/topography_20161215.ieeei4"
    file0     =  "/home/sun/data/cesm/gx1v7_151008.nc"
    file1     =  "/home/sun/data/cesm/gx1v7_220605_indian.nc"

    setfileoption("bin","ReadByteOrder","BigEndian")
    bath  = fbindirread (bathy_in, 0, -1, "integer")

    bathy = reshape(bath,(/384,320/))

    latlonf   =  addfile(file1,"r")
    lat       =  latlonf->grid_center_lat
    lon       =  latlonf->grid_center_lon
    imask     =  latlonf->grid_imask


    lat_reshape   = reshape(lat,(/384,320/))
    lon_reshape   = reshape(lon,(/384,320/))
    imask_reshape = reshape(imask,(/384,320/))

    pi        =  3.141592653
    print(bathy(100,200))

    ; range
    lat1      =  0
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



    do dim3=0,383
        do dim4=0,319
            if imask_reshape(dim3,dim4) .eq. 0 then
                bathy_f(dim3,dim4)  =  0.0
            end if
        end do
    end do
    bathy_int = floattointeger(bathy_f)



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
    plot = gsn_csm_contour(wks,bathy_int(150:280,50:150),res)  
    draw(plot)
    frame(wks)
    ;print(bath)

    bathy_out    =    "/home/sun/data/cesm/topography_noindian_220608.ieeei4"
    sys       =    systemfunc("rm "+bathy_out)
    setfileoption("bin","WriteByteOrder","BigEndian")
    fbindirwrite(bathy_out, bathy_int)


end