[English](../../shared-physical-desktop.md) · [简体中文](shared-physical-desktop.md)

[简体中文 · UU Remote Ubuntu Plus](../../../i18n/README.zh-Hans.md)

# RDP、RealVNC 与 UU 共用一个物理桌面

这套可选配置分享已存在的 GDM X11 桌面，保留现有应用和会话。普通桥接安装只有显式启用后才使用此后端。

## 桌面为什么变了

XRDP 的 Xorg/Xvnc port=-1 请求 sesman 创建或恢复独立会话；RealVNC Service Mode 显示物理控制台，UU auto 可选到其中任一会话。RDP 登录可能覆盖 systemd 用户管理器的 DISPLAY，因此 physical 目标从 GNOME 的 GDM Xauthority 或确认的 seat/GDM 会话识别物理桌面。显式 :N、xrdp、auto 仍可用。

## 连接布局

```text
Physical GNOME X11 desktop
  ├─ RealVNC Service Mode → existing RealVNC console/cloud connection
  └─ independent loopback x11vnc service, 127.0.0.1:5922
       ├─ XRDP VNC proxy → RDP client, after Ubuntu PAM authentication
       └─ UU viewer + existing native input bridge → UU clients
```

独立 x11vnc 服务不属于 RDP 或 UU 进程树，UU 重启保留它。复用时 UU 核对所有者、显示、回环监听器与进程。

## 安装可选后端

以桌面用户从源码目录执行：

```bash
install -m 0755 scripts/uu-shared-physical-vnc "$HOME/.local/bin/uu-shared-physical-vnc"
install -m 0644 systemd/uu-shared-physical-vnc.service "$HOME/.config/systemd/user/uu-shared-physical-vnc.service"
```

普通安装器会安装这些文件，但不启用服务。在 `~/.config/uu-remote-bridge/environment` 保留其余设置，每个键只写一次：

```ini
UURB_DESKTOP_TARGET=physical
UURB_DESKTOP_RELAY=vnc
UURB_DESKTOP_VNC_PORT=5922
```

后续安装保留 shared-port。移除 UURB_DESKTOP_VNC_PORT 后恢复 UU 自行启动 VNC。若 UU 正占用 5922，先只停它，启用独立后端再恢复：

```bash
systemctl --user stop uu-remote-bridge.service
systemctl --user daemon-reload
systemctl --user enable --now uu-shared-physical-vnc.service
systemctl --user start uu-remote-bridge.service
```

UU 会重连，GNOME 与账号保留。辅助程序发现当前用户的物理 GDM X11 和权限；不存在时失败，不创建虚拟桌面。开机物理会话仍依赖既有 GDM 登录配置。

## XRDP 先认证，再访问控制台

备份 /etc/xrdp/xrdp.ini 后加入以下连接，YOUR_DESKTOP_USER 换为桌面所有者。核对实际 sesman 监听地址；案例中 XRDP 0.9.24 使用 [::1]:3350：

```ini
[PhysicalDesktop]
name=Physical desktop (shared with RealVNC and UU)
lib=libvnc.so
username=YOUR_DESKTOP_USER
password=ask
ip=127.0.0.1
port=5922
pamusername=same
pampassword=same
pamsessionmng=::1
disabled_encodings_mask=1
```

Globals 中设置 autorun=PhysicalDesktop，新连接放在 Xorg/Xvnc 前，其他条目保留为独立桌面选项。客户端提供账号密码或由 XRDP 提示。

-nopw 只在回环后端使用，网络侧 RDP 必须经过 PAM。检查错误密码在连接 VNC 前被拒绝、正确密码可用；连接文件不保存 Ubuntu 密码。disabled_encodings_mask=1 关闭 ExtendedDesktopSize，让客户端缩放而不调整物理桌面。VNC 代理不是完整受管 XRDP 会话，音频、磁盘与剪贴板另行配置。

## 单独启用 RDP 文本剪贴板

VNC 的 -seldir recv 防止 UU 语义文字回送 Wine 后意外粘贴；保留它。XRDP 0.9.24 libvnc 自带回退为 Latin-1，不适合中日文。对现有物理显示 :0，可安装原生通道服务：

```bash
install -m 0755 scripts/shared-desktop-clipboard "$HOME/.local/bin/shared-desktop-clipboard"
install -m 0644 systemd/shared-desktop-clipboard.service "$HOME/.config/systemd/user/shared-desktop-clipboard.service"
systemctl --user daemon-reload
systemctl --user enable --now shared-desktop-clipboard.service
```

备份 XRDP 配置后，在 PhysicalDesktop 添加以下项目并保留 PAM：

```ini
chansrvport=DISPLAY(0)
channel.cliprdr=true
channel.rdpsnd=false
channel.rdpdr=false
channel.drdynvc=false
channel.rail=false
channel.xrdpvr=false
channel.tcutils=false
```

只启用 cliprdr。辅助程序验证物理 GDM 权限及显示号，运行发行版 xrdp-chansrv；不轮询或记录剪贴板，也不模拟粘贴。物理显示号改变时，同步检查 helper 与 chansrvport。

断开再连接 RDP 客户端并启用客户端剪贴板分享，保留 Ubuntu 登录。服务在未来登录启用，开机仍依赖 GDM；多个 RDP 客户端共享同一控制台需分别检查。2026-09-07 隔离测试以禁用选区的 VNC 后端确认原生 chansrv 路径：ASCII、中日文、重音与多行双向通过，多行有 CRLF/LF 转换；BMP 之外 emoji 双向失败，对应 [XRDP UTF-16 问题](https://github.com/neutrinolabs/xrdp/issues/2603)。实际手机输入与 Windows App 粘贴在重连后另行检查。

仅查看服务状态与套接字：

```bash
systemctl --user status shared-desktop-clipboard.service
ls -l /run/xrdp/sockdir/xrdp_chansrv_socket_0
```

回退时恢复 XRDP 配置，执行 `systemctl --user disable --now shared-desktop-clipboard.service`，然后重连客户端，保留共享 VNC 与物理桌面。案例中 XRDP 新连接直接读取新配置，无需重启 sesman。

## RealVNC 与旧辅助程序

RealVNC Service Mode 保持物理控制台。旧 realvnc-current-xrdp-desktop.service 若把 XRDP 查看器放到控制台，会形成相反方向；确认所有者后关闭该旧 helper，保留 vncserver-x11-serviced.service。独立 VNC 可在没有 UU 时供 RDP 使用，UU 卸载也保留它；移除前先调整消费者。

## 历史检查结果

2026-09-06 案例为物理 :0、UU 私有画布 :20、既有 XRDP :10。错误密码被 PAM 拒绝，正确密码连接既有控制台和原浏览器窗口，窗口 ID 保持，未新建 GNOME 会话。UU 复用物理后端，RealVNC 服务与许可证设置保留。配置检查完成但当时没有重启主机；手机输入、语音与全部 RDP 重定向功能未逐项重测。

参考 [XRDP 0.9.24 配置](https://github.com/neutrinolabs/xrdp/blob/v0.9.24/xrdp/xrdp.ini.in)、[连接认证实现](https://github.com/neutrinolabs/xrdp/blob/v0.9.24/xrdp/xrdp_mm.c) 和本机 xrdp.ini(5)。
