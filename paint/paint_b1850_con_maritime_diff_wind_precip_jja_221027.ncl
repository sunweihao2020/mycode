;2022/10/27
;This code calculate the difference between control and maritime experiment
;paint variables: wind precip
;lev: 850
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/shea_util.ncl"
begin
path_out   =  "/home/sun/data/model_data/climate/"
file_out1  =  "b1850_control_atmospheric_monthly_average_2.nc"
file_out2  =  "b1850_maritime_atmospheric_monthly_average_2.nc"
f0         =  addfile(path_out + file_out1,  "r")
f1         =  addfile(path_out + file_out2,  "r")

; read variable
ctl_u = f0->U(6:8,{850},:,:)
ctl_v = f0->V(6:8,{850},:,:)
mar_u = f1->U(6:8,{850},:,:)
mar_v = f1->V(6:8,{850},:,:)

ctl_precip  =  f0->PRECT(6:8,:,:)
mar_precip  =  f1->PRECT(6:8,:,:)

; replace nan
ctl_u@_FillValue   =  9999
ctl_v@_FillValue   =  9999
mar_u@_FillValue   =  9999
mar_v@_FillValue   =  9999
if (any(isnan_ieee(ctl_u))) then
replace_ieeenan (ctl_u, ctl_u@_FillValue, 0)
replace_ieeenan (ctl_v, ctl_v@_FillValue, 0)
replace_ieeenan (mar_u, mar_u@_FillValue, 0)
replace_ieeenan (mar_v, mar_v@_FillValue, 0)

end if


char_month=(/"June","JULY","August","November"/)
num_month = (/5,6,7,8/)

lev       = (/6/)
level = (/"850hPa"/)

; calculate difference
diff_u      =  ctl_u
diff_v      =  ctl_v
diff_precip = ctl_precip

diff_u      =   mar_u  -  ctl_u 
diff_v      =   mar_v  -  ctl_v 
diff_precip =   ((mar_precip - ctl_precip)) * 86400000  ; The percentage of changed precipitation

; year average
diff_u_avg  =   dim_avg_n_Wrap(diff_u, 0)
diff_v_avg  =   dim_avg_n_Wrap(diff_v, 0)
diff_precip_avg  =   dim_avg_n_Wrap(diff_precip, 0)


; ---- contour setting -------------
res                       = True

;lines
res@cnFillOn              = True
res@cnFillPalette         = "BlueDarkRed18"
res@cnLineLabelsOn        = False
res@cnLinesOn             = False
res@cnInfoLabelOn         = False 
res@cnLevelSelectionMode  = "ExplicitLevels" 
res@cnLevels              = fspan(-3,3,13)

res@gsnDraw               = False
res@gsnFrame              = False

; map settings
res@mpMinLatF             = -20 
res@mpMaxLatF             =  80.
res@mpMinLonF             =  40.
res@mpMaxLonF             =  280.
res@mpGeophysicalLineThicknessF  = 1

; labelbar
res@lbLabelBarOn          = False

;tick and ticklabel
res@tmYLLabelFontHeightF   =  0.024
res@tmXBLabelFontHeightF  =  0.024

; String
res@gsnRightString        =  "850 hPa"
;res@gsnStringFont         =  0.25


; -------  vector settings  ----------
vcres                     =  True

vcres@gsnDraw             =  False
vcres@gsnFrame            =  False

; magnitude for ref
vcres@vcRefMagnitudeF     =  2.5

; vector length
vcres@vcRefLengthF        =  0.055

;vector style
vcres@vcGlyphStyle        = "CurlyVector"
vcres@vcMinDistanceF      = 0.017
vcres@vcLineArrowThicknessF   = 1.5

; Strings
vcres@gsnLeftString       =  ""
vcres@gsnRightString      =  ""

;vector reference
vcres@vcRefAnnoOrthogonalPosF = -1.0
vcres@vcRefAnnoString2On  =  False

; figure setting
wks1 = gsn_open_wks("pdf","/home/sun/paint/b1850_exp/difference_in_sensitivity/b1850_diff_jja_average_850_circulation_with_prect")


; plot
res@gsnLeftString = "JJA average"
    
plot1 = gsn_csm_contour_map(wks1,diff_precip_avg,res)

a = gsn_csm_vector(wks1,diff_u_avg, diff_v_avg, vcres)
    
overlay(plot1,a)

pnlres = True
pnlres@gsnPanelLabelBar  = True

gsn_panel(wks1,plot1,(/1,1/),pnlres)


;draw(plot1)
;frame(wks1)
end