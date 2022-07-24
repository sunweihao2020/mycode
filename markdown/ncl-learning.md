---
title: ncl-learning
date: 2022-07-01 12:50:38
tags:
---



# BUG

## Segmentation fault (core dumped) **核心已转储**

这个问题出现是由于变量由python生成的话，缺测值是nan，需要把nan替换掉，就不会出这种错误了



# 设置

## 流线streamline

```
res@stArrowStride              = 3
```

