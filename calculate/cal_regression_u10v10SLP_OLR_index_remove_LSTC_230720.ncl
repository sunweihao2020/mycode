;2023-7-20
;This script calculate the regression of wind to the OLR
begin
    ; ================ Data processing1: abnormal, detrend, calculate monthly mean =======================
    ; Wind data
    f0 = addfile("/home/sun/data/long_time_series_after_process/ERA5/ERA5_10mwind_slp_pentad20to25_1940_2022.nc", "r")

    ; Land-Sea thermal contrast
    f1 = addfile("/home/sun/data/long_time_series_after_process/ERA5/ERA5_pentad_OLR_maritime_continent_1940_2022.nc", "r")
    f2 = addfile("/home/sun/data/long_time_series_after_process/ERA5/ERA5_pentad_LSTC_1940_2022.nc", "r")


    ; Read data
    u  = f0->uwind
    v  = f0->vwind
    slp = f0->slp

    olr = f1->olr(:, {20:25})
    lstc = f2->LSTC(:, {20:25})

    ;print(olr)

    ; Calculates and removes the mean of the given dimension(s) at all other dimensions.
    olr_abnormal  = dim_rmvmean_n_Wrap(olr, 0)
    lstc_abnormal = dim_rmvmean_n_Wrap(lstc, 0)
    u_abnormal    = dim_rmvmean_n_Wrap(u, 0)
    v_abnormal    = dim_rmvmean_n_Wrap(v, 0)
    slp_abnormal  = dim_rmvmean_n_Wrap(slp, 0)

    ;print(u_abnormal)
    ; Detrend
    lstc_detrend  = lstc_abnormal
    lstc_detrend  = (/dtrend_n(lstc_abnormal, True, 0)/)
    olr_detrend   = olr_abnormal
    olr_detrend   = (/dtrend_n(olr_abnormal, True, 0)/)

    u_detrend     = u_abnormal
    u_detrend     = (/dtrend_n(u_abnormal, True, 0)/)
    v_detrend     = v_abnormal
    v_detrend     = (/dtrend_n(v_abnormal, True, 0)/)
    slp_detrend   = slp_abnormal
    slp_detrend   = (/dtrend_n(slp_abnormal, True, 0)/)


    ; Claim array save the removed LSTC/OLR index
    lstc_detrend_remove = lstc_detrend
    olr_detrend_remove  = olr_detrend

    ; Remove the OLR signals from lstc; reference : http://bbs.06climate.com/forum.php?mod=viewthread&tid=47325
    do i = 0, 5
        tval1=new(1,"float",0)
        nptxy1=new(1,"integer",0)
        b1 = regcoef(olr_detrend(:, i), lstc_detrend(:, i), tval1, nptxy1)
        pinave = dim_avg(lstc_detrend(:, i))
        a1 = pinave - dim_avg(b1*olr_detrend(:, i))
        lstc_detrend_remove0 = lstc_detrend(:, i)
        lstc_detrend_remove0 = lstc_detrend_remove0 - (b1*olr_detrend(:, i) + a1)
        ;lstc_detrend_remove(:, i) = dim_standardize(lstc_detrend_remove0, 1)
        lstc_detrend_remove(:, i) = lstc_detrend_remove0
    end do
    ;;;;; Remove LSTC signal from OLR
    do i = 0, 5
        tval1=new(1,"float",0)
        nptxy1=new(1,"integer",0)
        b1 = regcoef(lstc_detrend(:, i), olr_detrend(:, i), tval1, nptxy1)
        pinave = dim_avg(olr_detrend(:, i))
        a1 = pinave - dim_avg(b1*lstc_detrend(:, i))
        olr_detrend_remove0 = olr_detrend(:, i)
        olr_detrend_remove0 = olr_detrend_remove0 - (b1*lstc_detrend(:, i) + a1)
        ;lstc_detrend_remove(:, i) = dim_standardize(lstc_detrend_remove0, 1)
        ;olr_detrend_remove(:, i) = dim_standardize(olr_detrend_remove0, 1)
        olr_detrend_remove(:, i) = olr_detrend_remove0
    end do
    ;print(olr_detrend_remove)
    

