[English](../../quality-guide.md) · [العربية](../ar/quality-guide.md) · [Deutsch](../de/quality-guide.md) · [Español](../es/quality-guide.md) · [Français](../fr/quality-guide.md) · [日本語](../ja/quality-guide.md) · [한국어](../ko/quality-guide.md) · [Русский](../ru/quality-guide.md) · [Tiếng Việt](../vi/quality-guide.md) · [简体中文](../zh-Hans/quality-guide.md) · [繁體中文](../zh-Hant/quality-guide.md)

[首页](../../../i18n/README.zh-Hans.md)

# 画质、分辨率与帧率

先在 Ubuntu 选择画布，再在控制电脑或手机上调整串流画质。画布大小、压缩画质、请求帧率和码率上限是独立设置。

## 选择画布

在 GNOME 应用列表打开 **UU Remote 画质与分辨率**，或运行：

```bash
uu-remote quality gui
uu-remote quality list
uu-remote quality status
uu-remote quality apply 2160p
uu-remote quality guide
```

![Ubuntu 四档画布选择器](../../images/quality-presets.png)

| 档位 | 画布 | 适合场景 |
| --- | --- | --- |
| `720p` | 1280 × 720 | 小屏幕或带宽有限 |
| `1080p` | 1920 × 1080 | 日常使用；首次安装默认值 |
| `1440p` | 2560 × 1440 | 增加工作空间，像素量低于 4K |
| `2160p` | 3840 × 2160 | 清晰文字与完整 4K 工作区 |

重装保留已保存的选择。智能缩放将整个源桌面放入画布，并按相同几何关系映射鼠标坐标。源分辨率和比例影响结果；画布不会改变 GNOME 物理桌面的分辨率，捕获仍可能处理完整源图像。

选择器分别显示**保存的启动／请求 RDP 尺寸**和**当前画布**。修改保存尺寸会短暂重连。重新应用已保存档位，可在支持的 RDP 路径上恢复实时画布而无需重启中继；选择器会核对实际尺寸。修改前启动回退定时器，桥接无法就绪时恢复旧配置。等待恢复结束后再改下一项。

固定档位使用安装默认值 `--follow-desktop-resolution off`。曾开启跟随桌面分辨率时，请先通过该安装参数关闭，再应用档位。见[安装说明](../../../i18n/README.zh-Hans.md)及 `./install.sh --help`。

实测 4K 源放大为 5K 后没有增加细节，在 Mac 上反而更模糊，因此常用选择最高为 4K。标称 60 Hz 描述虚拟显示模式，实际串流帧率取决于整条连接。

## 控制端画质与帧率

电脑打开**控制中心 → 画质**；手机打开**操作 → 显示**。支持真彩时，也在控制端选择。

![UU 原生画质与帧率菜单示例](../../images/uu-native-quality-menu.png)

此示例来自 Ubuntu 控制 Mac。可用画质、帧率和色彩选项取决于设备与编解码器。画质影响压缩和细节，请求帧率设置 UU 的目标更新速率，真彩可改善彩色文字和边缘。若 UU 提示设备性能限制，选择可用档位；用同一段文字和移动场景比较清晰度与响应。

参阅网易的[帧率与超级屏指南](https://uuyc.163.com/help/superscreen.html)、[真彩说明](https://uuyc.163.com/features/color/)和[兼容性说明](https://uuyc.163.com/help/20241216/40221_1200122.html)。Wine 下超级屏／虚拟显示驱动及 144 FPS 仍待测试。[性能说明](performance-evidence.md)介绍控制端测量方法。

## 码率上限

```bash
uu-remote quality bitrate 20
uu-remote quality bitrate 0
```

`20` 通过 UU CLI 请求 **20 Mbps 上限**，`0` 取消上限。它不设置目标码率、帧率或画布尺寸；切换档位保留码率设置。过低的上限会让运动画面细节变软，请在实际连接上比较。

## 光标与桌面动作

可选光标保护在首次安装时默认关闭。指针过大时可启用：

```bash
./install.sh --skip-packages --skip-account-login --cursor-guard on --cursor-size 24
```

`--cursor-size auto` 跟随桌面光标大小；固定值范围为 24–128 像素。GNOME 与应用光标设置独立保留。Dock 使用你的 GNOME 设置。Android 的显示桌面、显示所有窗口已映射到 GNOME 桌面与概览，手机按钮实测待完成。

## 管理窗口与恢复

`uu-remote open` 打开独立管理查看器。放大该窗口：

```bash
UURB_WINDOW_SCALE=2 ./install.sh --skip-packages --skip-account-login
```

支持 `1`（默认）、`1.5`、`2`、`3`，只改变查看器，不改变 Wine DPI 或桌面分辨率。管理窗口关闭剪贴板交换；桌面复制粘贴走中继。

```bash
uu-remote status
uu-remote quality status
uu-remote network
uu-remote logs
```

用户服务会重启故障中继组件，可能短暂重连。档位回退恢复设置，运行时部署使用自己的恢复流程。见[故障排查](troubleshooting.md)和[源码构建](source-build.md)。

主要用法是其他 UU 设备控制 Ubuntu。Ubuntu Wine 客户端控制其他电脑时，画质限制另行处理。本机物理显示器关闭／开启及虚拟输出待测，见 [Ubuntu 26.04 说明](ubuntu-26.04-port.md)。手机 → ToDesk → Mac → UU 多跳链路仍有重复输入问题；手机和 Mac 直连输入正常。
