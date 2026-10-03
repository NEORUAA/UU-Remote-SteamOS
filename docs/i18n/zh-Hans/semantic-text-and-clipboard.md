[English](../../semantic-text-and-clipboard.md) · [中文（简体）](../zh-Hans/semantic-text-and-clipboard.md)

[← 返回简体中文首页](../../../i18n/README.zh-Hans.md)

# 手机语义文字与剪贴板中继

UU 的物理键、手机 IME Unicode 提交与剪贴板更新是不同类别。口述换行不能变成提交终端的 Enter；中文也不能压成当前 XKB 上没有的组合键。

## 自适应路由

`UURB_PHONE_TEXT_MODE=auto` 默认开启。`legacy` 将可表达文本走普通键路（默认 RDP，可选 XTEST）；换行、tab、中文、emoji 等走语义选区和 `Shift+Insert`。Backspace 是编辑键。含 Unicode 的 composition 修订即使新内容仅 ASCII，也走有限语义编辑；单纯 ASCII 插入与物理 Backspace 保持普通路径。

`rdp-public/auto` 则将所有 Unicode 提交作为字面文字，包括 ASCII，经公共插件发送粘贴键并检查 owner/selection-request 屏障；物理键仍不变。显式 `keys` 要求翻译。见[架构](architecture.md)。

目标须暴露可授权的 X11/Xwayland，且原生 helper 活动。旧 RDP 分离路径在真实桌面拥有剪贴板，在私有 Wine/SDL 发粘贴组合键，经原有 RDP 到真实应用；不另开桌面会话。

## 选区与编辑顺序

broker 通过认证回环发送最多 2,048-record UTF-16，helper 校验、拼接分离 surrogate、转 UTF-8、将 CRLF 规范成一个换行，由 xclip 拥有 `CLIPBOARD` 和 `PRIMARY`。VTE 的 Shift+Insert 可能读 PRIMARY，其他应用读 CLIPBOARD，因此两者都要设置。

新 owner 建立且 quiet 前，不退出旧 owner，避免 owner=None 间隙。先等待 eager clipboard-manager 读取平静，发一次粘贴，再要求新的 selection request，才返回成功。请求串行处理，不能让下次口述过早替换尚未读取的选区。屏障说明一次选区事务，不能替代目标应用焦点与实际文字检查。

composition Backspace 只可修订同 broker client 最近插入的内容；新 client、空闲或无关键鼠清除额度。按事件顺序记 prospective credit，段成功才提交额度。每对 Backspace 在 X11 边界 flush 并按共享 5ms 编辑节奏处理。owner 未确认、manager 不 quiet、无后续 request 会失败，不授予 revision credit；通信结果不明时不重放。文本不写日志/磁盘。

```bash
./install.sh --skip-packages --skip-account-login \
  --phone-text-mode keys
./install.sh --skip-packages --skip-account-login \
  --phone-text-mode clipboard
```

`keys` 保留纯按键行为；`clipboard` 对文字提交使用粘贴，编辑键保持顺序。`auto` 根据已选输入路径自适应。一次 provisional SendInput 可能包含数百 records；旧 64-record 上限拒绝长口述，现在完整事务限 2,048。不能把一条语义提交切成多次选区粘贴：X11 延迟读取可能使所有排队粘贴只看见最后一段。超限在注入前拒绝。

成功后文本保留在桌面两个选区，不异步恢复旧内容，避免竞态，也可供后续手动粘贴。不要在密码框测试。

## VNC 的单向剪贴板

```text
ClientCutText=1
ServerCutText=0
SendPrimary=0
SendInitialClipboard=0
ServerClipboardGraceTime=5000
x11vnc -seldir recv
```

UU/Wine 更新 CLIPBOARD，优先 PRIMARY 会传旧选择或最后一行。启动不传已有剪贴板；Ubuntu 语义文字不回流到私有 display。控制端复制走此通道，手机键盘/口述走 broker，两者独立。

