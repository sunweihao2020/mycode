---
title: frp内网穿透踩坑
date: 2022-05-20 10:17:00
tags:
---

using tianyi yun and ubuntu to do frp

bug mainly from the cloud computer's 安全组,要记得该过程中所有的端口都要在安全组里面放行，且是“入方向”

tianyiyun的密码是19970130SWh@



<font color=red> 2022-7-13补</font>： 客户端frpc.ini的remote端口也要在安全组里设置好放行