;
    ;=================================================
    ; ================ Data processing1: abnormal, detrend, calculate monthly mean =======================
;
    ; ================ Data processing2: calculate regression =======================
    ;printVarSummary(u_detrend)
    ;printVarSummary(lstc_detrend_april)
    rc_u_lstc = (/u_detrend(0, :, :, :)/)
    rc_v_lstc = (/v_detrend(0, :, :, :)/)
    rc_u_olr  = (/u_detrend(0, :, :, :)/)
    rc_v_olr  = (/v_detrend(0, :, :, :)/)
    rc_slp_olr= (/slp_detrend(0, :, :, :)/)
    rc_slp_lstc = (/slp_detrend(0, :, :, :)/)


    do j = 0,5
        ;test = regCoef_n(lstc_detrend_remove(:, j), u_detrend(:, j, :, :), 0, 0)
        ;printVarSummary(test)
        ;printVarSummary(rc_u_lstc(j, :, :))
        rc_u_lstc(j, :, :) = regCoef_n(lstc_detrend_remove(:, j), u_detrend(:, j, :, :), 0, 0)  
        rc_v_lstc(j, :, :) = regCoef_n(lstc_detrend_remove(:, j), v_detrend(:, j, :, :), 0, 0)  
        rc_u_olr(j, :, :)  = regCoef_n(olr_detrend_remove(:, j), u_detrend(:, j, :, :), 0, 0)  
        rc_v_olr(j, :, :)  = regCoef_n(olr_detrend_remove(:, j), v_detrend(:, j, :, :), 0, 0)  
        rc_slp_olr(j, :, :)   = regCoef_n(olr_detrend_remove(:, j), slp_detrend(:, j, :, :), 0, 0)  
        rc_slp_lstc(j, :, :)  = regCoef_n(lstc_detrend_remove(:, j),slp_detrend(:, j, :, :), 0, 0) 
    end do
;   
    ; ================ Write to the nc file ==========================================
    copy_VarCoords(u_detrend(0, :, :, :), rc_u_lstc)
    copy_VarCoords(u_detrend(0, :, :, :), rc_u_olr)
    copy_VarCoords(v_detrend(0, :, :, :), rc_v_lstc)
    copy_VarCoords(v_detrend(0, :, :, :), rc_v_olr)
    copy_VarCoords(slp_detrend(0, :, :, :), rc_slp_lstc)
    copy_VarCoords(slp_detrend(0, :, :, :), rc_slp_olr)

    ;printMinMax(rc_u_lstc, 0)
;    printMinMax(rc_u, 0)
    system("rm /home/sun/data/ERA5_data_monsoon_onset/regression/regression_uv_to_OLR_to_LSTC_remove_each_other.nc")
    fout = addfile("/home/sun/data/ERA5_data_monsoon_onset/regression/regression_uv_to_OLR_to_LSTC_remove_each_other.nc", "c")
    filedimdef(fout,"time",-1,True)

    fout->u_detrend = u_detrend
    fout->v_detrend = v_detrend
    fout->rc_u_lstc = rc_u_lstc
    fout->rc_v_lstc = rc_v_lstc
    fout->rc_u_olr  = rc_u_olr
    fout->rc_v_olr  = rc_v_olr
    fout->olr_remove_lstc = olr_detrend_remove
    fout->lstc_remove_olr = lstc_detrend_remove
    fout->lstc_detrend = lstc_detrend
    fout->olr_detrend  = olr_detrend
    fout->rc_slp_lstc  = rc_slp_lstc
    fout->rc_slp_olr   = rc_slp_olr
;;
    

;;
;    ;; Set file attribute
    setfileoption(fout,"DefineMode",True)
    fAtt = True
    fAtt@description = "Create on 22/7/2023. This file include regression from u/v to the LSTC and OLR index. The regression has been removed from the signals of OLR and LSTC index"
    fileattdef(fout,fAtt)

end
