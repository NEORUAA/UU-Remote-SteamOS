[English](../../troubleshooting.md) · [العربية](../ar/troubleshooting.md) · [Deutsch](../de/troubleshooting.md) · [Español](../es/troubleshooting.md) · [Français](../fr/troubleshooting.md) · [日本語](../ja/troubleshooting.md) · [한국어](../ko/troubleshooting.md) · [Русский](../ru/troubleshooting.md) · [Tiếng Việt](../vi/troubleshooting.md) · [简体中文](../zh-Hans/troubleshooting.md) · [繁體中文](../zh-Hant/troubleshooting.md)

[Tiếng Việt · UU Remote Ubuntu Plus](../../../i18n/README.vi.md)

# Khắc phục sự cố

## Kiểm tra trước

Chạy từ thư mục mã nguồn. Nhật ký ở `~/.local/state/uu-remote-bridge`, thiết lập ở `~/.config/uu-remote-bridge/environment`. Gửi phiên bản và lỗi, bỏ thông tin tài khoản và nội dung nhập. Thay mã nguồn xong cần cài lại.

```bash
uu-remote status
./scripts/verify.sh --quick
uu-remote logs
uu-remote network
```

## Ngoại tuyến sau khởi động

Đăng nhập một lần trong cửa sổ chính thức rồi đóng bình thường. Kiểm tra dịch vụ người dùng và keyring. Nếu đổi mật khẩu, dùng `./scripts/configure-unattended.sh enable --replace-credential` cập nhật thông tin mã hóa. Xem quá trình khôi phục khi server thoát.

```bash
uu-remote login
./scripts/configure-unattended.sh status
journalctl --user -b -u uu-keyring-unlock.service -u uu-remote-bridge.service --no-pager
```

## Tìm tuyến mãi không xong

Kiểm tra máy chủ đã khởi động xong. Bản ghi thiết bị nhập và Bluetooth cũ trong Wine có thể gây chậm. Lệnh sửa sao lưu registry, dọn các mục đã nhận diện trong prefix UU rồi khởi động lại; Bluetooth Ubuntu được giữ nguyên.

```bash
uu-remote repair-registry
./scripts/verify.sh --quick
```

## Màn hình đen, trắng hoặc sai phiên

Kiểm tra phiên GNOME đã đăng nhập, cổng RDP và nhật ký SDL. Chọn `--desktop-target xrdp` cho XRDP, `physical` cho màn hình vật lý. `--desktop-relay vnc` chỉ dành cho X11; Wayland dùng RDP.

```bash
systemctl --user status uu-remote-bridge.service
/usr/bin/grdctl status
loginctl list-sessions
tail -80 ~/.local/state/uu-remote-bridge/freerdp.log
tail -80 ~/.local/state/uu-remote-bridge/gnome-remote-desktop.log
```

## Viền trống, cắt ảnh hoặc 4K nặng

So kích thước nguồn và khung hình. Chọn 720p/1080p/1440p/4K. Khung hình, FPS điều khiển và bitrate là thiết lập riêng. Chuyển chế độ gây kết nối lại ngắn và tự quay về khi lỗi; kiểm tra cả thay đổi kích thước XRDP.

```bash
uu-remote quality status
uu-remote quality gui
uu-remote quality apply 1080p
```

## Có ảnh nhưng không nhập được

Mở quản lý bằng uu-remote open, không chạy cùng prefix ở X display khác. Đóng viewer trả focus cho relay. Văn bản điện thoại dùng clipboard/RDP paste, phím vật lý giữ sự kiện. Cài lại và xem input injector sau cập nhật. Nếu lần nhấp đầu làm ngắt phiên, kiểm tra UU SendInput bridge active, UU Wine event-log compatibility active và broker; `uu-remote restart` khôi phục thành phần.

```bash
uu-remote open
./scripts/verify.sh --quick
tail -80 ~/.local/state/uu-remote-bridge/input-injector.log
```

## Phím chậm, sai ký hiệu hoặc giảm sau lâu

