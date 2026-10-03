[English](../../troubleshooting.md) · [العربية](../ar/troubleshooting.md) · [Deutsch](../de/troubleshooting.md) · [Español](../es/troubleshooting.md) · [Français](../fr/troubleshooting.md) · [日本語](../ja/troubleshooting.md) · [한국어](../ko/troubleshooting.md) · [Русский](../ru/troubleshooting.md) · [Tiếng Việt](../vi/troubleshooting.md) · [简体中文](../zh-Hans/troubleshooting.md) · [繁體中文](../zh-Hant/troubleshooting.md)

[简体中文 · UU Remote Ubuntu Plus](../../../i18n/README.zh-Hans.md)

# 故障排查

## 先查看状态

在源码目录运行下列命令。日志位于 `~/.local/state/uu-remote-bridge`，持久设置位于 `~/.config/uu-remote-bridge/environment`。反馈时保留版本、症状和错误信息，去掉账号、设备、输入及剪贴板内容。安装后的源码修改需要重新安装才能进入运行环境。

```bash
uu-remote status
./scripts/verify.sh --quick
uu-remote logs
uu-remote network
```

## 离线、重启后未上线或登录异常

先用官方管理窗口完成一次登录，正常关闭窗口后桥接器会恢复。重启后离线时检查用户服务和密钥环解锁状态；密钥环密码改变后可运行 `./scripts/configure-unattended.sh enable --replace-credential` 更新加密凭据。服务运行但设备离线时，检查服务器退出与重新注入记录。

```bash
uu-remote login
./scripts/configure-unattended.sh status
journalctl --user -b -u uu-keyring-unlock.service -u uu-remote-bridge.service --no-pager
```

## 一直显示正在寻找线路

先检查主机是否完成启动。Wine 中积累的虚拟输入或蓝牙设备记录可能拖慢 UU 启动，可用事务式修复命令清理专用前缀中的已识别记录。它会备份注册表并重启 UU 桥接器，保留 Ubuntu 蓝牙与其他 Wine 应用。

```bash
uu-remote repair-registry
./scripts/verify.sh --quick
```

## 黑屏、白屏或连接了错误桌面

逐段检查 GNOME RDP、SDL 中继和 UU 捕获。确认桌面已经登录，GRD 监听配置端口；多个 GNOME 会话同时存在时查看会话列表。需要现有 XRDP 桌面可重新安装时指定 `--desktop-target xrdp`，回到物理桌面用 `--desktop-target physical`。X11 桌面可选 `--desktop-relay vnc`；Wayland 使用 RDP。

```bash
systemctl --user status uu-remote-bridge.service
/usr/bin/grdctl status
loginctl list-sessions
tail -80 ~/.local/state/uu-remote-bridge/freerdp.log
tail -80 ~/.local/state/uu-remote-bridge/gnome-remote-desktop.log
```

## 画面留白、裁切或 4K 不合适

先查看当前画布，使用图形设置选择 720p、1080p、1440p 或 4K。画布大小、UU 控制端 FPS 和码率分别设置；字体太小或网络吃紧时先选 1080p/1440p。切换会短暂重连，失败时会回退。XRDP 动态改变桌面尺寸时，还要核对源桌面尺寸。

```bash
uu-remote quality status
uu-remote quality gui
uu-remote quality apply 1080p
```

## 画面正常但点击、中文或粘贴失效

通过 `uu-remote open` 打开管理窗口，不要把同一个 Wine 前缀的 UU 直接启动到另一个 X 显示。正常关闭管理查看器可恢复中继焦点。手机输入法提交与实体键事件分开处理；更新源码后重新安装并检查输入注入器。中文、代码和多行文本还依赖当前桌面剪贴板与 RDP 粘贴路径。 首次点击就断开时，检查 UU SendInput bridge active、UU Wine event-log compatibility active 与输入代理是否运行，再用 `uu-remote restart` 恢复。

```bash
uu-remote open
./scripts/verify.sh --quick
tail -80 ~/.local/state/uu-remote-bridge/input-injector.log
```

## 按键慢、丢键或长时间使用后输入退化

比较 UU 控制端网络、VPN、代理与中继线路，再检查主机默认网卡。`uu-remote network` 的历史会话可能标为 stale。确认网卡选择有误后可选 `--network-interface default`，恢复用 `all`。实体键节奏仅在复现后试 `--physical-key-delay-ms 8`，默认为 `0`。符号位置异常先检查 Ubuntu 键盘布局；长期退化时运行验证器查看 GRD 文件描述符与 libei 状态。

```bash
uu-remote network
ip -4 route show default
```

## 光标消失或太小

光标保护默认关闭。需要时启用并让 `auto` 跟随桌面光标大小，固定大小支持 `24` 到 `128`；关闭用 `--cursor-guard off`。无需为了光标改变整个桌面分辨率或全局 Wine DPI。

```bash
./install.sh --skip-packages --skip-account-login --cursor-guard on --cursor-size auto
```

## UU 终端退出码为 0 或文字位置异常

重新安装当前桥接器并检查终端通道。在 UU 中选择 PowerShell，实际打开的是 Ubuntu 登录 shell。光标位置异常时关闭旧终端，重新建立会话。查看 `terminal-bridge.log` 中的元数据；不要把任意程序覆盖到 UU 的 powershell.exe，也不需要额外 SSH 密码或公开端口。

```bash
./install.sh --skip-packages --skip-account-login
./scripts/verify.sh --quick
./scripts/test-terminal-bridge.sh
```

## GNOME RDP 认证或 FreeRDP NLA/SSPI 错误

下列查询只检查凭据是否存在，不显示密码。需要更换时运行 `secret-tool clear service uu-desktop-bridge username "$USER"`，再重新安装保存新凭据。SSPI 错误时从同一固定版本重建 FreeRDP、WinPR 和配套 DLL，避免混用不同主版本；详见同语源码构建指南。

