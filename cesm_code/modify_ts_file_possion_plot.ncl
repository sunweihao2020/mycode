;尝试possion差值试试 注意，possion差值之后是没有缺测的
begin
    bathy_in  =  "/home/sun/data/cesm/topography_20161215.ieeei4"
    ts_in     =  "/home/sun/data/cesm/ts_PHC2_jan_ic_gx1v6_20090205.ieeer8"
    ts_in2    =  "/home/sun/data/cesm/ts_noindian_0606.ieeer8"
    file0     =  "/home/sun/data/cesm/gx1v7_151008.nc"

    latlonf   =  addfile(file0,"r")
    lat       =  latlonf->grid_center_lat
    lon       =  latlonf->grid_center_lon
    imask     =  latlonf->grid_imask

    pi        =  3.141592653

    ; range
    lat1      =  0.13962634015954636
    lat2      =  0.4014257279586958
    lon1      =  1.1344640137963142
    lon2      =  1.5707963267948966

    setfileoption("bin","ReadByteOrder","BigEndian")
    tracer = fbindirread (ts_in, 0, -1, "double")
    tracer := reshape(tracer,(/2,60,384,320/))

    tracer2 = tracer

    lat_reshape   = reshape(lat,(/384,320/))
    lon_reshape   = reshape(lon,(/384,320/))
    imask_reshape = reshape(imask,(/384,320/))
    ;tracer := reshape(tracer,(/2,60,384,320/))
    ;print(tracer(1,10,:,0))



    


    do dim3=0,383
        do dim4=0,319
            if (lat_reshape(dim3,dim4) .gt. lat1 .and. lat_reshape(dim3,dim4) .lt. lat2 .and. lon_reshape(dim3,dim4) .gt. lon1 .and. lon_reshape(dim3,dim4) .lt. lon2) then
                if imask_reshape(dim3,dim4) .eq. 0 then
                    ;print(dim4)  大约在110位置
                    ;print(dim3)  大约在258
                    tracer2(0,0:9,dim3,dim4)  =  dim_avg_n(tracer2(0,0:9,dim3,:), 1)
                    tracer2(1,0:9,dim3,dim4)  =  dim_avg_n(tracer2(1,0:9,dim3,:), 1)
                end if
            end if
        end do
    end do
    tracer2@_FillValue = -99
    ;到这里除了目标区域，其他地方都还是缺测
    tracer@_FillValue = -99
    guess     = 1                ; use zonal means
    is_cyclic = True             ; cyclic [global]
    nscan     = 1500             ; usually much less than this
    eps       = 1.e-2            ; variable dependent
    relc      = 0.6              ; relaxation coefficient
    opt       = 0                ; not used

    ;poisson_grid_fill( tracer(:,0:49,:,:), is_cyclic, guess, nscan, eps, relc, opt) 
    ;每个点都给全球平均
    
    
    ;此时没有缺测值了，现在再给加上缺测值
    do dim3=150,250
        do ll=0,59
            tracer(0,ll,dim3,:)  =  where(tracer2(0,ll,dim3,:).eq.tracer2@_FillValue,tracer@_FillValue,dim_avg_n(tracer(0,ll,dim3,:),0))
            tracer(1,ll,dim3,:)  =  where(tracer2(1,ll,dim3,:).eq.tracer2@_FillValue,tracer@_FillValue,dim_avg_n(tracer(1,ll,dim3,:),0))
        end do
    end do
    tracer(:,:,0:1,:)=-99
    tracer(:,:,382:383,:)=-99
    ;print(tracer(1,:,258,110))
    ;print(tracer(1,:,220,110))


    ;print(imask_reshape(:,110))
    ;print(lat_reshape(:,110))
    ;print(tracer(1,:,258,110))
    ;----plot----
    wks  = gsn_open_wks("png","ts_possion")            ; send graphics to PNG file
    cmap = read_colormap_file("BlAqGrYeOrRe")       ; read color data
    res                      = True                 ; plot mods desired
    res@gsnDraw              = False                ; don't draw yet
    res@gsnFrame             = False                ; don't advance frame yet
    res@cnFillOn             = True                 ; turn on color fill
    res@cnLinesOn            = False                ; turn off contour lines
    res@cnLineLabelsOn       = False                ; turn off contour line labels
    ;res@cnFillMode           = "CellFill"
    res@gsnLeftString = "Temp"
    res@gsnRightString = " "
    print(tracer(0,:,100,100))
    plot = gsn_csm_contour(wks,tracer(0,0,:,:),res)  
    draw(plot)
    frame(wks)



ts_out    =    "/home/sun/data/cesm/ts_noindian_0607.ieeer8"
sys       =    systemfunc("rm "+ts_out)
setfileoption("bin","WriteByteOrder","BigEndian")
fbindirwrite (ts_out, tracer)



end