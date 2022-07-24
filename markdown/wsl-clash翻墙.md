---
title: wsl-clash翻墙
date: 2022-06-06 13:44:54
tags:
---

参考：

[解决WSL下使用Clash for Windows的记录 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/451198301)

[![-2022-06-06-134621.md.png](https://z4a.net/images/2022/06/06/-2022-06-06-134621.md.png)](https://z4a.net/image/2Eb9zJ)

注意这里要使用第二个

export all_proxy="sock5://192.168.3.13:7890"

然后四个export就好了

```shell
export http_proxy='http://192.168.3.13:7890'
export https_proxy='http://192.168.3.13:7890'
export all_proxy='sock5://192.168.3.13:7890'
export ALL_PROXY= 'sock5://192.168.3.13:7890'

```

