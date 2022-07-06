;2021/12/30
;本代码绘制论文version1.2 中的fig3
;内容为绘制4月的印度半岛与中南半岛的垂直加热廓线
;经向10-15平均，经度为75 100

begin
path  =  "/home/sun/qomo-data/"
path2 =  "/home/sun/paint/lunwen/version3.0/"

f1     =  addfile(path+"composite-heating-merra.nc","r")
fmask  =  addfile("/home/sun/data/merra2_land_sea_mask.nc","r")

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
lfrc1     =     fmask->land_mask({10:15},{75:80})
lfrc2     =     fmask->land_mask({10:15},{100:110})
printVarSummary(turbulence1)
printVarSummary(moist2)
printVarSummary(lfrc1)
printVarSummary(lfrc2)
;print(turbulence1&lon)
;print(lfrc1&lon)

lfrc1_new     = conform_dims(dimsizes(turbulence1), lfrc1, (/1,2/))
lfrc2_new     = conform_dims(dimsizes(turbulence2), lfrc2, (/1,2/))
copy_VarCoords(turbulence1, lfrc1_new)
copy_VarCoords(turbulence2, lfrc2_new)
printVarSummary(lfrc1_new)
printVarSummary(lfrc2_new)

;计算区域平均

turbulence1  =  where(lfrc1_new.le.0.5, turbulence1@_FillValue, turbulence1 )  ; make ocean missing
moist1       =  where(lfrc1_new.le.0.5, moist1@_FillValue,      moist1)
total1       =  where(lfrc1_new.le.0.5, total1@_FillValue,      total1)
turbulence2  =  where(lfrc2_new.le.0.5, turbulence2@_FillValue, turbulence2 )
moist2       =  where(lfrc2_new.le.0.5, moist2@_FillValue,      moist2)
total2       =  where(lfrc2_new.le.0.5, total2@_FillValue,      total2)


data1        = new((/6,dimsizes(turbulence1&level)/),double)
printVarSummary(data1)
data1(0,:) = dim_avg_n_Wrap(turbulence1,  (/1,2/))
data1(1,:) = dim_avg_n_Wrap(moist1,       (/1,2/))
data1(2,:) = dim_avg_n_Wrap(total1,       (/1,2/))
data1(3,:) = dim_avg_n_Wrap(turbulence2,  (/1,2/))
data1(4,:) = dim_avg_n_Wrap(moist2,       (/1,2/))
data1(5,:) = dim_avg_n_Wrap(total2,       (/1,2/))

;;------------------------------------------------------
plot = new(1,graphic)
dum  = new(1,graphic)
;wks  = gsn_open_wks("pdf",path2+"fig6_heating_profile_Apr_liuxl")
wks  = gsn_open_wks("pdf",path2+"lunwen_fig2c_v3.0_heating_profile_Apr_ocn_missing")

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
res@xyMarkers               =    (/6,6,6,16,16,16/)
res@xyLineColors            =    (/"red","blue","black","red","blue","black"/)

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

;lgres@lgLineColors          = (/"black"/)
;gsn_legend_ndc(wks,1,(/" total"/),0.15,0.15,lgres)
;lgres@lgLineColors          = (/"azure4"/)
;gsn_legend_ndc(wks,1,(/" radiation"/),0.35,0.15,lgres)

;lgres@lgLineColors          = (/"red"/)
;gsn_legend_ndc(wks,1,(/"  sensible"/),0.55,0.15,lgres)
;lgres@lgLineColors          = (/"blue"/)
;gsn_legend_ndc(wks,1,(/" moist"/),0.75,0.15,lgres)
lgres@lgMonoLineColor       = False
lgres@lgLineColors          = (/"red"/)
lgres@lgLabelFontColor      = (/"red"/)
gsn_legend_ndc(wks,1,(/" sensible heating"/),0.53,0.90,lgres)

lgres@lgLineColors          = (/"blue"/)
lgres@lgLabelFontColor      = (/"blue"/)
gsn_legend_ndc(wks,1,(/"   latent  heating"/),0.53,0.86,lgres)

lgres@lgLineColors          = (/"black"/)
lgres@lgLabelFontColor      = (/"black"/)
gsn_legend_ndc(wks,1,(/"   total   heating"/),0.53,0.82,lgres)
end

;调图记录
;前20天平均和前30天结果一样