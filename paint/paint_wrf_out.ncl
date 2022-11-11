load "$NCARG_ROOT/lib/ncarg/nclscripts/esmf/ESMF_regridding.ncl"
begin
;---Open WRF output file
  filename = "/home/sun/data/model_data/wrf_out/wrfout_d03_2022-10-30_23:00:00"    ; Add the ".nc" here". Actual file doesn't have this.
  a        = addfile(filename,"r")

;---Read temperature at first time step
  tc2 = wrf_user_getvar(a,"T2",0)      ; T2 in Kelvin
  tc2 = tc2-273.16                     ; T2 in C
  tc2@units = "degC"

;---Attach 2D coordinates
  tc2@lat2d = a->XLAT(0,:,:)
  tc2@lon2d = a->XLONG(0,:,:)

  minlon  = min(tc2@lon2d)-2   ; Do this to add a border around the
  minlat  = min(tc2@lat2d)-2   ; data in the plots. Not required.
  maxlon  = max(tc2@lon2d)+2
  maxlat  = max(tc2@lat2d)+2

;----------------------------------------------------------------------
; Start the regridding
;----------------------------------------------------------------------
  interp_method         = "bilinear"

  Opt                   = True

  Opt@InterpMethod      = interp_method

  Opt@SrcRegional       = True

  Opt@DstRegional       = True
  Opt@DstLLCorner       = (/ minlat,minlon /)
  Opt@DstURCorner       = (/ maxlat,maxlon /)

  Opt@ForceOverwrite    = True

;---Regrid using two different resolutions
  Opt@DstGridType    = "0.25deg"
  Opt@WgtFileName    = "WRF_to_0_25deg.nc"
  tc2_regrid_0_25deg = ESMF_regrid(tc2,Opt)

  Opt@DstGridType     = "0.125deg"
  Opt@WgtFileName     = "WRF_to_0_125deg.nc"
  tc2_regrid_0_125deg = ESMF_regrid(tc2,Opt)

  printVarSummary(tc2_regrid_0_25deg)
  printVarSummary(tc2_regrid_0_125deg)

;----------------------------------------------------------------------
; Start the graphics
;----------------------------------------------------------------------
  wks = gsn_open_wks("png","wrf_gsn")

  res                        = True

  res@gsnDraw                = False   ; Will panel later
  res@gsnFrame               = False

  res@cnFillOn               = True  
  res@cnFillPalette          = "BlAqGrYeOrReVi200"
  res@cnLinesOn              = False
  res@cnLineLabelsOn         = False
  res@cnLevelSelectionMode   = "ManualLevels"
  res@cnLevelSpacingF        =  2
  res@cnMinLevelValF         = 10
  res@cnMaxLevelValF         = 38

  res@lbLabelBarOn           = False

  res@pmTitleZone            = 4
  res@pmTickMarkDisplayMode  = "Always"
  res@mpOutlineBoundarySets  = "GeophysicalAndUSStates"
  res@mpGeophysicalLineColor = "gray"
  res@mpUSStateLineColor     = "gray"
  res@mpNationalLineColor    = "gray"

  res@mpDataBaseVersion      = "MediumRes"
  res@mpLandFillColor        = "beige"
  res@mpOceanFillColor       = "lightblue"
  res@mpInlandWaterFillColor = "lightblue"

  res@mpMinLonF              = minlon
  res@mpMinLatF              = minlat
  res@mpMaxLonF              = maxlon
  res@mpMaxLatF              = maxlat

  res@gsnRightString         = ""

;---Create contours of original data
  res@gsnLeftString  = "Original data (" + str_join(""+dimsizes(tc2)," x ") +")"
  plot_orig = gsn_csm_contour_map(wks,tc2,res)

;---Create contours of regridded data
  res@gsnAddCyclic   = False
  res@gsnLeftString  = "Regridded to 0.25 deg"
  plot_regrid_0_25deg = gsn_csm_contour_map(wks,tc2_regrid_0_25deg,res)

  res@gsnLeftString  = "Regridded to 0.125 deg"
  plot_regrid_0_125deg = gsn_csm_contour_map(wks,tc2_regrid_0_125deg,res)

;----------------------------------------------------------------------
; Draw both plots in one panel.
;----------------------------------------------------------------------
  pres                  = True
  pres@gsnMaximize      = True
  pres@txString         = "WRF output data - " + tc2@description + " (" + tc2@units + ")"
  pres@gsnPanelLabelBar = True
  pres@gsnPanelRowSpec  = True
  pres@pmLabelBarWidthF = 0.7

  gsn_panel(wks,(/plot_orig,plot_regrid_0_25deg,plot_regrid_0_125deg/),(/1,2/),pres)

;---Add grid lines at lat/lon locations to all three plots and panel again.
  lnres                  = True
  lnres@gsLineColor      = "Gray25"
  lnres@gsLineThicknessF = 1.0
  lnres@gsnCoordsAsLines = True
  lnres@gsnCoordsAttach  = True 
  gsn_coordinates(wks,plot_orig,tc2,lnres)
  gsn_coordinates(wks,plot_regrid_0_25deg,tc2_regrid_0_25deg,lnres)
  gsn_coordinates(wks,plot_regrid_0_125deg,tc2_regrid_0_125deg,lnres)

  gsn_panel(wks,(/plot_orig,plot_regrid_0_25deg,plot_regrid_0_125deg/),(/1,2/),pres)

end
