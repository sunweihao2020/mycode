;2023-5-2
;This script calculate the regression of wind to the thermal index between land and sea
begin
    ; ================ Data processing1: abnormal, detrend, calculate monthly mean =======================
    ; Wind data
    f0 = addfile("/home/sun/data/climate_data/ERA5_uv_925_april_1959_2022.nc", "r")

    ; Land-Sea thermal contrast
    f1 = addfile("/home/sun/data/ERA5_data_monsoon_onset/index/quantity_index_monsoon_onset_ERA5.nc", "r")
    f2 = addfile("/home/sun/data/ERA5_data_monsoon_onset/index/OLR_maritime_area_average_monthly.nc", "r")

    ; Read data
    u  = f0->u_april({1959:2021}, :, :)
    v  = f0->v_april({1959:2021}, :, :)

    lstc = f1->ls_diff
    olr  = f2->ttr_avg_mon({1959:2021}, 3)

    ; Calculates and removes the mean of the given dimension(s) at all other dimensions.
    lstc_abnormal = dim_rmvmean_n_Wrap(lstc, 0)
    olr_abnormal  = dim_rmvmean_n_Wrap(olr, 0)
    u_abnormal    = dim_rmvmean_n_Wrap(u, 0)
    v_abnormal    = dim_rmvmean_n_Wrap(v, 0)

    ;print(u_abnormal)
    ; Detrend
    lstc_detrend  = lstc_abnormal
    lstc_detrend  = (/dtrend_n(lstc_abnormal, True, 0)/)

    olr_detrend  =  olr_abnormal
    olr_detrend  =  (/dtrend_n(olr_abnormal, True, 0)/)

    u_detrend     = u_abnormal
    u_detrend     = (/dtrend_n(u_abnormal, True, 0)/)
    v_detrend     = v_abnormal
    v_detrend     = (/dtrend_n(v_abnormal, True, 0)/)


    ; Change the dimension sequence
    ;printVarSummary(u_abnormal)
    u_detrend_    = u_detrend
    v_detrend_    = v_detrend
    ;printVarSummary(lstc_detrend)
    ;printVarSummary(u_detrend_)

    ; Delete NAN value
    if (any(isnan_ieee(u_detrend_))) then
        value = 1.e20
        replace_ieeenan(u_detrend_, value, 0)
        replace_ieeenan(v_detrend_, value, 0)
        u_detrend_@_FillValue = value
        v_detrend_@_FillValue = value
    end if

    if (any(isnan_ieee(lstc_detrend))) then
        value = 1.e20
        replace_ieeenan(lstc_detrend, value, 0)
        lstc_detrend@_FillValue = value
    end if

    value = 1.e20
    replace_ieeenan(u_detrend, value, 0)

    ; Deal with lstc_detrend, calculate April month average
    lstc_detrend_april = new(63, double)
    do i = 0,62
        lstc_detrend_april(i) = dim_avg_n(lstc_detrend(i, 90:120), 0)
    end do

    ; Remove the OLR signals from lstc; reference : http://bbs.06climate.com/forum.php?mod=viewthread&tid=47325
    tval1=new(1,"float",0)
    nptxy1=new(1,"integer",0)
    b1 = regcoef(olr_detrend, lstc_detrend_april, tval1, nptxy1)
    pinave = dim_avg(lstc_detrend_april)
    a1 = pinave - dim_avg(b1*olr_detrend)
    lstc_detrend_april_remove = lstc_detrend_april
    lstc_detrend_april_remove = lstc_detrend_april_remove - (b1*olr_detrend + a1)
    lstc_detrend_april_remove = dim_standardize(lstc_detrend_april_remove, 1)

    ; Remove LSTC from OLR
    b1 = regcoef(lstc_detrend_april, olr_detrend, tval1, nptxy1)
    pinave = dim_avg(olr_detrend)
    a1 = pinave - dim_avg(b1*lstc_detrend_april)
    olr_detrend_remove = olr_detrend
    olr_detrend_remove = olr_detrend_remove - (b1*lstc_detrend_april + a1)
    olr_detrend_remove = dim_standardize(olr_detrend_remove, 1)

    ;print(lstc_detrend_april)
    ;print(lstc_detrend_april_remove)
    ;print(lstc_detrend&year)

    ; ======Add attributes and write to nc file======

    ;lstc_detrend_april@units = "Pa"
    ;;lstc_detrend_april!0     = "year"
    ;;lstc_detrend_april&year  = lstc_detrend&year
;
    ;fout = addfile("/home/sun/data/ERA5_data_monsoon_onset/index/LSTC_index_April_ERA5_1959to2021.nc", "c")
    ;filedimdef(fout,"time",-1,True)
;
    ;fout->LSTC_april = lstc_detrend_april
;
    ;; Set file attribute
    ;setfileoption(fout,"DefineMode",True)
    ;fAtt = True
    ;fAtt@description = "Create on 05/5/2023. This is the April mean LSTC index from 1959 to 2021, using variable ls_diff2 in ncfile quantity_index_monsoon_onset_ERA5.nc"
    ;fileattdef(fout,fAtt)

    ;=================================================
    ; ================ Data processing1: abnormal, detrend, calculate monthly mean =======================

    ; ================ Data processing2: calculate regression =======================
    ;printVarSummary(u_detrend)
    ;printVarSummary(lstc_detrend_april)
    rc_u = regCoef_n(lstc_detrend_april_remove, u_detrend_, 0, 0)  
    rc_v = regCoef_n(lstc_detrend_april_remove, v_detrend_, 0, 0)  

    ; ================ Write to the nc file ==========================================
    copy_VarCoords(u(0, :, :), rc_u)
    copy_VarCoords(v(0, :, :), rc_v)
    ;printMinMax(lstc_detrend_april, 0)
    system("rm -rf /home/sun/data/ERA5_data_monsoon_onset/regression/regression_uv_to_LSTC_remove_OLR.nc")
    fout = addfile("/home/sun/data/ERA5_data_monsoon_onset/regression/regression_uv_to_LSTC_remove_OLR.nc", "c")
    filedimdef(fout,"time",-1,True)

    fout->rc_u = rc_u
    fout->rc_v = rc_v

    ;; Set file attribute
    setfileoption(fout,"DefineMode",True)
    fAtt = True
    fAtt@description = "Create on 09/5/2023. This file include regression from u/v to the LSTC index, removing OLR index."
    fileattdef(fout,fAtt)

    rc_u2 = regCoef_n(olr_detrend_remove, u_detrend_, 0, 0)  
    rc_v2 = regCoef_n(olr_detrend_remove, v_detrend_, 0, 0)  

    ; ================ Write to the nc file ==========================================
    copy_VarCoords(u(0, :, :), rc_u2)
    copy_VarCoords(v(0, :, :), rc_v2)
    ;printMinMax(lstc_detrend_april, 0)
    system("rm -rf /home/sun/data/ERA5_data_monsoon_onset/regression/regression_uv_to_OLR_remove_LSTC.nc")
    fout2 = addfile("/home/sun/data/ERA5_data_monsoon_onset/regression/regression_uv_to_OLR_remove_LSTC.nc", "c")
    filedimdef(fout2,"time",-1,True)

    fout2->rc_u = rc_u2
    fout2->rc_v = rc_v2

    ;; Set file attribute
    setfileoption(fout2,"DefineMode",True)
    fAtt = True
    fAtt@description = "Create on 09/5/2023. This file include regression from u/v to the OLR index, removing LSTC index."
    fileattdef(fout2,fAtt)

end
