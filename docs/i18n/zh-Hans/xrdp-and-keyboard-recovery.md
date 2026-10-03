[English](../../xrdp-and-keyboard-recovery.md) · [简体中文](xrdp-and-keyboard-recovery.md)

[简体中文 · UU Remote Ubuntu Plus](../../../i18n/README.zh-Hans.md)

# XRDP 客户端停滞与 UU 键盘恢复

这篇工程记录对应 Windows App 停在 Configuring、UU 画面与鼠标正常但快速实体键遗漏的历史案例。先分清客户端连接状态、桌面焦点、画布尺寸与输入路由，再分别处理。

## 连接与焦点

案例中 XRDP 完成 TCP/TLS 后停在能力交换之前，本地 FreeRDP 探针可继续认证，远端 Windows App 保留了旧连接状态。VNC 与 XRDP 使用不同端口，但同一 X 会话改变时，依赖它的视图也可能结束。

画面正常而所有输入停止时，检查私有中继焦点。代理中重复 focus=timeout、result=0、error=21 对应未能取得前台窗口，可先恢复：

```bash
uu-agent focus 'Ubuntu-Desktop-Relay'
```

启动器在账号初始化后监看专用显示的焦点。重连后看新记录中的 focus=ready、结果数量与 error=0，再观察目标应用。

## XRDP 恢复顺序

先检查当前尝试：

```bash
ss -H -tnp 'sport = :3389'
journalctl -u xrdp.service -u xrdp-sesman.service \
  --since '-15 min' --no-pager
tail -n 80 /var/log/xrdp.log
```

若停在 TLS connection established，先在 Mac 重开 Windows App：

```bash
osascript -e 'tell application "Windows App" to quit'
open -a "Windows App"
```

只重开一个连接，保留服务器中的会话。若客户端关闭后监听器仍异常，再考虑服务器重启：

```bash
sudo systemctl restart xrdp.service
systemctl is-active xrdp.service xrdp-sesman.service
ss -H -ltn 'sport = :3389'
```

重启 xrdp.service 可能经依赖同时重启 sesman；后续登录可能新建显示并结束旧桌面。先保存图形工作并保留另一访问路径。恢复后的日志阶段为：

```text
TLS connection established
xrdp_caps_process_codecs
sesman connect ok
login successful
connected ok
```

<a id="desktop-uses-only-part-of-the-uu-canvas"></a>

## 画布与源桌面大小不同

Windows App 可随窗口动态改变 XRDP 尺寸。源桌面较小时有留白，较大时可能裁掉右侧或底部。比较实际显示与保存画布，命令中的 :11 需换成当前 XRDP 显示：

```bash
DISPLAY=:11 XAUTHORITY="$HOME/.Xauthority" xdotool getdisplaygeometry
sed -n 's/^UURB_RESOLUTION=//p' \
  "$HOME/.config/uu-remote-bridge/environment"
ps -eo pid,args | rg '[X]vfb :|[s]dl-freerdp.exe.*size:'
```

选定合适的源分辨率后，只对齐 UU 中继：

```bash
./install.sh --skip-packages --skip-account-login \
  --resolution 1920x1080
```

案例中 1920x1080 源桌面搭配 1620x1080 中继裁掉右侧 300 像素，对齐后恢复完整画面。此安装只重启 UU 桥接器。需要调整 XRDP 本身时，单独使用本地 FreeRDP 重连调整；可能断开附着的查看器，但保留 GNOME。FreeRDP 3 不接受旧 helper 的 subtype:0，当前 helper 省略该显式零值。

## 实体键节奏

默认延迟 0。若慢打正常、快速输入漏键，可比较 8 ms：

```bash
./install.sh --skip-packages --skip-account-login \
  --physical-key-delay-ms 8
./scripts/verify.sh --quick
```

节奏只在代理接受实体键片段后形成回压，不重发键。恢复为 0：

```bash
./install.sh --skip-packages --skip-account-login \
  --physical-key-delay-ms 0
```

查看不含文字的键盘类别元数据：

```bash
broker="$HOME/.local/share/wineprefixes/uu-remote/drive_c/users/$USER/Temp/uu-input-broker.log"
rg 'category=keyboard' "$broker" | tail -n 30
```

paced-physical=1、physical-delay-ms、focus=ready 和结果数量反映调用路径。延迟设置的效果仍在真实应用中观察。

## 直接 X11 路由

历史案例的 12 ms 采样中 219 次调用返回成功，使用者仍看到遗漏，之后改用已确认的 XRDP Xorg/XTEST 路径。其链路为：

```text
UU physical key, normalized phone text, or mouse input
  -> Wine hook -> user-token broker -> X11 helper -> Xorg

UU video/clipboard -> selected local desktop relay -> desktop
```

仅在确认 Xorg/XRDP 目标后启用：

```bash
./install.sh --skip-packages --skip-account-login \
  --keyboard-route x11 --physical-key-delay-ms 0
./scripts/verify.sh --quick
```

原生辅助程序在发现的桌面执行 XTEST，通过认证回环接收有界数组，预检完整数组；可能已注入后失败时返回错误而不重播。断开释放追踪中的按键和按钮。直接路由中延迟是最小按住间隔，零保持非阻塞。

恢复 RDP 键盘路径：

```bash
./install.sh --skip-packages --skip-account-login \
  --keyboard-route rdp --physical-key-delay-ms 0
```

keyboard-route 默认 rdp；auto 只在发现 X11 时选择直接输入，显式 x11 未生效会被验证器报错。这个键盘选项与当前安装器的输入后端选择是不同设置。

## 案例结果

隔离 Xvfb 实体键测试记录 58 个有序转换；手机文字批次返回 52 个源记录并观察到 26 次按下、26 次释放。分别用 `./scripts/test-x11-phone-text.sh` 和 `./scripts/test-x11-mouse.sh` 重现隔离测试。后续真实控制端的 256 条采样报告 route=x11 和匹配结果，使用者反馈输入明显顺畅。记录没有输入内容，也不能重建控制端发出的全部事件。每次换路径后重连并查看新 category=keyboard/route=x11 与 category=text/route=x11-text 记录。继续阅读 [当前输入设计](adaptive-keyboard-relays.md)。
