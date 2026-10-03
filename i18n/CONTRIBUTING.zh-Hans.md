[English](../CONTRIBUTING.md) · [العربية](CONTRIBUTING.ar.md) · [Deutsch](CONTRIBUTING.de.md) · [Español](CONTRIBUTING.es.md) · [Français](CONTRIBUTING.fr.md) · [日本語](CONTRIBUTING.ja.md) · [한국어](CONTRIBUTING.ko.md) · [Русский](CONTRIBUTING.ru.md) · [Tiếng Việt](CONTRIBUTING.vi.md) · [简体中文](CONTRIBUTING.zh-Hans.md) · [繁體中文](CONTRIBUTING.zh-Hant.md)

[简体中文 · UU Remote Ubuntu Plus](README.zh-Hans.md)

# 参与 UU Remote Ubuntu Plus

报告问题、补充翻译、改进文档和提交代码都欢迎。项目基于 [Lachlan Chen 的 MIT 桥接器](https://github.com/lachlanchen/uu-remote-ubuntu-bridge)，请保留上游署名、技术历史与许可证。

## 说明问题与使用路径

提供 Ubuntu、GNOME、Wine、UU 版本、画布、输入路由、操作步骤和观察结果。分别说明远程设备控制 Ubuntu、本机 UU 账号管理、Ubuntu 控制其他设备这三条路径。提交小而明确的改动，记录实测 FPS 或延迟所用的方法。可在[兼容性反馈表](https://github.com/llmir/uu-remote-ubuntu-plus/issues/new?template=compatibility.yml)提交反馈。

## 准备开发依赖

使用 Ubuntu 和系统 Python 3。下列软件包用于原生构建与隔离测试，安装运行环境仍由 install.sh 管理。选择其他工具链时使用 WINEGCC、MINGW_CC、HOST_CC 等变量，不写入个人绝对路径。测试使用临时 Wine 前缀和 Xvfb 显示。

```bash
sudo apt-get update
sudo apt-get install --no-install-recommends \
  build-essential binutils gcc-mingw-w64-x86-64-win32 \
  wine wine64 wine64-tools xvfb x11-utils x11-xserver-utils xclip xcompmgr
```

## 检查源码

对改动的 shell 文件运行 bash -n，再执行下列检查。C 编译警告保持严格检查；有些测试需要 Wine、Xvfb 或可用的用户 systemd 总线，报告实际执行与跳过项目。UURB_TEST_SYSTEMD=1 仅用于具备相应服务环境的测试。

```bash
python3 -m compileall -q scripts tests
python3 -m unittest discover -s tests -v
./scripts/build-compat.sh
git diff --check
```

## 修改文档与插画

文档改动运行现有文档测试。docs/images 中数据流和迁移图的英文与简中 SVG 共用布局，修改对应 SVG 标签或路径后，可选用 Node.js 与 Sharp 重绘 PNG/GIF。命令中的后两行仅在需要重绘时执行。图片需检查完整画面和元数据，收款码原文件保持不变。

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_documentation.py -q
npm install --no-save --package-lock=false sharp
node scripts/render-doc-graphics.cjs
```

## 检查安装后的运行行为

在授权的 Ubuntu 测试主机安装源码并检查运行组件；安装会短暂断开 UU，提前准备可用恢复连接。完整验证器含 270 秒稳定性阶段，输入、画面、重连等变化还需真实控制端操作。仅停止专用 Wine 前缀，不用全局 pkill wine。手动更新已有安装的步骤见[更新现有安装](../docs/i18n/zh-Hans/update-handoff.md)。

```bash
./install.sh --skip-packages --skip-account-login
./scripts/verify.sh --quick
./scripts/verify.sh
./uninstall.sh --dry-run
```

## 适配新版 UU

新版可执行文件需要新的审查与获准清单，核对安装器、原服务器、补丁服务器、健康监控的完整 SHA-256 和每项等长修改。提供补丁验证、逐字节恢复、冷启动、输入、重连与卸载结果。不要发布网易可执行文件、账号状态或私有原始审计日志。详细流程见[上游维护](../docs/i18n/zh-Hans/upstream-maintenance.md)。

定位兼容性问题时，可结合[工程方法与工具](../docs/i18n/zh-Hans/methodology-and-toolkit.md)、[4.33 逆向工程记录](../docs/i18n/zh-Hans/reverse-engineering.md)与[Windows 参考对照](../docs/i18n/zh-Hans/windows-reference.md)。

## 准备可公开的改动

提交前核对文件清单和暂存差异。保留源码和必要静态资源，排除构建产物、Wine 前缀、缓存、.omc 运行记录、凭据、设备标识和原始输入日志。保持认证、TLS、清单检查、账号状态与可逆卸载。

```bash
git status --short
git diff --cached
```

## 提交与协作

描述具体问题、改动后行为和实际运行的检查，邀请独立审阅。不要把中继设置值写成实测 FPS。阅读 [中文画质指南](../docs/i18n/zh-Hans/quality-guide.md)、[Ubuntu 适配](../docs/i18n/zh-Hans/ubuntu-26.04-port.md) 与 [安全说明](../docs/i18n/zh-Hans/security.md)。贡献保持 MIT 许可与原版权声明。
