;2021/12/30
;本代码绘制论文version1.2 中的fig3
;内容为绘制4月的印度半岛与中南半岛的垂直加热廓线
;经向10-15平均，经度为75 100

;version5.0 修改: 去除total的加热

begin
path  =  "/home/sun/qomo-data/"
path2 =  "/home/sun/paint/lunwen/version4.0/"

f1     =  addfile(path+"composite-heating-merra.nc","r")
fmask  =  addfile("/home/sun/qomo-data/merra2_land_sea_mask_low_resolution.nc","r")

;;Indian
turbulence1  =  dim_avg_n_Wrap( f1->turbulence(0:30,{1000:200},{10:15},{75:80}), 0)  ; SH
moist1       =  dim_avg_n_Wrap( f1->moist(0:30,{1000:200},{10:15},{75:80}),      0)  ; LH

;SE China
turbulence2  =  dim_avg_n_Wrap( f1->turbulence(0:30,{1000:200},{10:15},{100:110}),0)
moist2       =  dim_avg_n_Wrap( f1->moist(0:30,{1000:200},{10:15},{100:110}),     0)  

;;total Indian
total1       =  moist1
total2       =  moist2  
total1       =  turbulence1 + moist1
total2       =  turbulence2 + moist2

;; mask
lfrc1     =     fmask->ocean_fraction({10:15},{75:80})
lfrc2     =     fmask->ocean_fraction({10:15},{100:110})
printVarSummary(turbulence1)
printVarSummary(moist2)
printVarSummary(lfrc1)
printVarSummary(lfrc2)
;print(turbulence1&lon)
;print(lfrc1&lon)
;exit
lfrc1_new     = conform_dims(dimsizes(turbulence1), lfrc1, (/1,2/))
lfrc2_new     = conform_dims(dimsizes(turbulence2), lfrc2, (/1,2/))
copy_VarCoords(turbulence1, lfrc1_new)
copy_VarCoords(turbulence2, lfrc2_new)
printVarSummary(lfrc1_new)
printVarSummary(lfrc2_new)

;计算区域平均

turbulence1  =  where(lfrc1_new.gt.0.5, turbulence1@_FillValue, turbulence1 )  ; make ocean missing
moist1       =  where(lfrc1_new.gt.0.5, moist1@_FillValue,      moist1)
turbulence2  =  where(lfrc2_new.gt.0.5, turbulence2@_FillValue, turbulence2 )
moist2       =  where(lfrc2_new.gt.0.5, moist2@_FillValue,      moist2)


data1        = new((/4,dimsizes(turbulence1&level)/),double)
printVarSummary(data1)
data1(0,:) = dim_avg_n_Wrap(turbulence1,  (/1,2/))
data1(1,:) = dim_avg_n_Wrap(moist1,       (/1,2/))
data1(2,:) = dim_avg_n_Wrap(turbulence2,  (/1,2/))
data1(3,:) = dim_avg_n_Wrap(moist2,       (/1,2/))
printVarSummary(data1)
;exit
;;------------------------------------------------------
plot = new(1,graphic)
dum  = new(1,graphic)
;wks  = gsn_open_wks("pdf",path2+"fig6_heating_profile_Apr_liuxl")
wks  = gsn_open_wks("pdf",path2+"lunwen_fig2c_v5.0_heating_profile_Apr_ocn_missing")

res                         =    True
res@gsnDraw                 =    False
res@gsnFrame                =    False
res@gsnRightString          =    " "
res@gsnStringFontHeightF    =     0.04

res@trXMaxF                 =    12
res@trXMinF                 =    -4
res@trYReverse              =    True

res@tmYLLabelFontHeightF    =    0.017
res@tmXBLabelFontHeightF    =    0.017
res@tmXBLabelDeltaF         =    -0.6   ;; ; push the XB labels up from plot
res@tmYLLabelDeltaF         =    -0.6

res@tmXBMajorOutwardLengthF =    0.006
res@tmXBMinorOutwardLengthF =    0.006
res@tmYLMajorOutwardLengthF =    0.006
res@tmYLMinorOutwardLengthF =    0.006


res@tmXTOn                  =    False
res@tmYROn                  =    False

res@xyLineThicknessF        =    3.5
res@xyDashPattern           =    0
res@xyMarkLineMode          =    "MarkLines"
res@xyMarkerSizeF           =     13
res@xyMarkerThicknesses     =     (/2.5,2.5/)
res@xyMarkerColors          =    (/"maroon4","maroon4","green4","green4"/)
res@xyMarkers               =    (/7,7,16,16/)
res@xyLineColors            =    (/"red","blue","red","blue"/)

res@lgPerimOn               =    False  

polyres                     =    True
polyres@gsLineColor         =    "black"
polyres@gsLineThicknessF    =    1.5
polyres@gsLineDashPattern   =    2

res@gsnRightString           =    "  "
res@gsnRightStringFontHeightF=    0.026
plot = gsn_csm_xy(wks,data1,turbulence1&level,res)
dum  = gsn_add_polyline(wks, plot, (/0,0/), (/200,1000/), polyres)

;************************************************
  txres               = True                     ; text mods desired
  txres@txFontHeightF = 0.03                     ; font smaller. default big

  dum = gsn_add_text(wks,plot,"(c)",-3,250,txres) 

draw(plot)

lgres                       =    True   
lgres@lgMonoLineThickness   =    True
lgres@lgLineThicknessF      =    2.5
lgres@lgPerimOn             =    False              
lgres@lgLineLabelStrings    =    (/"",""/)          
lgres@lgAutoManage          =    False
lgres@lgLineDashSegLenF     =    0.15
lgres@lgLabelFontHeightF    =    0.34   
lgres@lgDashIndexes         =    (/0,0/)     

lgres@vpHeightF             =    0.295                  
lgres@vpWidthF              =    0.24    

lgres@lgMonoLineColor       = False
lgres@lgLineColors          = (/"red"/)
lgres@lgLabelFontColor      = (/"red"/)
gsn_legend_ndc(wks,1,(/" sensible heating"/),0.53,0.90,lgres)

lgres@lgLineColors          = (/"blue"/)
lgres@lgLabelFontColor      = (/"blue"/)
gsn_legend_ndc(wks,1,(/"   latent  heating"/),0.53,0.86,lgres)


end