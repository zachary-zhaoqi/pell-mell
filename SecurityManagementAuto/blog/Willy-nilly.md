# 一些未归类的笔记

## python中print打印显示颜色

显示颜色的格式：
` \ 033 [显示方式;字体色;背景色m ...... [\ 033 [0m] `  
显示方式|效果|字体色|背景色|颜色描述
-|-|-|-|-
0|终端默认设置|30|40|黑色
1|高亮显示|31|41|红色
4|使用下划线|32|42|绿色
5|闪烁|33|43|黄色
7|反白显示|34|44|蓝色
8|不可见|35|45|紫红色
|||36|46|青蓝色
|||37|47|白色
[本文为CSDN博主「Mr-Liuqx」的原创文章](https://blog.csdn.net/qq_34857250/article/details/79673698)


## Python 获取Windows管理员权限

我们在运行我们编写好的python代码时，会碰到这样的报错问题

```
PermissionError: [WinError 5] 拒绝访问。
```

这是因为我们编写的脚本的权限不够。一种解决办法是在管理员cmd中运行我们的脚本（右键以 run as administrator），但是这种办法不够优雅。我们经常看到当我们运行一些需要高权限的软件时，会弹出以下对话框


这被称为用户安全控制，简称为UAC。

用户帐户控制（User Account Control，简写作UAC)是微软司在其Windows Vista及更高版本操作系统中采用的一种控制机制。其原理是通知用户是否对应用程序使用硬盘驱动器8)和系统文件授权，以达到帮助阻止恶意程序（有时也称为“恶意软件”）损坏系统的效果。
那么我们在写代码的时候怎么添加这个功能呢？

这里我们要用到一个关键的函数ShellExecute
```c
HINSTANCE ShellExecute(
  _In_opt_ HWND    hwnd,
  _In_opt_ LPCTSTR lpOperation,
  _In_LPCTSTR lpFile,
  _In_opt_ LPCTSTR lpParameters,
  _In_opt_ LPCTSTR lpDirectory,
  _In_INTnShowCmd
);
```
具体细节看微软官方的文档[ShellExecute function](https://docs.microsoft.com/zh-cn/windows/win32/api/shellapi/nf-shellapi-shellexecutea?redirectedfrom=MSDN)

```python
from __future__ import print_function
import ctypes, sys

def is_admin():
    try:
   return ctypes.windll.shell32.IsUserAnAdmin()
    except:
   return False
if is_admin():
    # 将要运行的代码加到这里
else:
    if sys.version_info[0] == 3:
    	ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    else:#in python2.x
   ctypes.windll.shell32.ShellExecuteW(None, u"runas", unicode(sys.executable), unicode(__file__), None, 1)
```
要提醒你的是，不要在IDE中运行。

如果在非管理员权限下运行的话，其实这里运行了两次代码，第一次肯定是没有管理员权限的，第二次拥有管理员权限。

有的时候我们不希望有这种UAC弹框，我们希望程序偷偷的拥有管理员权限，这要怎么做呢？这其实挺邪恶的。感兴趣的话，可以看这篇
[python如果获取windows管理员权限（二）](https://blog.csdn.net/qq_17550379/article/details/79006718)

---  
[本文为CSDN博主「coordinate_blog」的原创文章](https://blog.csdn.net/qq_17550379/article/details/79006655)

## ShellExecute详细用法(可以单独打开一个文件)

hellExecute的功能是运行一个外部程序，或者打开一个已注册的文件、打开一个目录、打印文件等等功能，它可以打开电脑内的任何文件，也可以打开URL。

函数的原型：
```
HINSTANCE ShellExecute( 
    HWND hwnd, 
    LPCTSTR lpOperation,
    LPCTSTR lpFile, 
    LPCTSTR lpParameters, 
    LPCTSTR lpDirectory, 
    INT nShowCmd
);
```

1. hWnd:

    用于指定父窗口的句柄。当函数调用过程中出现错误时，它将作为Windows消息窗口的父窗口。

1. lpOperation：

    用于指定要进行的操作，当参数为NULL时，默认操作"open"。

   "open"，表示执行由lpFile参数指定的程序，或者打开由lpFile参数指定的文件或文件夹。

    "explort"，表示打开由lpFile参数指定的文件夹。

    "print",表示打印由lpFile参数指定的文件。

1. lpParameters：

    若lpFile参数是一个可执行文件，则此参数指定命令行参数，否则此参数应设为NULL。

1. lpDirectory：

    用于指定默认目录。

1. nShowCmd：

    用于指定程序窗口初始显示方式。 
    ||||
    |:-|:-|:-|
    |#define SW_HIDE|0|隐藏窗体，并激活另一个窗体|
    |#define SW_SHOWNORMAL|1|与SW_RESTORE相同
    |#define SW_SHOWMINIMIZED|2|激活并以最小化的形式显示窗体
    |#define SW_SHOWMAXIMIZED|3|激活并以最大化的形式显示窗体
    |#define SW_MAXIMIZE|3|最大化指定的窗体
    |#define SW_SHOWNOACTIVATE|4|以上次的状态显示指定的窗体，但不激活它
    |#define SW_SHOW|5|激活窗体，并将其显示在当前的大小和位置上
    |#define SW_MINIMIZE|6|最小化指定的窗体，并激活另一个窗体
    |#define SW_SHOWMINNOACTIVE|7|以最小化形式显示指定的窗体，但不激活它
    |#define SW_SHOWNA|8|以当前的状态显示指定的窗体，但不激活它
    |#define SW_RESTORE|9|以原本的大小和位置，激活并显示指定的窗体
    |#define SW_SHOWDEFAULT|1|0 设置显示的状态由STARTUPINFO结构体指定