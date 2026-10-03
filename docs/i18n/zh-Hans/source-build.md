[English](../../source-build.md) · [العربية](../ar/source-build.md) · [Deutsch](../de/source-build.md) · [Español](../es/source-build.md) · [Français](../fr/source-build.md) · [日本語](../ja/source-build.md) · [한국어](../ko/source-build.md) · [Русский](../ru/source-build.md) · [Tiếng Việt](../vi/source-build.md) · [简体中文](../zh-Hans/source-build.md) · [繁體中文](../zh-Hant/source-build.md)

[首页](../../../i18n/README.zh-Hans.md)

# 构建与复用桌面中继

安装器从固定版本源码构建 FreeRDP SDL 客户端，并应用 Plus 的剪贴板和桌面尺寸补丁。[构建配方](../../../vendor/freerdp-sdl-build/)、[源码锁定文件](../../../vendor/freerdp-sdl-build/source-lock.json)和[产品配置](../../../patches/freerdp-sdl-product.json)记录版本、归档、工具链及 13 个 Windows 运行时文件。

<a id="reference-toolchain"></a>

## 准备 Ubuntu 26.04 参考工具

在 Ubuntu 26.04 amd64 上，[工具链准备脚本](../../../scripts/prepare-build-toolchain.py)会下载 17 个固定版本的 Ubuntu 官方软件包，并按 `source-lock.json` 校验 14 个编译器／构建工具文件。[软件包清单](../../../patches/reference-build-packages.json)记录包版本、大小与哈希。脚本负责下载、私有解包和校验，不安装系统软件包。从仓库根目录运行：

```bash
python3 scripts/prepare-build-toolchain.py \
  --packages-dir "$HOME/.cache/uu-plus/reference-packages" \
  --root "$HOME/.cache/uu-plus/reference-root"
```

`--packages-dir` 指定软件包缓存；`--root` 须是新的或空的私有目录。使用已有缓存重新解包并校验工具时，换一个空目录，加上 `--verify-only`，整个过程不访问网络：

```bash
python3 scripts/prepare-build-toolchain.py \
  --packages-dir "$HOME/.cache/uu-plus/reference-packages" \
  --root "$HOME/.cache/uu-plus/reference-root-offline" \
  --verify-only
```

脚本会打印包含全部 17 个本地 `.deb` 路径的 `sudo apt install` 命令。在 Ubuntu 26.04 上手动执行这条命令，将参考工具安装到系统。现有构建配方读取固定的 `/usr` 路径；私有解包目录用于校验工具，不用于切换构建环境。

随后运行普通安装器。它会准备其余主机构建依赖、WineHQ 和 GNOME 运行包，进入现有中继构建流程，并在部署前验证运行时。工具准备校验的是 14 个参考文件；完整源码构建及其 13 个运行时文件由这条流程检查：

```bash
./install.sh
./scripts/verify.sh --quick
```

Ubuntu 24.04 可按下文复用流程，使用与当前产品配置匹配的已有已验证输出。上面的 Ubuntu 26.04 软件包仅适用于 26.04。

## 构建与复用

冷源码构建需要 `source-lock.json` 中记录的已审核编译器和构建工具文件，字节身份须一致。普通发行版 APT 软件包不会自动提供这套工具链。

正常执行 `./install.sh` 会准备依赖，并在替换已安装中继前验证运行时。只有来源记录与当前产品配置、配方和运行时固定值匹配时，才复用 `build/freerdp`；否则 `scripts/build-winpr.sh` 用新源码执行双任务构建，限时 900 秒，再检查结果。

已审核工具安装在配方指定的 `/usr` 路径，且主机构建依赖齐备后，也可单独构建中继缓存：

```bash
UURB_BUILD_DIR=/absolute/path/to/build-work   ./scripts/build-winpr.sh /absolute/path/to/fresh-output
```

使用新的输出目录。脚本在构建工作目录下创建唯一源码任务，与运行中的 Wine 前缀无关。更新时复用已验证输出：

从仓库根目录先按当前配置验证已有输出。普通安装器会准备主机依赖；只有主机兼容组件构建工具、WineHQ 和 GNOME 运行包已安装时，才使用 `--skip-packages`。已有账号配置时可选 `--skip-account-login`。

```bash
python3 scripts/verify-freerdp-runtime.py --mode build /absolute/path/to/verified/output
```

再通过现有安装入口复用该输出：

```bash
UURB_FREERDP_PREBUILT_DIR=/absolute/path/to/verified/output   ./install.sh
```

缓存须匹配当前配方、运行时固定值及产品配置的来源记录。配置变化后需要重新执行构建和验证入口；修改生成的收据或校验文件不能批准其他二进制。安装器在启动服务前还会检查复制后的运行时。

## 固定构建输入

FreeRDP/WinPR、SDL 3.2.28、SDL_ttf、OpenH264、FreeType、HarfBuzz 从固定输入构建，另配固定 OpenSSL、cJSON 和 uriparser 运行时包。编译前检查源码补丁以及 MinGW、编译器和构建工具哈希。改变工具或依赖需要审核新配方。

文件、宏和调试前缀映射会规范二进制中的源码与输出根路径。FreeRDP 的 opaque 设置从首次配置起明确关闭；兼容 DLL 使用相对输出文件名，避免把本机检出路径写入运行时。

## 构建结果

固定工具链在两组不同源码／输出根目录下产生了全部 13 个文件的相同字节。首次与重复 CMake 配置的元数据一致。一次不使用预构建输出的完整冷源码构建约耗时 700 秒，在 900 秒期限内完成，通过运行时和来源检查。

这些数据描述构建。画布与串流设置见[画质指南](quality-guide.md)，构建资源数据见[性能与成本](performance-evidence.md)。
