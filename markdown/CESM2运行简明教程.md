---
title: CESM2运行简明教程
date: 2022-06-18 14:13:44
tags: CESM2
---





本文以CESM2.2.0为例，结合自己平时使用的案例简单介绍一下CESM2运行的基本流程，因为本人也不算是模式方面的专家，如有遗漏请多包涵（抱拳）。

# 一般来说CESM2运行分为以下几个步骤：

1. 新建case
2. 设置使用核数、跑多少年、重新提交多少次、reset文件输出频次等设置
3. 修改各个分量的namelist（可选项）
4. 修改源代码（可选项）
5. 编译与提交

下面我将分别对以上几步进行介绍



## 1.新建case

这里假定CESM2已经成功的安装到了电脑上，且config等文件都已经在$HOME/.cime/路径下面配置好了，那么新建case的脚本在

{CESM_HOME}/cime/scripts 路径下 其中{CESM_HOME}是cesm2软件根目录所在的位置，该路径下的create_newcase即为运行创建case的脚本，关于此脚本详细的使用说明可以输入

```shell
./create_newcase --help
```

来进行查看。

这里举一个示例来说明用法

```shell
./create_newcase --case test_1 --res f09_t061 --compset B1850MOM --run-unsupported --compiler intel --mach oneapi
```

--case  后面跟的是你给这个case所取的名字，这里我取名为test1

