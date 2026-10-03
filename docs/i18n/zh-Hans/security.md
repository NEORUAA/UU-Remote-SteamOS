[English](../../security.md) · [العربية](../ar/security.md) · [Español](../es/security.md) · [Français](../fr/security.md) · [日本語](../ja/security.md) · [한국어](../ko/security.md) · [Tiếng Việt](../vi/security.md) · [中文（简体）](../zh-Hans/security.md) · [中文（繁體）](../zh-Hant/security.md) · [Deutsch](../de/security.md) · [Русский](../ru/security.md)

[← 返回简体中文首页](../../../i18n/README.zh-Hans.md)

# 安全

## 权限与隔离边界

仅在获授权的电脑和 UU 账户上使用。桥接器保留正常 UU 登录和 GNOME RDP 凭据；无人值守模式是可撤销的 GDM/systemd 配置。

- 全栈以已登录 Unix 用户运行，专用 Wine 前缀为 `~/.local/share/wineprefixes/uu-remote`，systemd 使用用户 unit。
- Xvfb 使用 Xauthority 且不监听 TCP；broker 管道限于这个 Wine wineserver 命名空间。
- 可选 X11 与原生终端辅助程序各绑定临时 IPv4 回环端口，各有每次启动新建的 256-bit token。运行目录 `0700`，终端交接文件 `0600`，最多四个 shell 会话。
- 管理窗口 VNC 不设置独立密码，但只监听 IPv4 回环，只导出一个 UU 窗口及关联弹窗，随本机查看器退出而结束。
- 可选 Mac 当前桌面中继在 Ubuntu 回环使用认证 VNC，通过 SSH 到达 Mac。经典 VNC 密码文件只是混淆而非加密，因此保持 `0600`，不能代替 SSH 边界。
- FreeRDP 只连接 `127.0.0.1`，按 SHA-256 固定 GNOME TLS 证书。GNOME 自己是否对 LAN 监听取决于其配置，应使用防火墙和独立强密码。
- 安装依赖、无人值守 GDM 配置、组成员及 root 回滚记录才使用 `sudo`。

启动器可能临时停止原生 GNOME RDP 服务，将 daemon 绑定到选定会话的总线；退出时恢复之前活动的服务。已有 socket/lock 的固定 X display 不会被抢用。

## 凭据和私有内容

安装器不回显密码，以 `secret-tool` 存入登录 keyring。FreeRDP 从标准输入接收凭据，随后清除 shell 变量，不放入进程参数、unit 或仓库。VNC 认证只使用凭据前八字节，这是经典 VNC 的限制；Mac keychain 可保存对应前缀。

无人值守启动另需 keyring 密码，用 `systemd-creds --with-key=tpm2` 加密。持久化只保存密文；systemd 在受保护 runtime credential 中解密，oneshot 经 D-Bus 解锁登录集合。`tss` 成员和临时 TPM ACL 使当前登录与下次启动都能访问 TPM；撤销会移除脚本添加的权限。该 keyring 私有接口原在 Ubuntu 24.04/GNOME 46 检查，升级后应检查解锁 unit。

UU 的 token 与账户状态留在专用前缀。不要发布该前缀、日志、registry 或桌面截图。输入日志只记录数量、类型、flags、route、结果、error，不记录按键值、Unicode、坐标或剪贴板。终端日志只记录 readiness、session/尺寸、拒绝和关闭，不保存命令和输出。

语义文字每次最多 2,048 records，在内存中转换 UTF-16/UTF-8，交由目标 `xclip` 拥有选区。先核实 owner，再粘贴；成功后文字保留在桌面剪贴板。`legacy/auto` 可将可表达文字转成组合键；`rdp-public/auto` 对 Unicode 提交使用字面文本。RDP `cliprdr` 可在 Wine 中继与 GNOME 间交换正常剪贴板；VNC 文字辅助只向目标桌面发送，不反馈回私有 display。细节见[文字与剪贴板](semantic-text-and-clipboard.md)。

## 二进制与更新

[4.42 清单](../../../patches/uu-remote-4.42.0.2770.json)记录原件和补丁结果完整 SHA-256、size、唯一签名、offset 与等长替换。`patch-gameviewer.py` 只接受 `approved`，未知字节拒绝；原件保留为 `GameViewerServer.exe.uu-original`。旧清单只批准对应旧版本，draft 必须先独立审阅指令语义。

GameViewerHealthd 同样按身份检查。FreeRDP/SDL 使用[固定产品 profile](../../../patches/freerdp-sdl-product.json)，复用 runtime 要使源码、recipe、profile、输出 pins 与 provenance 一致，见[源码构建](source-build.md)。旧 libei keymap-FD backport 仅在配置存在时用于受监督 GNOME 子进程；26.04 使用包含修复的系统库，不覆盖系统 libei。

`stage-uu-release.sh` 先静态解包。显式 `--sandbox-install` 使用无网络 Bubblewrap，或显式 root-managed systemd 后端，隐藏真实 home、只读主机、限定可写暂存目录；更强隔离可使用 VM。见[上游维护](upstream-maintenance.md)。

## 剩余风险与维护策略

Wine 不是同 Unix 用户间的强安全沙箱；UU 是闭源远程输入软件，云端与自更新行为可能改变。需要更强隔离时用独立 Unix 账户，并更新 OS、Wine、UU、GNOME。

自动检查不重启健康中继。修复在私有 clone 中生成 draft，不能自行批准或部署。自动上线需要显式开启，且精确 installer/server hash、已提交 acceptance、控制端与登录保留测试及至少 270 秒稳定期全部匹配。事务复制完整 Wine 前缀，账户状态必须逐字相等；失败、打断或重启恢复旧前缀并停止自动重试，不改 XRDP。见[自动更新](automatic-updates.md)。

GDM 自动登录使启动后有物理访问的人可使用账户；TPM 防止密文离线搬到另一台机器解密，不能保护已经登录的桌面。LUKS 等开机前密码仍需本地输入。

仓库仅保存源码、说明、hash 和必要反汇编结论。不要提交 UU/FreeRDP 编译产物、Wine 前缀、registry、凭据、token、设备标识、现场日志或私有截图。
