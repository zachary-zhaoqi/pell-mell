# 制作为windows服务的方法

需要用到`python32`（python的win32库）

继承`win32serviceutil.ServiceFramework`类并实现其方法即可

服务运行时会自动调用`SvcDoRun()`函数
