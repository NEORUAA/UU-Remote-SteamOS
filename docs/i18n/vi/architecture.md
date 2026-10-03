[English](../../architecture.md) · [العربية](../ar/architecture.md) · [Español](../es/architecture.md) · [Français](../fr/architecture.md) · [日本語](../ja/architecture.md) · [한국어](../ko/architecture.md) · [Tiếng Việt](../vi/architecture.md) · [中文（简体）](../zh-Hans/architecture.md) · [中文（繁體）](../zh-Hant/architecture.md) · [Deutsch](../de/architecture.md) · [Русский](../ru/architecture.md)

[← Về trang chủ tiếng Việt](../../../i18n/README.vi.md)

# Kiến trúc

## Hai màn hình, hai chiều dữ liệu

Ứng dụng Windows chính thức của UU chạy trong Wine prefix riêng. Driver nhập liệu kernel Windows không điều khiển GNOME trực tiếp. Cầu nối cung cấp cửa sổ chuyển tiếp trên X11 riêng: hình ảnh đi từ Ubuntu tới bộ điều khiển UU; bàn phím, chuột và văn bản đã xác nhận đi ngược lại. Cửa sổ quản lý cục bộ là nhánh độc lập. Mã nguồn dùng manifest UU 4.42 và bản dựng FreeRDP/SDL cố định.

Cài mới chọn `rdp`, đầu vào `rdp-public`, đích `auto`, 1920 × 1080, theo độ phân giải `off` và văn bản điện thoại `auto`. Nâng cấp giữ cấu hình đã lưu. Khi không có cấu hình route đã cài, launcher dùng `legacy`. Bốn mức chuẩn là 720p, 1080p, 1440p và 4K. VNC phải chọn rõ ràng cho X11/XRDP với `legacy`, không thay thế phiên Wayland.

## Hình ảnh và điều khiển

GNOME Remote Desktop khởi động trên D-Bus của phiên được chọn. FreeRDP nối loopback, mặc định `127.0.0.1:3390`, kiểm tra dấu vân tay TLS và nhận mật khẩu qua stdin. Xvfb dùng Xauthority và `-nolisten tcp`. Với `rdp-public`, XComposite chỉ ghép cửa sổ SDL đã ràng buộc lên root riêng; UU chụp, mã hóa và truyền ảnh đó.

Bản vá đúng phiên bản chọn đường `SendInput` sẵn có. Broker công khai gửi sự kiện tới pipe cục bộ của `uurb-full-input`, rồi hàm FreeRDP đưa vào kết nối RDP hiện hữu. `/dvc:uurb-full-input` nạp plugin, không yêu cầu kênh nhập liệu mới phía máy chủ. `legacy` thử Wine trước cho sự kiện thường rồi gửi phần chưa nhận tới broker. XTEST trực tiếp là tùy chọn cho X11; không phát lại sự kiện đã gửi nhưng kết quả không rõ.

## Văn bản và clipboard

Phím vật lý khác với `KEYEVENTF_UNICODE`. `rdp-public/auto` giữ nguyên mọi commit Unicode, kể cả ASCII. `legacy/auto` chuyển ký tự biểu diễn được thành tổ hợp phím, còn tiếng Trung, tab, xuống dòng dùng dán ngữ nghĩa. Helper sở hữu `CLIPBOARD` và `PRIMARY`, kiểm tra owner mới rồi gửi `Shift+Insert` theo route đã chọn. Hàng rào selection xác nhận giao dịch, nhưng ứng dụng vẫn cần focus và hỗ trợ dán. Copy thông thường dùng `cliprdr`. Helper VNC chỉ gửi văn bản GameViewer sang Ubuntu, không đọc ngược hay nhấn phím dán.

## Quản lý và vòng đời

`uu-remote open` dùng XComposite chụp cửa sổ quản lý và popup liên quan sang TigerVNC cục bộ. Đầu vào quay lại đúng cửa sổ sở hữu. Đóng viewer thu hồi sidecar và trả focus về relay; cửa sổ UU vẫn mapped. Nhánh này không nằm nối tiếp trong luồng desktop.

Chất lượng thay đổi canvas riêng, không đổi màn hình vật lý. Phục hồi được chuẩn bị trước thay đổi; lỗi phục hồi được báo. User service giám sát tiến trình con và chỉ dọn prefix của mình. GNOME xử lý đầu vào Wayland; adapter gọi FreeRDP, không gọi libei trực tiếp. Backport libei cũ là tùy chọn; Ubuntu 26.04 đã có sửa hệ thống. Terminal và khởi động không người trực có route riêng.

[Chất lượng](quality-guide.md) · [Dựng nguồn](source-build.md) · [Bảo mật](security.md)

