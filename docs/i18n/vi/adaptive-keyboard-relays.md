[English](../../adaptive-keyboard-relays.md) · [العربية](../ar/adaptive-keyboard-relays.md) · [Español](../es/adaptive-keyboard-relays.md) · [Français](../fr/adaptive-keyboard-relays.md) · [日本語](../ja/adaptive-keyboard-relays.md) · [한국어](../ko/adaptive-keyboard-relays.md) · [Tiếng Việt](../vi/adaptive-keyboard-relays.md) · [中文（简体）](../zh-Hans/adaptive-keyboard-relays.md) · [中文（繁體）](../zh-Hant/adaptive-keyboard-relays.md) · [Deutsch](../de/adaptive-keyboard-relays.md) · [Русский](../ru/adaptive-keyboard-relays.md)

[← Về trang chủ tiếng Việt](../../../i18n/README.vi.md)

# Chuyển tiếp bàn phím thích ứng

XRDP mang metadata bố cục và scancode; RFB/X11 mang keysym; UU máy tính gửi sự kiện Windows vật lý; IME điện thoại gửi Unicode. Giữ riêng các lớp này để không mất ý nghĩa ký tự.

Để XRDP chọn bố cục mà client báo. `setxkbmap ... -layout jp` vô điều kiện trong `~/.xsessionrc` sẽ ghi đè cho mọi client. Giữ sửa lỗi Mac bàn phím Nhật dưới dạng lệnh chạy chủ động, không vòng lặp đăng nhập toàn cục. IBus, văn bản ngữ nghĩa và terminal không phụ thuộc XKB vật lý.

## Viewer VNC chuyên dụng

Relay toàn màn hình dùng `UURB_VNC_GRAB_KEYBOARD=on` và `-GrabKeyboard=1`. Nếu không, desktop trung gian có thể lấy Shift/Ctrl/Alt/Super: `(` thành `8`, `?` thành `/`, `@` thành `2`. x11vnc dùng `-modtweak -xkb -add_keysyms` để phục hồi modifier và bổ sung keysym, chỉ nghe IPv4 loopback.

Chỉ tắt grab khi viewer không chuyên dụng. Test RFB/Xvfb cô lập kiểm tra 21 ký hiệu Shift và `你好` với XKB Nhật. Sau đó dùng ô văn bản dùng một lần kiểm tra ký tự thường, Shift, Ctrl+A/C/V, Enter/Backspace và IME thật; không dùng ô mật khẩu.

## Giới hạn bố cục

X11 trực tiếp theo bố cục phiên đích. UU không truyền mã bố cục đáng tin theo kết nối: chỉ `Shift+7` không thể đoán `&` hay `'`. XRDP/RFB dùng metadata/keysym, điện thoại dùng Unicode. Đổi rõ profile client cần thiết, không áp một bố cục cho mọi người. `rdp-public/auto` giữ nguyên commit Unicode, còn phím vật lý dùng route thường.

[Kiến trúc](architecture.md) · [Bảo mật](security.md)

## Lệnh và giá trị kỹ thuật

```text
UURB_VNC_GRAB_KEYBOARD=on
-GrabKeyboard=1
-repeat -nobell -modtweak -xkb -add_keysyms
```

```bash
./install.sh --skip-packages --skip-account-login \
  --vnc-grab-keyboard off
./scripts/test-vnc-keyboard-relay.sh
```

```text
vnc-symbols=23/23 order=exact target-layout=jp
isolated VNC keyboard acceptance passed
```

## Mã nguồn và tài liệu liên quan


Tài liệu kỹ thuật chuyên sâu có bằng tiếng Anh và tiếng Trung giản thể:

- [release-tracks](../../release-tracks.md) · [简体中文](../zh-Hans/release-tracks.md)
- [semantic-text-and-clipboard](../../semantic-text-and-clipboard.md) · [简体中文](../zh-Hans/semantic-text-and-clipboard.md)
