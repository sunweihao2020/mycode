; 2021/12/28
; 本代码绘制论文version1.1中的加热廓线
; 这里是感热潜热+中南半岛印度一起画
begin
path  =  "/home/sun/qomo-data/"
path2 =  "/home/sun/paint/lunwen/version1.1/"

f1     =  addfile(path+"composite-heating-merra.nc","r")
fmask  =  addfile("/home/sun/data/merra2_land_sea_mask.nc","r")

;;Indian
turbulence1  =  f1->turbulence(:,{1000:200},{10:15},{75:80})  ; SH
moist1       =  f1->moist(:,{1000:200},{10:15},{75:80})  ; LH

;SE China
turbulence2  =  f1->turbulence(:,{1000:200},{10:15},{100:110})
moist2       =  f1->moist(:,{1000:200},{10:15},{100:110})     

;; total
total1       =  moist1
total2       =  moist2  
total1       =  turbulence1 + moist1
total2       =  turbulence2 + moist2

;; mask
lfrc1     =     fmask->land_mask({10:15},{75:80})
lfrc2     =     fmask->land_mask({10:15},{100:110})
;printVarSummary(turbulence1)
;printVarSummary(moist2)
;printVarSummary(lfrc1)
;printVarSummary(lfrc2)
;print(turbulence1&lon)
;print(lfrc1&lon)

lfrc1_new     = conform_dims(dimsizes(turbulence1), lfrc1, (/2,3/))
lfrc2_new     = conform_dims(dimsizes(turbulence2), lfrc2, (/2,3/))
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


data1        = new((/6,61,dimsizes(turbulence1&level)/),double)
printVarSummary(data1)
data1(0,:,:) = dim_avg_n_Wrap(turbulence1,  (/2,3/))
data1(1,:,:) = dim_avg_n_Wrap(moist1,       (/2,3/))
data1(2,:,:) = dim_avg_n_Wrap(total1,       (/2,3/))
data1(3,:,:) = dim_avg_n_Wrap(turbulence2,  (/2,3/))
data1(4,:,:) = dim_avg_n_Wrap(moist2,       (/2,3/))
data1(5,:,:) = dim_avg_n_Wrap(total2,       (/2,3/))

;;------------------------------------------------------
plot = new(4,graphic)
dum  = new(4,graphic)
wks  = gsn_open_wks("pdf",path2+"fig6_v1.1_heating_profile")

res                         =    True
res@gsnDraw                 =    False
res@gsnFrame                =    False
res@gsnRightString          =    " "
res@gsnStringFontHeightF    =     0.04

res@trXMaxF                 =    12
res@trXMinF                 =    -4
res@trYReverse              =    True

res@tmYLLabelFontHeightF    =    0.032
res@tmXBLabelFontHeightF    =    0.032

res@xyLineThicknessF        =    2
res@xyDashPattern           =    0
res@xyMarkLineMode          =    "MarkLines"
res@xyMarkers               =    (/6,6,6,16,16,16/)
res@xyMarkerSizeF           =    0.015
res@xyLineColors            =    (/"red","blue","black","red","blue","black"/)

res@lgPerimOn               =    False  

polyres                     =    True
polyres@gsLineColor         =    "black"
polyres@gsLineThicknessF    =    1.5
polyres@gsLineDashPattern   =    2

res@gsnRightString           =    "units: K/day"
res@gsnRightStringFontHeightF=    0.034

days = (/"D0-6","D0","D0+3"/)
dd  =  (/24,30,33/)  
do day = 0,2
res@gsnLeftString = days(day)
plot(day) = gsn_csm_xy(wks,data1(:,dd(day),:),turbulence1&level,res)
dum(day)  = gsn_add_polyline(wks, plot(day), (/0,0/), (/0,1000/), polyres)
end do

lgres                       =    True   
lgres@lgMonoLineThickness   =    True
lgres@lgLineThicknessF      =    3.5
lgres@lgPerimOn             =    False              
lgres@lgLineLabelStrings    =    (/"",""/)          
lgres@lgAutoManage          =    False
lgres@lgLineDashSegLenF     =    0.12
lgres@lgLabelFontHeightF    =    0.34   
lgres@lgDashIndexes         =    (/0,0/)     

lgres@vpHeightF             =    0.32                  
lgres@vpWidthF              =    0.24    

;lgres@lgLineColors          = (/"black"/)
;gsn_legend_ndc(wks,1,(/" total"/),0.15,0.15,lgres)
;lgres@lgLineColors          = (/"azure4"/)
;gsn_legend_ndc(wks,1,(/" radiation"/),0.35,0.15,lgres)

;lgres@lgLineColors          = (/"red"/)
;gsn_legend_ndc(wks,1,(/"  sensible"/),0.55,0.15,lgres)
;lgres@lgLineColors          = (/"blue"/)
;gsn_legend_ndc(wks,1,(/" moist"/),0.75,0.15,lgres)

;lgres@lgLineColors          = (/"red"/)
;gsn_legend_ndc(wks,1,(/" sensible heating"/),0.55,0.90,lgres)
;lgres@lgLineColors          = (/"blue"/)
;gsn_legend_ndc(wks,1,(/"    latent heating"/),0.55,0.85,lgres)


lgres@lgLineColors          = (/"red"/)
gsn_legend_ndc(wks,1,(/" sensible heating"/),0.05,0.46,lgres)
lgres@lgLineColors          = (/"blue"/)
gsn_legend_ndc(wks,1,(/" latent heating"/),0.45,0.46,lgres)
lgres@lgLineColors          = (/"black"/)
gsn_legend_ndc(wks,1,(/" total heating"/),0.75,0.46,lgres)


pnlres = True
pnlres@lgPerimOn             = False
pnlres@lgAutoManage          = False
pnlres@lgLineLabelStrings    = (/"",""/)
pnlres@gsnPanelDebug     = True  
;pnlres@gsnPanelMainString = "(10N,80E) vertical heating profile"
gsn_panel(wks,plot,(/1,3/),pnlres)
end

;调图记录
;前20天平均和前30天结果一样