只更新 GameViewer Win32 clipboard 的控制端由 VNC/X11 专用 companion 处理：以启动 sequence 为基线，读取前后都要求 owner 是 `GameViewer.exe`，认证 helper 在目标拥有两选区，不注入粘贴键、不读主机内容回传。listener 有有限 socket deadline，launcher 将 companion 视为关键子进程，退出清理 owner。

## 隔离回归

```bash
./scripts/test-rdp-semantic-text.sh
./scripts/test-x11-clipboard-text.sh
./scripts/test-vnc-clipboard-relay.sh
./scripts/test-controller-clipboard.sh
./scripts/test-x11-phone-text.sh
./scripts/test-vnc-keyboard-relay.sh
```

测试使用临时 display/prefix，不读用户剪贴板。RDP split 检查 `UU broker 中文 123` 精确送达、粘贴键只进私有 relay。X11 检查中文、split emoji、两行、2,000-record composition 及一次真实 paste；VNC 检查 cut-text 和无回路；controller 检查启动不重播、非 GameViewer 忽略、multiline 两选区、xclip 缺失与超时拒绝、退出无子进程。快速文本测试单独检查可表达文字，VNC 键盘测试单独检查实体符号/keysyms。

```text
route=x11-clipboard-text error=0
```

## 混合语言修订

2026-09-05 的回归曾在每次 ACK 成功时仍删掉前一段中文。原因是一段 ASCII replacement 绕过语义删除额度，以及 text/Backspace/text 的插入额度直到整段末尾才记账。修复使所有 Unicode 编辑批次走同一有限路径，逐事件记账，段成功后才提交。`language-revisions` 检查中文→ASCII→中文、过量 stale Backspace、插删交错和其他 client 的既有文字。

这些是有限 GUI 编辑，不是编辑器原子事务；外部 cursor/selection、grapheme 规则或 IME 边界不同仍可能中断，不重放不明输入。

## 只看无内容诊断

```bash
tail -n 100 \
  "$HOME/.local/share/wineprefixes/uu-remote/drive_c/users/$USER/Temp/uu-input-broker.log" \
  | rg 'category=text|phone-text-mode'
```

旧/直接 X11 的可表达路径 `x11-text`，语义路径 `x11-clipboard-text`；旧 RDP 普通 `rdp`、语义 `rdp-clipboard-text`。error1113 表示旧按键路径不能翻译 Unicode；旧超过 64 records 的 result0/error5 是旧容量边界。当前应返回原完整 count。公共 `rdp-public` 要按其插件与 literal 路径读记录，不混成旧分支。

## 2026 年 9 月：owner 交接与长修订

GNOME/XRDP 上新 xclip 在粘贴前退出，error8195 映射 broker31，XRes 发现新 owner 为 gnome-shell。旧实现先杀旧 owner，短暂 None，GNOME 旧选区恢复可能晚到抢走新 owner。修复保留旧 owner 直到新 pair 建立并 quiet，再 reap。隔离 XFixes 模型与真实同桌面 A/B 指向这一竞态，不需要关闭剪贴板管理器或改布局。

另一问题是 300 字 provisional 成功，608-record 修订删到一半断开。300 次删除按 5ms 需要约 1,500ms，旧 socket receive 1,000ms 不够。普通仍 1,000ms，语义 selection 3,000ms，每个 paced Backspace release 加共享 5ms；总 records 仍限 2,048。这是工作预算，不是追加等待，结果不明不重试。

```bash
python3 -m unittest discover -s tests -v
bash scripts/test-x11-clipboard-text.sh
bash scripts/test-x11-phone-text.sh
bash scripts/test-rdp-semantic-text.sh
bash scripts/test-vnc-clipboard-relay.sh
bash scripts/test-vnc-keyboard-relay.sh
```

两个输入文件都需重建：`uu-x11-input`、`uu-input-broker.exe`。通过正常 guarded 部署保持输入轨道；若只更新两个文件，私下记录部分部署和 hash，不将整个新源码 digest 冒充已安装。pull 不更新运行 helper，bridge restart 不关闭 GNOME/XRDP 应用，仍需真实控制端重连与 IME 检查。
