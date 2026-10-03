[English](../../security.md) · [العربية](../ar/security.md) · [Español](../es/security.md) · [Français](../fr/security.md) · [日本語](../ja/security.md) · [한국어](../ko/security.md) · [Tiếng Việt](../vi/security.md) · [中文（简体）](../zh-Hans/security.md) · [中文（繁體）](../zh-Hant/security.md) · [Deutsch](../de/security.md) · [Русский](../ru/security.md)

[← Về trang chủ tiếng Việt](../../../i18n/README.vi.md)

# Bảo mật

## Quyền sử dụng và ranh giới

Chỉ dùng cầu nối trên máy và tài khoản UU được phép quản trị. Toàn bộ chạy với người dùng Unix đã đăng nhập, trong Wine prefix riêng. Xvfb dùng Xauthority, không TCP; pipe thuộc wineserver của prefix. Helper X11 và terminal có cổng IPv4 loopback tạm thời và token 256-bit riêng mới mỗi lần chạy. Thư mục `0700`, tệp bàn giao terminal `0600`, tối đa bốn shell.

VNC quản lý không có mật khẩu riêng nhưng chỉ nghe loopback và xuất một cửa sổ UU, không root riêng. Relay Mac tùy chọn dùng VNC xác thực qua SSH. FreeRDP chỉ nối `127.0.0.1` và kiểm tra TLS. Listener LAN của GNOME tùy cấu hình của nó; dùng firewall và mật khẩu độc lập đủ mạnh.

## Mật khẩu và dữ liệu

`secret-tool` lưu mật khẩu relay trong login keyring; FreeRDP đọc qua stdin. VNC cổ điển dùng tám byte đầu, tệp luôn `0600`. Khởi động không người trực mã hóa thêm mật khẩu keyring bằng TPM2/systemd-creds và chỉ giải mã trong runtime được bảo vệ. GDM autologin mở quyền truy cập vật lý sau boot; TPM không chặn chương trình của người đã đăng nhập và LUKS vẫn cần tương tác.

Log nhập liệu chỉ có số lượng, loại, flags, route, kết quả, mã lỗi; không có ký tự, tọa độ hay clipboard. Terminal không ghi lệnh hoặc đầu ra. Văn bản ngữ nghĩa giới hạn 2.048 bản ghi và được giữ trong clipboard sau khi dán. Không công bố token, registry, prefix, log thô hoặc ảnh cá nhân.

## Nhị phân và bảo trì

Patcher chỉ nhận manifest `approved` với hash đầy đủ, kích thước, signature duy nhất và thay thế cùng độ dài. Bản gốc `.uu-original` được giữ. Manifest 4.42 không cho phép phiên bản khác; draft cần kiểm tra ngữ nghĩa độc lập. Tái sử dụng relay phải khớp source, recipe, profile, pins và provenance.

Installer lạ được giải nén tĩnh trước. `--sandbox-install` là lựa chọn rõ ràng dùng staging Bubblewrap/systemd không mạng. Wine không cách ly mạnh các tiến trình cùng người dùng. Repair không tự phê duyệt: promotion cần hash chính xác, acceptance đã commit, thử controller/login thực và ít nhất 270 giây ổn định. Giao dịch sao chép toàn prefix, phục hồi khi lỗi và không đổi XRDP.

[Dựng nguồn](source-build.md) · [Cập nhật](automatic-updates.md)

## Lệnh và giá trị kỹ thuật

```text
~/.local/share/wineprefixes/uu-remote
~/.config/uu-remote-bridge/environment
CLIPBOARD / PRIMARY
KEYEVENTF_UNICODE / cliprdr
```

## Mã nguồn và tài liệu liên quan

- [patches/uu-remote-4.42.0.2770.json](../../../patches/uu-remote-4.42.0.2770.json)
- [patches/freerdp-sdl-product.json](../../../patches/freerdp-sdl-product.json)

Tài liệu kỹ thuật chuyên sâu có bằng tiếng Anh và tiếng Trung giản thể:

- [semantic-text-and-clipboard](../../semantic-text-and-clipboard.md) · [简体中文](../zh-Hans/semantic-text-and-clipboard.md)
- [upstream-maintenance](../../upstream-maintenance.md) · [简体中文](../zh-Hans/upstream-maintenance.md)
