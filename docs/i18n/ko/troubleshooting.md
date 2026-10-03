[English](../../troubleshooting.md) · [العربية](../ar/troubleshooting.md) · [Deutsch](../de/troubleshooting.md) · [Español](../es/troubleshooting.md) · [Français](../fr/troubleshooting.md) · [日本語](../ja/troubleshooting.md) · [한국어](../ko/troubleshooting.md) · [Русский](../ru/troubleshooting.md) · [Tiếng Việt](../vi/troubleshooting.md) · [简体中文](../zh-Hans/troubleshooting.md) · [繁體中文](../zh-Hant/troubleshooting.md)

[한국어 · UU Remote Ubuntu Plus](../../../i18n/README.ko.md)

# 문제 해결

## 먼저 상태 확인

소스 폴더에서 실행합니다. 로그는 `~/.local/state/uu-remote-bridge`, 설정은 `~/.config/uu-remote-bridge/environment`에 있습니다. 버전과 오류를 공유하되 계정과 입력 내용은 제거합니다. 소스 수정 후 다시 설치합니다.

```bash
uu-remote status
./scripts/verify.sh --quick
uu-remote logs
uu-remote network
```

## 오프라인 또는 재부팅 후 연결 실패

공식 관리 창에서 한 번 로그인하고 정상 종료합니다. 사용자 서비스와 키링을 확인합니다. 비밀번호 변경 후 `./scripts/configure-unattended.sh enable --replace-credential`로 암호화 자격 정보를 갱신합니다. 서버 종료 시 복구 기록도 확인합니다.

```bash
uu-remote login
./scripts/configure-unattended.sh status
journalctl --user -b -u uu-keyring-unlock.service -u uu-remote-bridge.service --no-pager
```

## 경로 찾기가 계속됨

호스트 시작이 완료됐는지 확인합니다. Wine의 오래된 입력·Bluetooth 장치 기록이 시작을 지연할 수 있습니다. 복구 명령은 레지스트리를 백업하고 UU 전용 기록을 정리한 뒤 재시작하며 Ubuntu Bluetooth는 유지합니다.

```bash
uu-remote repair-registry
./scripts/verify.sh --quick
```

## 검은 화면·흰 화면·잘못된 데스크톱

로그인된 GNOME 세션, RDP 리스너, SDL 로그를 확인합니다. XRDP는 `--desktop-target xrdp`, 물리 데스크톱은 `physical`입니다. `--desktop-relay vnc`는 X11에만 쓰며 Wayland는 RDP를 사용합니다.

```bash
systemctl --user status uu-remote-bridge.service
/usr/bin/grdctl status
loginctl list-sessions
tail -80 ~/.local/state/uu-remote-bridge/freerdp.log
tail -80 ~/.local/state/uu-remote-bridge/gnome-remote-desktop.log
```

## 여백·잘림·무거운 4K

소스 크기와 캔버스를 비교하고 720p/1080p/1440p/4K를 선택합니다. 캔버스, 컨트롤러 FPS, 비트레이트는 별도 설정입니다. 변경 시 잠깐 재연결하며 실패하면 복원합니다. XRDP의 동적 크기도 확인합니다.

```bash
uu-remote quality status
uu-remote quality gui
uu-remote quality apply 1080p
```

## 화면은 보이지만 입력이 안 됨

uu-remote open으로 관리 창을 열고 같은 Wine 환경을 다른 X 디스플레이에 직접 실행하지 않습니다. 뷰어를 닫으면 릴레이에 포커스가 돌아옵니다. 휴대폰 문자는 클립보드/RDP 붙여넣기, 물리 키는 이벤트입니다. 재설치 후 입력 주입기를 확인합니다. 첫 클릭에 연결이 종료되면 UU SendInput bridge active, UU Wine event-log compatibility active와 broker를 확인하고 `uu-remote restart`로 복구합니다.

```bash
uu-remote open
./scripts/verify.sh --quick
tail -80 ~/.local/state/uu-remote-bridge/input-injector.log
```

## 키 지연·기호 오류·장기 사용 문제

