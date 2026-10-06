[English](../CHANGELOG.md) · [العربية](CHANGELOG.ar.md) · [Deutsch](CHANGELOG.de.md) · [Español](CHANGELOG.es.md) · [Français](CHANGELOG.fr.md) · [日本語](CHANGELOG.ja.md) · [한국어](CHANGELOG.ko.md) · [Русский](CHANGELOG.ru.md) · [Tiếng Việt](CHANGELOG.vi.md) · [简体中文](CHANGELOG.zh-Hans.md) · [繁體中文](CHANGELOG.zh-Hant.md)

[Trang chủ](README.vi.md)

# Nhật ký thay đổi

Thẻ phát hành của cầu nối và phiên bản Windows UU được phê duyệt được quản lý riêng.

## Plus 0.2.0-work — 2026-10-06

- **Tiếp tục terminal:** chế độ tùy chọn `persistent` giữ shell, thư mục và tác vụ khi kết nối lại; mặc định vẫn là `fresh`.

- **Nhận nhiều tệp:** sao chép tệp thường trên bộ điều khiển, dán cả lô sau khi nhận xong vào Ubuntu; tiến độ theo byte thực nhận.

- **Tương thích ảnh:** giữ PNG gốc cùng DIBV5/DIB; trợ giúp Mac tùy chọn bổ sung TIFF cho PNG.

- **Khám phá chụp gốc:** nguyên mẫu CPU/GPU tùy chọn còn thử nghiệm, không nằm trong cài đặt mặc định.

Chỉ nhận tệp thường. Đồng bộ ảnh Ubuntu → Mac hiện tại và tiêu điểm giữa hai bộ điều khiển còn chưa giải quyết.

[CPU (MIT)](../vendor/uur-native-cpu/NOTICE) · [GPU (AGPL-3.0)](../vendor/uuway-gpu-component/README.md) · [Cách dùng và cập nhật bằng tiếng Anh](../docs/updates/2026-10-06.md)

## Plus 0.1.0 — 2026-10-03

Plus dựa trên bộ cầu nối gốc với giấy phép MIT.

### Bổ sung

- Khung hình: Bốn mức tới 4K, khớp toàn desktop và khôi phục kích thước.
- Nhập từ điện thoại: Cải tiến đường nhập Plus và đường văn bản FreeRDP công khai.
- Quản lý: Chụp riêng cửa sổ/hộp thoại, tái dùng trình xem.
- Con trỏ: Dự phòng theo theme và sửa khởi động, mặc định tắt.
- Thao tác: Ánh xạ desktop/tổng quan GNOME.
- Công cụ: Chất lượng/VNC/FreeRDP/Openbox với font, DPI và đăng nhập riêng.
- Biên dịch và khôi phục: Nguồn vá cố định, kiểm tra thành phần và khôi phục mức/trình xem.
- Trang chủ và hướng dẫn cốt lõi bằng 11 ngôn ngữ, hình kiến trúc, chuyển nền tảng và so sánh có thể chỉnh sửa.

### Sửa lỗi

- Clipboard: Vá nguồn SDL để kiểm tra nền, đổi chủ sở hữu và cache định dạng.
- Mở lại cửa sổ quản lý, tiêu đề UTF-8, chụp hộp thoại liên quan và trả focus khi đóng trình xem.
- Gửi văn bản điện thoại, khởi tạo hook, xử lý nhập một phần và giới hạn thời gian đóng terminal gốc.
- Ánh xạ con trỏ toàn khung, tách kích thước/bitrate, bảo vệ phiên RDP thủ công và launcher có thể khôi phục.

### Tương thích

- Ubuntu 24.04 / GNOME 46 · Ubuntu 26.04 / GNOME 50 · x86-64.
- Windows UU: Mặc định 4.42.0.2770 đã rà soát.

## Kế thừa dự án gốc — chưa phát hành

Kế thừa giao dịch clipboard Unicode, chỉnh sửa lúc gõ và đọc chính tả dài, bố cục phím vật lý, nhập có xác thực, chẩn đoán mạng/runtime, tách Bluetooth Wine và khôi phục phiên không người trực.

## Bản gốc 0.2.0 — 2026-07-18

Chẩn đoán mạng và digest nguồn đã cài, chọn adapter mặc định/cố định không đổi tuyến host. Sửa descriptor GNOME RDP/libei, giới hạn descriptor, chờ Keyring, dùng Python/GI hệ thống. Điều chỉnh nhịp văn bản điện thoại, mặc định phím vật lý không trễ; ưu tiên `SendInput` rồi broker với focus đã xác nhận. Thêm X11/XTEST có xác thực, bộ đếm phân loại, dọn phiên cũ, phục hồi mạng có chống lặp và hướng dẫn XRDP/không người trực.

## Bản gốc 0.1.0 — 2026-07-17

Cầu nối được hỗ trợ đầu tiên gồm Wine/UU, Xvfb, SDL FreeRDP, GNOME relay, broker, tái chèn và dịch vụ giám sát. Có thiết lập lưu, kiểm toán nhị phân, hoàn tác và clipboard RDP; TPM2/GDM tùy chọn. Sửa nhập điện thoại, tìm phiên Wayland/Xorg/XRDP, tương thích sự kiện Wine và dọn prefix cũ.

Phát hành gốc: [v0.1.0](https://github.com/lachlanchen/uu-remote-ubuntu-bridge/releases/tag/v0.1.0) · [v0.2.0](https://github.com/lachlanchen/uu-remote-ubuntu-bridge/releases/tag/v0.2.0). Lịch sử đầy đủ và hồ sơ kiểm tra gốc: [CHANGELOG.md — e2854e2b](https://github.com/lachlanchen/uu-remote-ubuntu-bridge/blob/e2854e2b/CHANGELOG.md).
