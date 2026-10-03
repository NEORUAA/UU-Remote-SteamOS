[English](../../controller-agent.md) · [简体中文](controller-agent.md)

[简体中文 · UU Remote Ubuntu Plus](../../../i18n/README.zh-Hans.md)

# UU 控制端 CLI 与远程代理

## 用途与命令

在 UU 4.34.0.8979 中观察到的 `uuyc-cli.exe` 与官方控制端同目录，通过本地 IPC 联系已登录的 GUI/服务器。桥接器安装的 `uu-agent` 从运行中的 systemd 服务发现专用 X 显示、Xauthority、Wine 前缀与控制端路径，使用官方接口。

已观察到的命令：

```text
version
user info|wallet
device list|connect|disconnect|status
cloudpc list|launch|shutdown|connect|disconnect
echo
term
```

更新 UU 后运行 `uu-agent cli --help`，按当前安装版本列出的命令编写自动化。

## 本地包装器

```bash
uu-agent version
uu-agent list
uu-agent status
uu-agent runtime
```

`runtime` 显示路径和显示号；`list` 可能输出设备名称与 ID，留作私有诊断。专用显示的窗口、焦点与截图命令如下：

```bash
uu-agent windows
uu-agent focus '网易UU远程'
capture="$(uu-agent snapshot)"
printf '%s\n' "$capture"
```

截图默认写入 `~/.local/state/uu-remote-agent/captures`，文件权限 `0600`，不要放入 Git。

## Mac 终端代理

对具有终端功能且有权访问的 Mac，可打开 shell：

```bash
uu-agent term 'Mac device name' --shell zsh --new-session
```

非交互输入示例：

```bash
printf '%s\n' \
  'sw_vers' \
  'xcodebuild -version' \
  'xcrun simctl list devices available' \
  'exit' |
  uu-agent term 'Mac device name' --shell zsh --new-session
```

从当前设备列表选择确切名称，个人设备 ID 不写死在文档或复用脚本里。终端使用远端登录用户的权限，凭据、签名密钥与破坏性操作不放进此类脚本。CLI 列出 powershell、cmd、zsh、bash，具体功能取决于被控平台和 UU 版本。

## 从 UU 进入 Ubuntu 本机终端

选择 UU 的 PowerShell 入口，安装的代理会打开 Ubuntu 用户的原生交互登录 shell，走本地终端通道。早期立即退出码 0 来自 Wine 占位 powershell.exe。安装与回退见 [原生 Ubuntu 终端](native-ubuntu-terminal.md)。

## 图形操作

Xcode、模拟器、系统设置和钥匙串等需要视觉交互时使用：

```bash
uu-agent connect 'Mac device name'
uu-agent windows
uu-agent snapshot
```

确认远程窗口出现再发送输入，按当前分辨率重新发现窗口并查看新截图。购买、账号发布、凭据输入或破坏性确认保持人工操作。