VPN, 프록시, UU 경로를 비교합니다. stale은 과거 세션입니다. 잘못된 NIC가 확인되면 `--network-interface default`, 복원은 `all`입니다. `--physical-key-delay-ms 8`을 시험할 수 있으며 기본은 `0`입니다. 기호는 Ubuntu 배열을 따릅니다. GRD/libei와 파일 디스크립터도 확인합니다.

```bash
uu-remote network
ip -4 route show default
```

## 커서가 없거나 작음

선택적 커서 보호는 기본 꺼짐입니다. auto는 데스크톱 크기를 따르고 고정값은 24~128입니다. `--cursor-guard off`로 끕니다. 전체 해상도나 Wine DPI를 바꿀 필요가 없습니다.

```bash
./install.sh --skip-packages --skip-account-login --cursor-guard on --cursor-size auto
```

## UU 터미널 종료·문자 위치 오류

현재 브리지를 설치하고 터미널 채널을 검사합니다. UU의 PowerShell을 선택하면 Ubuntu 로그인 shell이 열립니다. 위치 오류는 새 세션으로 확인하고 terminal-bridge.log 메타데이터를 봅니다. powershell.exe를 임의로 바꾸지 않습니다.

```bash
./install.sh --skip-packages --skip-account-login
./scripts/verify.sh --quick
./scripts/test-terminal-bridge.sh
```

## RDP 인증·NLA·SSPI 오류

조회는 비밀번호를 출력하지 않습니다. 필요한 경우 전용 키링 항목만 지우고 다시 설치합니다. FreeRDP, WinPR, DLL은 같은 고정 버전에서 빌드합니다.

```bash
/usr/bin/secret-tool lookup service uu-desktop-bridge username "$USER" >/dev/null
/usr/bin/grdctl status
```

## Mac RDP/VNC·Windows App 멈춤

내부 FreeRDP가 데스크톱 공유 포트를 사용하며 원격 로그인은 다른 세션을 엽니다. 실제 루프백 VNC 포트를 조회해 SSH로 전달합니다. Configuring이면 먼저 Mac 앱을 다시 열고 XRDP를 확인합니다.

```bash
~/.local/bin/uu-remote-console relay-port
ss -ltnp
```

## 반복 재시작·소리·삭제

전체 검증기는 안정성을 확인합니다. 전용 환경에서 UU 오디오, Wine PulseAudio, VNC 벨을 각각 점검합니다. 삭제 전에 미리 봅니다. 일반 삭제는 프리픽스를 보존하고 `./uninstall.sh --purge`는 계정 상태도 삭제합니다. `wpctl status`로 실제 오디오 스트림을 확인합니다. `UURB_UU_AUDIO=system`이 호환 기본값이며 전용 무음 ALSA와 원복은 영어 상세 가이드를 참고합니다.

```bash
./scripts/verify.sh
uu-remote logs
./uninstall.sh --dry-run
```

더 보기: [화질](quality-guide.md), [빌드](source-build.md), [구조](architecture.md), [입력](adaptive-keyboard-relays.md), [업데이트](reusable-upgrade.md). [상세 기술과 기록(English)](../../troubleshooting.md)에는 레지스트리, 드라이버, 오디오, XRDP, 터미널 설명이 있습니다.

## 상세 안내

- XRDP와 키보드 복구 · [English](../../xrdp-and-keyboard-recovery.md) · [简体中文](../zh-Hans/xrdp-and-keyboard-recovery.md)
- 키보드 호환성 · [English](../../mobile-keyboard-parity-handoff.md) · [简体中文](../zh-Hans/mobile-keyboard-parity-handoff.md)
- Mac에서 현재 데스크톱 · [English](../../macos-current-desktop.md) · [简体中文](../zh-Hans/macos-current-desktop.md)
- 물리 데스크톱 공유 · [English](../../shared-physical-desktop.md) · [简体中文](../zh-Hans/shared-physical-desktop.md)
- 종료 후 복구 · [English](../../clean-exit-recovery.md) · [简体中文](../zh-Hans/clean-exit-recovery.md)
- 컨트롤러 에이전트 · [English](../../controller-agent.md) · [简体中文](../zh-Hans/controller-agent.md)
- SSH 에이전트 메시지 · [English](../../agent-link.md) · [简体中文](../zh-Hans/agent-link.md)