--res     告诉脚本你想给这个case使用什么样的分辨率，CESM2里面提供了各种各样的分辨率配置，所有的分辨率及详细介绍可见[CESM2.2.0 Grid Resolution Definitions (ucar.edu)](https://www.cesm.ucar.edu/models/cesm2/config/grids.html)常见情况是下划线前面是大气与陆面（这俩常用同一个）的格点，下划线后面是海洋的格点，这里我选用的是f09_t061，在前面的网页中搜索，结果如下，嗯大气与陆面大约是1°的分辨率，海洋分辨率大约是0.66°

[![-2022-06-18-143543.md.png](https://z4a.net/images/2022/06/18/-2022-06-18-143543.md.png)](https://z4a.net/image/2n9VeP)

--compset  命令是设置使用什么样的模式组合，CESM2软件本身给我们提供了多种多样的模式配置，很多时候我们进行试验只需要其中几个分量模式运转，亦或者想让所有分量模式都参与运转。比如有时候我们希望只跑陆气耦合实验，海洋模式让它不运转，或者我们想跑全耦合实验，等等配置通过设置compset的值我们可以达到目的，正如它的全称所示：compset = component set。详细的compset介绍可见[CESM2.2.0 Component Sets Definitions (ucar.edu)](https://www.cesm.ucar.edu/models/cesm2/config/compsets.html)。通过缩略名的首字母我们可以判断在这个compset中有哪些模式参与了工作，这里引一张官方示意图

[![-2022-06-18-144701.md.png](https://z4a.net/images/2022/06/18/-2022-06-18-144701.md.png)](https://z4a.net/image/2n9HYn)

根据这张图，回到我们的示例，这里我们用的是B1850MOM，可知用的是全耦合的实验。如果开头是F的话，那么海洋海冰模式是不参与运转的，需要海表面的物理量了模式就会去读取现成的SST文件。

--run-unsupported  的作用是：因为cesm2会给某些compsets设置“官方的”分辨率，表示这个分辨率是经过他们验证，充分可靠的，譬如FHIST的官方支持分辨率为f09_f09_mg17，但假如你就是想用f09_g17这个分辨率呢，也是可以跑。在创建case的时候不加--run-unsupported后面是会报错的。因此这个设置我理解的意思就是官方说“你小子用这个分辨率跑出来奇怪的结果可别找我，谁让你不用官方的分辨率”，哈哈开个玩笑。

后面两个--compiler 与 --mach 是与你在一直模式过程中设置的config文件有关的，以--mach为例，指定了值后模式会进入~/.cime/config_machines.xml文件中读取与这个值相匹配的设置，并用到case的创建中，--compiler与之同理。这些应归于移植模式的设置，这里就不做讨论了。

<font size=6>以上是关于第一步创建case的介绍</font>

输入上述命令后如果不报错，成功出现以case名的文件夹，就说明成功了。



## 2.核数、年份等设置

新建完case，那么就要开始对模式进行设置，此时模式的状态如下：

[![ceeb653ely8gzmw4b464pj20c408gq38.jpg](https://z4a.net/images/2022/06/18/ceeb653ely8gzmw4b464pj20c408gq38.jpg)](https://z4a.net/image/2n9dn9)

因此我们要告诉模式都要让他干什么，进入新创建的case文件夹后，对变量的修改推荐使用文件夹下的./xmlchange与./xmlquery脚本

这里列举几个常用到的设置示例

```shell
./xmlchange NTASKS=-10
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=6
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
```

下面分点对上述的命令进行讲解：

1. 关于核数的设置，一般cesm2在超算上跑，需要对模式使用的核数进行设置，这里我给NTASKS的值为-10，复数表示节点数，假如一个节点有28个核，那么最后我调用的总核数就是28*10=280核。如果仅设置NTASKS的话，那么所有的分量都使用这个配置，若想对不同的分量模式给予不同的设置，可以分别设置NTASKS_ATM NTASKS_OCN等等。直接对NTASKS进行设置固然省事，但合理地对不同分量模式设置核数可以提高运算速度+节约计算时间（钱），这里推荐一篇文章里面比较详细地介绍了核数的设置，因本文旨在介绍运行的一般流程，故不做展开[ CESM2 实验笔记_一株草的世界的博客-CSDN博客](https://blog.csdn.net/qq_38607066/article/details/109445839)

2. STOP_OPTION应该跟STOP_N配合着来看，STOP_N+STOP_OPTION告诉模式运转 X（单位），这里我给STOP_N = 2, STOP_OPTION=nyears，因此模式就运转两年，但如果STOP_OPTION=nmonths，那么就是模式运行2个月，ndays就是2天。
3. 关于RESUBMIT，一般在超算上单次任务是有时间限制的，比如12个小时，超过这个值了就给你kill掉，因此我们要结合模式模拟的时间对任务进行分割并多次提交。这里我设置RESUBMIT为6，那么在模式跑完第一个2年后，模式会自动提交，接着跑两年，结束后再次自动提交，那么最终我们的模式跑了2+（6*2）=14年。
4. REST_N和REST_OPTION这两个量也是配合起来看的，因为模式再重新提交之后它需要读取restart文件，才可以继续往下跑。这两个设置就是设置restart文件的输出频率，这里我设置的含义即为每2年输出一次start文件。

以上是关于模式设置几个常用到的量，但是不能覆盖所有情况，所有的量以及介绍可以在[CESM2 Driver Caseroot Variable Definitions (ucar.edu)](https://www.cesm.ucar.edu/models/cesm2/settings/current/drv_input.html)中找到。



上述变量设置完毕后就可以执行

```shell
./case.setup
```

上述变量就被读入模式设置里了



## 3.namelist的设置

执行上述命令以后，模式会在当前文件夹下生成下面几个文件，格式均为user_nl_ + 分量名

[![-2022-06-18-153550.png](https://z4a.net/images/2022/06/18/-2022-06-18-153550.png)](https://z4a.net/image/2n981J)

如果不去修改这些文件，那么在编译的过程中模式会读取默认的设置，但如果你想对某些设置进行修改，那么就在这个文件下进行替换。那样的话模式在编译的过程中就会将你新给的量替换掉默认的设置。这里改哪个分量模式就去修改哪个namelist文件，譬如我要对大气模式进行修改那么就去改user_nl_cam文件

官方主页有关于所有设置的介绍，这里分享链接[CESM2 Component Configuration Settings (ucar.edu)](https://www.cesm.ucar.edu/models/cesm2/settings/current/index.html)

譬如你想增加输出的变量，那么就在user_nl_cam文件中的空白处加一行

```
fincl2         = 'U:A','V:A','OMEGA:A','T:A','PRECT:A','SHFLX:A','LHFLX:A','Q:A','TS:A'
nhtfrq         = 0,-24
mfilt          = 12,1
```

那么模式在运行过程中输出变量就会有一组新的变量，等号右边的这些量。':A'表示’平均的意思‘，nhtfrq意思为输出频率，负数代表“小时”，0表示“月平均”，mfilt表示一个文件里有几个时间样本。

那么上述三行综合起来看就是，在我新增加的这些变量，每24小时输出一次（-24），得到的值为在这24小时内的平均值，每个文件包含1个时次。nhtfrq的0和mfilt的12是对大气模式默认的输出进行设置。后面的（-24，1）则是对应fincl2的设置。



## 4. 源代码的修改

有时候需要对模式进行深层次的修改，那么就需要修改源代码。模式源代码位置在{CESM_HOME}/component下面，一般是不在这里进行模式代码的修改的。如果需要修改的话就找到相应的模式代码把它拷贝到case目录下面的SourceMods对应位置，在编译的时候就自动会将新的代码覆盖掉旧的代码了。



## 5. 编译

如果不需要进行源代码的修改，再进行完第三步就可以输入

```
./case.build
```

进行编译了，编译成功后./case.submit脚本是提交运算的脚本，但如果在超算上面提交的话是需要写一个提交脚本再提交的，以上就是cesm2运行的一般流程。
