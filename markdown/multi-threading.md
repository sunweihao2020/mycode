---
title: multi-threading
date: 2022-04-10 19:34:00
title: python多进程
tags: python
comment: 'valine'
categories: computer
---

# 网上资料

[(48条消息) python多线程详解（超详细）_笨小孩哈哈的博客-CSDN博客_python 多线程](https://blog.csdn.net/weixin_40481076/article/details/101594705)

https://realpython.com/intro-to-python-threading/

>Getting multiple tasks running simultaneously requires a non-standard implementation of Python, writing some of your code in a different language, or using `multiprocessing` which comes with some extra overhead.
>
>Because of the way CPython implementation of Python works, threading may not speed up all tasks. This is due to interactions with the [GIL](https://realpython.com/python-gil/) that essentially limit one Python thread to run at a time.

> If a program is running `Threads` that are not `daemons`, then the program will wait for those threads to complete before it terminates. `Threads` that *are* daemons, however, are just killed wherever they are when the program is exiting.

非守护进程的话要等所有线程结束后，程序才结束。如果线程设置为守护进程，那么主程序结束之后，该线程立马去世
