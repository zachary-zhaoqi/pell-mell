# Secedit.exe 命令行工具

## 此命令的语法为

```shell
secedit [/configure | /analyze | /import | /export | /validate | /generaterollback]
```

### secedit /configure  |配置组策略

允许你用保存在数据库中的安全性设置来配置系统。

#### 此命令的语法为

```shell
secedit /configure /db filename [/cfg filename] [/overwrite][/areas area1 area2...] [/log filename] [/quiet]
```

|||
-|-
/db filename|指定用来执行安全性配置的数据库。
/cfg filename|指定在配置次计算机前要导入到数据库的安全性模板。安全性模板是用安全性模板管理单元创建的。
/overwrite|指定在导入安全性模板前数据库应该被清空。如果没有指定此参数，在安全性模板中指定的将累积到数据库中。如果没有指定此参数而且在数据库中的设置与要导入的模板冲突，将采用模板中的设置。
/areas|指定要应用到系统的安全性范围。如果没有指定此参数，在数据库中定义的所有安全性设置都将应用到系统中。要配置多个范围，用空格将它们分开。下列安全性范围将被导出:<li>SECURITYPOLICY包括帐户策略，审核策略，事件日志设置和安全选项。</li><li>GROUP_MGMT包括受限制的组设置</li><li>USER_RIGHTS包括用户权限分配</li><li>REGKEYS包括注册表权限</li><li>FILESTORE包括文件系统权限</li><li>SERVICES包括系统服务设置</li>
/log filename|指定要记录配置操作状态的文件。如果没有指定，配置操作信息将被记录到 scesrv.log 文件中，此文件为于 %windir%\security\logs 目录。
/quiet|指定配置操作的执行不需要提示用户进行任何确认。

#### 示例

`secedit /configure /db hisecws.sdb /cfg hisecws.inf /overwrite /log hisecws.log`

对于所有的文件名，如果没有指定路径，则是用当前目录。

### secedit /analyze    |分析组策略

### secedit /import     |导入组策略

### secedit /export     |导出组策略

允许你导出保存在数据库中的安全设置。

#### 此命令的语法为

```shell
secedit /export [/db filename] [/mergedpolicy] /cfg filename [/areas area1 area2...] [/log filename]
```
|||
-|-
/db filename|指定要导出数据的数据库。如果没有指定，将使用系统安全数据库。
/cfg filename|指定要导出数据库内容的安全模板。
/mergedpolicy|合并并且导出域和本地策略安全设置。
/areas|指定要应用到系统的安全性范围。如果没有指定此参数，在数据库中定义的所有安全性设置都将应用到系统中。要配置多个范围，用空格将它们分开。下列安全性范围将被导出:<li>SECURITYPOLICY包括帐户策略，审核策略，事件日志设置和安全选项。</li><li>GROUP_MGMT包括受限制的组设置</li><li>USER_RIGHTS包括用户权限分配</li><li>REGKEYS包括注册表权限</li><li>FILESTORE包括文件系统权限</li><li>SERVICES包括系统服务设置</li>
/log filename|指定要记录导出操作状态的文件。如果没有指定，配置操作信息将被记录到 scesrv.log file 中，此文件为于 %windir%\security\logs 目录。

#### 示例

`secedit /export /db hisecws.sdb /cfg hisecws.inf /log hisecws.log`

对于所有的文件名，如果没有指定路径，则是用当前目录。

### secedit /validate   |验证模板语法

### secedit /generaterollback |更新组策略

## inf文件

### 结构

INF文件其实是一种纯文本文件，可以用任意一款文本编辑软件来打开进行编辑，如：记事本、写字板等。INF文件有一整套的编写规则，每一个INF文件都是严格按照这些规则来编写的。

- 规则一
INF文件是分节的，每一个INF文件有许多的节组成，节名用方括号括起来。这些节名有些是系统定义好的，有一些是用户自定义的。每一个节名最长为255个字符（Windows 2000/XP/2003操作系统中）或28个字符（Windows 98操作系统中）。节与节之间没有先后顺序的区别，另外，同一个INF文件中如果出现两个同样的节名，则系统会自动将这两个节名下面的条目合并到一起。
- 规则二
在节与节之间的内容叫条目，每一个节又是由许多的条目组成的，每一个条目都是由形如“signature="$CHICAGO$"”的形式组成的。如果每一个条目的等号后有多个值，则每一个值之间用“，”号分隔开。
- 规则三
INF文件对大小写不敏感。
- 规则四
“；”号后面的内容为注释。
- 规则五
如果一个条目的内容过多，在一行无法书写完全，则用“\”将一行内容书写为多行。
