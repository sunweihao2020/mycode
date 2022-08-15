; 2022-8-11
; 本代码对kmt文件进行处理
begin
    path0     =  "/home/sun/data/model_data/input/"
    bathy_in  =  path0+"topography_20190315.ieeei4"
    file1     =  path0+"tx0.66v1_SCRIP_noinch_220811.nc" 


    setfileoption("bin","ReadByteOrder","BigEndian")
    bath  = fbindirread (bathy_in, 0, -1, "integer")

    bathy = reshape(bath,(/458,540/))

    latlonf   =  addfile(file1,"r")
    lat       =  latlonf->grid_center_lat
    lon       =  latlonf->grid_center_lon
    imask     =  latlonf->grid_imask


    lat_reshape   = reshape(lat,(/458,540/))
    lon_reshape   = reshape(lon,(/458,540/))
    imask_reshape = reshape(imask,(/458,540/))




    guess     = 1                ; use zonal means
    is_cyclic = True             ; cyclic [global]
    nscan     = 1500             ; usually much less than this
    eps       = 1.e-2            ; variable dependent
    relc      = 0.6              ; relaxation coefficient
    opt       = 0                ; not used

    bathy_f  =  int2flt(bathy)
    bathy_f@_FillValue = 0.0
    poisson_grid_fill( bathy_f, is_cyclic, guess, nscan, eps, relc, opt) 



    do dim3=0,(458-1)
        do dim4=0,(540-1)
            if imask_reshape(dim3,dim4) .eq. 0 then
                bathy_f(dim3,dim4)  =  0.0
            end if
        end do
    end do
    bathy_int = floattointeger(bathy_f)



    wks  = gsn_open_wks("png","/home/sun/paint/change_land_mask/kmt_cice_tx66_inch")            ; send graphics to PNG file
    ;cmap = read_colormap_file("BlAqGrYeOrRe")       ; read color data
    res                      = True                 ; plot mods desired
    res@gsnDraw              = False                ; don't draw yet
    res@gsnFrame             = False                ; don't advance frame yet
    res@cnFillOn             = True                 ; turn on color fill
    res@cnLinesOn            = False                ; turn off contour lines
    res@cnLineLabelsOn       = False                ; turn off contour line labels
    ;res@cnLevelSelectionMode       = "ExplicitLevels"
    ;res@cnLevels             = fspan(0,60,61)
    plot = gsn_csm_contour(wks,bathy_int,res)  
    draw(plot)
    frame(wks)

 

    bathy_out    =    "/home/sun/data/model_data/input/topography_tx66_noinch_220811.ieeei4"
    sys       =    systemfunc("rm "+bathy_out)
    setfileoption("bin","WriteByteOrder","BigEndian")
    fbindirwrite(bathy_out, bathy_int)


end