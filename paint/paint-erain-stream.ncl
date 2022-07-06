;2021/3/15
;此代码使用erain绘制合成分析后的流场用以比较
;使用资料：composite-erain.nc
f = addfile("/data5/2019swh/data/composite-erain.nc")
u = f->u