```bash
/usr/bin/secret-tool lookup service uu-desktop-bridge username "$USER" >/dev/null
/usr/bin/grdctl status
```

## Mac 直连 RDP/VNC、Windows App 卡在 Configuring

GNOME 桌面共享端口已由内部 FreeRDP 使用，远程登录会建立另一桌面。需要本地中继镜像时查询实际回环端口，再通过 SSH 转发；不要依赖旧显示号或旧 VNC 端口。Windows App 停在 TLS 配置阶段时，先退出并重开 Mac 客户端，再检查 XRDP 监听状态。

```bash
~/.local/bin/uu-remote-console relay-port
ss -ltnp
```

## 周期重启、意外声音与恢复卸载

完整验证器包含稳定性等待，可检查服务器周期退出和运行组件。声音异常时先用 `wpctl status` 查明实际流，再分别检查 UU 音频设置、Wine PulseAudio 与 VNC 铃声。`UURB_UU_AUDIO=system` 是兼容默认；专用静音 ALSA 的设置与恢复见[UU 专用静音 ALSA](#uu-silent-alsa)。卸载先预览，普通卸载恢复上游文件并保留专用前缀，`./uninstall.sh --purge` 会连同账号状态删除。

```bash
./scripts/verify.sh
uu-remote logs
./uninstall.sh --dry-run
```

<a id="uu-silent-alsa"></a>

## UU 专用静音 ALSA 与恢复

先确认声音来自哪个应用和设备。内部 SDL FreeRDP 使用 `/audio-mode:2`；查看实时音频流、所属进程与设备时，使用下列命令，`STREAM_OR_CLIENT_ID` 换成当前流或客户端的 ID：

```bash
wpctl status
wpctl inspect STREAM_OR_CLIENT_ID
pgrep -a -u "$UID" -f 'sdl-freerdp|GameViewer|SHI'
```

需要让 UU 静音并释放物理音频设备时，为专用 Wine 前缀提供静音 ALSA。UU 仍需要可以初始化的音频设备；只设 `UURB_UU_AUDIO=off` 可能让控制端停在连接阶段。静音 ALSA 保留这层音频接口，普通 Ubuntu 应用、XRDP 和其他 Wine 前缀继续使用原来的音频设置。

在源码目录安装模板，并为默认 UU 前缀选择 ALSA 驱动：

```bash
install -d -m 0700 ~/.config/uu-remote-bridge
install -m 0600 config/alsa-null.conf \
  ~/.config/uu-remote-bridge/alsa-null.conf

WINEPREFIX="$HOME/.local/share/wineprefixes/uu-remote" \
  /opt/wine-stable/bin/wine reg add \
  'HKCU\Software\Wine\Drivers' /v Audio /t REG_SZ /d alsa /f
```

在 `~/.config/systemd/user/uu-remote-bridge.service.d/` 中新建或编辑 `20-audio-isolation.conf`，写入：

```ini
[Service]
Environment="UURB_UU_AUDIO=off"
Environment="ALSA_CONFIG_PATH=%h/.config/uu-remote-bridge/alsa-null.conf"
```

执行 `systemctl --user daemon-reload`，在 UU 已断开时仅重启 `uu-remote-bridge.service`。重新连接，确认实际画面和输入正常；`wpctl status` 中应没有 GameViewer 占用物理设备的流。再检查对应播放设备是否已经释放：

```bash
cat /proc/asound/card*/pcm*p/sub*/status
fuser -v /dev/snd/*
```

受影响的播放 PCM 应显示 `closed`；静音或 `SUSPENDED` 本身不表示设备已释放。

恢复系统音频时，移除 `20-audio-isolation.conf`，删除这个专用前缀的显式音频驱动设置：

```bash
WINEPREFIX="$HOME/.local/share/wineprefixes/uu-remote" \
  /opt/wine-stable/bin/wine reg delete \
  'HKCU\Software\Wine\Drivers' /v Audio /f
```

再次执行 `systemctl --user daemon-reload` 并仅重启桥接服务，回到默认的 `UURB_UU_AUDIO=system`。整个操作不需要重启 PipeWire、WirePlumber、XRDP、GDM 或 GNOME。

继续阅读：[画质设置](quality-guide.md)、[源码构建](source-build.md)、[架构](architecture.md)、[输入与剪贴板](semantic-text-and-clipboard.md)、[键盘中继](adaptive-keyboard-relays.md)、[升级](reusable-upgrade.md)。终端与登录问题可继续查看[原生 Ubuntu 终端](native-ubuntu-terminal.md)、[无人值守启动](unattended-startup.md)和下列桌面恢复指南。

## 深入阅读

- XRDP 与键盘恢复 · [English](../../xrdp-and-keyboard-recovery.md) · [简体中文](../zh-Hans/xrdp-and-keyboard-recovery.md)
- 键盘兼容检查 · [English](../../mobile-keyboard-parity-handoff.md) · [简体中文](../zh-Hans/mobile-keyboard-parity-handoff.md)
- Mac 当前桌面 · [English](../../macos-current-desktop.md) · [简体中文](../zh-Hans/macos-current-desktop.md)
- 共享物理桌面 · [English](../../shared-physical-desktop.md) · [简体中文](../zh-Hans/shared-physical-desktop.md)
- 退出恢复 · [English](../../clean-exit-recovery.md) · [简体中文](../zh-Hans/clean-exit-recovery.md)
- 控制端代理 · [English](../../controller-agent.md) · [简体中文](../zh-Hans/controller-agent.md)
- SSH 代理消息 · [English](../../agent-link.md) · [简体中文](../zh-Hans/agent-link.md)
