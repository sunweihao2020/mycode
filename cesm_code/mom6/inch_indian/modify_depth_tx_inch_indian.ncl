; 2022-8-11
; 针对tx格点，本代码对depth进行操作
begin
    path0  =  "/home/sun/data/model_data/input/"
    f0     =  addfile(path0+"ocean_topog_200701.nc","r")

    depth  =  f0->depth
    mask0   =  f0->mask

    ; range here lat lon is expressed using degree
    lat_min  =  0
    lat_max  =  23
    lon_min  =  (65 - 360)
    lon_max  =  (95 - 360)


    ; f0 do not contain lat/lon message. f1 is SCRIP file
    f1     =  addfile(path0+"tx0.66v1_SCRIP_190314.nc","r")
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
            if (lat_reshape(dim1,dim2) .ge. 17 .and. lat_reshape(dim1,dim2) .le. 21 .and. lon_reshape(dim1,dim2) .ge. (90-360) .and. lon_reshape(dim1,dim2) .le. (108-360)) .or. (lat_reshape(dim1,dim2) .ge. 8 .and. lat_reshape(dim1,dim2) .le. 17 .and. lon_reshape(dim1,dim2) .ge. (90-360) .and. lon_reshape(dim1,dim2) .le. (110-360)) .or. (lat_reshape(dim1,dim2) .ge. 5 .and. lat_reshape(dim1,dim2) .le. 8 .and. lon_reshape(dim1,dim2) .ge. (98-360) .and. lon_reshape(dim1,dim2) .le. (104-360)) .or. (lat_reshape(dim1,dim2) .ge. 4 .and. lat_reshape(dim1,dim2) .le. 5 .and. lon_reshape(dim1,dim2) .ge. (100-360) .and. lon_reshape(dim1,dim2) .le. (104-360)) .or. (lat_reshape(dim1,dim2) .ge. 3 .and. lat_reshape(dim1,dim2) .le. 4 .and. lon_reshape(dim1,dim2) .ge. (100-360) .and. lon_reshape(dim1,dim2) .le. (104-360)) .or. (lat_reshape(dim1,dim2) .ge. 2 .and. lat_reshape(dim1,dim2) .le. 3 .and. lon_reshape(dim1,dim2) .ge. (101-360) .and. lon_reshape(dim1,dim2) .le. (105-360)) .or. (lat_reshape(dim1,dim2) .ge. 1 .and. lat_reshape(dim1,dim2) .le. 2 .and. lon_reshape(dim1,dim2) .ge. (102-360) .and. lon_reshape(dim1,dim2) .le. (105-360)) .or. (lat_reshape(dim1,dim2) .gt. lat_min .and. lat_reshape(dim1,dim2) .lt. lat_max .and. lon_reshape(dim1,dim2) .gt. lon_min .and. lon_reshape(dim1,dim2) .lt. lon_max) then
                mask0(dim1,dim2) = 1
            end if
        end do
    end do
    ; modify mask1
    do dim0 = 0,(458*540-1)
        if (lat1(dim0) .ge. 17 .and. lat1(dim0) .le. 21 .and. lon1(dim0) .ge. (90-360) .and. lon1(dim0) .le. (108-360)) .or. (lat1(dim0) .ge. 8 .and. lat1(dim0) .le. 17 .and. lon1(dim0) .ge. (90-360) .and. lon1(dim0) .le. (110-360)) .or. (lat1(dim0) .ge. 5 .and. lat1(dim0) .le. 8 .and. lon1(dim0) .ge. (98-360) .and. lon1(dim0) .le. (104-360)) .or. (lat1(dim0) .ge. 4 .and. lat1(dim0) .le. 5 .and. lon1(dim0) .ge. (100-360) .and. lon1(dim0) .le. (104-360)) .or. (lat1(dim0) .ge. 3 .and. lat1(dim0) .le. 4 .and. lon1(dim0) .ge. (100-360) .and. lon1(dim0) .le. (104-360)) .or. (lat1(dim0) .ge. 2 .and. lat1(dim0) .le. 3 .and. lon1(dim0) .ge. (101-360) .and. lon1(dim0) .le. (105-360)) .or. (lat1(dim0) .ge. 1 .and. lat1(dim0) .le. 2 .and. lon1(dim0) .ge. (102-360) .and. lon1(dim0) .le. (105-360)) .or. (lat1(dim0) .gt. lat_min .and. lat1(dim0) .lt. lat_max .and. lon1(dim0) .gt. lon_min .and. lon1(dim0) .lt. lon_max) then
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
            if (lat_reshape(dim1,dim2) .ge. 17 .and. lat_reshape(dim1,dim2) .le. 21 .and. lon_reshape(dim1,dim2) .ge. (90-360) .and. lon_reshape(dim1,dim2) .le. (108-360)) .or. (lat_reshape(dim1,dim2) .ge. 8 .and. lat_reshape(dim1,dim2) .le. 17 .and. lon_reshape(dim1,dim2) .ge. (90-360) .and. lon_reshape(dim1,dim2) .le. (110-360)) .or. (lat_reshape(dim1,dim2) .ge. 5 .and. lat_reshape(dim1,dim2) .le. 8 .and. lon_reshape(dim1,dim2) .ge. (98-360) .and. lon_reshape(dim1,dim2) .le. (104-360)) .or. (lat_reshape(dim1,dim2) .ge. 4 .and. lat_reshape(dim1,dim2) .le. 5 .and. lon_reshape(dim1,dim2) .ge. (100-360) .and. lon_reshape(dim1,dim2) .le. (104-360)) .or. (lat_reshape(dim1,dim2) .ge. 3 .and. lat_reshape(dim1,dim2) .le. 4 .and. lon_reshape(dim1,dim2) .ge. (100-360) .and. lon_reshape(dim1,dim2) .le. (104-360)) .or. (lat_reshape(dim1,dim2) .ge. 2 .and. lat_reshape(dim1,dim2) .le. 3 .and. lon_reshape(dim1,dim2) .ge. (101-360) .and. lon_reshape(dim1,dim2) .le. (105-360)) .or. (lat_reshape(dim1,dim2) .ge. 1 .and. lat_reshape(dim1,dim2) .le. 2 .and. lon_reshape(dim1,dim2) .ge. (102-360) .and. lon_reshape(dim1,dim2) .le. (105-360)) .or. (lat_reshape(dim1,dim2) .gt. lat_min .and. lat_reshape(dim1,dim2) .lt. lat_max .and. lon_reshape(dim1,dim2) .gt. lon_min .and. lon_reshape(dim1,dim2) .lt. lon_max) then
                depth2(dim1,dim2) = 100
            end if
        end do
    end do
    depth2@_FillValue = 0

    delete(depth@_FillValue)
    depth = where(ismissing(depth2),0,depth)

    ;write variables to files

    sys1   = systemfunc("rm /home/sun/data/model_data/input/ocean_topog_inch_indian_220920.nc") 
    sys2   = systemfunc("rm /home/sun/data/model_data/input/tx0.66v1_SCRIP_noinch_indian_220920.nc")

    fout1 = addfile(path0+"ocean_topog_inch_indian_220920.nc","c")
    fout1->depth  =  depth
    fout1->mask   =  mask0

    fout2 = addfile(path0+"tx0.66v1_SCRIP_noinch_indian_220920.nc","c")
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
    wks  = gsn_open_wks("png","/home/sun/paint/change_land_mask/t66_depth_after_possion_inch_indian")            ; send graphics to PNG file
    cmap = read_colormap_file("BlAqGrYeOrRe")       ; read color data
    res                      = True                 ; plot mods desired
    res@gsnDraw              = False                ; don't draw yet
    res@gsnFrame             = False                ; don't advance frame yet
    res@cnFillOn             = True                 ; turn on color fill
    res@cnLinesOn            = False                ; turn off contour lines
    res@cnLineLabelsOn       = False                ; turn off contour line labels
    res@cnLevelSelectionMode       = "ExplicitLevels"
    res@cnLevels             = ispan(10,5000,200)
    plot = gsn_csm_contour(wks,depth,res)  
    draw(plot)
    frame(wks)
end