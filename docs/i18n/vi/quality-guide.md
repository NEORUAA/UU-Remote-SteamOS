[English](../../quality-guide.md) · [العربية](../ar/quality-guide.md) · [Deutsch](../de/quality-guide.md) · [Español](../es/quality-guide.md) · [Français](../fr/quality-guide.md) · [日本語](../ja/quality-guide.md) · [한국어](../ko/quality-guide.md) · [Русский](../ru/quality-guide.md) · [Tiếng Việt](../vi/quality-guide.md) · [简体中文](../zh-Hans/quality-guide.md) · [繁體中文](../zh-Hant/quality-guide.md)

[Trang chủ](../../../i18n/README.vi.md)

# Chất lượng, độ phân giải và tốc độ khung hình

Chọn khung hình trên Ubuntu, rồi chỉnh chất lượng truyền trên máy tính hoặc điện thoại điều khiển. Kích thước, mức nén, FPS yêu cầu và giới hạn bitrate là các thiết lập riêng.

## Chọn khung hình

Mở **UU Remote 画质与分辨率** trong GNOME hoặc chạy:

```bash
uu-remote quality gui
uu-remote quality list
uu-remote quality status
uu-remote quality apply 2160p
uu-remote quality guide
```

![Bộ chọn bốn độ phân giải](../../images/quality-presets.png)

| Mức | Khung hình | Dùng khi |
| --- | --- | --- |
| `720p` | 1280 × 720 | Màn hình nhỏ hoặc đường truyền hạn chế |
| `1080p` | 1920 × 1080 | Hằng ngày; mặc định khi cài mới |
| `1440p` | 2560 × 1440 | Không gian rộng hơn, ít điểm ảnh hơn 4K |
| `2160p` | 3840 × 2160 | Chữ nhỏ và không gian 4K đầy đủ |

Cài lại giữ lựa chọn đã lưu. Co giãn thông minh đưa toàn bộ màn hình nguồn vào khung và ánh xạ chuột theo cùng hình học. Độ phân giải/tỉ lệ nguồn ảnh hưởng kết quả. Khung không đổi màn hình vật lý GNOME; việc chụp có thể vẫn xử lý toàn bộ nguồn.

Bộ chọn phân biệt kích thước khởi động/RDP đã lưu và khung hiện tại. Đổi kích thước lưu sẽ ngắt rồi nối lại ngắn. Áp dụng lại mức đã lưu khôi phục khung đang chạy trên đường RDP hỗ trợ mà không khởi động lại relay, rồi xác nhận kích thước. Bộ hẹn giờ khôi phục được bật trước thay đổi; nếu cầu nối không sẵn sàng sẽ trả cấu hình cũ. Chờ khôi phục xong trước lần đổi tiếp theo.

Mức cố định dùng mặc định `--follow-desktop-resolution off`. Nếu đã bật theo độ phân giải nguồn, hãy tắt trước. Xem [cài đặt](../../../i18n/README.vi.md), `./install.sh --help`. Phóng nguồn 4K đã thử lên 5K không thêm chi tiết và xấu hơn trên Mac, nên lựa chọn thông thường tối đa 4K. 60 Hz danh nghĩa là chế độ màn hình ảo; FPS thực phụ thuộc cả kết nối.

## Chất lượng trên thiết bị điều khiển

Máy tính: **控制中心 → 画质**. Điện thoại: **操作 → 显示**. Chọn True Color ở thiết bị điều khiển khi được hỗ trợ.

![Menu chất lượng UU](../../images/uu-native-quality-menu.png)

Ví dụ từ Ubuntu điều khiển Mac. Thiết bị/codec quyết định lựa chọn. Chất lượng chỉnh nén/chi tiết; FPS là tần số yêu cầu. True Color có thể cải thiện chữ màu/đường biên. Nếu UU báo giới hạn hiệu năng, chọn mức khả dụng. So sánh cùng chữ và chuyển động.

Tài liệu NetEase: [FPS / Super Screen](https://uuyc.163.com/help/superscreen.html) · [True Color](https://uuyc.163.com/features/color/) · [UU](https://uuyc.163.com/help/20241216/40221_1200122.html). Super Screen/trình điều khiển màn hình ảo trong Wine và 144 FPS chưa thử. Xem [đo lường](performance-evidence.md).

## Giới hạn bitrate

```bash
uu-remote quality bitrate 20
uu-remote quality bitrate 0
```

`20` yêu cầu trần **20 Mbps**, `0` bỏ trần. Không đặt bitrate mục tiêu, FPS hay kích thước. Đổi độ phân giải giữ thiết lập này. Trần thấp có thể làm mất chi tiết khi chuyển động.

## Con trỏ và thao tác màn hình

Bảo vệ con trỏ tùy chọn mặc định tắt khi cài mới. Nếu chuột quá lớn:

```bash
./install.sh --skip-packages --skip-account-login --cursor-guard on --cursor-size 24
```

`--cursor-size auto` theo kích thước trên desktop; số cố định 24–128 điểm ảnh. GNOME/ứng dụng vẫn có thiết lập riêng. Dock dùng GNOME. Thao tác hiện desktop/tất cả cửa sổ Android được nối tới desktop/tổng quan GNOME; nút trên thiết bị thật còn chờ thử.

## Quản lý và phục hồi

`uu-remote open` mở trình xem quản lý riêng. Phóng lớn:

```bash
UURB_WINDOW_SCALE=2 ./install.sh --skip-packages --skip-account-login
```

Hệ số `1` mặc định, `1.5`, `2`, `3`; chỉ đổi trình xem, không đổi DPI Wine/độ phân giải. Clipboard quản lý bị tách; sao chép desktop dùng relay.

```bash
uu-remote status
uu-remote quality status
uu-remote network
uu-remote logs
```

Dịch vụ người dùng khởi động lại thành phần lỗi, có thể nối lại ngắn. Hoàn tác mức khôi phục thiết lập; triển khai runtime có quy trình riêng. [Khắc phục](troubleshooting.md), [biên dịch](source-build.md). Điều khiển máy khác từ Wine có giới hạn riêng. Màn hình vật lý/bộ xuất ảo còn chờ thử: [Ubuntu 26.04](ubuntu-26.04-port.md). Điện thoại → ToDesk → Mac → UU còn lặp chữ; kết nối trực tiếp bình thường.
