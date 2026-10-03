[English](../../methodology-and-toolkit.md) · [中文（简体）](../zh-Hans/methodology-and-toolkit.md)

[← 返回简体中文首页](../../../i18n/README.zh-Hans.md)

# 工程方法与工具

兼容性排查先把“Wine 下的 UU 不工作”拆成具体层：账户/signaling、capture、输入策略、执行、生命周期、RDP 认证。每层分别用 account IPC、窗口检查、switch/driver 日志、最小 SendInput probe、同 PID 时长和 SSPI 记录定位，不能将一跳成功当端到端完成。

## 参考实现与小探针

同一 UU 版本在获授权 Windows 11 上表现为签名 root HID、键盘 collection、kernel switch 开启。Wine 有重复合成 HID、没有 UU 键盘与可用 `gvinput.sys`。因此找现成用户态 fallback，而非模拟内核驱动。

小型临时 Windows 程序分别问：普通 Wine SendInput 能否到 SDL？focus/pointer 是否可用？是否只有 service token 被拒？Xvfb 软件图形是否正常？结论进入源码/测试/文档后，不将实验二进制放 Git。

`rg` 对齐状态迁移、PID 和时间，分出三因：选不可用 kernel 路、Wine 拒 service-token SendInput、未实现 event-log API 独立 abort。每因只加必要适配。

## PE 坐标与接口

file offset 是 `xxd`/manifest 坐标；RVA 相对 image base；VA 是 objdump 地址；section raw offset 与 virtual address 可因对齐不同。audit 工具读 section header 转换坐标，曾发现手工 VA 范围漏 `.text` 对齐差。按 `strings -a -t x` 找语义、`objdump -h` 映射、`objdump -d -M intel` 查控制流、`xxd -g 1` 保存字节、`sha256sum` 认完整身份，围绕编辑保留较长唯一签名。字节模式只是候选，字段写入、xref、日志和 Windows 行为建立意义。

稳定接口上的适配包括：IAT SendInput hook、有限命名管道 broker、单函数 event-log 文档错误返回、WinPR handle SSPI shim、可捕获 Windows SDL 窗口、GNOME RDP 的会话 capture/input。当前公共插件与 manager 分支见[架构](architecture.md)。

## 生命周期

旧 health monitor 误判 Wine 卡死与 event-log abort 是独立问题，只修一个跨不过四分钟。保持同 PID 的定时观察识别余因。systemd 拥有完整生命周期，内部 supervisor 处理 UU 替换 server，verifier 同时查静态身份和运行行为。

## 工具地图

| 工具 | 用途 |
| --- | --- |
| `rg`、`strings`、`xxd` | 源码/日志、语义位置、准确字节 |
| MinGW `objdump`、Python `struct` | PE import/section、反汇编、VA 映射 |
| `sha256sum`、MinGW GCC/binutils | 完整身份、DLL/Windows helper 构建 |
| Wine/WineGCC、Xvfb/Openbox | Windows 环境、Winlogon 形态、私有画布 |
| `xdotool`、`xauth` | 窗口焦点、受保护 X11 |
| SDL FreeRDP/WinPR、GNOME RDP | 中继窗口、原生 GNOME capture/input |
| `grdctl`、`gsettings`、`secret-tool` | RDP 设置、keyring 凭据 |
| `systemd-creds`、TPM2、D-Bus | 绑定密文、解锁已有 keyring |
| `crudini`、systemd units/sandbox | 可撤销 GDM、监督、隔离暂存 |
| `7z`、Windows SSH/PowerShell | 非执行解包、已知正常参考 |
| Git/`gh` | 版本与可复用源码；发布仍需授权 |

## 源码地图

| 文件 | 职责 |
| --- | --- |
| `patches/*.json` | 版本身份、字节编辑 |
| `gameviewer_patchlib.py`、`patch-gameviewer.py` | 校验与 patch/verify/status/restore |
| `stage-uu-release.sh`、`audit-gameviewer.py` | 私有暂存、PE 候选与审阅入口 |
| `uu_input_bridge.c`、`uu_input_broker.c`、`uu_injector.c` | IAT、有限输入、DLL 注入 |
| `winpr_sspi_shim.c`、`uu-remote-bridge` | NLA、X/RDP/UU 监督 |
| `configure-unattended.sh`、`uu-keyring-unlock.py` | GDM/TPM/回滚、D-Bus 解锁 |
| `install.sh`、`verify.sh` | 部署、静态/进程/稳定性检查 |

编译物、installer、prefix、日志、截图和反汇编留在忽略目录或私有 runtime。

可复用习惯是：先重现，拆独立链路，比已知正常实现，小探针问单一问题，选稳定 API，不在不明结果中继续，完整 hash 绑定语义，保留原字节恢复材料，检查时长与重启，将发现落入源码/测试/文档，并检查交互登录暗含依赖。四处历史字节修改只是特定版本的应用。
