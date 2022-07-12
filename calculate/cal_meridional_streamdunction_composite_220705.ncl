; 2022/7/5
; This code calculate regional meridional streamfunction between 90 and 100°E
; based on composite3.nc
begin
    path0  =  "/home/sun/data/"
    f0  =  addfile(path0+"composite3.nc","r")
    f1  =  addfile(path0+"composite_PS.nc","r")

    ps    =  f1->PS
    u     =  f0->uwind
    v     =  f0->vwind

    lat   =  f0->lat
    lon   =  f0->lon
    level =  f0->level

    level =  level * 100
    level@units  =  "Pa"

    dd    =  new((/61,42,361,576/),double)
    dv    =  new((/2,61,42,361,576/),double)

    ; fill missing value with zero
    u     =  where(ismissing(u),0,u)
    v     =  where(ismissing(v),0,v)

    ; first process using u and v
    i = 0
    do ll = 0,41
        do day = 0,60
            print(i)
            dd(day,ll,:,:)   = uv2dv_cfd(u(day,ll,:,:), v(day,ll,:,:), lat, lon, 2)
            dv(:,day,ll,:,:) = dv2uvF(dd(day,ll,:,:))
            i = i+1
        end do
    end do

    dv_v  =  dv(1,:,:,:,:)

    mpsi  =  new((/61,31,361/),double)
    ; calculate mpsi
    j = 0
    do day = 0,60
        print(j)
        ;mpsi(day,:,:)  =  zonal_mpsi_Wrap(dv_v(day,1:31:-1,:,432:440), lat, level(1:31:-1), ps(day,:,432:440))  ; 90-95
        mpsi(day,:,:)  =  zonal_mpsi_Wrap(dv_v(day,1:31:-1,:,440:448), lat, level(1:31:-1), ps(day,:,440:448))  ; 95-100
        
        j = j+1
    end do

    ; write to file
    ;mpsi!0 = "time"
    ;mpsi!1 = "lev"
    ;mpsi!2 = "lat"
    ;mpsi&lev = level(1:31:-1)
    ;mpsi&lat = lat
    ;mpsi = mpsi/1E+9

    fout = addfile(path0+"composite_zonal_meridional_streamfunction_95to100.nc","c")
    filedimdef(fout,"time",-1,True)
    fout->MPSI  =  mpsi

    fileatt  =  True
    fileatt@time  =  "2022-7-12"
    fileatt@description  =  "This file generate zonal meridional streamfunction between 95 to 100, based on composite3.nc. Generated script from cal_meridional_streamdunction_composite_220705.ncl"  

end
