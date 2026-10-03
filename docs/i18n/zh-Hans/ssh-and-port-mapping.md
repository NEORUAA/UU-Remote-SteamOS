[English](../../ssh-and-port-mapping.md) · [简体中文](ssh-and-port-mapping.md)

[首页](../../../i18n/README.zh-Hans.md)

# SSH 与可选 UU 端口映射

原生 OpenSSH 独立于桌面中继。下文使用示例别名与本机端口，请配置自己的授权端点；路由器、VPN、云中继或 UU 映射需另外准备。

## 准备 SSH 端点

目标须有 SSH 服务与授权账号。通过可信渠道核对主机密钥并配置密钥认证。SSH 密钥、真实主机名、账号和连接记录保留本地。

使用 UU 端口映射时，在官方主控建立规则并确认本地转发端口。可用性与控制权由厂商管理，接管或替换其他主控的映射前需得到操作者同意。

## 建立本地别名

`uu-ssh` 为已有映射创建 SSH 别名，不建立映射本身。示例的 `peer`、`remoteuser`、`2222` 都须替换为自己的配置：

```bash
uu-ssh add peer --port 2222 --user remoteuser --shell-transport ssh
uu-ssh check peer
uu-ssh peer
```

`uu-ssh --help` 显示当前命令；`uu-ssh key` 输出需在目标授权的公钥，私钥不要分享。配置位于 `~/.config/uu-ssh/peers/`，受管 SSH 片段位于 `~/.ssh/uu-bridge/`，均保留私有。

普通 SSH 端点可直接配置 `~/.ssh/config` 并运行 `ssh peer`；地址变化时仍保留主机密钥检查。

## 终端与消息辅助

`uu-ssh shell peer` 使用显式选定的 shell 传输。厂商终端与映射 SSH 是不同选项，终端支持取决于 UU 版本与平台。见[Ubuntu 原生终端](native-ubuntu-terminal.md)。

已授权 UTF-8 消息通道可用已有 SSH 别名，见[SSH 私有消息](agent-link.md)。消息作为数据保存，不作为命令执行。

## 转发本地服务

通过 SSH 将授权服务转发到本机：

```bash
ssh -N -o ExitOnForwardFailure=yes \
  -L 15922:127.0.0.1:5922 desktop-host
```

监听地址是回环端点。此示例供 [macOS 当前桌面访问](macos-current-desktop.md)使用，先启动服务并配置 `desktop-host`。关闭 SSH 即移除转发。密码与私有映射标识保留本地。

其他参数见 [OpenSSH 手册](https://man.openbsd.org/ssh)、[SSH 配置手册](https://man.openbsd.org/ssh_config)。UU 从[网易](https://uuyc.163.com/)获取。
