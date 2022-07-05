; 2022/7/5
; This code calculate regional meridional streamfunction between 90 and 100°E
; based on composite3.nc
begin
    f0  =  addfile("/home/sun/data/composite3.nc","r")
    f1  =  addfile("/home/sun/qomo-data/composite_PS.nc","r")

    ps    =  f1->PS(:,{90:100},:)
    u     =  f0->uwind(:,{90:100},:)
    v     =  f0->vwind(:,{90:100},:)

    lat   =  f0->lat
    lon   =  f0->lon
    level =  f0->level

    level =  level * 100
    level@units  =  "Pa"

    dd    =  new((/61,42,361,576),double)
    dv    =  new((/2,61,42,361,576),double)

    ; fill missing value with zero
    u     =  where(ismissing(u),0,u)
    v     =  where(ismissing(v),0,v)

    ; first process using u and v
    do ll = 0,41
        do day = 0,60
            dd(day,ll,:,:)   = uv2dv_cfd(u(day,ll,:,:), v(day,ll,:,:), lat, lon, 2)
            dv(:,day,ll,:,:) = dv2uvF(dd(day,ll,:,:))
        end do
    end do

    dv_v  =  dv(1,:,:,:,:)

    ;mpsi  =  new((/61,31,361/),double)
    ;; calculate mpsi
    ;do day = 0,60
    ;    mpsi(day,:,:)  =  zonal_mpsi(dvv(ipen-1,1:31:-1,:,416:448), lat, p, ps)
