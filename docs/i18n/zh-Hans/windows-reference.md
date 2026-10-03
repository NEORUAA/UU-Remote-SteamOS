[English](../../windows-reference.md) · [简体中文](windows-reference.md)

[首页](../../../i18n/README.zh-Hans.md)

# Windows 参考对照

使用同一 UU 版本的 Windows 安装，对照主机服务、输入设备和控制端行为，了解 Windows 与 Wine 的输入路径。

## 安装布局

通过 Windows 服务的 `PathName` 查明实际安装位置。以下为通用目录示例：

```text
C:\path\to\GameViewer
C:\path\to\GameViewer\bin\GameViewerService.exe --service
C:\path\to\GameViewer\bin\drivers\gvInput\gvinput.sys
C:\path\to\GameViewer\bin\drivers\gvInput\gvinputmf.sys
```

Windows 的 `GameViewerService` 与 `gvinput` 驱动提供内核 HID 输入路径。设备管理器和 UU 日志可识别 `ROOT\HIDCLASS`、`HID\GVINPUT` 设备及键盘集合；Wine 则使用桥接器的用户态输入路径。

## 只读检查命令

在 PowerShell 中查询服务并查看可执行文件路径，把下方示例目录换成 `PathName` 中的实际安装根目录：

```powershell
Get-Service GameViewerService
Get-CimInstance Win32_Service -Filter "Name='GameViewerService'" |
  Select-Object Name, State, PathName
$installRoot = 'C:\path\to\GameViewer'
Get-ChildItem (Join-Path $installRoot 'bin\drivers\gvInput')
Get-PnpDevice | Where-Object InstanceId -Match 'GVINPUT'
```

日志位于安装目录的 `log\server`、`log\service` 和 `log\client`。对照相关服务与输入状态，分享片段前去掉账号和设备信息。

## 真实主控测试

用 Windows UU 打开 Ubuntu 设备，确认实时桌面、鼠标点击、新终端、快捷键和文字输入。普通断开并重连一次，检查同一桌面是否继续可用；较长会话中同时观察服务与控制端操作。

## 仓库内容

仓库提供桥接器的用户态实现；Windows `gvinput` 驱动、证书、网易二进制和账号状态保留在各自安装环境中。
