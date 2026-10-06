[English](../../performance-evidence.md) · [العربية](../ar/performance-evidence.md) · [Deutsch](../de/performance-evidence.md) · [Español](../es/performance-evidence.md) · [Français](../fr/performance-evidence.md) · [日本語](../ja/performance-evidence.md) · [한국어](../ko/performance-evidence.md) · [Русский](../ru/performance-evidence.md) · [Tiếng Việt](../vi/performance-evidence.md) · [简体中文](../zh-Hans/performance-evidence.md) · [繁體中文](../zh-Hant/performance-evidence.md)

[Trang chủ](../../../i18n/README.vi.md)

# Trải nghiệm và hiệu năng

![Cải thiện nhập tiếng Trung, bộ nhớ tạm và cửa sổ quản lý](../../images/experience-refinements-en.png)

[SVG có thể chỉnh sửa](../../images/experience-refinements-en.svg)

![Diện tích điểm ảnh và lựa chọn bốn khung hình](../../images/canvas-pixel-scale-en.png)

[SVG có thể chỉnh sửa](../../images/canvas-pixel-scale-en.svg)

Chọn720p/1080p/1440p/4K theo màn hình/kết nối; chất lượng, FPS yêu cầu, bitrate riêng.

**0.2.0-work · 2026-10-06:** Chỉ nhận tệp thường. Đồng bộ ảnh Ubuntu → Mac hiện tại và tiêu điểm giữa hai bộ điều khiển còn chưa giải quyết. [Cách dùng và cập nhật bằng tiếng Anh](../../updates/2026-10-06.md)

## Cải thiện hằng ngày

Các cải tiến gần đây tập trung vào nhập tiếng Trung, dán văn bản và thao tác cửa sổ.

| Tình huống | Bối cảnh | Trải nghiệm trước | Trải nghiệm sau cải tiến |
| --- | --- | --- | --- |
| Tiếng Trung trên điện thoại | Nhập điện thoại trong Plus trước đây | Một phần văn bản gửi đi chưa đến desktop đúng cách | Tiếng Trung gửi qua kết nối điện thoại trực tiếp được nhập đúng vào desktop Ubuntu |
| Sao chép và dán | Trung chuyển văn bản Plus trước đây | Sau khi sao chép mới, nội dung dán vẫn có thể là văn bản cũ | Văn bản mới sao chép được cập nhật để dán trên desktop; sao chép và dán văn bản từ máy tính hoạt động |
| Cài đặt và cửa sổ UU | Khung quản lý Plus trước đây | Cửa sổ quản lý có thể che desktop hoặc để điểm nhập ở sai chỗ | Chụp riêng quản lý UU và menu. Mất tiêu điểm khi đổi hai bộ điều khiển vẫn chưa được giải quyết. |
| Độ rõ và kích thước | Thử mở rộng khung của Plus | Phóng nguồn 4K đã thử không thêm chi tiết và trông xấu hơn | Bốn mức hiển thị toàn desktop và khôi phục kích thước lưu; nguồn đã thử chỉ cần đến 4K |
| Kết nối lại | Cập nhật ứng dụng Mac UU | Cần kiểm tra thao tác thường dùng sau khi cập nhật Mac UU | Kết nối lại, nhập tiếng Trung trực tiếp và dán vẫn hoạt động; cảm giác 4K tương tự |

[Trang so sánh](upstream-comparison.md) phân biệt nền tảng kế thừa, tương thích phiên bản mới, tính năng bổ sung và các sửa đổi trong quá trình dùng Plus.

![Nền tảng upstream, thay đổi của Plus và kỳ vọng thiết kế](../../images/uu-plus-evolution-en.png)

[SVG có thể chỉnh sửa](../../images/uu-plus-evolution-en.svg)

**Kỳ vọng thiết kế:** cập nhật văn bản kịp thời và trả điểm nhập ổn định giúp giảm việc dán lại và gián đoạn khi chuyển giữa cài đặt với desktop. Khung nhỏ cung cấp ít điểm ảnh hơn mỗi hình; phản hồi nhìn thấy còn phụ thuộc vào chụp, mã hóa, mạng và màn hình điều khiển.

| Khung | Điểm ảnh mỗi khung | So với1080p |
| --- | ---: | ---: |
| 1280 × 720 | 921,600 | 0.44× |
| 1920 × 1080 | 2,073,600 | 1.00× |
| 2560 × 1440 | 3,686,400 | 1.78× |
| 3840 × 2160 | 8,294,400 | 4.00× |

Đây là tỉ lệ diện tích. Chụp có thể toàn nguồn; nén/chuyển động/mạng ảnh hưởng tải. Co giãn không đổi độ phân giải vật lý.

| Thiết lập | Vai trò |
| --- | --- |
| KhungUbuntu |Kích thước relay, bắt đầu1080p,4K cho chữ/không gian|
| Chất lượng/FPS/True Color |Nén/yêu cầu cập nhật/màu hỗ trợ|
| `uu-remote quality bitrate 20` |Trần 20 Mbps,`0`bỏ,thấp làm giảm chi tiết chuyển động|

[Chất lượng](quality-guide.md) có menu/lệnh/phục hồi.

## Chi phí biên dịch

Nguồn sạch đầy đủ, chuẩn bị và kiểm tra:

| Mục | Kết quả |
| --- | --- |
| Thời gian |699.851 giây, khoảng11 phút 40 giây|
| Giới hạn |CPU tương đương2 nhân, RAM4 GiB|
| Đỉnh báo cáo |~1.8 GB, số làm tròn dịch vụ|
| Swap |0 byte|
| Đầu ra |13 nhị phân Windows|
| Tái lập |Đầu vào cố định,byte giống nhau ở thư mục khác|

Đầu vào thường chuẩn hóa đường/cấu hình rõ. Máy khác chịu ảnh hưởng tải về/compiler; đầu ra đã kiểm tra dùng lại được. [Biên dịch](source-build.md).

| Môi trường | Ubuntu | GNOME | Windows UU |
| --- | --- | --- | --- |
| Gốc |24.04|46|4.33.0.8907|
| Plus cục bộ |26.04|50|4.42.0.2770|

## Đo cùng điều kiện

Các bản ghi hiện có chưa có phép đo cùng điều kiện về FPS phía điều khiển hoặc độ trễ từ thao tác nhập đến phản hồi trên màn hình giữa upstream cố định và Plus. Đo thời gian trung chuyển và thử hạn mức CPU là đo từng thành phần.


Giữ host/controller/độ phân giải/app/mạng/quality/FPS/bitrate. Môi trường riêng, phiên bản cố định, xét càiUbuntu 24.04 gốc. Đo từ thao tác tới đáp ứng trên controller, đếm cập nhật nhìn thấy khi chuyển động lặp. Lặp lại, báo độ phân tán/độ rõ chữ/phương pháp.
