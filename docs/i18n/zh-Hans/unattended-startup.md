[English](../../unattended-startup.md) · [中文（简体）](../zh-Hans/unattended-startup.md)

[← 返回简体中文首页](../../../i18n/README.zh-Hans.md)

# 无人值守启动

桥接通常依赖已登录 GNOME。需要开机后无需本地/RDP 先登录即可连接时，使用显式 GDM 自动登录。自动登录没有 PAM 密码，GNOME Keyring 仍锁定，GNOME RDP 读不到凭据；本功能同时解决会话和 keyring，不移除 Unix 密码，也不在 launcher 存明文。

一个物理工作区供 RDP/RealVNC/UU 共用，另见[共享物理桌面](shared-physical-desktop.md)，其独立 VNC 不随 UU 重启。

## 启用

```bash
./install.sh --unattended
./scripts/configure-unattended.sh enable
```

配置询问登录 keyring 密码，通常是 Ubuntu 登录密码，验证 TPM2，以 `systemd-creds --with-key=tpm2` 加密，持久化只存密文。添加桌面用户到 `tss`，组尚未生效时加临时 TPM ACL；安排 `uu-keyring-unlock.service` 在 GNOME RDP 前执行，保存 root-only GDM 回滚记录，再为当前用户开启自动登录。重启一次使组生效并检查完整启动路径。LUKS、固件密码等 GDM 前关卡仍需本地交互。

## 启动链

```text
GDM 自动登录 → GNOME + gnome-keyring-daemon
  → systemd 通过 TPM2 解密 login-keyring-password.cred
  → uu-keyring-unlock.py 通过 session D-Bus 解锁 login collection
  → GNOME RDP 读取正常凭据
  → uu-remote-bridge.service 启动 Wine / UU / Xvfb / FreeRDP
  → 授权控制端可连接设备
```

明文只在 oneshot 运行期间存在于 systemd 受保护 credential 目录，不进入环境变量、参数、仓库或 journal。master-password 调用是 GNOME Keyring 私有接口，原在 Ubuntu 24.04/Keyring 46 检查，桌面升级后需检查 unit。

helper 最多等 Secret Service bus name 120 秒；成功后 oneshot 保持 `active (exited)`。不需要 `loginctl enable-linger`：user unit 等真实 GNOME Shell，不创建登录前合成桌面，GDM 提供会话。

## 检查

```bash
./scripts/configure-unattended.sh status
systemctl --user status uu-keyring-unlock.service
systemctl --user status uu-remote-bridge.service
scripts/verify.sh --quick
```

首次重启前 `Account in tss group` 应为 yes，`tss active in this login` 可为 no；临时 ACL 让当前登录也能重启桥接。重启重新创建设备，没有临时 ACL，而组已生效，两项应为 yes。

```bash
journalctl --user -b \
  -u uu-keyring-unlock.service \
  -u gnome-remote-desktop.service \
  -u uu-remote-bridge.service
./scripts/configure-unattended.sh status
scripts/verify.sh --quick
```

解锁 unit 应 `status=0/SUCCESS`，RDP 监听指定端口，verifier 正常。

## 改密码与撤销

Unix 密码改变不一定改变已有 keyring 密码。keyring 密码变更后重建 TPM credential：

```bash
./scripts/configure-unattended.sh enable --replace-credential
```

命令询问两次，不接受参数密码。错误密码使解锁失败，不重置 keyring。

```bash
./scripts/configure-unattended.sh disable
sudo reboot
```

disable 移除密文、临时 ACL、drop-in 和 unit，恢复仍与受管理值一致的旧 GDM 设置，移除脚本添加的 tss 成员。若别人已改 GDM，保留其新值。uninstall 调用相同回滚。

## 工具与取舍

`crudini` 只改两项 GDM INI；`systemd-creds` 与 TPM2 绑定密文；`/dev/tpmrm0`/tss 提供用户 manager 访问；user units 表达依赖；D-Bus 解锁已有集合。`gdbus`、`stat`/`getfacl`、`systemd-analyze verify` 和当次启动 journal 分别检查锁、权限、unit、启动结果。

排查时画完整依赖链，找交互登录隐式提供的条件，只补缺失项；先保存 privileged 配置，分开检查解密与应用启动，再检查真实集合、消费服务和回滚。

自动登录意味着启动后任何有物理访问的人可使用账户。TPM 防离线复制到别机，不防已登录用户代码访问 keyring。仅在无人值守可达性优先于本地登录门槛时开启。另见[排查方法](debugging-journey.md)和[安全](security.md)。
