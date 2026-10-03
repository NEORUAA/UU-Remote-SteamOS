[English](../../porting.md) · [العربية](../ar/porting.md) · [Deutsch](../de/porting.md) · [Español](../es/porting.md) · [Français](../fr/porting.md) · [日本語](../ja/porting.md) · [한국어](../ko/porting.md) · [Русский](../ru/porting.md) · [Tiếng Việt](../vi/porting.md) · [简体中文](../zh-Hans/porting.md) · [繁體中文](../zh-Hant/porting.md)

[Trang chủ](../../../i18n/README.vi.md)

# Chuyển sang desktop Linux khác

GNOME x86-64 gần nhất: giữ RDP và đổi cài đặt. KDE/Xfce cần bộ thích nghi riêng. Hiện cài Ubuntu 24.04/26.04; nền tảng khác là mục tiêu chuyển.

Cài relay cần đúng bộ công cụ đã duyệt hoặc đầu ra đã kiểm tra có sẵn; các gói APT thông thường không tự cung cấp bộ công cụ này. Xem [điều kiện biên dịch và dùng lại bộ đệm](source-build.md).

![Ba lớp chuyển nền tảng](../../images/uu-plus-porting.png)

[SVG chỉnh sửa được](../../images/uu-plus-porting.svg)

| Lớp | Dùng lại | Thích nghi/nguồn |
| --- | --- | --- |
| Lõi |Wine/UU riêng, manifest, SDL/FreeRDP, broker/plugin, khung/quản lý|Giữ biên giới, táchUnicode/phím; [broker](../../../src/uu_input_broker.c), [RDP](../../../src/freerdp-adapter.c), [plugin](../../../src/plugin.c), [chụp](../../../src/uu_manager_capture.c)|
| Phân phối |Công thức/kiểm tra/cấu hình/dịch vụ|Gói/đường/thư viện/launcher; [cài](../../../install.sh), [build](../../../scripts/build-winpr.sh), [kiểm tra](../../../scripts/verify-freerdp-runtime.py), [dịch vụ](../../../systemd/uu-remote-bridge.service)|
| Desktop |Sự kiệnRDP/văn bản/thao tác|Phiên/chụp/nhập/clipboard/hình học/thao tác; [chạy](../../../scripts/uu-remote-bridge), [văn bản](../../../src/uu_x11_input.c), [mức](../../../scripts/uu-display-modes.py)|

API công khai FreeRDP dùng kết nối có sẵn; đổi máy chủ độc lập hook Windows UU. Unicode cần clipboard nguồn/dán, hiện X11/Xwayland. Quản lý ở X11 riêng Wine. [Kiến trúc](architecture.md).

| Nền tảng | Dùng lại và việc cần làm |
| --- | --- |
| Ubuntu 24.04/GNOME 46 |Installer/backend có sẵn, backport libei tùy chọn|
| Ubuntu 26.04/GNOME 50 |Plus, libei hệ thống, UU 4.42|
| Debian/GNOME |Lõi/khung/RDP; gói/Wine Debian, preflight/daemon/thư viện; [APT/dpkg](https://www.debian.org/doc/manuals/debian-reference/ch02.en.html)|
| Fedora/GNOME |Lõi/backend; RPM/DNF/đường/quyền; [GRD](https://packages.fedoraproject.org/pkgs/gnome-remote-desktop/gnome-remote-desktop/)|
| Arch/GNOME |Lõi/backend; pacman/đường/công cụ/cập nhật GNOME libei; [GRD](https://archlinux.org/packages/extra/x86_64/gnome-remote-desktop/)|
| KDE |Lõi/khung/quản lý; phiên/chụp/nhập/đầu ra/clipboard/thao tác; [KRDP](https://github.com/KDE/krdp) cần xác thực/codec/văn bản|
| Xfce/X11 |Lõi/khung/quản lý/X11; phiên/hình học/thao tác; VNC `legacy` là khởi điểm|

Đổi quản lý gói chỉ giải quyết cài đặt. Phải nối chụp, nhập, hình học nguồn và thao tác.

| Giao diện | Hiện tại / chuyển đổi |
| --- | --- |
| Kiến trúc |`x86_64`, AMD64 PE; máy khác cần chạyAMD64/kiểm tra|
| Gói |Ubuntu, `apt-get`, `dpkg`, i386, WineHQ; ánh xạ đích|
| Wine |`/opt/wine-stable/bin/wine`, `wineserver`, `winepath`; đồng nhất chạy/dọn|
| Công cụ |MinGW/CMake/Meson/Ninja/gói cố định; khớp hoặc duyệt mới; [nguồn](source-build.md)|
| Phiên |`gnome-shell`, D-Bus, `/usr/libexec/gnome-remote-desktop-daemon`; tìm/thay|
| Đăng nhập |Keyring, `secret-tool`, `grdctl`, `org.gnome.desktop.remote-desktop.rdp`; TLS/dịch vụ riêng UU|
| Đầu ra |`org.gnome.Mutter.DisplayConfig`, màn hình ảo; compositor/XRandR X11|
| Chữ |`uu-x11-input`/`xclip`, `CLIPBOARD`/`PRIMARY`; display đúng, WaylandAPI|
| Thao tác |`_NET_SHOWING_DESKTOP`, `org.gnome.Shell.OverviewActive`; WM/trạng thái đích|
| Dịch vụ |`systemctl --user`, D-Bus đồ họa; phiên/init đích|
| Công cụ desktop |`/usr/bin/xfreerdp`, `xtigervncviewer`, `obconf`, `zenity`; đường/font/DPI/đăng nhập tương tác/bảo vệrelay|

Khung riêng Wine/Xvfb khác đầu ra vật lý/ảo. Giữ bốn mức và thay logic Mutter trên KDE/Xfce.

1. Chọn OS/phiên x86-64, ghi OS/desktop/Wine/UU.
2. Đổi gói/đường/thư viện/dịch vụ/launcher, kiểm tra relay.
3. Nối chụp/nhập/bus/display/đăng nhập/hình học/clipboard.
4. Thử controller thật: chuột/click/cuộn/kéo, phím tắt, Unicode/dán/nối lại, quản lý/popup.
5. Thử bốn mức, khôi phục, hoàn tác, dọn tiến trình/thao tác.

Đóng góp mapping/đường/phiên bản/kết quả, không kèm UU hay tài khoản. [So sánh](upstream-comparison.md), [chất lượng](quality-guide.md).
