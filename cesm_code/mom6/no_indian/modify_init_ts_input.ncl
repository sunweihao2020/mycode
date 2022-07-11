; 2022-6-15
; 本代码对输入的ts initial文件进行处理
begin
    f0  =  addfile("/home/sun/mydown/model_input/b1850/woa18_04_initial_conditions.nc","r")
    f1  =  addfile("/home/sun/mydown/model_input/b1850/state_restore_tx0.66v1_20200616.nc","r")
    f2  =  addfile("/home/sun/mydown/model_input/b1850/energy_new_t0.66v1_conserve_190315.nc","r")

    ;lat/lon message
    f3     =  addfile("/home/sun/mydown/model_input/b1850/tx0.66v1_SCRIP_190314.nc","r")
    lat1   =  f3->grid_center_lat
    lon1   =  f3->grid_center_lon
    mask1  =  f3->grid_imask

    ; reshape
    lat_reshape   =  reshape(lat1,(/458,540/))
    lon_reshape   =  reshape(lon1,(/458,540/))
    mask_reshape  =  reshape(mask1,(/458,540/))

    ; deal with f1. Variables in f1 is salt and theta0,dimension is 12 * 458 * 540
    salt    =  f1->salt
    theta0  =  f1->theta0

    ; range here lat lon is expressed using degree
    lat_min  =  0
    lat_max  =  23
    lon_min  =  (65 - 360)
    lon_max  =  (95 - 360)

    ; deal with salt
    ; reference salt2 and theta02
    salt2    =  salt
    ; because theta0 is nan, need to br replaced
    nan_value  :=  theta0(0,0,0)
    if (any(isnan_ieee(theta0))) then
      value = 1.e20
      replace_ieeenan (theta0, value, 0)
      theta0@_FillValue = value
    end if
    theta02  =  theta0 
    do dim0 = 0,(12-1)
        do dim1 = 0,(458-1)
            do dim2 = 0,(540-1)
                if (lat_reshape(dim1,dim2) .gt. lat_min .and. lat_reshape(dim1,dim2) .lt. lat_max .and. lon_reshape(dim1,dim2) .gt. lon_min .and. lon_reshape(dim1,dim2) .lt. lon_max) then
                    salt2(dim0,dim1,dim2) = dim_avg_n(salt(dim0,dim1,:), 0)
                    theta02(dim0,dim1,dim2) = dim_avg_n(theta0(dim0,dim1,:), 0)
                end if
            end do
        end do
    end do

    ; possion fill for salt and theta0
    guess     = 1      
    is_cyclic = True   
    nscan     = 1500   
    eps       = 1.e-2  
    relc      = 0.6    
    opt       = 0      

    poisson_grid_fill( salt, is_cyclic, guess, nscan, eps, relc, opt)  ; after possion, min value is 10
    poisson_grid_fill( theta0, is_cyclic, guess, nscan, eps, relc, opt) 
    salt    =  where(ismissing(salt2),salt@_FillValue,salt)
    theta0  =  where(ismissing(theta02),theta0@_FillValue,theta0)
    theta0  =  where(ismissing(theta0),nan_value,theta0)
    theta0@_FillValue = nan_value
    ; ---------------------that is end for the modifying file1-----------------------

    ; ---------------------below is the process for file2----------------------------
    wave  =  f2->wave_dissipation
    wave2 =  wave
    do dim1 = 0,(458-1)
        do dim2 = 0,(540-1)
            if (lat_reshape(dim1,dim2) .gt. lat_min .and. lat_reshape(dim1,dim2) .lt. lat_max .and. lon_reshape(dim1,dim2) .gt. lon_min .and. lon_reshape(dim1,dim2) .lt. lon_max) then
                wave2(dim1,dim2) = dim_avg_n(wave(dim1,:), 0)
            end if
        end do
    end do
    poisson_grid_fill( wave, is_cyclic, guess, nscan, eps, relc, opt)  ; after possion, min value is 10
    wave    =  where(ismissing(wave2),wave@_FillValue,wave)
    ; ---------------------that is end for the modifying file2-----------------------

    ; ---------------------writing to files------------------------------------------
    sys1   = systemfunc("rm /home/sun/data/cesm/state_restore_tx0.66v1_noindian_220615.nc") 
    sys2   = systemfunc("rm /home/sun/data/cesm/energy_new_t0.66v1_conserve_noindian_220615.nc")
    fout1 = addfile("/home/sun/data/cesm/state_restore_tx0.66v1_noindian_220615.nc","c")
    fout2 = addfile("/home/sun/data/cesm/energy_new_t0.66v1_conserve_noindian_220615.nc","c")
    
    fout1->salt  =  salt
    fout1->theta0 = theta0

    fout2->wave_dissipation = wave
    ;printVarSummary(wave)

    ; print
    ;printVarSummary(theta0)  
    ;print(theta0(5,:,10))


    ;plot
    wks  = gsn_open_wks("png","/home/sun/paint/change_land_mask/t66_wave_after_possion")            ; send graphics to PNG file
    cmap = read_colormap_file("BlAqGrYeOrRe")       ; read color data
    res                      = True                 ; plot mods desired
    res@gsnDraw              = False                ; don't draw yet
    res@gsnFrame             = False                ; don't advance frame yet
    res@cnFillOn             = True                 ; turn on color fill
    res@cnLinesOn            = False                ; turn off contour lines
    res@cnLineLabelsOn       = False                ; turn off contour line labels
    ;res@cnLevelSelectionMode       = "ExplicitLevels"
    ;res@cnLevels             = ispan(10,5000,200)
    plot = gsn_csm_contour(wks,wave(:,:),res)  
    draw(plot)
    frame(wks)

end