So VPN, proxy và tuyến UU; stale là phiên cũ. Nếu xác nhận sai NIC, thử `--network-interface default`, quay về `all`. Có thể thử `--physical-key-delay-ms 8`, mặc định `0`. Ký hiệu theo bàn phím Ubuntu. Kiểm tra GRD/libei và file descriptor khi dùng lâu bị giảm.

```bash
uu-remote network
ip -4 route show default
```

## Con trỏ mất hoặc nhỏ

Bảo vệ con trỏ mặc định tắt. auto theo kích thước desktop, giá trị cố định 24–128. Tắt bằng `--cursor-guard off`; không cần đổi độ phân giải hay DPI Wine toàn cục.

```bash
./install.sh --skip-packages --skip-account-login --cursor-guard on --cursor-size auto
```

## Terminal UU thoát hoặc lệch chữ

Cài bản cầu nối hiện tại và kiểm tra kênh. Chọn PowerShell trong UU để mở shell đăng nhập Ubuntu. Mở phiên mới nếu vị trí chữ sai, xem metadata terminal-bridge.log, không tùy ý thay powershell.exe.

```bash
./install.sh --skip-packages --skip-account-login
./scripts/verify.sh --quick
./scripts/test-terminal-bridge.sh
```

## RDP, NLA hoặc SSPI báo lỗi

Truy vấn chỉ kiểm tra có thông tin đăng nhập, không in mật khẩu. Nếu cần, xóa riêng mục keyring của cầu nối rồi cài lại. FreeRDP, WinPR và DLL phải cùng phiên bản cố định.

```bash
/usr/bin/secret-tool lookup service uu-desktop-bridge username "$USER" >/dev/null
/usr/bin/grdctl status
```

## Mac RDP/VNC, Windows App kẹt

FreeRDP nội bộ đã dùng cổng chia sẻ desktop; remote login mở phiên khác. Tìm cổng VNC loopback thực rồi chuyển tiếp SSH. Configuring thì mở lại Windows App trên Mac trước, sau đó kiểm tra XRDP.

```bash
~/.local/bin/uu-remote-console relay-port
ss -ltnp
```

## Khởi động lại, âm thanh và gỡ bỏ

Trình xác minh đầy đủ kiểm tra ổn định. Xem riêng âm thanh UU, Wine PulseAudio và chuông VNC trong môi trường chuyên dụng. Xem trước khi gỡ; bình thường giữ prefix, `./uninstall.sh --purge` xóa cả trạng thái tài khoản. Dùng `wpctl status` xác định luồng âm thanh thật. `UURB_UU_AUDIO=system` là mặc định tương thích; ALSA im lặng riêng và cách hoàn nguyên nằm trong hướng dẫn tiếng Anh chi tiết.

```bash
./scripts/verify.sh
uu-remote logs
./uninstall.sh --dry-run
```

Đọc thêm: [hình ảnh](quality-guide.md), [biên dịch](source-build.md), [kiến trúc](architecture.md), [nhập liệu](adaptive-keyboard-relays.md), [nâng cấp](reusable-upgrade.md). [Chi tiết kỹ thuật và lịch sử (English)](../../troubleshooting.md) giải thích registry, driver, âm thanh, XRDP và terminal.

## Hướng dẫn chi tiết

- Khôi phục XRDP và bàn phím · [English](../../xrdp-and-keyboard-recovery.md) · [简体中文](../zh-Hans/xrdp-and-keyboard-recovery.md)
- Tương thích bàn phím · [English](../../mobile-keyboard-parity-handoff.md) · [简体中文](../zh-Hans/mobile-keyboard-parity-handoff.md)
- Desktop hiện tại từ Mac · [English](../../macos-current-desktop.md) · [简体中文](../zh-Hans/macos-current-desktop.md)
- Desktop vật lý dùng chung · [English](../../shared-physical-desktop.md) · [简体中文](../zh-Hans/shared-physical-desktop.md)
- Khôi phục sau thoát · [English](../../clean-exit-recovery.md) · [简体中文](../zh-Hans/clean-exit-recovery.md)
- Agent điều khiển · [English](../../controller-agent.md) · [简体中文](../zh-Hans/controller-agent.md)
- Tin nhắn agent qua SSH · [English](../../agent-link.md) · [简体中文](../zh-Hans/agent-link.md)
