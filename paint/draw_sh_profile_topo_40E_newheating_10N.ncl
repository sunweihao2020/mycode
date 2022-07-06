load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/shea_util.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
begin

;f1     = addfile("/data5/2019swh/data/composite_shlh.nc", "r")
;sh0    = f1->SSHF
;lh0    = f1->SLHF

f1     = addfile("/data5/2019swh/data/composite-all_heating.nc", "r")
sh0    = f1->sshf
lh0    = f1->slhf

sh     = doubletofloat(sh0)
lh     = doubletofloat(lh0)
copy_VarCoords(sh0, sh)
copy_VarCoords(lh0, lh)

sh     = sh/3600.0/24.0*(-1)
lh     = lh/3600.0/24.0*(-1)

printVarSummary(sh)
printMinMax(sh, False)


sh_p    = sh(0:5,:,:)
lh_p    = lh(0:5,:,:)

do ip   = 0,5
 sh_p(ip,:,:)   = dim_avg_n_Wrap(sh(ip*5:ip*5+4,:,:), 0)
 lh_p(ip,:,:)   = dim_avg_n_Wrap(lh(ip*5:ip*5+4,:,:), 0)
end do

printVarSummary(lh_p)

time            = sh_p&lon
time!0          = "lon"
time&lon        = sh_p&lon

char            = new(6,"string")
char            = (/"D0-30 - D0-26","D0-25 - D0-21","D0-20 - D0-16","D0-15 - D0-11","D0-10 - D0-6","D0-5 - D0-1"/)
;---------------------------------------------------------------------------------------------------
;f4              = addfile("/data5/2019swh/liuxl/Geopotential_1.0_1.0.nc","r")
f4              = addfile("/data5/2019swh/liuxl/ERAIN_Geopotential_0.5X0.5.nc","r")


dixing0         = short2flt(f4->z(0,::-3,::3))
dixing          = dixing0/9.8  ;({-89.5:90},:)
copy_VarCoords(dixing0, dixing)
printVarSummary(dixing)

dixing          = dixing/1000  ; gpm ~m  ==》 km
;print(dixing&longitude)
;print(lh_p&lon)
;***************************
wks                           = gsn_open_wks("pdf","pic_sh_profile_topo_40E_newheating_10N")                    ; send graphics to PNG file 
plot                          = new(9,graphic)

; resources for "left" variable
  resL                        =  True 
  resL@gsnDraw                =  False
  resL@gsnFrame               =  False
  resL@tmXTOn                 =  False
  resL@xyLineThicknesses      =  2.                  ; thicker line
  resL@tiYAxisString          =  " LH  (W/m~S~2~N~)  "   ; axis string
  resL@tiYAxisFontColor       =  "blue"
  resL@xyLineColors           =  "blue" 
  resL@trYMaxF                =   160.                    ; axis max
  resL@trYMinF                =    0.                    ; axis min
  resL@tmXBMode               =  "Explicit" 
  resL@tmXBValues             =  ispan(40,120, 10)  ;
  resL@tmXBLabels             =  (/"40E","50E","60E","70E","80E","90E","100E","110E","120E"/);tostring(ispan(40,120,10))  ;
  resL@tmXBLabelFontHeightF   =  0.025
  resL@tmYLLabelFontHeightF   =  0.025
  resL@trXMaxF                =  120
  resL@trXMinF                =  40
  resL@vpWidthF               = 0.6
  resL@vpHeightF              = 0.3

; resources for "right" variable
  resR                        =  True                      
  resR@gsnDraw                =  False
  resR@gsnFrame               =  False
  resR@tmXTOn                 =  False
  resR@xyDashPatterns         =  1                   ; dashed line for 2nd
  resR@xyLineThicknesses      =  2                   ; thicker line
  resR@tiYAxisString          =  " SH (W/m~S~2~N~)"    ; axis string
  resR@tiYAxisFontColor       =  "red"
  resR@xyLineColors           =  "red" 
  resR@trYMaxF                =   160.                    ; axis max
  resR@trYMinF                =   0.   
  resR@gsnRightString          =   "lat=10N" 
  resR@gsnRightStringFontHeightF = 0.025

  resR@tmXBValues             =  ispan(40,120, 10)  ;
  resR@tmXBLabels             =  (/"40E","50E","60E","70E","80E","90E","100E","110E","120E"/);tostring(ispan(40,120,10))  ;
  resR@tmXBLabelFontHeightF   =  0.025
  resR@tmYLLabelFontHeightF   =  0.025
  resR@trXMaxF                =  120
  resR@trXMinF                =  40
  resR@vpWidthF               =  0.6
  resR@vpHeightF              =  0.3

do ip       = 0,5
   resR@gsnLeftString         = char(ip) 
   resR@gsnLeftStringFontHeightF = 0.025
   ;plot(ip) = gsn_csm_xy2(wks,time({40:120}),lh_p(ip,{10},{40:120}),sh_p(ip,{10},{40:120}),resL,resR)
   plot(ip) = gsn_csm_xy(wks,time({40:120}),sh_p(ip,{10},{40:120}),resR)
end do

  res                        =  True 
  res@gsnDraw                =  False
  res@gsnFrame               =  False
  res@tmXTOn                 =  False
  res@xyLineThicknesses      =  2.                  ; thicker line
  res@tiYAxisString          =  "Topography"   ; axis string
  res@tiYAxisFontColor       =  "black"
  res@xyLineColors           =  "black" 
  res@trYMaxF                =   2.4                   ; axis max
  res@trYMinF                =    0.                    ; axis min
  res@tmXBMode               =  "Explicit" 
  res@tmXBValues             =  ispan(40,120, 10)  ;
  res@tmXBLabels             =  (/"40E","50E","60E","70E","80E","90E","100E","110E","120E"/);tostring(ispan(40,120,10))  ;
  res@trXMaxF                =  120
  res@trXMinF                =  40
  res@vpWidthF               =  0.6
  res@vpHeightF              =  0.3
  res@tmXBLabelFontHeightF   =  0.025
  res@tmYLLabelFontHeightF   =  0.025
  res@gsnRightString          =   "lat=10N" 
  res@gsnRightStringFontHeightF = 0.025
  do ip = 6,8
  plot(ip)  = gsn_csm_xy (wks,time({40:120}),dixing({10},{40:120}),res) 
  end do

resP             = True
resP@gsnPanelYWhiteSpacePercent =5
resP@gsnMaximize = True
gsn_panel(wks, plot, (/3,3/), resP)

end