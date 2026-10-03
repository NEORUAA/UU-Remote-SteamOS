[English](../../upstream-maintenance.md) · [中文（简体）](../zh-Hans/upstream-maintenance.md)

[← 返回简体中文首页](../../../i18n/README.zh-Hans.md)

# 跟随 UU 上游更新维护桥接

这套方法自动化收集、比较、补丁包装和校验，把指令语义留给人工审阅。类似字节不保证相同对象布局、分支或调用约定；不要为绕过新版身份检查而接受未知 hash。

## 每个可执行清单的条件

原 server 精确 SHA-256 与 size；完整签名在声明 offset 唯一出现；替换等长且互不重叠；预计算完整 patched hash；反汇编后明确标 `approved`；同 release 的 installer/healthd hash 一并记录。`patch-gameviewer.py` 拒绝 draft，安装器将所选清单复制进前缀供 verify/uninstall 使用。

## 1. 保留基线

从干净仓库与健康桥接开始，新 release 新增 `patches/` 文件，不重写旧 approved 清单。

```bash
git status -sb
scripts/verify.sh --quick
python3 -m unittest discover -s tests -v
```

## 2. 获取和暂存

从网易官方 endpoint 获取 installer 并算完整 hash，先尝试不执行的解包：

```bash
scripts/stage-uu-release.sh \
  --installer ~/Downloads/UU-Remote/uuyc_NEW.exe
```

wrapper 无法由 7z 提取时，操作者显式选择 sandbox：

```bash
scripts/stage-uu-release.sh \
  --installer ~/Downloads/UU-Remote/uuyc_NEW.exe \
  --sandbox-install
```

Bubblewrap 隐藏真实 home、隔离 network/PID/IPC、放弃 capabilities、只读 host，只给 staging 可写。没有可用 user namespace 时，显式 systemd 后端使用 root-managed transient service，以桌面 UID 跑 Wine，private network/devices/tmp、no-new-privileges，并拒 Internet socket families。

```bash
scripts/stage-uu-release.sh --installer uuyc_NEW.exe \
  --sandbox-install --sandbox-backend bubblewrap
```

分析文件复制后删除临时 prefix；只有需要检查安装布局才用 `--keep-workdir`。更强隔离用 VM，直接传提取文件给 audit。所有 staged 文件在忽略的 `build/upstream/`，不提交。

## 3. 生成 audit，而非执行补丁

当前 4.42 approved 清单可作为行为基线；对具体目标始终重新建立语义。

```bash
scripts/audit-gameviewer.py inspect \
  --server build/upstream/NEW/GameViewerServer.exe \
  --healthd build/upstream/NEW/GameViewerHealthd.exe \
  --installer ~/Downloads/UU-Remote/uuyc_NEW.exe \
  --baseline patches/uu-remote-4.42.0.2770.json \
  --version NEW_VERSION
```

私有目录包含 `REPORT.md`、`audit.json`、`draft-manifest.json`、`objdump-headers.txt`、带 offset 的 `strings.txt` 和小范围 `disassembly/*.txt`。候选扫描只 mask 旧补丁变化字节，用最长不变 context 锚定，报告零/一/多个结果，不写 binary，不自行标 reviewed。

## 4. 重新建立意义

在真实 Windows 比较同版，记录 driver、virtual switch、生命周期、imports 的无账户元数据；找语义 string/xref，检查完整函数、caller、字段写入、指令边界与寄存器/stack。设计最小等长替换，并保留长唯一原/新签名。

```bash
strings -a -t x GameViewerServer.exe | \
  rg 'virtual switch state:|set_virtual_mouse_switch|read_user_setting'

x86_64-w64-mingw32-objdump -h GameViewerServer.exe
x86_64-w64-mingw32-objdump -p GameViewerServer.exe | \
  rg -C 3 'SendInput|wevtapi|Evt[A-Z]'

x86_64-w64-mingw32-objdump -d -M intel \
  --start-address=START_VA --stop-address=STOP_VA \
  GameViewerServer.exe

xxd -g 1 -s FILE_OFFSET -l LENGTH GameViewerServer.exe
```

只在此后编辑 private draft：`candidate_status` 从 unreviewed 改 reviewed，确认 offset、原字节、替换、description、rationale。候选缺失或多义必须人工解决，不挑最近位置。

