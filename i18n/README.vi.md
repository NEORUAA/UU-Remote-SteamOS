<div align="center">

[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)

<a href="README.vi.md"><img src="../docs/images/uu-plus-logo.png" alt="UU Remote Ubuntu Plus" width="140"></a>

# UU Remote Ubuntu Plus

**Kết nối khi ý tưởng đến, giữ môi trường phát triển trên Ubuntu.**

Giữ trình soạn thảo, terminal và các phiên ứng dụng trên Ubuntu. Kết nối từ điện thoại, Mac hoặc Windows để Vibe Coding theo cách của bạn, đổi màn hình rồi viết tiếp.

[![Ubuntu 24.04 / 26.04](https://img.shields.io/badge/Ubuntu-24.04%20%7C%2026.04-E95420?logo=ubuntu&logoColor=white)](../docs/i18n/vi/ubuntu-26.04-port.md)
[![GNOME 46 / 50](https://img.shields.io/badge/GNOME-46%20%7C%2050-4A86CF?logo=gnome&logoColor=white)](../docs/i18n/vi/architecture.md)
[![UU Remote 4.42](https://img.shields.io/badge/UU_Remote-4.42.0.2770-00A870)](../patches/uu-remote-4.42.0.2770.json)
[![MIT](https://img.shields.io/badge/License-MIT-2F81F7)](../LICENSE)

<img src="../docs/images/vibe-coding-cross-device-en.png" alt="UU Remote Ubuntu Plus" width="1120">

</div>

Plus kết nối NetEase UU Remote với phiên Ubuntu GNOME đã đăng nhập.
Ứng dụng UU chính thức dành cho Windows chạy trong môi trường Wine riêng.
Bộ chuyển tiếp cục bộ hiển thị màn hình thật; cửa sổ quản lý riêng dùng cho
tài khoản và thiết lập UU. Ứng dụng, tệp và phiên làm việc được giữ nguyên
khi bạn chuyển giữa sử dụng tại máy và từ xa.

Dự án dựa trên **[UU Remote Ubuntu Bridge của Lachlan Chen](https://github.com/lachlanchen/uu-remote-ubuntu-bridge)**.
Plus mở rộng tương thích Ubuntu và UU, cung cấp bốn kích thước khung hình,
sửa nhập liệu và bảng nhớ tạm, đồng thời cải thiện quản lý và thao tác desktop.

Bộ cài hướng tới x86-64 Ubuntu 24.04 / GNOME 46 và Ubuntu 26.04 / GNOME 50 với UU 4.42.0.2770. Cài mới chọn 1080p và tắt bảo vệ con trỏ tùy chọn.

Các trang và hướng dẫn kỹ thuật ở 11 ngôn ngữ giới thiệu Plus bằng cùng ngôn ngữ; tiếng Anh là bản tham chiếu gốc.

## Tính năng mới trong 0.2.0-work

- **Tiếp tục terminal:** chế độ tùy chọn `persistent` giữ shell, thư mục và tác vụ khi kết nối lại; mặc định vẫn là `fresh`.

- **Nhận nhiều tệp:** sao chép tệp thường trên bộ điều khiển, dán cả lô sau khi nhận xong vào Ubuntu; tiến độ theo byte thực nhận.

- **Tương thích ảnh:** giữ PNG gốc cùng DIBV5/DIB; trợ giúp Mac tùy chọn bổ sung TIFF cho PNG.

- **Khám phá chụp gốc:** nguyên mẫu CPU/GPU tùy chọn còn thử nghiệm, không nằm trong cài đặt mặc định.

[CPU (MIT)](../vendor/uur-native-cpu/NOTICE) · [GPU (AGPL-3.0)](../vendor/uuway-gpu-component/README.md)

<img src="../docs/images/uu-plus-update-20261006-en.png" alt="Tính năng mới trong 0.2.0-work" width="1120">

Chỉ nhận tệp thường. Đồng bộ ảnh Ubuntu → Mac hiện tại và tiêu điểm giữa hai bộ điều khiển còn chưa giải quyết.

[Cách dùng và cập nhật bằng tiếng Anh](../docs/updates/2026-10-06.md) · [SVG](../docs/images/uu-plus-update-20261006-en.svg)

## Từ cài đặt đến làm việc từ xa

1. Cài bridge trên desktop Ubuntu.
2. Chạy `uu-remote open` và đăng nhập UU trong cửa sổ quản lý.
3. Kết nối đến Ubuntu bằng UU trên điện thoại, Mac hoặc Windows.
4. Chọn kích thước khung hình và dùng các ứng dụng thường ngày.

## Chức năng và cải tiến

Upstream cung cấp chuyển tiếp desktop, bàn phím và chuột, xử lý IME điện thoại và phục hồi dịch vụ. Plus phát triển nền tảng này với tương thích mới hơn, thiết lập chất lượng rõ hơn và cải tiến cho sử dụng thường ngày.

| Sử dụng thường ngày | Plus cải tiến |
| --- | --- |
| Ubuntu và UU mới hơn | Ubuntu 26.04 / GNOME 50 và UU 4.42, đồng thời giữ cách cài Ubuntu 24.04. |
| Chọn khung hình phù hợp | Đổi giữa 720p, 1080p, 1440p, 4K bằng giao diện đồ họa. Co toàn bộ desktop vào khung và khôi phục thiết lập đã lưu. |
| Tiếng Trung, mã và sao chép/dán | Sửa gửi văn bản từ điện thoại và làm mới bảng nhớ tạm. Văn bản mới đến desktop; đoạn mã và văn bản nhiều dòng giữ nội dung. |
| Mở thiết lập, giữ kết nối | Chụp riêng quản lý UU và menu. Mất tiêu điểm khi đổi hai bộ điều khiển vẫn chưa được giải quyết. |
| Công cụ cục bộ thuận tiện | Mở chất lượng, VNC, FreeRDP, Openbox với cải tiến phông chữ, DPI và khởi chạy. |
| Cài đặt và bảo trì | Biên dịch chuyển tiếp từ nguồn cố định và kiểm tra thành phần trước khi cài. Phục hồi thay đổi khung thất bại và xem trước khi gỡ. |

Xem [so sánh upstream](../docs/i18n/vi/upstream-comparison.md) để biết thay đổi và bối cảnh phiên bản.

<img src="../docs/images/experience-refinements-en.png" alt="Trải nghiệm và đo lường" width="1120">

[Trải nghiệm và đo lường](../docs/i18n/vi/performance-evidence.md)

## Cài đặt nhanh

Trên máy Ubuntu x86-64 đã đăng nhập GNOME, hãy lấy mã nguồn dự án:

```bash
git clone https://github.com/llmir/uu-remote-ubuntu-plus.git
cd uu-remote-ubuntu-plus
```

Cài đặt cần bộ công cụ đã được rà soát để biên dịch relay hoặc kết quả đã xác minh khớp hồ sơ sản phẩm; gói không kèm tệp nhị phân relay. Ubuntu 26.04 có quy trình chuẩn bị công cụ tham chiếu; Ubuntu 24.04 dùng lại đầu ra đã xác minh. [Chuẩn bị công cụ và tái sử dụng relay](../docs/i18n/vi/source-build.md#reference-toolchain)

Khi công cụ hoặc đầu ra phù hợp đã sẵn sàng, chạy bộ cài thông thường:

```bash
./install.sh
./scripts/verify.sh --quick
uu-remote open
```

Bộ cài chuẩn bị phụ thuộc, biên dịch thành phần, cấu hình GNOME Remote Desktop
và chạy dịch vụ người dùng. Mật khẩu chuyển tiếp được lưu vào GNOME Keyring;
UU mở để đăng nhập tài khoản. Cài lại giữ thiết lập và trạng thái tài khoản.
Để bắt đầu với 4K:

```bash
./install.sh --resolution 3840x2160
```

Gửi môi trường và các bước tái hiện qua [biểu mẫu tương thích](https://github.com/llmir/uu-remote-ubuntu-plus/issues/new?template=compatibility.yml).

Lần đầu có thể tải và biên dịch các phụ thuộc. Xem
[Biên dịch mã nguồn](../docs/i18n/vi/source-build.md) và [Bảo mật](../docs/i18n/vi/security.md).
Lấy UU Windows từ trang NetEase chính thức [uuyc.163.com](https://uuyc.163.com/). Bridge chạy trong môi trường Wine riêng. UU giữ giấy phép gốc.

## Tổng quan kỹ thuật

<img src="../docs/images/architecture-premium-v2-en.png" alt="Luồng hình ảnh, nhập liệu và quản lý UU cục bộ trên Ubuntu." width="1120">

Desktop Ubuntu đi qua GNOME RDP vào chuyển tiếp SDL / FreeRDP, rồi qua UU đến thiết bị điều khiển. Bàn phím và chuột đi qua cầu nhập liệu về cùng phiên. Tài khoản và thiết lập UU có cửa sổ quản lý cục bộ riêng.

Chạy `uu-remote open` để mở quản lý; bridge tiếp tục chạy khi đóng trình xem. `uu-remote console` tùy chọn cung cấp màn hình trình duyệt cục bộ. Xem [Kiến trúc](../docs/i18n/vi/architecture.md) cho mô-đun và đường nhập liệu.

## Độ phân giải và chất lượng

<img src="../docs/images/quality-controls-cartoon-v2-en.png" alt="Ubuntu canvas and UU controller quality controls" width="1120">

Mở **UU Remote 画质与分辨率** trong GNOME hoặc chạy:

```bash
uu-remote quality gui
```

Toàn bộ desktop nguồn được co vừa khung, còn độ phân giải màn hình vật lý giữ nguyên.
Đổi mức sẽ kết nối lại trong chốc lát; nếu thất bại thì khôi phục cấu hình cũ.

```bash
uu-remote quality list
uu-remote quality apply 2160p
uu-remote quality status
uu-remote quality guide
```

Chất lượng mã hóa, FPS và True Color đặt ở **thiết bị điều khiển UU**:
**Trung tâm điều khiển → Chất lượng** trên máy tính,
**Thao tác → Hiển thị** trên điện thoại.

Giới hạn bitrate được đặt riêng:

```bash
uu-remote quality bitrate 20
uu-remote quality bitrate 0
```

`20` yêu cầu trần 20 Mbps; `0` bỏ trần.
Kích thước khung, chất lượng, FPS yêu cầu và bitrate là các thiết lập riêng.
Xem [hướng dẫn chất lượng](../docs/i18n/vi/quality-guide.md).

## Nhập liệu và con trỏ

Văn bản từ IME điện thoại, đoạn mã và nội dung nhiều dòng đi theo đường văn bản vào Ubuntu. Phím vật lý và phím tắt giữ sự kiện phím. Plus sửa gửi văn bản và làm mới bảng nhớ tạm cho nhập và sao chép/dán hằng ngày. Các chế độ được mô tả ở [chuyển tiếp bàn phím](../docs/i18n/vi/adaptive-keyboard-relays.md).

Bảo vệ con trỏ tùy chọn có từ upstream; Plus cải thiện tài nguyên và xử lý con trỏ.
Để bật:

```bash
./install.sh --skip-packages --skip-account-login \
  --cursor-guard on --cursor-size auto
```

`auto` theo kích thước con trỏ desktop; giá trị như `24` đặt kích thước con trỏ dự phòng.
`--cursor-guard off` tắt chức năng này. Cài lại làm UU kết nối lại ngắn.

## Sử dụng và bảo trì

```bash
uu-remote status
uu-remote network
uu-remote logs
uu-remote restart
uu-remote stop
```

Dùng `uu-remote open` cho quản lý và `uu-remote login` để đăng nhập hoặc phục hồi tài khoản.
Khởi động lại, đăng nhập và cài lại ngắt kết nối từ xa trong chốc lát.

Lưu thay đổi cục bộ, cập nhật mã nguồn rồi cài lại:

```bash
./install.sh --skip-packages --skip-account-login
./scripts/verify.sh --quick
```

Mã chạy thay đổi có hiệu lực sau cài lại. Xem
[Nâng cấp](../docs/i18n/vi/reusable-upgrade.md) cho `uu-remote upgrade` và
[Cập nhật tự động](../docs/i18n/vi/automatic-updates.md) cho bảo trì tùy chọn.

Gỡ bridge nhưng giữ trạng thái tài khoản UU:

```bash
./uninstall.sh --dry-run
./uninstall.sh
```

`./uninstall.sh --purge` còn xóa Wine prefix riêng, thông tin xác thực chuyển tiếp
và cấu hình bật GNOME RDP.

## Ngoài Ubuntu và chuyển sang Linux khác

Bộ cài hiện tại dành cho Ubuntu 24.04 và 26.04 x86-64. [Hướng dẫn chuyển sang Linux khác](../docs/i18n/vi/porting.md) chia các bản chuyển tương lai thành ba lớp:

- Tái sử dụng lõi tương thích UU, chuyển tiếp và nhập liệu.
- Điều chỉnh gói của bản phân phối, đường dẫn Wine và dịch vụ.
- Kết nối backend riêng của desktop cho chụp hình, nhập liệu, chế độ màn hình và thao tác.

Các bản GNOME khác có thể tái sử dụng nhiều tích hợp hiện có hơn. KDE và Xfce cần backend desktop riêng.

## Tài liệu và đóng góp

- [Chất lượng](../docs/i18n/vi/quality-guide.md), [Biên dịch](../docs/i18n/vi/source-build.md), [Ubuntu 26.04](../docs/i18n/vi/ubuntu-26.04-port.md)
- [Kiến trúc](../docs/i18n/vi/architecture.md), [Bảo mật](../docs/i18n/vi/security.md), [Khắc phục lỗi](../docs/i18n/vi/troubleshooting.md)
- [So sánh](../docs/i18n/vi/upstream-comparison.md), [Đo hiệu năng](../docs/i18n/vi/performance-evidence.md)
- [Thay đổi](CHANGELOG.vi.md), [Đóng góp](CONTRIBUTING.vi.md)

Ghi phiên bản, thiết lập và các bước tái hiện hành vi.

## Hỗ trợ dự án

**Mời mình một ly cà phê ☕**

UU và Ubuntu liên tục cập nhật, mình cũng sẽ tiếp tục điều chỉnh Plus cho các phiên bản mới và cải thiện nhập văn bản, sao chép/dán cùng chất lượng hình ảnh. Một ly cà phê giúp chia sẻ chi phí thử phiên bản, công cụ phát triển và token.

| PayPal | Alipay · CNY | AlipayHK · HKD | WeChat · CNY | WeChat · HKD |
| :---: | :---: | :---: | :---: | :---: |
| <a href="https://paypal.me/mirmirlin"><img src="../docs/images/support-paypal-en.png" alt="PayPal" width="160"></a> | <a href="../docs/images/support/alipay-cny.jpg"><img src="../docs/images/support-alipay-cny-en.png" alt="Alipay · CNY" width="160"></a> | <a href="../docs/images/support/alipay-hkd.png"><img src="../docs/images/support-alipay-hkd-en.png" alt="AlipayHK · HKD" width="160"></a> | <a href="../docs/images/support/wechat-zh.png"><img src="../docs/images/support-wechat-zh-en.png" alt="WeChat · CNY" width="160"></a> | <a href="../docs/images/support/wechat-en.png"><img src="../docs/images/support-wechat-en-en.png" alt="WeChat · HKD" width="160"></a> |

<details>
<summary>Mã thanh toán Alipay và WeChat</summary>

<p><a href="../docs/i18n/vi/support.md#alipay-cny">Alipay CNY</a><br><a href="../docs/images/support/alipay-cny.jpg"><img src="../docs/images/support/alipay-cny.jpg" alt="Alipay CNY" width="240"></a></p>

<p><a href="../docs/i18n/vi/support.md#alipay-hkd">AlipayHK HKD</a><br><a href="../docs/images/support/alipay-hkd.png"><img src="../docs/images/support/alipay-hkd.png" alt="AlipayHK HKD" width="240"></a></p>

<p><a href="../docs/i18n/vi/support.md#wechat-zh">WeChat · CNY</a><br><a href="../docs/images/support/wechat-zh.png"><img src="../docs/images/support/wechat-zh.png" alt="WeChat · CNY" width="240"></a></p>

<p><a href="../docs/i18n/vi/support.md#wechat-en">WeChat · HKD</a><br><a href="../docs/images/support/wechat-en.png"><img src="../docs/images/support/wechat-en.png" alt="WeChat · HKD" width="240"></a></p>

</details>

Báo lỗi kèm bước tái hiện, kinh nghiệm chuyển sang Linux và pull request đều được chào đón. Cảm ơn bạn đã góp phần làm phiên bản tiếp theo thuận tiện hơn.

[Ủng hộ UU Remote Ubuntu Plus](../docs/i18n/vi/support.md)

## Ghi nhận và giấy phép

Dựa trên **[UU Remote Ubuntu Bridge của Lachlan Chen](https://github.com/lachlanchen/uu-remote-ubuntu-bridge)**.
Giữ thông báo bản quyền gốc và [giấy phép MIT](../LICENSE).
UU và phụ thuộc giữ giấy phép và nhãn hiệu riêng.
Đây là dự án cộng đồng độc lập.

Biểu tượng thương hiệu thanh toán: [Simple Icons](https://simpleicons.org/) (CC0); quyền nhãn hiệu thuộc về chủ sở hữu tương ứng.
