; 2022/6/10
; 本代码处理MOM6中的更改海陆分布文件
begin
    ; region
    lat_extent1  =  (/0,23/)
    lon_extent1  =  (/65,90/)
    lat1      =  0.0
    lat2      =  0.4014257279586958
    lon1      =  1.1344640137963142
    lon2      =  1.5707963267948966

    ;files
    f0  =  addfile("/home/sun/mydown/model_input/b1850/gx1v6_090205.nc","r")
    f1  =  addfile("/home/sun/mydown/model_input/b1850/ocean_topog.nc","r")
    f2  =  addfile("/home/sun/mydown/model_input/b1850/WOA05_pottemp_salt.nc","r")
    f3  =  addfile("/home/sun/data/cesm/gx1v6_220610_indian.nc","r")

    imask  =  f0->grid_imask
    imask2 =  f3->grid_imask
    imask_reshape  =  reshape(imask,(/384,320/))
    imask_reshape2  =  reshape(imask2,(/384,320/))
    lat    =  f0->grid_center_lat
    lon    =  f0->grid_center_lon
    lat_reshape    =  reshape(lat,(/384,320/))
    lon_reshape    =  reshape(lon,(/384,320/))

    depth  =  f1->depth
    temp   =  f2->PTEMP
    salt   =  f2->SALT


    ;print message
    ;print(f0)
    ;print(lat_reshape(:,100))
    ;print(f2)

    ;change depth
    ;do dim1=0,383
    ;    do dim2=0,319
    ;        if (lat_reshape(dim1,dim2) .gt. lat1 .and. lat_reshape(dim1,dim2) .lt. lat2 .and. lon_reshape(dim1,dim2) .gt. lon1 .and. lon_reshape(dim1,dim2) .lt. lon2) then ; 纬向平均
    ;            depth(dim1,dim2)  =  dim_avg_n(depth(dim1,:), 0)
    ;        end if
    ;    end do
    ;end do
;
    ;; change temp/salt , using possion
    ;guess     = 1                ; use zonal means
    ;is_cyclic = True             ; cyclic [global]
    ;nscan     = 1500             ; usually much less than this
    ;eps       = 1.e-2            ; variable dependent
    ;relc      = 0.6              ; relaxation coefficient
    ;opt       = 0                ; not used
;
    ;poisson_grid_fill(temp, is_cyclic, guess, nscan, eps, relc, opt) 
    ;poisson_grid_fill(salt, is_cyclic, guess, nscan, eps, relc, opt) 
;
    ;; writing
    ;sys1   = systemfunc("rm /home/sun/data/cesm/mom6_gx1v6_depth_indian.nc") 
    ;sys2   = systemfunc("rm /home/sun/data/cesm/mom6_gx1v6_ic_indian.nc") 
;
;
    ;fout1 = addfile("/home/sun/data/cesm/mom6_gx1v6_depth_indian.nc","c")
    ;fout2 = addfile("/home/sun/data/cesm/mom6_gx1v6_ic_indian.nc","c")
;
    ;fout1->depth  =  depth
;
    ;fout2->TIME   =  f2->TIME
    ;fout2->DEPTH  =  f2->DEPTH
    ;fout2->LAT    =  f2->LAT
    ;fout2->LON    =  f2->LON
    ;fout2->PTEMP  =  temp
    ;fout2->SALT   =  salt

    ;plot
    wks  = gsn_open_wks("png","/home/sun/paint/change_land_mask/salt_possion")            ; send graphics to PNG file
    cmap = read_colormap_file("BlAqGrYeOrRe")       ; read color data
    res                      = True                 ; plot mods desired
    res@gsnDraw              = False                ; don't draw yet
    res@gsnFrame             = False                ; don't advance frame yet
    res@cnFillOn             = True                 ; turn on color fill
    res@cnLinesOn            = False                ; turn off contour lines
    res@cnLineLabelsOn       = False                ; turn off contour line labels
    res@gsnRightString = " "
    plot = gsn_csm_contour(wks,imask_reshape2,res)  
    draw(plot)
    frame(wks)



end