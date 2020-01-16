# windows组策略配置检查 参数说明

导出安全策略：`secedit /export /cfg model.inf`  
导入全案策略：`secedit /configure /db model.sdb /cfg gp.inf /quiet`  
参考模板：`%windir%\security\templates`  

## 1 审核口令设置安全策略

密码必须符合复杂性要求 `PasswordComplexity = 1`  
密码长度最小值 `MinimumPasswordLength = 8`  
密码最长使用期限 `MaximumPasswordAge = 42`  
密码最短使用期限 `MinimumPasswordAge = 1`  
强制密码历史 `PasswordHistorySize = 24`  
用可还原的加密来储存密码 `ClearTextPassword = 0`  
复位帐户锁定计时器 `ResetLockoutCount = 15`  
帐户锁定时间 `LockoutDuration = 15`  
帐户锁定阈值 `LockoutBadCount = 15`  

## 2 审核策略

审核策略更改：`AuditPolicyChange = 3` // 成功、失败  
审核登录事件：`AuditLogonEvents = 3` // 成功、失败  
审核对象访问：`AuditObjectAccess = 3` // 成功、失败  
审计过程跟踪：`AuditPrivilegeUse = 0` //无审核  
审计目录服务访问：`AuditProcessTracking = 0` //无审核  
审核特权使用：`AuditDSAccess = 0` //无审核  
审核系统事件：`AuditSystemEvents = 3` // 成功、失败  
审核帐户登录事件：`AuditAccountLogon = 1` // 成功  
审核帐户管理：`AuditAccountManage = 2` //失败  

## 3 Microsoft网络服务器

设置在挂起会话之前的所需的空闲时间 15分钟`MACHINE\System\CurrentControlSet\Services\LanManServer\Parameters\AutoDisconnect=4,15`  
数字签名的通信（若客户端同意） 已启用`MACHINE\System\CurrentControlSet\Services\LanManServer\Parameters\RequireSecuritySignature=4,1`  
当登录时间用完时自动注销用户 已启用`MACHINE\System\CurrentControlSet\Services\LanManServer\Parameters\EnableForcedLogOff=4,1`

## 4 Microsoft网络客户端

建议设置数字签名的通信（总是） 已启用`MACHINE\System\CurrentControlSet\Services\LanmanWorkstation\Parameters\RequireSecuritySignature=4,1`  
数字签名的通信（若服务器同意） 已启用`MACHINE\System\CurrentControlSet\Services\LanmanWorkstation\Parameters\EnableSecuritySignature=4,1`  
发送未加密的密码到第三方SMB服务器 已禁用`MACHINE\System\CurrentControlSet\Services\LanmanWorkstation\Parameters\EnablePlainTextPassword=4,0`

## 5 交互式登录设置

建议设置不显示上次登录的用户名 已启用`MACHINE\Software\Microsoft\Windows\CurrentVersion\Policies\System\DontDisplayLastUserName=4,1`  
不需要按Ctrl+Alt+Del 已禁用`MACHINE\Software\Microsoft\Windows\CurrentVersion\Policies\System\DisableCAD=4,0`  
在密码到期前提示用户更改密码建议最小设置 14天
`MACHINE\Software\Microsoft\Windows`  
`NT\CurrentVersion\Winlogon\PasswordExpiryWarning=4,14`  
智能卡移除操作 锁定工作站
`MACHINE\Software\Microsoft\Windows`  `NT\CurrentVersion\Winlogon\ScRemoveOption=1,”1″`  

## 6 网络访问

1. 允许匿名SID/名称 转换 已禁用；
LSAAnonymousNameLookup = 1
2. 不允许SAM帐户的匿名枚举 已启用；
RestrictAnonymousSAM=4,1
3. 不允许SAM帐户和共享的匿名枚举 已启用；
RestrictAnonymous=4,1
4. 不允许为网络身份验证储存凭证或.net passports 已启用；
MACHINE\System\CurrentControlSet\Control\Lsa\DisableDomainCreds=4,1
5. 让每个人（Everyone）权限应用于匿名用户 已禁用；
MACHINE\System\CurrentControlSet\Control\Lsa\EveryoneIncludesAnonymous=4,0
6. 限制匿名访问命名管道和共享 已启用；
MACHINE\System\CurrentControlSet\Services\LanManServer\Parameters\RestrictNullSessAccess=4,1
7. 本地帐户的共享和安全模式 经典；
MACHINE\System\CurrentControlSet\Control\Lsa\ForceGuest=4,0
8. 可匿名访问的命名管道 无；
MACHINE\System\CurrentControlSet\Services\LanManServer\Parameters\NullSessionPipes=7,
9. 可远程访问的注册表路径

MACHINE\System\CurrentControlSet\Control\SecurePipeServers\Winreg\AllowedExactPaths\Machine=7,System\CurrentControlSet\Control\ProductOptions,System\CurrentControlSet\Control\Server Applications,Software\Microsoft\Windows NT\CurrentVersion

## 7 网络安全

不要在下次更改密码时存储LAN manager的哈希值 已启用；
MACHINE\System\CurrentControlSet\Control\Lsa\NoLMHash=4,1

LAN manager身份验证级别 仅发送 NTLMv2响应\拒绝 LM；
MACHINE\System\CurrentControlSet\Control\Lsa\LmCompatibilityLevel=4,4

LDAP客户端签名要求 协商签名；
MACHINE\System\CurrentControlSet\Services\LDAP\LDAPClientIntegrity=4,1

