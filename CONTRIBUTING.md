# 贡献指南

本分支面向使用 Plasma Wayland 的 SteamOS 桌面模式，以及使用 gamescope 的游戏模式，兼容层采用 Steam Proton。所有生成文件都应保存在选定的安装根目录内。不要为启动器添加系统软件包安装、独立 Wine 发行版或特定设备的硬编码路径。

主要入口为 `scripts/uu-steamos`；`install.sh` 调用其 `setup` 操作。会话管理进程负责私有 Xvfb/Openbox/FreeRDP 画布、KRDP 和该 prefix 中的 Proton 工作进程。游戏模式的管理界面使用 Xephyr、Openbox 和 xcompmgr。兼容程序由 `scripts/build-compat.sh` 构建。修改 UU 二进制文件前，必须按 `patches/uu-remote-4.42.0.2770.json` 中的完整哈希进行验证。

运行源码测试和检查：

```sh
python3 -B -m unittest discover -s tests -v
bash -n install.sh scripts/build-compat.sh
python3 -B scripts/patch-gameviewer.py manifests
```

测试覆盖 Proton 发现、生成文件存放位置、共享 PID 命名空间、CUR 图像编码、模拟输入认证、鼠标和滚轮的定点数转换、输入代理分发，以及版本补丁安全性。本机测试时，请将 `TMPDIR` 设为工作区内的目录。

在已配置的 SteamOS 安装环境中，可在 `uu-steamos sandbox` 内将 `UURB_TEST_CC` 设为 `tools/host-cc`，将 `UURB_TEST_MINGW_CC` 设为 `tools/mingw-cc`，在清理编译器之前运行实际 Proton 光标加载测试。测试应使用正在运行的私有显示和对应的 Xauthority。

本机状态为 `ready` 只能证明启动和注入成功，不能证明控制端实际可用。修改画面或输入相关代码后，需要通过真实手机或电脑上的 UU 控制端连接验证，检查管理窗口外的桌面点击、悬停、键盘、光标尺寸和形状、纵向和横向滚动、滚动方向以及重新连接。

重启时保留账号数据。协议兼容补丁应只作用于已审核的 KRDP 版本及进程，不应修改桌面合成器或系统设置。
