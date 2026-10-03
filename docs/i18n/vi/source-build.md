[English](../../source-build.md) · [العربية](../ar/source-build.md) · [Deutsch](../de/source-build.md) · [Español](../es/source-build.md) · [Français](../fr/source-build.md) · [日本語](../ja/source-build.md) · [한국어](../ko/source-build.md) · [Русский](../ru/source-build.md) · [Tiếng Việt](../vi/source-build.md) · [简体中文](../zh-Hans/source-build.md) · [繁體中文](../zh-Hant/source-build.md)

[Trang chủ](../../../i18n/README.vi.md)

# Biên dịch và dùng lại relay

Trình cài biên dịch FreeRDP SDL cố định với bản vá clipboard/kích thước Plus. [Công thức](../../../vendor/freerdp-sdl-build/), [khóa nguồn](../../../vendor/freerdp-sdl-build/source-lock.json), [hồ sơ sản phẩm](../../../patches/freerdp-sdl-product.json) ghi phiên bản, gói, công cụ và 13 tệp runtime Windows.

<a id="reference-toolchain"></a>

## Chuẩn bị công cụ tham chiếu Ubuntu 26.04

Trên Ubuntu 26.04 amd64, [script chuẩn bị](../../../scripts/prepare-build-toolchain.py) tải 17 gói Ubuntu chính thức đã cố định và kiểm tra 14 tệp trình biên dịch/công cụ theo `source-lock.json`. [Danh sách gói](../../../patches/reference-build-packages.json) ghi phiên bản, kích thước và hàm băm. Script tải, giải nén vào thư mục riêng và kiểm tra, không cài gói hệ thống. Chạy từ gốc kho mã:

```bash
python3 scripts/prepare-build-toolchain.py \
  --packages-dir "$HOME/.cache/uu-plus/reference-packages" \
  --root "$HOME/.cache/uu-plus/reference-root"
```

`--packages-dir` chọn bộ đệm gói; `--root` phải là thư mục riêng mới hoặc rỗng. Để giải nén và kiểm tra lại chỉ từ bộ đệm, chọn thư mục rỗng khác và thêm `--verify-only`; không truy cập mạng:

```bash
python3 scripts/prepare-build-toolchain.py \
  --packages-dir "$HOME/.cache/uu-plus/reference-packages" \
  --root "$HOME/.cache/uu-plus/reference-root-offline" \
  --verify-only
```

Script in lệnh `sudo apt install` chứa đường dẫn của cả 17 tệp `.deb` cục bộ. Chạy lệnh đó thủ công trên Ubuntu 26.04 để cài công cụ tham chiếu. Công thức hiện có đọc các đường dẫn `/usr` cố định; thư mục giải nén riêng dùng để kiểm tra, không để chọn môi trường biên dịch khác.

Sau đó chạy bộ cài thông thường. Nó chuẩn bị các phụ thuộc biên dịch còn lại trên máy chủ, WineHQ và gói chạy GNOME, biên dịch relay rồi kiểm tra trước khi triển khai. Bước chuẩn bị kiểm tra 14 tệp tham chiếu; bản biên dịch nguồn đầy đủ và 13 tệp chạy được kiểm tra qua luồng sau:

```bash
./install.sh
./scripts/verify.sh --quick
```

Trên Ubuntu 24.04, dùng đầu ra đã xác minh khớp hồ sơ hiện tại theo luồng tái sử dụng bên dưới. Các gói Ubuntu 26.04 ở trên dành riêng cho 26.04.

## Biên dịch và bộ nhớ đệm

Biên dịch từ nguồn mới cần đúng các tệp trình biên dịch và công cụ đã duyệt trong `source-lock.json`, khớp từng byte. Các gói APT thông thường của bản phân phối không tự cung cấp bộ công cụ này.

`./install.sh` chuẩn bị gói và kiểm tra trước khi thay relay. Chỉ dùng lại `build/freerdp` nếu nguồn gốc khớp hồ sơ/công thức/tệp cố định. Nếu không, `scripts/build-winpr.sh` dùng nguồn mới, hai tác vụ, giới hạn 900 giây rồi kiểm tra.

Khi công cụ đã duyệt được cài tại các đường dẫn `/usr` của công thức và phụ thuộc biên dịch đã sẵn sàng, cũng có thể tạo bộ đệm relay riêng:

```bash
UURB_BUILD_DIR=/absolute/path/to/build-work   ./scripts/build-winpr.sh /absolute/path/to/fresh-output
```

Dùng thư mục đầu ra mới. Công việc nguồn riêng được tạo dưới thư mục làm việc, không dùng Wine prefix đang chạy. Dùng lại đầu ra đã kiểm tra:

Từ gốc kho mã, trước tiên kiểm tra đầu ra hiện có theo hồ sơ hiện tại. Bộ cài thông thường chuẩn bị phụ thuộc máy chủ. Chỉ dùng `--skip-packages` khi công cụ tương thích máy chủ, WineHQ và gói chạy GNOME đã được cài; có thể dùng `--skip-account-login` với tài khoản đã cấu hình.

```bash
python3 scripts/verify-freerdp-runtime.py --mode build /absolute/path/to/verified/output
```

Sau đó dùng lại đầu ra qua lối cài đặt hiện có:

```bash
UURB_FREERDP_PREBUILT_DIR=/absolute/path/to/verified/output   ./install.sh
```

Bộ đệm phải khớp công thức/tệp/nguồn gốc hồ sơ hiện tại. Hồ sơ thay đổi cần chạy lại đầu vào biên dịch/kiểm tra; sửa biên nhận/checksum không phê duyệt nhị phân khác. Bản sao cũng được kiểm tra trước khi chạy dịch vụ.

## Đầu vào và kết quả

Cố định FreeRDP/WinPR, SDL 3.2.28, SDL_ttf, OpenH264, FreeType, HarfBuzz và OpenSSL/cJSON/uriparser. Kiểm tra bản vá và hash MinGW/trình biên dịch/công cụ trước khi biên dịch; đổi cần duyệt công thức mới.

Ánh xạ tiền tố tệp/macro/debug chuẩn hóa đường dẫn. FreeRDP opaque OFF ngay cấu hình đầu, DLL tương thích có tên đầu ra tương đối, tránh nhúng đường dẫn máy.

Hai gốc nguồn/đầu ra khác nhau tạo cùng byte cho 13 tệp. CMake lần đầu/lặp lại có cùng metadata. Toàn bộ biên dịch sạch không dùng đầu ra sẵn mất khoảng 700 giây trong hạn900 và đạt kiểm tra runtime/nguồn gốc. [Chất lượng](quality-guide.md), [chi phí](performance-evidence.md).
