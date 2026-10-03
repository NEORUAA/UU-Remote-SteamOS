[English](../../ubuntu-26.04-port.md) · [العربية](../ar/ubuntu-26.04-port.md) · [Deutsch](../de/ubuntu-26.04-port.md) · [Español](../es/ubuntu-26.04-port.md) · [Français](../fr/ubuntu-26.04-port.md) · [日本語](../ja/ubuntu-26.04-port.md) · [한국어](../ko/ubuntu-26.04-port.md) · [Русский](../ru/ubuntu-26.04-port.md) · [Tiếng Việt](../vi/ubuntu-26.04-port.md) · [简体中文](../zh-Hans/ubuntu-26.04-port.md) · [繁體中文](../zh-Hant/ubuntu-26.04-port.md)

[Trang chủ](../../../i18n/README.vi.md)

# Ubuntu 26.04 và GNOME 50

Plus mở rộng [cầu nối MIT của Lachlan Chen](https://github.com/lachlanchen/uu-remote-ubuntu-bridge) tới x86-64 Ubuntu 26.04/GNOME 50, giữ24.04/GNOME 46. Wine riêng, manifest duyệt, broker, relay và dịch vụ là nền tảng.

Cài relay cần đúng bộ công cụ đã duyệt hoặc đầu ra đã kiểm tra có sẵn; các gói APT thông thường không tự cung cấp bộ công cụ này. Xem [điều kiện biên dịch và dùng lại bộ đệm](source-build.md).

| Thành phần | Bản gốc | Plus |
| --- | --- | --- |
| Ubuntu |24.04|24.04/26.04; bản khác cần `UURB_ALLOW_UNVALIDATED_UBUNTU=1`|
| Windows UU |4.33.0.8907|Duyệt4.42.0.2770; còn chọn manifest cũ|
| libei |Backport1.2.1 riêng|Thư viện hệ thống đã sửa, nếu không dùng backport|
| Relay |Nightly SDL/WinPR cố định|Nguồn cố định và bản vá; [biên dịch](source-build.md)|
| CI |24.04|24.04/26.04; xem kết quả mỗi lượt|

Máy quan sát dùng GRD 50.2/libei 1.5.0. Thư viện cũ có backport `ee27dd5c92e4e9496a36ca2d4112049fe02d2269`. `UURB_LIBEI_MODE=system|backport` lưu lựa chọn; `verify.sh` kiểm tra thư viện được nạp. Dùng WineHQ stable.

## Desktop

Bốn mức, toàn màn hình/ánh xạ chuột. Cài mới1080p, nâng cấp giữ thiết lập. Đổi kích thước lưu nối lại có hoàn tác; áp dụng lại khôi phục khung. Người dùng xác nhận nối lại và menu tối đa 4K. RDP mới `rdp-public`, nâng cấp giữ đường. Unicode/phím vật lý riêng. Cửa sổ quản lý/popup chụp riêng; đóng trình xem trả focus cho relay, cửa sổ vẫn được ánh xạ. Clipboard desktop hoạt động, quản lý tách biệt.

| Tính năng | Kết quả |
| --- | --- |
| Tiếng Trung trực tiếp điện thoại/Mac |Người dùng xác nhận khi tích hợp|
| Sao chép văn bản |Người dùng xác nhận bình thường|
| Mac UU nâng cấp |Nối lại/chữ/dán bình thường,4K tương tự|
| Chồng cửa sổ/focus |Đã giải quyết theo phản hồi, kiểm tra chọn lọc bình thường|
| Android |Backend hai chiều, nút thật chờ thử|
| Con trỏ |Theme/một phần bình thường, đủ hình dạng chờ thử|
| Màn hình/bộ xuất ảo |Chờ thử trên máy này|
| Điện thoại→ToDesk→Mac→UU |Lặp`a` chưa giải quyết|

VNC/FreeRDP/Openbox có font CJK/DPI/thông tin đăng nhập riêng. Dock thuộc GNOME. Điều khiển ra ngoài/độ phân giải vật lý tách với khung đầu vào. [Chất lượng](quality-guide.md), [kiến trúc](architecture.md), [so sánh](upstream-comparison.md).

## Cập nhật

Giữ Plus là `origin`:

```bash
git remote add upstream https://github.com/lachlanchen/uu-remote-ubuntu-bridge.git
git fetch upstream
```

Duyệt thay đổi ở nhánh phát triển. Sau thay runtime:

```bash
./install.sh --skip-packages --skip-account-login
./scripts/verify.sh --quick
```

Cài đặt ngắt ngắn; digest báo khác tới khi cài lại. [Nâng cấp tái sử dụng](reusable-upgrade.md) xử lý runtime; hoàn tác mức xử lý khung. Hash UU lạ chặn bản vá tự động; phiên bản mới cần duyệt ngữ nghĩa/manifest/kiểm tra: [bảo trì](../../upstream-maintenance.md). Phân phối nguồn MIT/manifest; UU và phụ thuộc giữ giấy phép.
