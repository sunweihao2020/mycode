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

    tracer@_FillValue = -99
    guess     = 1                ; use zonal means
    is_cyclic = True             ; cyclic [global]
    nscan     = 1500             ; usually much less than this
    eps       = 1.e-2            ; variable dependent
    relc      = 0.6              ; relaxation coefficient
    opt       = 0                ; not used

    poisson_grid_fill( tracer(:,:,:,:), is_cyclic, guess, nscan, eps, relc, opt) 
    tracer(:,:,0:1,:)=-99
    tracer(:,:,382:383,:)=-99




    ts_out    =    "/home/sun/data/cesm/ts_possion_0608.ieeer8"
    ;sys       =    systemfunc("rm "+ts_out)
    setfileoption("bin","WriteByteOrder","BigEndian")
    fbindirwrite (ts_out, tracer)



end