## 5. 完成清单

finalize 重算原身份，在内存应用 reviewed signature，得完整 patched hash，检查 schema，但不改可执行文件：

```bash
scripts/audit-gameviewer.py finalize \
  --server build/upstream/NEW/GameViewerServer.exe \
  --draft build/audits/NEW/draft-manifest.json \
  --output patches/uu-remote-NEW_VERSION.json \
  --reviewed-by 'reviewer name' \
  --review-note 'Windows comparison, disassembly report, and test reference' \
  --accept-reviewed-disassembly
```

placeholder、未 reviewed、错误 server hash、签名重叠/格式不对或已有 output 都拒绝。

## 6. 测试副本

第一次 patch 不对 installed server 执行：

```bash
cp build/upstream/NEW/GameViewerServer.exe build/upstream/NEW/server-test.exe

scripts/patch-gameviewer.py patch \
  build/upstream/NEW/server-test.exe \
  --manifest patches/uu-remote-NEW_VERSION.json

scripts/patch-gameviewer.py verify \
  build/upstream/NEW/server-test.exe \
  --manifest patches/uu-remote-NEW_VERSION.json

scripts/patch-gameviewer.py restore \
  build/upstream/NEW/server-test.exe \
  --manifest patches/uu-remote-NEW_VERSION.json

cmp build/upstream/NEW/server-test.exe \
  build/upstream/NEW/server-test.exe.uu-original
```

```bash
python3 -m unittest discover -s tests -v
```

检查 patch/verify/restore 后与 `.uu-original` 相等，再继续完整桥接。

## 7. 完整桌面与登录检查

只在副本验证后，将清单用于 disposable prefix：

```bash
./install.sh \
  --release-manifest patches/uu-remote-NEW_VERSION.json \
  --uu-installer ~/Downloads/UU-Remote/uuyc_NEW.exe
```

检查设备 online、真正 GNOME 画面/尺寸、鼠标移动/按钮/wheel/drag、可打印键/modifier/shortcut/key-up、所选 clipboard policy。停止整个 prefix 冷启动，确认新 server 到 `update_gvinput end` 和 `room_state_changed: created`；断开重连和 service restart 恢复，同 server PID 至少 270 秒，verify、uninstall dry-run 和原件恢复均正确。

要记录登录保留，复制一个已登录测试前缀，在副本就地装 accepted installer，两次重启并重连，设备无需登录提示返回 online。registry、token、手机号、device ID、原始日志和私有画面不发布。

## 8. 记录 promotion acceptance

`review_status: approved` 表达二进制补丁解释，不等于可用性接受。完成完整桥接与登录检查后才新增顶层 acceptance：

```json
{
  "acceptance": {
    "schema_version": 1,
    "disposable_prefix": true,
    "controller_input": true,
    "reconnect": true,
    "service_restart": true,
    "login_preservation": true,
    "stability_seconds": 270,
    "installer_sha256": "COPY installer.sha256 EXACTLY",
    "patched_server_sha256": "COPY server.patched_sha256 EXACTLY",
    "evidence": "docs/releases/NEW_VERSION-acceptance.md",
    "accepted_at": "ISO-8601 timestamp",
    "accepted_by": "maintainer identity"
  }
}
```

清单和 evidence 同 commit，acceptance hash 与周围字段完整相等。版本字符串、部分 hash、Codex 输出或未提交文件不是上线授权。只记录测试 profile 和可观察结果，不带账户数据。

```bash
python3 -m unittest discover -s tests -v
git diff --check
```

自动上线仍须 `--auto-promote-accepted`，等空闲期、复制完整前缀、就地 installer、启动前检查账户，并在失败恢复；不管理 XRDP。见[自动更新](automatic-updates.md)和[可复用升级](reusable-upgrade.md)。

## 旧方法失效时

virtual-switch string/字段消失、用户态 SendInput 被移除、输入改进程/IPC、token 不再 error5、event-log/health 行为变化、捕获不再普通窗口或 installer 需要 staging 网络时，重新设计对应适配，不强行套 manifest。固定版本和签名使维护可复用、可审阅、可恢复，不使版本批准自动化。

版本差异的具体案例见[4.39.1 静态审核](releases/4.39.1.1375-static-review.md)与[4.39.2 静态与临时运行审核](releases/4.39.2.1561-static-review.md)。
