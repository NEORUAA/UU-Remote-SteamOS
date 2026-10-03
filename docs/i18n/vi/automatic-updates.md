[English](../../automatic-updates.md) · [العربية](../ar/automatic-updates.md) · [Español](../es/automatic-updates.md) · [Français](../fr/automatic-updates.md) · [日本語](../ja/automatic-updates.md) · [한국어](../ko/automatic-updates.md) · [Tiếng Việt](../vi/automatic-updates.md) · [中文（简体）](../zh-Hans/automatic-updates.md) · [中文（繁體）](../zh-Hant/automatic-updates.md) · [Deutsch](../de/automatic-updates.md) · [Русский](../ru/automatic-updates.md)

[← Về trang chủ tiếng Việt](../../../i18n/README.vi.md)

# Kiểm tra tự động và sửa chữa tiếp tục được

Bảo trì tách quan sát, sửa nguồn riêng và promotion trực tiếp đã chấp nhận rõ. Kiểm tra thông thường không ngắt relay đang hoạt động.

## Cấu hình và timer

Lịch sử phát hành riêng của Plus bắt đầu từ `v0.1.0`. Các tag đường nhập có ngày thuộc lịch sử dự án gốc và không có trong kho độc lập này. Cài đặt thông thường không cần chúng. Khi tag Plus đã có cục bộ, chọn rõ `--track v0.1.0 --branch main`; cấu hình mặc định vẫn chọn tên track cũ và từ chối tag không tồn tại.

Sau khi checkout tag phát hành, chạy `git switch main` trước lệnh nâng cấp thông thường có lấy mã nguồn. Nhánh được duy trì là `origin/main`, còn tag cài lại được chọn rõ là `v0.1.0`. Để chủ động giữ nguyên cây mã nguồn tại tag khi nâng cấp, dùng `--no-pull`.

`--auto-promote-accepted` chỉ cho phiên bản sau đã được maintainer chấp nhận gắn hash, không draft Codex tự tạo. Model, reasoning và đường dẫn Codex tuyệt đối nằm trong `updater.json`; cùng người dùng phải đăng nhập. Mọi cửa sổ quota included phải dưới mặc định 20%; không xác minh được thì hoãn ít nhất một giờ.

`uu-remote-update-check.timer` chạy mỗi ngày khoảng 04:20 với trễ ngẫu nhiên và 12 phút sau boot; `Persistent=true` bù một lần đã bỏ lỡ. Monitor bắt đầu sau bảy phút, rồi 15 phút sau lần trước.

## Quan sát và sửa

Checker theo redirect HEAD chính thức, bỏ query key tạm và so phiên bản đầy đủ. ETag, size và hash-sidecar tránh tải lại file giống nhau. Endpoint cũ không phải update. Hai lỗi sức khỏe cách 20 giây tạo evidence/task mà không dừng Wine/RDP/UU. Chỉ opt-in riêng `--auto-reinstall` cho phục hồi.

Download tối đa 1 GiB. Hash lạ được giải nén tĩnh, phân tích trong clone riêng với bản hợp đồng `0600`. Wrapper không giải nén được cần staging không mạng chủ động. Codex không sudo, đổi live-prefix, push hay tự phê duyệt nhị phân.

## Promotion đã chấp nhận

Hash chính thức, manifest `approved`, acceptance schema-1 và evidence phải khớp cùng commit fetched `origin/main`, gắn hash installer/server đã vá. Thử prefix tạm, controller, reconnect, cold-start, service restart, signaling mới và giữ login; ổn định 270–1800 giây. Bật auto-promotion rõ và UU thường cần yên 45 phút.

Chỉ dừng bridge-service. Sao toàn prefix cộng 1 GiB dự phòng, cài tại chỗ, so byte dữ liệu tài khoản, đợi room mới và hai check runtime. Không đổi XRDP. State/prefix phải cùng filesystem. Lỗi, reboot hoặc gián đoạn khôi phục cũ, giữ snapshot và chặn tự thử lại. `--now` chỉ bỏ chờ rảnh.

## Task, riêng tư và sandbox

UUID từ `thread.started` được lưu để `codex exec resume`; chưa có UUID thì tạo thread mới cùng context. Retry tăng từ 15 phút tới 24 giờ. Kết quả theo schema được test riêng: `ready-for-review`, `no-change`, `blocked`; các phase promotion: `promotion-waiting-idle`, `promotion-running`, `promoted`, `promotion-blocked`.

Thư mục riêng `0700`, file `0600`, clone tắt push, Codex workspace-write/never, service `NoNewPrivileges=yes`; xác thực vẫn cần mạng. Ubuntu 24.04 không nên dùng mount namespace user-service cản Bubblewrap lồng. Khi `codex-sandbox-deferred`, chỉ cài profile AppArmor distro bằng lệnh dưới, không nới hạn chế toàn cục. `retry` giữ evidence/checkout, thay thread lỗi và nhập staging chỉ khi hash installer/server/healthd khớp.

`disable` giữ evidence; `disable --purge-state` xóa cả cấu hình/state riêng. Sang máy khác chỉ chuyển nguồn và chọn input-profile của máy đó.

[Nâng cấp](reusable-upgrade.md) · [Bảo mật](security.md)

## Lệnh và giá trị kỹ thuật

```bash
git switch main
git fetch --tags origin
./scripts/configure-updater.sh enable \
  --track v0.1.0 --branch main \
  --model codex-auto-review --reasoning-effort medium \
  --auto-promote-accepted
uu-remote update
systemctl --user list-timers --all \
  uu-remote-update-check.timer uu-remote-repair-monitor.timer
journalctl --user -u uu-remote-update-check.service -n 100 --no-pager
journalctl --user -u uu-remote-repair-monitor.service -n 100 --no-pager
uu-remote upgrade apply --now
```

```bash
sudo apt install apparmor-profiles
sudo install -o root -g root -m 0644 \
  /usr/share/apparmor/extra-profiles/bwrap-userns-restrict \
  /etc/apparmor.d/bwrap-userns-restrict
sudo apparmor_parser -r /etc/apparmor.d/bwrap-userns-restrict
uu-remote update retry
systemd-run --user --wait --pipe --collect \
  --property=NoNewPrivileges=yes \
  /usr/bin/bwrap --die-with-parent --unshare-user --uid 0 --gid 0 \
  --ro-bind / / /bin/true
systemctl --user cat uu-remote-repair-monitor.service
./scripts/configure-updater.sh status
./scripts/configure-updater.sh disable
./scripts/configure-updater.sh disable --purge-state
```

## Mã nguồn và tài liệu liên quan


Tài liệu kỹ thuật chuyên sâu có bằng tiếng Anh và tiếng Trung giản thể:

- [automated-repair-agent-handoff](../../automated-repair-agent-handoff.md) · [简体中文](../zh-Hans/automated-repair-agent-handoff.md)
- [release-tracks](../../release-tracks.md) · [简体中文](../zh-Hans/release-tracks.md)
- [upstream-maintenance](../../upstream-maintenance.md) · [简体中文](../zh-Hans/upstream-maintenance.md)
