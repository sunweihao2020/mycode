;2021/8/17
;本代码为检查控制实验和关闭感热实验之间的差异
begin
;读取三个感热实验
path  =  "/home/sun/test1/"
f1    =  addfile(path+"close_all.cam.h1.1979-03-24-00000.nc","r")
f2    =  addfile(path+"close_all.cam.h1.1979-04-26-00000.nc","r")
f3    =  addfile(path+"close_all.cam.h1.1979-05-10-00000.nc","r")

;读取三个控制实验
path2 = "/home/sun/cesm_output/control/atm/hist/"
c1    =  addfile(path2+"control.cam.h1.1979-03-24-00000.nc","r")
c2    =  addfile(path2+"control.cam.h1.1979-04-26-00000.nc","r")
c3    =  addfile(path2+"control.cam.h1.1979-05-10-00000.nc","r")