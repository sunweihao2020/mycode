;2022/1/8
;所用资料：composite-merra2-single.nc merra2合成分析后的2m风场
;内容： 分解为流函数和势函数
begin
f = addfile("/home/sun/qomo-data/composite-merra2-single.nc","r")

u  =  f->U2M
v  =  f->V2M

sf =  u
vp =  u

uv2sfvpf(u, v, sf, vp)



sf@longname  =  "stream function"
vp@longname  =  "velocity potential function"

fout  =  addfile("/home/sun/data/composite-single_merra2_stream_vp_function.nc","c")

filedimdef(fout, "time", -1, True)

fout->stream_function  =  sf
fout->velocity_potential_function  =  vp

end