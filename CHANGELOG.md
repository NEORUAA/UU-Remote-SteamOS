# 更新日志

## 0.1.0-steamos

- 将 Ubuntu 产品入口替换为可移植的 SteamOS 桌面模式运行环境。
- 复用已安装的 Steam Proton，自动发现用户及外部 Steam 库。
- 将安装、构建和运行时生成的数据集中保存在可配置目录中。
- 在宿主 Xwayland 桌面上直接显示 UU 管理窗口。
- 通过 KRDP 和原生 FreeRDP 转发 Plasma 桌面，使用原生 XTEST 输入。
- 修正 KRDP 6.4.3 的认证，以及鼠标位置、滚轮的定点数编码。
- 将原生光标图像读入 Proton，保留实际尺寸和热点。
- 恢复失效的控制套接字，通过临时桌面用户单元运行后台服务。
- 显示桌面启动错误，将启动器日志保存在安装根目录内。
- 检测游戏模式，通过现有系统库转发 gamescope 的 PipeWire 输出。
- 通过现有 EIS 输入席位转发游戏模式下的鼠标、键盘和滚轮输入。
- 关闭管理窗口后保留远程后台，再次启动时恢复实际 UU 界面。
- 将原生 Steam 快捷方式的 AppId 传给管理窗口，无需选择 Steam Play 兼容性工具。
- 跟随获得焦点的 gamescope 光标，并兼容热点未更新的隐藏光标。
- 提供停止会话后的清理功能，保留账号数据和必要运行组件。
- 移除 Ubuntu/GNOME 服务、TigerVNC 管理窗口和未使用的实验功能。

衍生自 UU Remote Ubuntu Plus 和 Lachlan Chen 采用 MIT 许可证的桥接项目。
