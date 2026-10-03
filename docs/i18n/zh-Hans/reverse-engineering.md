[English](../../reverse-engineering.md) · [中文（简体）](../zh-Hans/reverse-engineering.md)

[← 返回简体中文首页](../../../i18n/README.zh-Hans.md)

# 逆向工程记录

本页记录 **4.33.0.8907** 兼容补丁的可复现分析。地址和字节只对应该版本，不用于 4.42 或其他版本。机器可读基准为[4.33 清单](../../../patches/uu-remote-4.33.0.8907.json)，新版本按[上游维护](upstream-maintenance.md)重新审阅，generic patcher 拒绝未知 hash 与 draft。

## 文件与 Windows 参考

下列原始身份块依次给 installer、server 原件/补丁结果和 healthd；改前保留 `.uu-original`。相同版本 Windows 11 有签名 root HID、键盘 collection 和 switch=1；Wine 枚举百余重复合成 HID/鼠标、无键盘且 `gvinput.sys` 未安装。目标是选已有用户态输入，不模拟/削弱内核 driver。

## 字符串、xref 与坐标

strings/objdump 找 `virtual switch state` 等语义，并由 `.rdata` file offset `0x1531000`、VA `0x141532000` 推出目标 string VA `0x14154e2f0`，xref 在 `0x1402305cd`。针对两个函数小范围反汇编。早期手工范围漏 `.text` 对齐 delta，manifest 一直用 file offset，准确补丁字节未受影响。

xxd 保留编辑附近字节。构造器在 `0x1e0` 写 DWORD `0x100`，使 `0x1e1` switch 为 true。四个等长编辑保持周边流：

| File offset | 原字节 | 替换 | 意义 |
| --- | --- | --- | --- |
| `0x22f719` | `00 01 00 00` | `00 00 00 00` | 默认 false |
| `0x22f906` | `0f b6 08` | `31 c9 90` | 构造设置 false |
| `0x1dbab6` | `0f 94 c0` | `31 c0 90` | 读设置返回 false |
| `0x1dbcb7` | `40 88 37` | `c6 07 00` | setter 写 false |

patcher 检查长唯一签名、预期 offset、完整输入/输出 hash，不搜索三字节片段猜版本。

## service token 与四分钟 abort

普通 Wine SendInput probe 可经过 SDL/RDP 到 Ubuntu，但 GameViewerServer 同调用返回 error5 `ERROR_ACCESS_DENIED`。GameViewerService 经 `CreateProcessAsUser`/TokenUIAccess 创建的 token 在 Wine 被拒。IAT hook 先调用原函数，失败再交普通 Wine 用户 broker 的有限 INPUT 数组；这是历史旧输入分支，当前 `rdp-public` 见[架构](architecture.md)。

health monitor 在 Wine 误判 main loop，替换 sleeping stub 后 server 仍每四分钟退出，stderr 指向未实现 `wevtapi.dll.EvtOpenPublisherMetadata`。只改该 IAT slot，返回 null 与文档错误 15002，caller 原本可处理；同 PID 遂跨过旧时限。其他 event-log import 不泛化绕过。

## FreeRDP/NLA

Windows SDL 窗口正常，但 Wine SSPI 私有 handle 不满足 NLA。按同版源码构建 libwinpr3，启内部 MD4/MD5/RC4，关闭 native SSPI，固定 OpenSSL/cJSON/uriparser runtime，使用 `/sspi-module` shim 与 `/auth-pkg-list:none,ntlm`。shim 调 WinPR InitSecurityInterfaceExA/W，在 AcquireCredentialsHandle/InitializeSecurityContext 周围规范 credential/context package field；WinPR 3.31 使用反转 numeric package ID，旧版本是反转 name pointer。

## 原始技术块与复现命令

以下块按英文记录原顺序保留，分别是身份、Windows/Wine 状态、strings/section/disassembly、准确字节、构造写入、switch/input 结果及 event-log import。用于复现同一历史版本，不表达当前安装版本。


```text
UU installer 4.33.0.8907
5e3cfe8cfdc6552c1fc26f1ad2c94df133ca20dc3c45c23155358c32ac9bf53e

GameViewerServer.exe, upstream
be1c6c108e6e4d0d5cc15dcd22650dc5fde34c7e7b9f19eee72aba0160ea3494

GameViewerServer.exe, patched
30cad61560213c7a66244c6f79c9017cc9dfa81996d7faa15a0e8bf330aa0948

GameViewerHealthd.exe, upstream
ba4cdef465b3714940b154d6d40d7cfca4d65c3d639a6254bb0fb7be69bd19e6
```

```text
virtual switch state:1
input_device_count:1 keyboard_device_count:1
input_driver_installed:1
```

```text
input_device_count:127 keyboard_device_count:0
input_driver_installed:0
```

```bash
server='GameViewerServer.exe.uu-original'

strings -a -t x "$server" | \
  rg 'virtual switch state:|set_virtual_mouse_switch|read setting read_user_setting:'

x86_64-w64-mingw32-objdump -h "$server"
x86_64-w64-mingw32-objdump -d -M intel "$server" > server.objdump
rg -n '14154e2f0|set_virtual_mouse_switch' server.objdump
```

```text
01543b10 read setting read_user_setting:...
01543b40 set_virtual_mouse_switch function label
01543b90 set_virtual_mouse_switch log text
0154d2f0 virtual switch state
```

```bash
x86_64-w64-mingw32-objdump -d -M intel \
  --start-address=0x140230280 --stop-address=0x140230980 "$server"

x86_64-w64-mingw32-objdump -d -M intel \
  --start-address=0x1401dc640 --stop-address=0x1401dc930 "$server"
```

```bash
xxd -g 1 -s 0x22f700 -l 64 "$server"
xxd -g 1 -s 0x22f8f0 -l 48 "$server"
xxd -g 1 -s 0x1dbaa0 -l 48 "$server"
xxd -g 1 -s 0x1dbca0 -l 48 "$server"
```

```text
0022f710: 00 01 00 c7 86 e0 01 00 00 00 01 00 00 88 86 e4
0022f900: ff e8 c9 10 e0 ff 0f b6 08 88 8d 38 01 00 00 48
001dbab0: f5 e5 ff 83 fb 02 0f 94 c0 88 07 48 8d 05 06 84
001dbcb0: 01 cc e8 62 f3 e5 ff 40 88 37 48 8d 05 7f 82 36
```

```text
c7 86 e0 01 00 00 00 01 00 00
```

```text
virtual switch state:0
```

```text
count=1 type=0 flags=0x00000001 result=0 error=5
```

```text
route=broker result=1 error=0
```

```text
wine: Call from ... to unimplemented function
wevtapi.dll.EvtOpenPublisherMetadata, aborting
```

```bash
x86_64-w64-mingw32-objdump -p "$server" | \
  rg -C 3 'wevtapi|Evt[A-Z]'
```

```text
EvtQuery
EvtNext
EvtRender
EvtOpenPublisherMetadata
EvtClose
```

`audit-gameviewer.py` 自动生成 PE 映射、landmark、masked signature 候选与有限反汇编；输出仍是 draft，必须审阅语义。临时 capture/SendInput probe 不属于产品源码。
