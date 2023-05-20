; 2023-5-17
; This script calculate the regression of the LSTC/OLR index
begin
    ; ================ Data processing1: abnormal, detrend, calculate monthly mean =======================
    ; Wind data
    f0 = addfile("/home/sun/mycode/down/era/ERA5_single_monthly_sea_level_pressure.nc", "r")

    ; Land-Sea thermal contrast
    f1 = addfile("/home/sun/data/ERA5_data_monsoon_onset/index/quantity_index_monsoon_onset_ERA5.nc", "r")
    f2 = addfile("/home/sun/data/ERA5_data_monsoon_onset/index/OLR_maritime_area_average_monthly.nc", "r")

    ; Read data
    msl  = f0->msl(19:81, 0, :, :)

    lstc = f1->ls_diff
    olr  = f2->ttr_avg_mon({1959:2021}, 3)

    ; Calculates and removes the mean of the given dimension(s) at all other dimensions.
    lstc_abnormal = dim_rmvmean_n_Wrap(lstc, 0)
    olr_abnormal  = dim_rmvmean_n_Wrap(olr, 0)
    msl_abnormal  = dim_rmvmean_n_Wrap(msl, 0)


    ;print(u_abnormal)
    ; Detrend
    lstc_detrend  = lstc_abnormal
    lstc_detrend  = (/dtrend_n(lstc_abnormal, True, 0)/)

    olr_detrend  =  olr_abnormal
    olr_detrend  =  (/dtrend_n(olr_abnormal, True, 0)/)

    msl_detrend     = msl_abnormal
    msl_detrend     = (/dtrend_n(msl_abnormal, True, 0)/)


    ; Change the dimension sequence
    ;printVarSummary(u_abnormal)
    msl_detrend_    = msl_detrend
    ;printVarSummary(lstc_detrend)
    ;printVarSummary(u_detrend_)

    ; Delete NAN value
    if (any(isnan_ieee(msl_detrend_))) then
        value = 1.e20
        replace_ieeenan(msl_detrend_, value, 0)
        msl_detrend_@_FillValue = value
        msl_detrend_@_FillValue = value
    end if

    if (any(isnan_ieee(lstc_detrend))) then
        value = 1.e20
        replace_ieeenan(lstc_detrend, value, 0)
        lstc_detrend@_FillValue = value
    end if

    value = 1.e20
    replace_ieeenan(msl_detrend, value, 0)

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
    ; ================ The end of the Processing 1 =======================

    ; ================ Data processing 2: calculate regression ===========
    ; ================ 2.1 regression to lstc ============================
    ;printVarSummary(lstc_detrend_april_remove)
    ;printVarSummary(msl_detrend_)
    rc_msl = regCoef_n(lstc_detrend_april_remove, msl_detrend_, 0, 0)  

    copy_VarCoords(msl(0, :, :), rc_msl)
    ; ================ 2.2 write to ncfile ===============================
    system("rm -rf /home/sun/data/ERA5_data_monsoon_onset/regression/regression_msl_to_LSTC_remove_OLR.nc")
    fout = addfile("/home/sun/data/ERA5_data_monsoon_onset/regression/regression_msl_to_LSTC_remove_OLR.nc", "c")
    filedimdef(fout,"time",-1,True)

    fout->rc_msl = rc_msl

    ;; Set file attribute
    setfileoption(fout,"DefineMode",True)
    fAtt = True
    fAtt@description = "Create on 17/5/2023. This file include regression from msl to the LSTC index, removing OLR index."
    fileattdef(fout,fAtt)

    ; ================ 2.3 regression to olr =============================
    rc_msl2 = regCoef_n(olr_detrend_remove, msl_detrend_, 0, 0)  

    copy_VarCoords(msl(0, :, :), rc_msl2)

    ; ================ 2.4 Write to the nc file ==========================================
    system("rm -rf /home/sun/data/ERA5_data_monsoon_onset/regression/regression_msl_to_OLR_remove_LSTC.nc")
    fout2 = addfile("/home/sun/data/ERA5_data_monsoon_onset/regression/regression_msl_to_OLR_remove_LSTC.nc", "c")
    filedimdef(fout2,"time",-1,True)

    fout2->rc_msl2 = rc_msl2

    ;; Set file attribute
    setfileoption(fout2,"DefineMode",True)
    fAtt = True
    fAtt@description = "Create on 17/5/2023. This file include regression from msl to the OLR index, removing LSTC index."
    fileattdef(fout2,fAtt)

end