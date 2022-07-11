begin
    bathy_in  =  "/home/sun/data/cesm/topography_20161215.ieeei4"
    ts_in     =  "/home/sun/data/cesm/ts_PHC2_jan_ic_gx1v6_20090205.ieeer8"
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



    tracer2@_FillValue = -99


    do dim3=0,383
        do dim4=0,319
            if (lat_reshape(dim3,dim4) .gt. lat1 .and. lat_reshape(dim3,dim4) .lt. lat2 .and. lon_reshape(dim3,dim4) .gt. lon1 .and. lon_reshape(dim3,dim4) .lt. lon2) then
                if imask_reshape(dim3,dim4) .eq. 0 then
                    ;print(dim4)  大约在110位置
                    ;print(dim3)  大约在258
                    tracer(0,0:50,dim3,dim4)  =  dim_avg_n(tracer2(0,0:50,dim3,:), 1)
                    tracer(1,0:50,dim3,dim4)  =  dim_avg_n(tracer2(1,0:50,dim3,:), 1)
                end if
            end if
        end do
    end do
    tracer@_FillValue = -99



    ;poisson_grid_fill( tracer(:,0,:,:), is_cyclic, guess, nscan, eps, relc, opt) 
   ; tracer(:,:,0:1,:)=-99
   ; tracer(:,:,382:383,:)=-99

    ;print(imask_reshape(:,110))
    ;print(lat_reshape(:,110))
    ;print(tracer(1,:,258,110))



ts_out    =    "/home/sun/data/cesm/ts_noindian_0606.ieeer8"
;sys       =    systemfunc("rm "+ts_out)
setfileoption("bin","WriteByteOrder","BigEndian")
fbindirwrite (ts_out, tracer)



end