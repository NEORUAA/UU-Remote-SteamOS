[English](../../upstream-comparison.md) · [العربية](../ar/upstream-comparison.md) · [Deutsch](../de/upstream-comparison.md) · [Español](../es/upstream-comparison.md) · [Français](../fr/upstream-comparison.md) · [日本語](../ja/upstream-comparison.md) · [한국어](../ko/upstream-comparison.md) · [Русский](../ru/upstream-comparison.md) · [Tiếng Việt](../vi/upstream-comparison.md) · [简体中文](../zh-Hans/upstream-comparison.md) · [繁體中文](../zh-Hant/upstream-comparison.md)

[Trang chủ](../../../i18n/README.vi.md)

# Plus thay đổi gì

![Nền tảng upstream, thay đổi của Plus và kỳ vọng thiết kế](../../images/uu-plus-evolution-en.png)

[SVG có thể chỉnh sửa](../../images/uu-plus-evolution-en.svg)

Dựa trên [dự án Lachlan Chen](https://github.com/lachlanchen/uu-remote-ubuntu-bridge), [`e2854e2b`](https://github.com/lachlanchen/uu-remote-ubuntu-bridge/commit/e2854e2b50c48ead1246bec027c2e13b5693a10a). Wine riêng, GNOME relay, nhập/quản lý/dịch vụ được kế thừa.

## Thay đổi trong sử dụng hằng ngày

| Phần | Nền tảng gốc | Thay đổi của Plus | Cách dùng |
| --- | --- | --- | --- |
| Máy chủ | Ubuntu 24.04 và libei backport tách riêng | Điều chỉnh Ubuntu 26.04/GNOME 50, chọn libei; giữ mục tiêu 24.04 | Đọc hướng dẫn nền tảng và biên dịch cho máy chủ |
| Windows UU | Mặc định 4.33.0.8907 và manifest đã rà soát | Mặc định 4.42.0.2770 đã rà soát | Chọn manifest khớp phiên bản UU |
| Khung hình | Độ phân giải lưu sẵn và đổi kích thước RDP | Bốn mức tới 4K, khớp toàn desktop và khôi phục kích thước | Chọn 720p, 1080p, 1440p hoặc 4K và xem khung hiện tại |
| Nhập từ điện thoại | Chuẩn hóa IME và dán Unicode | Cải tiến đường nhập Plus và đường văn bản FreeRDP công khai | Nhập tiếng Trung, mã và nhiều dòng |
| Clipboard | Clipboard RDP và giao dịch Unicode | Vá nguồn SDL để kiểm tra nền, đổi chủ sở hữu và cache định dạng | Sao chép/dán văn bản hiện tại khi bộ chuyển tiếp ở nền |
| Quản lý | Cửa sổ riêng và trả focus | Chụp riêng cửa sổ/hộp thoại, tái dùng trình xem | Mở tài khoản/cài đặt UU rồi trở lại desktop |
| Con trỏ | Bảo vệ kích thước cố định tùy chọn | Dự phòng theo theme và sửa khởi động, mặc định tắt | Bật bảo vệ con trỏ khi cần |
| Thao tác | Điều khiển desktop bằng chuột/phím | Ánh xạ desktop/tổng quan GNOME | Nối thao tác của điều khiển với backend GNOME |
| Công cụ | Phụ thuộc bộ chuyển tiếp và lệnh UU | Chất lượng/VNC/FreeRDP/Openbox với font, DPI và đăng nhập riêng | Mở công cụ với thiết lập cục bộ của nó |
| Biên dịch và khôi phục | Nightly SDL/WinPR cố định và dịch vụ nối lại | Nguồn vá cố định, kiểm tra thành phần và khôi phục mức/trình xem | Chuẩn bị bộ chuyển tiếp khớp và giữ thiết lập khi bảo trì |

## Phân loại triển khai

- Văn bản điện thoại: cải tiến đường nhập Plus — [uu_input_broker.c](https://github.com/lachlanchen/uu-remote-ubuntu-bridge/blob/e2854e2b50c48ead1246bec027c2e13b5693a10a/src/uu_input_broker.c) · [uu_input_broker.c](../../../src/uu_input_broker.c) · [freerdp-adapter.c](../../../src/freerdp-adapter.c)
- Clipboard: bản vá nguồn SDL — [freerdp-sdl-owner-refresh.patch](../../../vendor/freerdp-sdl-build/freerdp-sdl-owner-refresh.patch)
- Quản lý: chụp riêng và xử lý trình xem — [uu_manager_capture.c](../../../src/uu_manager_capture.c) · [uu-remote-console](../../../scripts/uu-remote-console)
- Công cụ: tích hợp desktop mới — [uu-desktop-tool.py](../../../scripts/uu-desktop-tool.py) · [uu-tools-fonts.conf](../../../desktop/uu-tools-fonts.conf)

## Đường nhập

Cài RDP mới chọn `rdp-public`, đưa thao tác từ broker qua API FreeRDP công khai. Unicode gồm ASCII được dán nguyên văn ở chế độ tự động; phím vật lý đi riêng. Nâng cấp giữ đường đã lưu. `legacy` dùng phím cho ký tự biểu diễn được, dán cho CJK/xuống dòng; chạy chưa cấu hình cũng dùng `legacy`.

Khi so FPS và độ trễ, cố định phiên bản, độ phân giải nguồn, chất lượng/FPS, bitrate, mạng và tải, đồng thời ghi phương pháp đo; xem [hướng dẫn đo](performance-evidence.md).
