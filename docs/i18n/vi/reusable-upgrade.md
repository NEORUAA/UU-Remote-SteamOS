[English](../../reusable-upgrade.md) · [العربية](../ar/reusable-upgrade.md) · [Español](../es/reusable-upgrade.md) · [Français](../fr/reusable-upgrade.md) · [日本語](../ja/reusable-upgrade.md) · [한국어](../ko/reusable-upgrade.md) · [Tiếng Việt](../vi/reusable-upgrade.md) · [中文（简体）](../zh-Hans/reusable-upgrade.md) · [中文（繁體）](../zh-Hant/reusable-upgrade.md) · [Deutsch](../de/reusable-upgrade.md) · [Русский](../ru/reusable-upgrade.md)

[← Về trang chủ tiếng Việt](../../../i18n/README.vi.md)

# Nâng cấp lặp lại và giữ đăng nhập

`uu-remote-upgrade` và `uu-remote upgrade` kết hợp cập nhật repo, promotion UU đã chấp nhận, làm mới cầu nối và kiểm tra. `status` xem trạng thái, `check` không đổi sản phẩm, `apply` đợi lúc rảnh. `apply --now` chỉ bỏ chờ hoạt động, không ép nhị phân lạ hoặc chưa chấp nhận.


Sau khi checkout tag phát hành, chạy `git switch main` trước lệnh nâng cấp thông thường có lấy mã nguồn. Nhánh được duy trì là `origin/main`, còn tag cài lại được chọn rõ là `v0.1.0`. Để chủ động giữ nguyên cây mã nguồn tại tag khi nâng cấp, dùng `--no-pull`.

## Giao dịch

Checkout phải sạch, không detached. Fetch/fast-forward không gộp lịch sử phân nhánh; script chạy lại từ nguồn mới nếu thay đổi. Tests và shell parser chạy trước. Kiểm tra sản phẩm được duyệt, relay, route, timing và marker tài khoản. Chỉ installer chính thức có hash/acceptance khớp manifest được tiếp tục.

Promotion sao chép toàn Wine prefix, cài tại chỗ, vá rồi so từng byte phần login registry và hai cây tài khoản. Có hai kiểm tra runtime cách nhau bằng khoảng ổn định. Sau đó lưu riêng runtime cầu nối, cập nhật helper/service nhưng giữ environment, track và cấu hình Codex. XRDP chỉ được hỏi trạng thái; đổi active-state làm thao tác thất bại.

## Phục hồi và đầu vào

Lỗi hoặc gián đoạn trả lại toàn prefix và `promotion-blocked`, không tự thử lại. Xếp lại rõ cùng bản chấp nhận yêu cầu commit mã promotion đã đổi; task cũ ở `tasks/retired/`. Nếu làm mới nguồn thất bại, khôi phục runtime sau promotion. Timer không xóa snapshot.

Giá trị X11 mẫu không nên chép sang máy khác: route đã lưu mới là chuẩn. Quick verifier không gõ vào ứng dụng của bạn; sau update thử văn bản điện thoại, phím vật lý nhanh, di chuyển/click/drag/cuộn.

Bus cố định `/run/user/UID/bus` tránh hỏi nhầm user manager từ terminal lồng. Sự cố 4.34 tháng 7/2026 không phải hiện trạng Plus 4.42. Các sửa khi đó liên quan verifier thiếu, timestamp PE và race readiness; nay đợi listener thật/helper đã chọn tối đa 45 giây. Sang máy khác chỉ chuyển nguồn, không prefix, keyring hoặc state riêng. `~/.local/bin` phải nằm trong `PATH`.

[Cập nhật tự động](automatic-updates.md) · [Bàn phím](adaptive-keyboard-relays.md)

## Lệnh và giá trị kỹ thuật

```bash
uu-remote-upgrade status
uu-remote upgrade status
uu-remote upgrade check
uu-remote upgrade apply
uu-remote upgrade apply --now
./scripts/upgrade-uu-remote.sh apply --now
```

```text
UURB_TEXT_KEY_DELAY_MS=8
UURB_PHYSICAL_KEY_DELAY_MS=0
UURB_KEYBOARD_ROUTE=x11
UURB_NETWORK_INTERFACE=default
unix:path=/run/user/UID/bus
~/.local/state/uu-remote-updater/tasks/*/promotion/snapshot-prefix
~/.local/state/uu-remote-upgrader/transactions/TIMESTAMP/
~/.local/state/uu-remote-upgrader/latest
```

```bash
git status --short
git switch main
git pull --ff-only origin main
./install.sh --skip-packages --skip-account-login
./scripts/configure-updater.sh enable --track v0.1.0 --branch main \
  --model codex-auto-review --reasoning-effort medium \
  --auto-promote-accepted
./scripts/upgrade-uu-remote.sh check
```

## Mã nguồn và tài liệu liên quan


Tài liệu kỹ thuật chuyên sâu có bằng tiếng Anh và tiếng Trung giản thể:

- [release-tracks](../../release-tracks.md) · [简体中文](../zh-Hans/release-tracks.md)
- [upstream-maintenance](../../upstream-maintenance.md) · [简体中文](../zh-Hans/upstream-maintenance.md)