![UU / GNOME](../../images/architecture-premium-v2-en.png)

![Video / Input](../../images/uu-plus-data-flow-en.gif)

[PNG](../../images/uu-plus-data-paths-en.png) · [SVG](../../images/uu-plus-data-paths-en.svg)

![UU manager](../../images/manager-premium-en.png)

## Lệnh và giá trị kỹ thuật

```text
GNOME -> GNOME Remote Desktop -> loopback RDP -> SDL FreeRDP
  -> private X11 / UU capture -> UU controller
UU controller -> SendInput hook -> broker -> uurb-full-input
  -> FreeRDP input -> GNOME Remote Desktop -> GNOME
GameViewer + popups -> XComposite -> loopback x11vnc -> local TigerVNC
```

## Mã nguồn và tài liệu liên quan

- [install.sh](../../../install.sh#L358)
- [scripts/uu-remote-bridge](../../../scripts/uu-remote-bridge#L6)
- [scripts/runtime-settings.sh](../../../scripts/runtime-settings.sh)
- [scripts/uu-remote-bridge](../../../scripts/uu-remote-bridge#L1010)
- [scripts/uu-remote-bridge](../../../scripts/uu-remote-bridge#L1758)
- [scripts/uu-remote-bridge](../../../scripts/uu-remote-bridge#L1437)
- [scripts/uu-manual-plane.py](../../../scripts/uu-manual-plane.py#L155)
- [scripts/uu-remote-bridge](../../../scripts/uu-remote-bridge#L1040)
- [scripts/uu-remote-bridge](../../../scripts/uu-remote-bridge#L1844)
- [patches/uu-remote-4.42.0.2770.json](../../../patches/uu-remote-4.42.0.2770.json)
- [src/uu_input_bridge.c](../../../src/uu_input_bridge.c#L688)
- [src/uu_input_broker.c](../../../src/uu_input_broker.c#L1081)
- [src/plugin.c](../../../src/plugin.c#L200)
- [src/freerdp-adapter.c](../../../src/freerdp-adapter.c#L48)
- [src/uu_input_bridge_legacy.c](../../../src/uu_input_bridge_legacy.c#L595)
- [src/uu_input_broker.c](../../../src/uu_input_broker.c#L1101)
- [src/uu_input_broker.c](../../../src/uu_input_broker.c#L454)
- [src/uu_input_broker.c](../../../src/uu_input_broker.c#L641)
- [scripts/uu-remote-bridge](../../../scripts/uu-remote-bridge#L1182)
- [src/uu_x11_input.c](../../../src/uu_x11_input.c#L1000)
- [scripts/uu-remote-bridge](../../../scripts/uu-remote-bridge#L1266)
- [src/uu_wine_clipboard_bridge.c](../../../src/uu_wine_clipboard_bridge.c#L195)
- [src/uu_x11_clipboard.c](../../../src/uu_x11_clipboard.c#L329)
- [scripts/uu-remote-console](../../../scripts/uu-remote-console#L1121)
- [src/uu_manager_capture.c](../../../src/uu_manager_capture.c#L464)
- [src/uu_manager_capture.c](../../../src/uu_manager_capture.c#L1090)
- [scripts/uu-remote-console](../../../scripts/uu-remote-console#L1193)
- [scripts/uu-remote-console](../../../scripts/uu-remote-console#L622)
- [scripts/uu-remote-console](../../../scripts/uu-remote-console#L299)
- [scripts/uu-quality.py](../../../scripts/uu-quality.py#L329)
- [scripts/uu-display-modes.py](../../../scripts/uu-display-modes.py#L166)
- [scripts/uu-remote-bridge](../../../scripts/uu-remote-bridge#L199)
- [scripts/uu-remote-bridge](../../../scripts/uu-remote-bridge#L1121)
- [scripts/uu-remote-bridge](../../../scripts/uu-remote-bridge#L2207)
- [scripts/uu-remote-bridge](../../../scripts/uu-remote-bridge#L478)
- [systemd/uu-remote-bridge.service](../../../systemd/uu-remote-bridge.service)

Tài liệu kỹ thuật chuyên sâu có bằng tiếng Anh và tiếng Trung giản thể:

- [native-ubuntu-terminal](../../native-ubuntu-terminal.md) · [简体中文](../zh-Hans/native-ubuntu-terminal.md)
- [unattended-startup](../../unattended-startup.md) · [简体中文](../zh-Hans/unattended-startup.md)
- [semantic-text-and-clipboard](../../semantic-text-and-clipboard.md) · [简体中文](../zh-Hans/semantic-text-and-clipboard.md)
