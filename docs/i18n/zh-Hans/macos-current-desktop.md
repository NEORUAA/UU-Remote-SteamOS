[English](../../macos-current-desktop.md) · [简体中文](macos-current-desktop.md)

[简体中文 · UU Remote Ubuntu Plus](../../../i18n/README.zh-Hans.md)

# 从 macOS 查看当前 Ubuntu 桌面

桥接器已经使用 GNOME 桌面共享的 RDP 连接；GNOME 远程登录会另开会话。需要加入现有桌面时，可把桥接器的本地 VNC 视图通过原生 SSH 转发到 Mac。示例别名 `desktop-host` 需配置为自己有权访问的主机，并核对主机密钥。

## 开启桌面视图

在 Ubuntu 已登录的用户会话中运行：

```bash
uu-remote-console relay
```

辅助程序定位现有中继，在 `127.0.0.1:5922` 提供带认证的视图，使用桥接器密钥环中的凭据。网络访问通过 SSH，VNC 保持回环监听。

在 Mac 保持以下隧道运行：

```bash
ssh -N -o ExitOnForwardFailure=yes \
  -L 15922:127.0.0.1:5922 desktop-host
```

随后打开屏幕共享：

```bash
open vnc://127.0.0.1:15922
```

提示时输入已设置的桥接密码。按这台 Mac 的使用习惯决定是否保存在钥匙串中。公开反馈移除密码、真实主机信息与个人 SSH 别名。

## 可选启动器

可编辑 [macos-connect.applescript](../../../scripts/macos-connect.applescript)，设置自己的 `targetName`、`targetHost`、`sshAlias`、`rdpUsername`，核对 SSH 后用 `osacompile` 编译。仓库中的值是示例，含个人设置的副本与应用留在私有目录。

## 关闭与排查

关闭查看器会结束桌面交互，关闭 SSH 会撤掉转发。最后一个查看器断开后，视图辅助程序退出，桌面桥接器仍运行。

连接失败时查看 Ubuntu 辅助程序与 Mac 隧道；出现递归画面时关闭 Ubuntu 上反向查看 Mac 的窗口。只有需要另一个登录会话时才使用 GNOME 远程登录。继续阅读 [SSH 配置](ssh-and-port-mapping.md)。
