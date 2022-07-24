---
title: python learning
date: 2022-04-05 10:39:02
tags: python
categories: computer
---

# python知识码

[python的slice函数](https://stackoverflow.com/questions/509211/understanding-slice-notation)

---

关于波浪线 ~

它的作用起到了一个补码的作用

[波浪线](https://blog.csdn.net/lanchunhui/article/details/51746477)

---

### lambda函数

[匿名函数](https://www.liaoxuefeng.com/wiki/1016959663602400/1017451447842528)

---

### 关于一个插值实现的记录

对于零散的nan值怎么进行插值处理，这里的做法是把所有非nan的数据抽出来组成没有缺测的数组，然后再插入到原来的网格中，妙



---

python保存为PDF文件

[Python中的绘图(论文中保存成PDF不失真) - helloHKTK - 博客园 (cnblogs.com)](https://www.cnblogs.com/helloHKTK/p/12483478.html)



##





---

### 关于隐循环

```python
file_prect    =  [x for x in file1 if ("PRECT-" in x)]
```

一个例子，假如我要挑选在某个列表里满足条件的文件



## cartopy一个教程

https://zhajiman.github.io/post/cartopy_introduction/



## 还有这种赋值方法

```python
lonmin,lonmax,latmin,latmax = 30,120,-10,30
```



## python在字符串前面加u

[python字符串前面加u_Honghong的博客-CSDN博客_python字符串前加u](https://blog.csdn.net/CherryChanccc/article/details/82428220)



## 打出上下标的方法

```python
plt.plot(x_data, x_data**3, label = '$x^3$')
n="x\u00b2"
```



## python 格式化输出

[python中几种格式化输出 的用法_下雨天再见的博客-CSDN博客](https://blog.csdn.net/weixin_43213268/article/details/88932999)



---

# python中的科学计算

### 关于使用xarray来截取时间的操作

```python
file  =  xr.open_dataset(path+"HadISST_sst.nc")
start_time = '1980-01-01'
end_time   = '2019-12-31'
time_slice = slice(start_time, end_time)
sst   =  file["sst"].sel(time=time_slice)
```

这里start和end_time中和dataset里面的时间并不对应，但是却可以把分割出我想要的时间段

dataset里面的时间长这样：

![image-20210831170356576.png](https://z4a.net/images/2022/04/05/image-20210831170356576.png)

总之这样是可以的，很神奇，嗯

---

使用xarray来对dimension进行查看

![image-20210906164823478.png](https://z4a.net/images/2022/04/05/image-20210906164823478.png)

可以使用f2.nj来看，也是直接跟名字就好，但是基本上这类不过是自然数的累加而已

## numpy.interp

[参考网站](https://numpy.org/doc/stable/reference/generated/numpy.interp.html#numpy-interp)

[Interpolate NaN values in a numpy array](https://stackoverflow.com/questions/6518811/interpolate-nan-values-in-a-numpy-array)



## numpy中的引用问题

有时候多维数组，但我只想固定某一维度，其余的不想输了，要不要把所有的：,都加上

```python
a.shape
> (12, 37, 192, 288)
a[11].shape
> (37, 192, 288)
a[:,11].shape
> (12, 192, 288)
a[10,:].shape
> (37, 192, 288)
```

以上为一些例子



## 跳点取值

```python
u.lon.data[::20]
```

结果是每隔20个取一个



## 取消科学记数法

np.set_printoptions(suppress=True)



## 矩阵内只对符合条件的数据进行运算

```python
>>import numpy as np
>>arr = np.random.rand(5,5) # 5x5的随机数组
>>arr
array([[ 0.36401504,  0.87729325,  0.53453396,  0.5031851 ,  0.90744627],
       [ 0.44607108,  0.22673265,  0.77539262,  0.84064101,  0.41774629],
       [ 0.91686641,  0.71480639,  0.09617148,  0.41535823,  0.4175782 ],
       [ 0.25753864,  0.73196495,  0.43557823,  0.97497112,  0.54451645],
       [ 0.58167148,  0.50382906,  0.88490307,  0.77238085,  0.17427672]])
>>mask = arr>0.5 # 选取数组中元素大于0.5的元素的bool数组
>>mask
array([[False,  True,  True,  True,  True],
       [False, False,  True,  True, False],
       [ True,  True, False, False, False],
       [False,  True, False,  True,  True],
       [ True,  True,  True,  True, False]], dtype=bool)
>>arr[mask] = 0 # 将数组中大于0.5的值设为0
>>arr
array([[ 0.36401504,  0.        ,  0.        ,  0.        ,  0.        ],
       [ 0.44607108,  0.22673265,  0.        ,  0.        ,  0.41774629],
       [ 0.        ,  0.        ,  0.09617148,  0.41535823,  0.4175782 ],
       [ 0.25753864,  0.        ,  0.43557823,  0.        ,  0.        ],
       [ 0.        ,  0.        ,  0.        ,  0.        ,  0.17427672]])
```



## 模式后处理的插值函数

注意虽然没有缺测，但是位势高度会出现负值，这点需要特别注意



## python滤波平滑教程

https://blog.csdn.net/weixin_42782150/article/details/107176500

滑动平均：

https://stackoverflow.com/questions/13728392/moving-average-or-running-mean



## python中对包含nan值的函数

https://numpy.org/doc/stable/reference/generated/numpy.nanmean.html



## 计数numpy中符合条件元素的个数

https://blog.csdn.net/qq_18351157/article/details/107448247

思想是先生成一个bool的数组再用np.count_nonzero()



## isel的用法

xarray中isel的用法是针对位置来进行选择的，这里给出一个例子

```python
april  =  [x*12+3 for x in range(0,120)]
f  =  xr.open_dataset("/home/sun/data/HadISST_sst.nc").isel(time=april)
```

如是便可以把每年的四月挑出来了



## 并行计算学习

资料：

[(48条消息) python多线程详解（超详细）_笨小孩哈哈的博客-CSDN博客_python 多线程](https://blog.csdn.net/weixin_40481076/article/details/101594705)

https://realpython.com/intro-to-python-threading/





# matplotlib

## plot绘制2d图样式

[matplotlib.pyplot.plot — Matplotlib 3.4.3 documentation](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html#matplotlib.pyplot.plot)

一个是关于markers，一个是关于line style



## 设置线段样式

设置线段样式的三种方法

```python
plt.plot(x, y, linewidth=2.0)
```

```python
line, = plt.plot(x, y, '-')
line.set_antialiased(False) # turn off antialiasing
```

```python
lines = plt.plot(x1, y1, x2, y2)
# use keyword args
plt.setp(lines, color='r', linewidth=2.0)
# or MATLAB style string value pairs
plt.setp(lines, 'color', 'r', 'linewidth', 2.0)
```

官网网址关于点线虚线什么的

https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html



## 生成多个figure和subpolt

```python
import matplotlib.pyplot as plt
plt.figure(1)                # the first figure
plt.subplot(211)             # the first subplot in the first figure
plt.plot([1, 2, 3])
plt.subplot(212)             # the second subplot in the first figure
plt.plot([4, 5, 6])


plt.figure(2)                # a second figure
plt.plot([4, 5, 6])          # creates a subplot() by default

plt.figure(1)                # figure 1 current; subplot(212) still current
plt.subplot(211)             # make subplot(211) in figure1 current
plt.title('Easy as 1, 2, 3') # subplot 211 title
```

这里注意从figure2调到figure1需要执行命令，此时指向figure1中的subpolt(212),因此还得再指向plt.subplot(211)

<span style='color:red;background:white;font-size:16;font-family:楷体;'>小结：在画图之前你需要指定在哪个figure，有axes还需指定在哪个subplot</span>



---

## 任意设置子图在指定位置

[Axes Demo — Matplotlib 3.4.3 documentation](https://matplotlib.org/stable/gallery/subplots_axes_and_figures/axes_demo.html)



---

## 直方图

[matplotlib.pyplot.hist — Matplotlib 3.4.3 documentation](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.hist.html#matplotlib.pyplot.hist)



## 在python里面打数学公式

[Writing mathematical expressions — Matplotlib 3.4.3 documentation](https://matplotlib.org/stable/tutorials/text/mathtext.html)



## 调整子图的教程

https://matplotlib.org/stable/tutorials/intermediate/gridspec.html



## Constrained Layout 的用法 

https://blog.csdn.net/MTandHJ/article/details/90272935



## contour等值线合集

### 官方contour教程

https://matplotlib.org/stable/gallery/images_contours_and_fields/contour_demo.html

### contour设置

```python
im   =  ax.contour(f1.lon,f1.level,avg_theta,np.linspace(-2,4,15),linewidths=0.9,colors='b')
rcParams["contour.negative_linestyle"] = 'solid' # 设置负数的线段样式
```

注意设置contour的负数样式并不能直接在contour函数里面搞，需要像第二行那样搞



## Tick设置



### 调整坐标轴标签和刻度之间的距离

```python
ax.tick_params(pad=0.2)
```



### 使用预定义的刻度设置

https://matplotlib.org/stable/gallery/ticks_and_spines/tick-formatters.html



### 经纬度的ticklabel形式

```python
# 设置Formatter.
if xformatter is None:
    xformatter = LongitudeFormatter()
if yformatter is None:
    yformatter = LatitudeFormatter()
ax.xaxis.set_major_formatter(xformatter)
ax.yaxis.set_major_formatter(yformatter)
```

这样的话会自动转换成经纬度形式的labels，不需要我再自己搞tick_labels了



## 设置绘图的范围

需求：比如我只想在原图的基础上只画某个范围内的图像，只需要对x轴进行设置就好。

```python
plt.xlim(xmin=60,xmax=130)
plt.ylim(ymin=-0.5,ymax=0.5)

#ax的方法
ax.set_xlim(xmin=60,xmax=200)
ax.set_ylim(ymin=-0.5,ymax=1.5)
```

在这个范围之外的就不会再有了



## 设置x轴y轴标题

```python
ax1.set_xlabel('time')
ax1.set_ylabel('s1 and s2')
```



## 关于刻度

```python
'''这条命令定义了两个major刻度之间分成多少份'''
ax.xaxis.set_minor_locator(AutoMinorLocator(10))

```



## 设置coutour等值线的label有一个单独的函数

https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.clabel.html

https://matplotlib.org/stable/api/contour_api.html?highlight=inline#matplotlib.contour.ContourLabeler.calc_label_rot_and_inline



## 双y轴

https://www.cnblogs.com/atanisi/p/8530693.html



## 倒转y轴

https://stackoverflow.com/questions/2051744/reverse-y-axis-in-pyplot

```python
plt.gca().invert_yaxis()
```



## 怎么给NAN值赋颜色

```shell
plt.gca().set_facecolor("black")
```



## histgram 教程

https://matplotlib.org/stable/gallery/statistics/hist.html



## 绘制bar图

https://www.jianshu.com/p/47dfbe43dae1 讲调整柱子颜色的



## matplotlib 颜色列表

https://finthon.com/matplotlib-color-list/



## colormap参考列表

https://matplotlib.org/stable/gallery/color/colormap_reference.html



### 一个第三方colormap

https://github.com/1313e/CMasher



## 调整视图的长宽比

```python
axs.set(aspect=0.5)
```

https://jdhao.github.io/2017/06/03/change-aspect-ratio-in-mpl/



## 像素图

https://matplotlib.org/stable/gallery/images_contours_and_fields/contour_image.html#sphx-glr-gallery-images-contours-and-fields-contour-image-py



## colormap的设置教程

1. [Creating Colormaps in Matplotlib — Matplotlib 3.5.1 documentation](https://matplotlib.org/stable/tutorials/colors/colormap-manipulation.html)

   ```python
   viridis = cm.get_cmap('viridis', 256)
   newcolors = viridis(np.linspace(0, 1, 256))
   pink = np.array([248/256, 24/256, 148/256, 1])
   newcolors[:25, :] = pink
   newcmp = ListedColormap(newcolors)  #注意这最后一步是把一堆rgb array生成一个数组
   ```

2. [Customized Colorbars Tutorial — Matplotlib 3.5.1 documentation](https://matplotlib.org/stable/tutorials/colors/colorbar_only.html)

   这里面主要是看extend两边的颜色设置



## 关于边框（xy轴）的设置（粗细、颜色）

https://stackoverflow.com/questions/4761623/how-to-change-the-color-of-the-axis-ticks-and-labels-for-a-plot-in-matplotlib



## CMAP教程

https://matplotlib.org/stable/tutorials/colors/colormaps.html

### cmap名字后面加r等于反过来

```python
cmap = 'Blues'
cmap = 'Blues_r'
```



### 第三方cmap库

[Palettable (jiffyclub.github.io)](https://jiffyclub.github.io/palettable/)



## 流线中的箭头样式设置

https://matplotlib.org/stable/api/_as_gen/matplotlib.patches.FancyArrowPatch.html#matplotlib.patches.FancyArrowPatch

注意，对于'<-'这种箭头，方向是反着的



## 绘制streamplot的例子

https://matplotlib.org/stable/gallery/images_contours_and_fields/plot_streamplot.html



## 添加文本

[(9条消息) Python可视化31|matplotlib-图添加文本(text)及注释(annotate)_pythonic生物人的博客-CSDN博客](https://blog.csdn.net/qq_21478261/article/details/108290310)



## Unidata中的各种例子

https://unidata.github.io/python-training/gallery/gallery-home/



## 文本框的样式实例

https://matplotlib.org/3.1.1/gallery/pyplots/whats_new_98_4_fancy.html#sphx-glr-gallery-pyplots-whats-new-98-4-fancy-py



## matplotlib里面有一个很多教程的集合网站

[Tutorials — Matplotlib 3.5.0 documentation](https://matplotlib.org/stable/tutorials/)

点进去在左边框



## 第三方colorbar库

[Palettable (jiffyclub.github.io)](https://jiffyclub.github.io/palettable/)



## 给等值线添加图例

https://github.com/matplotlib/matplotlib/issues/11134



## 关于刻度label的大小设置

```python
ax.tick_params(labelsize=labelsize)
```

参考网站

https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.tick_params.html

labelsize一个是可以设置具体值，还有就是设置字符串

字符串选项xx-small, x-small, small, medium, large, x-large, xx-large, larger, smaller



## 给刻度线加上label

```python
ax.clabel(im2, np.linspace(2,12,6), inline=True, fontsize=12)
```



## tick_params 对坐标轴刻度的设置

官方文档 https://matplotlib.org/3.5.0/api/_as_gen/matplotlib.axes.Axes.tick_params.html

这里以labelsize设置，如果只想设置x或者y轴的话

```
ax1.tick_params(axis='y', labelcolor=color)
```

在里面指定一下就好了



## subplots与add_subplot之间的subplot_kw

在使用cartopy画图的过程中，添加地图映射用的是这个语句

```python
ax = fig1.add_subplot(projection=proj)
```

我很好奇那如果使用plt.subplots可以给添加地图映射么？

在官网给出的例子里是这样的：

```python
fig, axs = plt.subplots(2, 2, subplot_kw=dict(projection="polar"))
```

有了 subplot_kw 这个参数，关于这个参数的解释

> **subplot_kw**dict, optional
>
> Dict with keywords passed to the [`add_subplot`](https://matplotlib.org/3.5.0/api/figure_api.html#matplotlib.figure.Figure.add_subplot) call used to create each subplot.



## 关于colorbar的设置

起因是我想把colorbar下面的数字改大一点，参考资料：

https://stackoverflow.com/questions/23172282/how-to-change-font-properties-of-a-matplotlib-colorbar-label

```python
from matplotlib.pylab import *
from numpy import arange

pcolor(arange(20).reshape(4,5))
cb = colorbar(label='a label')
ax = cb.ax
text = ax.yaxis.label
font = matplotlib.font_manager.FontProperties(family='times new roman', style='italic', size=16)
text.set_font_properties(font)
show()
```

[![-2022-04-27-211751.md.png](https://z4a.net/images/2022/04/27/-2022-04-27-211751.md.png)](https://z4a.net/image/2kXYfa)

从这里我们可以知道：

1. cb = colorbar(label='a label') 这句话调用之后返回的是一个句柄，也就是后面的ax
2. 让我惊奇的是后面的text也是ax能够返回的对象，还有用这种方法来设置fontproperties，以及最后的set_font_properties

**学习了学习了**

关于对colorbar labelsize的设置：

```python
a = fig.colorbar(im,shrink=0.6, pad=0.05)
a.ax.tick_params(labelsize=8)
```

跟上面一样，也是在返回的句柄上进行操作，这里注意tick_params这个函数

文档：https://matplotlib.org/3.5.0/api/_as_gen/matplotlib.axes.Axes.tick_params.html

## legend

### 官方教程

https://matplotlib.org/3.1.1/tutorials/intermediate/legend_guide.html



### 线图的legend控制label的颜色跟线的颜色一致

```py
labelcolor='linecolor'

ax.legend(loc='upper left',prop={'size': 25},labelcolor='linecolor')
```



## 关于画图过程中字典形式的传入参数

举例、积累：

```python
ax.quiverkey(q, X=quiver_x, Y=quiver_y, U=speed,
                    label=f'{speed} m/s', labelpos='S', labelsep=0.1,fontproperties={'size':18})

```



## 设置-自我总结

1. 关于相互重叠啊，跑出去了啊等等问题

   加plt.tight_layout()让它自己调整

2. range()也是不包含尾端的

3. 在绘制等值线图的时候，关闭extend = both，超过的值不会画，会造成有白斑出现



### 打出°的上标

```python
u'' + str(xxxx) + "\N{DEGREE SIGN}"

```

### 上标下标的教程

[python为字体添加上下标_Mr.horse的博客-CSDN博客_python怎么打上角标](https://blog.csdn.net/weixin_38314865/article/details/89392911?spm=1001.2101.3001.6650.1&utm_medium=distribute.pc_relevant.none-task-blog-2~default~CTRLIST~default-1.nonecase&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2~default~CTRLIST~default-1.nonecase)

### pad参数调整子图之间的距离

```python
ig1, axes = plt.subplots(1,2,figsize = (16,7))
fig1.tight_layout(pad = 1) #pad参数设置子图之间的间隔 
```



### tips

label不一定要是文本，数字也可以



### contour中的线段设置问题

设置了cmap后再设置negative_linestyle无法呈现负值对应虚线的效果

```python
im   =  ax.contour(f1.lon,f1.level,avg_theta,np.linspace(-2,4,15),linewidth=0.9,cmap='Blues',negative_linestyle='dashed')
```



### 调整矢量图的箭头稀疏程度

目前没找到现成的函数，我发现可以跳点画

```python
q  =  ax.quiver(f2.lon[::4], f2.level[::2], uwind[::2,::4], omega[::2,::4], 
                angles='uv',# regrid_shape这个参数越小，是两门就越稀疏
                scale_units='xy', scale=1.5,        # scale是参考矢量，所以取得越大画出来的箭头就越短
                units='xy', width=2,
                color='b')
```





# 函数

## matplotlib.axes.Axes.pcolormesh

https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.pcolormesh.html



## matplotlib.pyplot.colorbar

https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.colorbar.html#matplotlib.pyplot.colorbar



## numpy.average

[numpy.average — NumPy v1.21 Manual](https://numpy.org/doc/stable/reference/generated/numpy.average.html)



## matplotlib.patches.Circle

https://matplotlib.org/stable/api/_as_gen/matplotlib.patches.Circle.html



## isinstance函数 

https://blog.csdn.net/wanglei_storage/article/details/52849081



## matplotlib中的流线函数

https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.streamplot.html#matplotlib.axes.Axes.streamplot



## strip函数

用来去掉字符串头尾的特殊字符，比如换行符



## main函数

注意在main函数中我发现由于main函数里面的值是非全局变量，再调用外部函数的话，会因为无全局变量而不错，因此编写的外部函数要有传入参数



## 在pycharm中设置运行断点

```python
# %%
```



## 函数中的参数问题

没有指定函数值的参数要放在前面，指定了函数值的要放在后面，不能乱



### xarray读取era数据存在的问题

似乎无法处理short类型数据，无法获取factor和offset这些量



# debug

## cartopy设置与添加水平线

添加水平线用到的函数hlines()给的是xmin和xmax

但是在实际操作中并不能对上，需要进行调整，原因目前还没搞清



## jupyterlab中的设置密码问题

网上给的教程有问题，真正的教程在jupyterlab的config文件里面可以找到

```python
from jupyter_server.auth import passwd; passwd()
```



## cartopy加载地图信息显示下载失败

[(7条消息) Cartopy加载地图信息报错 TimeoutError: [WinError 10060\]_会计师-CSDN博客](https://blog.csdn.net/weixin_50569998/article/details/108814321)

地图信息储存的服务器有问题，下载github里面的资料再放进去



## cartopy地图只画出来一半

```python
f   =  plt.figure(figsize=(10,5))
ax  =  f.add_subplot(
    111,
    projection=ccrs.PlateCarree()
)
ax.streamplot(
    u.lon,u.lat,
    u1,v1,
    transform=ccrs.PlateCarree()
)
ax.coastlines()
plt.show()

```

![image-20210921145438951.png](https://z4a.net/images/2022/04/05/image-20210921145438951.png)

```python
f   =  plt.figure(figsize=(10,5))
ax  =  f.add_subplot(
    111,
    projection=ccrs.PlateCarree(central_longitude=0)
)
ax.streamplot(
    u.lon,u.lat,
    u1,v1,
    transform=ccrs.PlateCarree()
)
ax.coastlines()
plt.show()
```

加了一个central的设置后就好了，原因目前不明



## cartopy 中的set_extent

在设置刻度的时候可能会覆盖之前设置的ax.set_extent，所以这个语句要放在刻度设置的后面，覆盖回去



# cartopy

## 设置边界线的粗细

```
ax.add_feature(cf.COASTLINE, lw=2) #lw参数
```





# matplotlib画图总结

## 2021/11/15 时间序列

![image-20211115092534567.png](https://z4a.net/images/2022/04/05/image-20211115092534567.png)

```python
fig,axs  =  plt.subplots(tight_layout=True)

# axs.set_yticks(np.arange(90, 160,10))

axs.bar(year,day-120,width=1,color=color_list,edgecolor='black') # 使用自定义的柱的颜色 定义边缘的颜色
# 刻度设置
axs.set_xlim(1979,2020)
axs.xaxis.set_major_locator(MultipleLocator(5))  # 设置大刻度和小刻度
axs.xaxis.set_minor_locator(MultipleLocator(1))  # 注意只设置小刻度是出不来的，得先设置大刻度

axs.set_yticks(np.arange(-20,25,5))
axs.set_yticklabels(y_label)

axs.plot([1979,2020],[0,0],color='black')
axs.plot([1979,2020],[np.ceil(np.mean(day)-np.std(day))-120,np.ceil(np.mean(day)-np.std(day))-120],color='k',linestyle='dashed')
axs.plot([1979,2020],[np.floor(np.mean(day)+np.std(day))-120,np.floor(np.mean(day)+np.std(day))-120],color='k',linestyle='dashed')

axs.set_aspect(0.5)  # 调整图像的长宽比

plt.savefig('/home/sun/paint/lunwen/bob_time_seris.pdf',dpi=350)

plt.show()

```





## 矢量图绘制

![image-20211115211956868.png](https://z4a.net/images/2022/04/05/image-20211115211956868.png)

```python
lonmin,lonmax,latmin,latmax  =  30,120,-10,30
extent     =  [lonmin,lonmax,latmin,latmax]

proj = ccrs.PlateCarree()
fig  = plt.figure()
ax   = fig.add_subplot(111, projection=proj)

set_map_ticks(ax, dx=10, dy=10, nx=1, ny=1, labelsize='small')
ax.set_extent(extent, crs=proj)
ax.coastlines(resolution='10m',lw=1)

ax.plot([30,120],[0,0],linestyle='dashed',color='grey')

im  =  ax.contourf(f3.lon,f3.lat,late_prect,levels=np.linspace(2,18,9),cmap='Blues',alpha=1,extend='both')

q  =  ax.quiver(lon, lat, 
                  late_u, late_v, 
          regrid_shape=15, angles='uv',   # regrid_shape这个参数越小，是两门就越稀疏
        scale_units='xy', scale=1,        # scale是参考矢量，所以取得越大画出来的箭头就越短
        units='xy', width=0.25,
        transform=proj,
                  color='k',linewidth=1.2,headlength = 5, headaxislength = 4, headwidth = 5
)

rect = mpl.patches.Rectangle(
        (0.88, 0.8), 0.12, 0.2, transform=ax.transAxes,    # 这个能辟出来一块区域，第一个参数是最左下角点的坐标，后面是矩形的长和宽
        fc='white', ec='k', lw=0.5, zorder=1.1
    )
ax.add_patch(rect)

qk = ax.quiverkey(
        q, X=0.94, Y=0.93, U=5,
        label=f'{5} m/s', labelpos='S', labelsep=0.08,
    )
```



## 多张子图共用一个colorbar

![image-20211124142236875.png](https://z4a.net/images/2022/04/05/image-20211124142236875.png)



```python
dates  =  [-12,-9,-6,-3,0,3] #总共6张图
date   =  [18,21,24,27,30,33]
props = dict(boxstyle='square', edgecolor='white', facecolor='white', alpha=1)

proj    =  ccrs.PlateCarree()
fig1    =  plt.figure(figsize=(14,12))
    
for j in range(1,6,2):
    ax = fig1.add_subplot(3,2,j,projection=proj)  #这里添加子图的方式是（行，列，index）默认是从左往右，所以想从上往下要处理一下
    ax.coastlines(resolution='110m',lw=1)
    # 设置经纬度刻度.
    set_map_ticks(ax, dx=10, dy=10, nx=1, ny=1, labelsize='small')
    ax.set_extent(extent, crs=proj)
    
    ax.plot([40,120],[0,0],'k--')
    im  =  ax.contourf(f2.lon,f2.lat,f2.T2M.data[date[int((j-1)/2)],:],levels=np.linspace(280,310,16),cmap='coolwarm',alpha=1,extend='both')
    if dates[int((j-1)/2)] <= 0:
        ax.text(0.825,0.825,"D"+str(dates[int((j-1)/2)]),transform=ax.transAxes,bbox=props,fontsize=15)
    else:
        ax.text(0.825,0.825,"D+"+str(dates[int((j-1)/2)]),transform=ax.transAxes,bbox=props,fontsize=15)
        
for j in range(2,7,2):
    ax = fig1.add_subplot(3,2,j,projection=proj)
    ax.coastlines(resolution='110m',lw=1)
    # 设置经纬度刻度.
    set_map_ticks(ax, dx=10, dy=10, nx=1, ny=1, labelsize='small')
    ax.set_extent(extent, crs=proj)
    
    ax.plot([40,120],[0,0],'k--')
    im  =  ax.contourf(f2.lon,f2.lat,f2.T2M.data[date[int(j/2+2)],:],levels=np.linspace(280,310,16),cmap='coolwarm',alpha=1,extend='both')
    if dates[int(j/2+2)] <= 0:
        ax.text(0.825,0.825,"D"+str(dates[int(j/2+2)]),transform=ax.transAxes,bbox=props,fontsize=15)
    else:
        ax.text(0.825,0.825,"D+"+str(dates[int(j/2+2)]),transform=ax.transAxes,bbox=props,fontsize=15)
            
       

fig1.subplots_adjust(top=0.8) #整体往上紧凑来给下面的colorbar增加空间

cbar_ax = fig1.add_axes([0.2, 0.05, 0.6, 0.03])  #依次是左端 下端 宽度 高度
fig1.colorbar(im, cax=cbar_ax, shrink=0.5, pad=0.2, orientation='horizontal') #这样画就可以了
```

## 2021/12/28 垂直流场、等值线、等值填色

![image-20211228152302834.png](https://z4a.net/images/2022/04/05/image-20211228152302834.png)

```python
# 创建画布
fig  =  plt.figure()
ax   =  fig.add_subplot()
ax.invert_yaxis()

# 绘制等值线
im1   =  ax.contour(f1.lon,f1.level,avg_theta,np.linspace(-2,4,13),linewidth=0.9,colors='grey',negative_linestyle='dashed')
im2   =  ax.contourf(f4.lon,f4.level,div,10,cmap='seismic',extend='both')
q  =  ax.quiver(f2.lon[::4], f2.level[::2], uwind[::2,::4], omega[::2,::4], 
                angles='uv',# regrid_shape这个参数越小，是两门就越稀疏
                scale_units='xy', scale=1.5,        # scale是参考矢量，所以取得越大画出来的箭头就越短
                units='xy', width=2,
                color='k')
fig.colorbar(im2,label='divergence units: ${10^6}$ ${s^-1}$') # 注意这里怎么加上标

# 添加地形
ax2  =  ax.twinx()
ax2.set_ylim((0,4.5))
#ax2.set_yticks(np.arange(0,21,1))
ax2.plot(f5.lon.data,topo/1000,color='k')
ax2.fill_between(f5.lon.data,0,topo/1000,where=topo>0,color='k')

ax2.set_yticklabels([])  # 这里把刻度设置成无
ax2.set_yticks([])

```



## 关于自制colormap与配合uigradient

uigradient网址

[uiGradients - Beautiful colored gradients](https://uigradients.com/#WeddingDayBlues)

![image-20220309161441953.png](https://z4a.net/images/2022/04/05/image-20220309161441953.png)

直接复制了粘贴进puthon里即可，python是认这玩意儿的

自制colormap例子

```python
from pylab import *
from matplotlib.colors import ListedColormap,LinearSegmentedColormap
clist=['#40E0D0','#FF8C00','#FF0080']

newcmp = LinearSegmentedColormap.from_list('chaos',clist)
```



# numpy计算总结

### 函数返回值问题

```python
def get_flist(path,var):
    list1  =  [x for x in os.listdir(path) if (var+"-" in x)]
    return list1.sort()

id  =  get_flist(path_id,"V")
```

注意，返回值是.sort()的话最后结果什么也没有，必须要sort完再返回

## xarray中的slice问题

注意使用slice挑选的时候是需要考虑顺序的，不是说可以反过来在这个范围内即可



## 利用隐循环计算pentad平均





## 交换象限

https://numpy.org/doc/stable/reference/generated/numpy.swapaxes.html



# xarray

## 关于获取dataarray dataset一些属性的知识

[Data Structures (xarray.dev)](https://docs.xarray.dev/en/stable/user-guide/data-structures.html)



# python资源网址记录

## Iris 一个处理地球科学数据的软件包

https://scitools-iris.readthedocs.io/en/latest/generated/gallery/index.html#sphx-glr-generated-gallery



## matplotlib官网的gallery，记载着很多种例子加代码

https://matplotlib.org/stable/gallery/images_contours_and_fields/contour_label_demo.html



## 一个教程，说的是关于python中main函数的

https://realpython.com/python-main-function/



## real python 一个python学习网站

[Python Tutorials – Real Python](https://realpython.com/)



## 从知乎上看到的几个学习网站

[The Hitchhiker’s Guide to Python! — The Hitchhiker's Guide to Python (python-guide.org)](https://docs.python-guide.org/)

[Python 3 Module of the Week — PyMOTW 3](https://pymotw.com/3/)

[Welcome to Python for you and me — Python for you and me 0.5.beta1 documentation (pymbook.readthedocs.io)](https://pymbook.readthedocs.io/en/latest/)

[py.CheckiO - Python coding challenges and exercises with solutions for beginners and advanced](https://py.checkio.org/)
