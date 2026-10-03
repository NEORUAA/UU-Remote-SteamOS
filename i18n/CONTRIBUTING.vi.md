[English](../CONTRIBUTING.md) · [العربية](CONTRIBUTING.ar.md) · [Deutsch](CONTRIBUTING.de.md) · [Español](CONTRIBUTING.es.md) · [Français](CONTRIBUTING.fr.md) · [日本語](CONTRIBUTING.ja.md) · [한국어](CONTRIBUTING.ko.md) · [Русский](CONTRIBUTING.ru.md) · [Tiếng Việt](CONTRIBUTING.vi.md) · [简体中文](CONTRIBUTING.zh-Hans.md) · [繁體中文](CONTRIBUTING.zh-Hant.md)

[Tiếng Việt · UU Remote Ubuntu Plus](README.vi.md)

# Đóng góp cho UU Remote Ubuntu Plus

Chào đón báo lỗi, bản dịch, tài liệu và mã. Giữ bản quyền và giấy phép MIT của [cầu nối Lachlan Chen](https://github.com/lachlanchen/uu-remote-ubuntu-bridge).

## Mô tả lỗi và đường sử dụng

Ghi Ubuntu/GNOME/Wine/UU, khung hình, tuyến nhập và cách tái hiện. Phân biệt điều khiển Ubuntu, quản lý tại máy và Ubuntu điều khiển máy khác. Thay đổi nhỏ, có phương pháp đo. Gửi phản hồi qua [biểu mẫu tương thích](https://github.com/llmir/uu-remote-ubuntu-plus/issues/new?template=compatibility.yml).

## Môi trường phát triển

Dùng Ubuntu và Python hệ thống. Các gói này phục vụ build/test riêng, install.sh quản lý runtime. Chọn compiler bằng WINEGCC/MINGW_CC/HOST_CC, dùng prefix Wine và display Xvfb tạm.

```bash
sudo apt-get update
sudo apt-get install --no-install-recommends \
  build-essential binutils gcc-mingw-w64-x86-64-win32 \
  wine wine64 wine64-tools xvfb x11-utils x11-xserver-utils xclip xcompmgr
```

## Kiểm tra mã

Chạy bash -n với shell đã đổi, rồi các kiểm tra sau. Giữ cảnh báo C nghiêm ngặt. Wine/Xvfb/systemd có thể cần thiết; ghi rõ test bỏ qua. UURB_TEST_SYSTEMD=1 chỉ khi bus người dùng hoạt động.

```bash
python3 -m compileall -q scripts tests
python3 -m unittest discover -s tests -v
./scripts/build-compat.sh
git diff --check
```

## Tài liệu và hình

Chạy test tài liệu hiện có. SVG Anh/Trung chung bố cục; hai lệnh Node/Sharp cuối chỉ dành cho dựng lại ảnh. Xem toàn ảnh và metadata, giữ mã thanh toán gốc.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_documentation.py -q
npm install --no-save --package-lock=false sharp
node scripts/render-doc-graphics.cjs
```

## Xác minh bản cài

Cài trên máy được cho phép, chuẩn bị kết nối phục hồi trước lúc ngắt ngắn. Xác minh đầy đủ gồm 270 giây ổn định; ảnh/nhập/kết nối lại cần thiết bị điều khiển thật. Chỉ dừng prefix UU.

```bash
./install.sh --skip-packages --skip-account-login
./scripts/verify.sh --quick
./scripts/verify.sh
./uninstall.sh --dry-run
```

## UU phiên bản mới

Cần manifest được duyệt, SHA-256 đầy đủ và giải thích sửa bằng độ dài. Ghi phục hồi đúng byte, khởi động, nhập và gỡ. Không đưa binary độc quyền hay log riêng. Xem [bảo trì upstream (English)](../docs/upstream-maintenance.md).

## Chuẩn bị công bố

Xem danh sách và staged diff. Loại build, prefix, cache, trạng thái .omc, thông tin đăng nhập, ID thiết bị và nội dung nhập. Giữ xác thực, TLS, kiểm tra manifest và gỡ có thể hoàn nguyên.

```bash
git status --short
git diff --cached
```

## Gửi xem xét

Mô tả lỗi, kết quả và kiểm tra đã chạy, xin review độc lập. FPS đặt không phải đo thực. Đọc [chất lượng](../docs/i18n/vi/quality-guide.md), [Ubuntu](../docs/i18n/vi/ubuntu-26.04-port.md), [an toàn](../docs/i18n/vi/security.md), giữ MIT và bản quyền.