基于NTLM SSP（包括安全RPC）服务器的最小会话安全 Require Message Integrity, Message Confidentiality,NTLMv2 Session Security, 128-bit Encryption ；
MACHINE\System\CurrentControlSet\Control\Lsa\MSV1_0\NTLMMinServerSec=4,537395248

基于NTLM SSP（包括安全RPC）客户端的最小会话安全为Require Message Integrity, Message Confidentiality,NTLMv2 Session Security, 128-bit Encryption MACHINE\System\CurrentControlSet\Control\Lsa\MSV1_0\NTLMMinClientSec=4,537395248

## 8 故障恢复控制台

允许系统自动管理级登录 已禁用。
MACHINE\Software\Microsoft\Windows NT\CurrentVersion\Setup\RecoveryConsole\SecurityLevel=4,0

## 9 关机

清除虚拟内存页面文件 已启用；
MACHINE\System\CurrentControlSet\Control\Session Manager\Memory Management\ClearPageFileAtShutdown=4,1

允许系统在未登录前关机 已禁用。
MACHINE\System\CurrentControlSet\Control\Session Manager\Memory Management\ClearPageFileAtShutdown=4,0

## 10 系统加密

存储在计算机上的用户密钥强制使用强密钥保护 用户每次使用密钥时必须键入密码。

MACHINE\Software\Microsoft\Windows\CurrentVersion\Policies\System\ShutdownWithoutLogon=4,1
MACHINE\Software\Policies\Microsoft\Cryptography\ForceKeyProtection=4,2

## 11 系统对象

由管理员（administrators）组成员所创建的对象的默认所有者 对象创建者；

MACHINE\System\CurrentControlSet\Control\Lsa\NoDefaultAdminOwner=4,1

增强内部系统对象的默认权限 已启用。

MACHINE\System\CurrentControlSet\Control\Session Manager\ProtectionMode=4,1

## 12 帐户

来宾帐户状态 已禁用；
EnableGuestAccount = 0

使用空白密码的本地帐户只允许进行控制台登录 已启用；
MACHINE\System\CurrentControlSet\Control\Lsa\LimitBlankPasswordUse=4,1

重命名系统管理员帐户不要使用administrator；

NewAdministratorName = “Administrator”

## 13 设备设置

允许格式化与弹出可移动媒体 administrators；
MACHINE\Software\Microsoft\Windows NT\CurrentVersion\Winlogon\AllocateDASD=1,”0″

防止用户安装打印机驱动程序 已启用
MACHINE\System\CurrentControlSet\Control\Print\Providers\LanMan Print Services\Servers\AddPrinterDrivers=4,1

未签名驱动程序的安装操作 允许安装但发出警告。
MACHINE\Software\Microsoft\Driver Signing\Policy=3,1

1.14 域成员
对安全通道数据进行数字加密或签名（总是） 已启用；
MACHINE\System\CurrentControlSet\Services\Netlogon\Parameters\RequireSignOrSeal=4,1

对安全通道数据进行数字签名（如果可能） 已启用；
MACHINE\System\CurrentControlSet\Services\Netlogon\Parameters\SealSecureChannel=4,1

禁用更改机器帐户密码 已禁用；

MACHINE\System\CurrentControlSet\Services\Netlogon\Parameters\DisablePasswordChange=4,0

最长机器帐户密码寿命 30天；
MACHINE\System\CurrentControlSet\Services\Netlogon\Parameters\MaximumPasswordAge=4,30

需要强会话密钥 已启用。

MACHINE\System\CurrentControlSet\Services\Netlogon\Parameters\RequireStrongKey=4,1

有了这些对应关系,做检查时即可用脚本来自动检查,并将不合格的项排出,具体脚本可参考如下:

@echo off
:: +———————————————+
:: Script Title : Windows_Safe_Check
:: date : 2012-02-22
:: Author : FeiFei(http://jafee.net)
:: Tested on : Windows 2003 SP2
:: +———————————————+

if exist no.txt (del no.txt)
cls
echo 正在进行 “审计与帐户策略” 安全检查
echo > list.txt PasswordComplexity = 1
echo >> list.txt MinimumPasswordLength = 8
echo >> list.txt MaximumPasswordAge = 42
echo >> list.txt MinimumPasswordAge = 1
echo >> list.txt PasswordHistorySize = 5
echo >> list.txt ClearTextPassword = 0
echo >> list.txt ResetLockoutCount = 15
echo >> list.txt LockoutDuration = 15
echo >> list.txt LockoutBadCount = 15
echo >> list.txt AuditPolicyChange = 3
echo >> list.txt AuditLogonEvents = 3
echo >> list.txt AuditObjectAccess = 3
echo >> list.txt AuditPrivilegeUse = 0
echo >> list.txt AuditProcessTracking = 0
echo >> list.txt AuditDSAccess = 0
echo >> list.txt AuditSystemEvents = 3
echo >> list.txt AuditAccountLogon = 3
echo >> list.txt AuditAccountManage = 3

secedit /export /cfg model.inf >nul

for /F “tokens=1,3″ %%i in (list.txt) do (
call :Getgp %%i %%j
)
ping 127.0.0.1 /n 2 >nul
del tmp.txt
del list.txt
del model.inf
goto :EOF
:Getgp
find “%1″ model.inf >tmp.txt
for /f “skip=2 tokens=3″ %%i in (tmp.txt) do (
if “%%i”==”%2″ (echo %1=%%i ok) else (echo %1 策略不符合规则>>bad.txt)
)

goto :EOF  
