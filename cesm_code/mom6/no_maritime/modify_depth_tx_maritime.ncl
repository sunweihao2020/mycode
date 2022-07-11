; 2022-6-15
; 针对tx格点，本代码对depth进行操作
begin
    f0  =  addfile("/home/sun/mydown/model_input/b1850/ocean_topog_200701.nc","r")

    depth  =  f0->depth
    mask0   =  f0->mask

    ; range here lat lon is expressed using degree
    lat_min  =  -10
    lat_max  =  15
    lon_min  =  (95 - 360)
    lon_max  =  (150 - 360)

    ; f0 do not contain lat/lon message. f1 is SCRIP file
    f1     =  addfile("/home/sun/mydown/model_input/b1850/tx0.66v1_SCRIP_190314.nc","r")
    lat1   =  f1->grid_center_lat
    lon1   =  f1->grid_center_lon
    mask1  =  f1->grid_imask

    ; reshape
    lat_reshape   =  reshape(lat1,(/458,540/))
    lon_reshape   =  reshape(lon1,(/458,540/))


    ; change mask
    ; 1. here wo modify mask variables: mask0 mask_reshape 
    ; 2. mask_reshape should be same as mask0

    ; modify mask0
    do dim1 = 0,(458-1)
        do dim2 = 0,(540-1)
            if (lat_reshape(dim1,dim2) .ge. -10 .and. lat_reshape(dim1,dim2) .le. 6 .and. lon_reshape(dim1,dim2) .ge. (95-360) .and. lon_reshape(dim1,dim2) .le. (100-360)) .or. (lat_reshape(dim1,dim2) .ge. -10 .and. lat_reshape(dim1,dim2) .le. 3 .and. lon_reshape(dim1,dim2) .ge. (100-360) .and. lon_reshape(dim1,dim2) .le. (101-360)) .or. (lat_reshape(dim1,dim2) .ge. -10 .and. lat_reshape(dim1,dim2) .le. 2.2 .and. lon_reshape(dim1,dim2) .ge. (101-360) .and. lon_reshape(dim1,dim2) .le. (102-360)) .or. (lat_reshape(dim1,dim2) .ge. -10 .and. lat_reshape(dim1,dim2) .le. 1.7 .and. lon_reshape(dim1,dim2) .ge. (102-360) .and. lon_reshape(dim1,dim2) .le. (103-360)) .or. (lat_reshape(dim1,dim2) .ge. -10 .and. lat_reshape(dim1,dim2) .le. 1.25 .and. lon_reshape(dim1,dim2) .ge. (103-360) .and. lon_reshape(dim1,dim2) .le. (104-360)) .or. (lat_reshape(dim1,dim2) .ge. -10 .and. lat_reshape(dim1,dim2) .le. 1.25 .and. lon_reshape(dim1,dim2) .ge. (104-360) .and. lon_reshape(dim1,dim2) .le. (105-360)) .or. (lat_reshape(dim1,dim2) .ge. -10 .and. lat_reshape(dim1,dim2) .le. 5 .and. lon_reshape(dim1,dim2) .ge. (105-360) .and. lon_reshape(dim1,dim2) .le. (110-360)) .or. (lat_reshape(dim1,dim2) .ge. -10 .and. lat_reshape(dim1,dim2) .le. 15 .and. lon_reshape(dim1,dim2) .ge. (110-360) .and. lon_reshape(dim1,dim2) .le. (120-360)) .or. (lat_reshape(dim1,dim2) .ge. -10 .and. lat_reshape(dim1,dim2) .le. 20 .and. lon_reshape(dim1,dim2) .ge. (120-360) .and. lon_reshape(dim1,dim2) .le. (130-360)) .or. (lat_reshape(dim1,dim2) .ge. -10 .and. lat_reshape(dim1,dim2) .le. 10 .and. lon_reshape(dim1,dim2) .ge. (130-360) .and. lon_reshape(dim1,dim2) .le. (160-360)) then
                mask0(dim1,dim2) = 1
            end if
        end do
    end do
    ; modify mask1
    do dim0 = 0,(458*540-1)
        if (lat1(dim0) .ge. -10 .and. lat1(dim0) .le. 6 .and. lon1(dim0) .ge. (95-360) .and. lon1(dim0) .le. (100-360)) .or. (lat1(dim0) .ge. -10 .and. lat1(dim0) .le. 3 .and. lon1(dim0) .ge. (100-360) .and. lon1(dim0) .le. (101-360)) .or. (lat1(dim0) .ge. -10 .and. lat1(dim0) .le. 2.2 .and. lon1(dim0) .ge. (101-360) .and. lon1(dim0) .le. (102-360)) .or. (lat1(dim0) .ge. -10 .and. lat1(dim0) .le. 1.7 .and. lon1(dim0) .ge. (102-360) .and. lon1(dim0) .le. (103-360)) .or. (lat1(dim0) .ge. -10 .and. lat1(dim0) .le. 1.25 .and. lon1(dim0) .ge. (103-360) .and. lon1(dim0) .le. (104-360)) .or. (lat1(dim0) .ge. -10 .and. lat1(dim0) .le. 1.25 .and. lon1(dim0) .ge. (104-360) .and. lon1(dim0) .le. (105-360)) .or. (lat1(dim0) .ge. -10 .and. lat1(dim0) .le. 5 .and. lon1(dim0) .ge. (105-360) .and. lon1(dim0) .le. (110-360)) .or. (lat1(dim0) .ge. -10 .and. lat1(dim0) .le. 15 .and. lon1(dim0) .ge. (110-360) .and. lon1(dim0) .le. (120-360)) .or. (lat1(dim0) .ge. -10 .and. lat1(dim0) .le. 20 .and. lon1(dim0) .ge. (120-360) .and. lon1(dim0) .le. (130-360)) .or. (lat1(dim0) .ge. -10 .and. lat1(dim0) .le. 10 .and. lon1(dim0) .ge. (130-360) .and. lon1(dim0) .le. (160-360)) then
            mask1(dim0) = 1
        end if
    end do
    mask_reshape  =  reshape(mask1,(/458,540/))
    ; modify depth
    depth2  =  depth ; original reference
    depth@_FillValue = depth2(0,0)

    ; possion interpolate

    guess     = 1      
    is_cyclic = True   
    nscan     = 1500   
    eps       = 1.e-2  
    relc      = 0.6    
    opt       = 0      

    poisson_grid_fill( depth, is_cyclic, guess, nscan, eps, relc, opt)  ; after possion, min value is 10

    ; compared with reference and replace the land except target area
    do dim1 = 0,(458-1)
        do dim2 = 0,(540-1)
            if (lat_reshape(dim1,dim2) .ge. -10 .and. lat_reshape(dim1,dim2) .le. 6 .and. lon_reshape(dim1,dim2) .ge. (95-360) .and. lon_reshape(dim1,dim2) .le. (100-360)) .or. (lat_reshape(dim1,dim2) .ge. -10 .and. lat_reshape(dim1,dim2) .le. 3 .and. lon_reshape(dim1,dim2) .ge. (100-360) .and. lon_reshape(dim1,dim2) .le. (101-360)) .or. (lat_reshape(dim1,dim2) .ge. -10 .and. lat_reshape(dim1,dim2) .le. 2.2 .and. lon_reshape(dim1,dim2) .ge. (101-360) .and. lon_reshape(dim1,dim2) .le. (102-360)) .or. (lat_reshape(dim1,dim2) .ge. -10 .and. lat_reshape(dim1,dim2) .le. 1.7 .and. lon_reshape(dim1,dim2) .ge. (102-360) .and. lon_reshape(dim1,dim2) .le. (103-360)) .or. (lat_reshape(dim1,dim2) .ge. -10 .and. lat_reshape(dim1,dim2) .le. 1.25 .and. lon_reshape(dim1,dim2) .ge. (103-360) .and. lon_reshape(dim1,dim2) .le. (104-360)) .or. (lat_reshape(dim1,dim2) .ge. -10 .and. lat_reshape(dim1,dim2) .le. 1.25 .and. lon_reshape(dim1,dim2) .ge. (104-360) .and. lon_reshape(dim1,dim2) .le. (105-360)) .or. (lat_reshape(dim1,dim2) .ge. -10 .and. lat_reshape(dim1,dim2) .le. 5 .and. lon_reshape(dim1,dim2) .ge. (105-360) .and. lon_reshape(dim1,dim2) .le. (110-360)) .or. (lat_reshape(dim1,dim2) .ge. -10 .and. lat_reshape(dim1,dim2) .le. 15 .and. lon_reshape(dim1,dim2) .ge. (110-360) .and. lon_reshape(dim1,dim2) .le. (120-360)) .or. (lat_reshape(dim1,dim2) .ge. -10 .and. lat_reshape(dim1,dim2) .le. 20 .and. lon_reshape(dim1,dim2) .ge. (120-360) .and. lon_reshape(dim1,dim2) .le. (130-360)) .or. (lat_reshape(dim1,dim2) .ge. -10 .and. lat_reshape(dim1,dim2) .le. 10 .and. lon_reshape(dim1,dim2) .ge. (130-360) .and. lon_reshape(dim1,dim2) .le. (160-360)) then
                depth2(dim1,dim2) = 100
            end if
        end do
    end do
    depth2@_FillValue = 0

    delete(depth@_FillValue)
    depth = where(ismissing(depth2),0,depth)

    ;write variables to files
    ;sys1   = systemfunc("rm /home/sun/data/cesm/mom6_gx1v6_depth_indian.nc") 
    sys1   = systemfunc("rm /home/sun/data/cesm/ocean_topog_nomaritime_20220623.nc") 
    sys2   = systemfunc("rm /home/sun/data/cesm/tx0.66v1_SCRIP_nomaritime_220623.nc")

    fout1 = addfile("/home/sun/data/cesm/ocean_topog_nomaritime_20220623.nc","c")
    fout1->depth  =  depth
    fout1->mask   =  mask0

    fout2 = addfile("/home/sun/data/cesm/tx0.66v1_SCRIP_nomaritime_220623.nc","c")
    fout2->grid_dims         =  f1->grid_dims
    fout2->grid_center_lat   =  f1->grid_center_lat
    fout2->grid_center_lon   =  f1->grid_center_lon
    fout2->grid_imask        =  mask1
    fout2->grid_corner_lat   =  f1->grid_corner_lat
    fout2->grid_corner_lon   =  f1->grid_corner_lon
    fout2->grid_area         =  f1->grid_area







    ; print
    ; print(depth(:,10))  ; 实际海深m
    ; print(mask0(:,10))  ; 1 ocean; 0 land
    ; print(lon_reshape(100,:))
    ; print(mask_reshape(:,10)) 
    ; printMinMax(depth2, 1)
    ;printVarSummary(depth)

    ;plot
    wks  = gsn_open_wks("png","/home/sun/paint/change_land_mask/t66_depth_after_possion_maritime")            ; send graphics to PNG file
    cmap = read_colormap_file("BlAqGrYeOrRe")       ; read color data
    res                      = True                 ; plot mods desired
    res@gsnDraw              = False                ; don't draw yet
    res@gsnFrame             = False                ; don't advance frame yet
    res@cnFillOn             = True                 ; turn on color fill
    res@cnLinesOn            = False                ; turn off contour lines
    res@cnLineLabelsOn       = False                ; turn off contour line labels
    ;res@cnLevelSelectionMode       = "ExplicitLevels"
    ;res@cnLevels             = ispan(10,5000,200)
    plot = gsn_csm_contour(wks,mask_reshape,res)  
    draw(plot)
    frame(wks)
end