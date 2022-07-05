;2020/12/26
;计算olr的20-70天带通滤波
;使用资料：1980-2019
;权重选用365*2+1，前后各损失一年

;-----------------1.计算滤波并输出文件-------------------
begin
;f = addfile("/data5/2019swh/mydown/OLR/olr.nc","r")
;olr = f->olr
;;***************************************************
;;                    设置带通滤波
;;***************************************************
;ihp     = 2                             ; band pass
;sigma   = 1.0                           ; Lanczos sigma
;nWgt    = 201                           ; loose 100 each end                            
;fca     = 1./70.                       ; start freq
;fcb     = 1./20.                        ; last  freq
;wgt     = filwgts_lanczos(nWgt, ihp, fca, fcb, sigma )
;printVarSummary(wgt)
;filted_olr    = wgt_runave_n(olr, wgt, 0,0)
;printVarSummary(filted_olr)
;
;filted_olr!0 = "time"
;filted_olr!1 = "lat"
;filted_olr!2 = "lon"
;filted_olr&lat = olr&lat
;filted_olr&lon = olr&lon
;
;filted_olr@units = olr@units
;filted_olr@valid_range = olr@valid_range
;
;fout = addfile("/data5/2019swh/mydown/OLR/olr_bandpass.nc","c")
;filedimdef(fout, "time", -1, True)
;
;fout->OLR = filted_olr
;
;end
;
;------------------------------------end------------------------------

;----------------------对lancozs滤波结果进行检验----------------------
f = addfile("/data5/2019swh/mydown/OLR/olr.nc","r")
system("rm -rf /data5/2019swh/mydown/OLR/olr_bandpass.nc")
olr = f->olr
olr_a = dim_avg_n(olr, 0)
olr_anomaly = olr
do x = 0,72
    do y = 0,143
        olr_anomaly(:,x,y) = olr(:,x,y)-olr_a(x,y)
    end do
end do

ihp     = 2                             ; band pass
sigma   = 1.0                           ; Lanczos sigma
nWgt    = 365*2+1                           ; loose 100 each end   
fca     = 1./70.                       ; start freq
fcb     = 1./20.                        ; last  freq
wgt     = filwgts_lanczos(nWgt, ihp, fca, fcb, sigma )
filt1    = wgt_runave_n(olr_anomaly, wgt, 0,0)
filted_olr  =  filt1

filted_olr!0 = "time"
filted_olr!1 = "lat"
filted_olr!2 = "lon"
filted_olr&lat = olr&lat
filted_olr&lon = olr&lon

filted_olr@units = olr@units
filted_olr@valid_range = olr@valid_range

fout = addfile("/data5/2019swh/mydown/OLR/olr_bandpass.nc","c")
filedimdef(fout, "time", -1, True)

fout->OLR = filted_olr(366:(14610-365-1),:,:)

end