---
title: 计算机知识
date: 2022-04-20 10:20:02
tags: computer
---





# 给普通用户赋予root权限：

https://zhuanlan.zhihu.com/p/67882734

这里使用的是第三种方法，亲测可行



# 在win的git bash下面安装rsync并使用

[Add rsync to Windows Git Bash | by Prasanna Wijesiriwardana | Medium](https://prasaz.medium.com/add-rsync-to-windows-git-bash-f42736bae1b3)



# WGET下载网页下所有资源文件

[wget命令下载页面里所有资源文件 - marklove - 博客园 (cnblogs.com)](https://www.cnblogs.com/marklove/p/14817043.html)

```shell
wget -F -B -c -r -np -k -L -p www.iro.umontreal.ca/~panneton/well/
```

上面这个可以



# 获取文件夹大小

[(63条消息) Python获取文件及文件夹大小_Always0nTheWay的博客-CSDN博客_python 计算文件夹大小](https://blog.csdn.net/wukai_std/article/details/54946636)



# 使用心得：

## 新服务器的ssh设置

修改

```shell
vi /etc/ssh/sshd_config
```

```
FROM:
#PermitRootLogin prohibit-password
TO:
PermitRootLogin yes
```

```
sudo systemctl restart ssh
sudo passwd
```

注意要设置root的密码



<font color=red>这里我只给新用户root权限但是不设置ssh里面允许root登陆的话，是登陆不上去的</font>
