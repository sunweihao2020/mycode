; 2022-10-27
; This code test the vector

load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/shea_util.ncl"

begin

;---Read in netCDF file
path_out   =  "/home/sun/data/model_data/climate/"
file_out1  =  "b1850_control_atmospheric_monthly_average.nc"
file_out2  =  "b1850_maritime_atmospheric_monthly_average.nc"
f0         =  addfile(path_out + file_out1,  "r")
f1         =  addfile(path_out + file_out2,  "r")

;---Read in zonal [u] and meridional [v] winds (July)
  u = f0->U(6,6,:,:)                             
  v = f0->V(6,6,:,:)

  printVarSummary(u)

  u@_FillValue   =  9999
  v@_FillValue   =  9999
if (any(isnan_ieee(u))) then
  replace_ieeenan (u, u@_FillValue, 0)
  replace_ieeenan (v, v@_FillValue, 0)

end if

;---Create plot
  wks = gsn_open_wks("png","vector")               ; send graphics to PNG file

  vcres                         = True             ; plot mods desired
  vcres@gsnFrame                = False            ; so we can draw time stamp
  vcres@vcRefAnnoOrthogonalPosF = -1.0             ; move ref vector up
  vcres@vcRefMagnitudeF         = 10.0             ; define vector ref mag
  vcres@vcRefLengthF            = 0.045            ; define length of vec ref
  vcres@vcGlyphStyle            = "CurlyVector"    ; turn on curly vectors
  vcres@vcMinDistanceF          = 0.017

  vector = gsn_csm_vector_map(wks,u,v,vcres)

;---Add time stamp to plot
  infoTimeStamp(wks,0.025,"uv300.nc")      ; arguments are workstation
                                           ; size of text desired, and
                                           ; right string.         
  frame (wks)  
end