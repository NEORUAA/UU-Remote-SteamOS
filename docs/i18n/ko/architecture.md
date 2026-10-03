[English](../../architecture.md) · [العربية](../ar/architecture.md) · [Deutsch](../de/architecture.md) · [Español](../es/architecture.md) · [Français](../fr/architecture.md) · [日本語](../ja/architecture.md) · [한국어](../ko/architecture.md) · [Русский](../ru/architecture.md) · [Tiếng Việt](../vi/architecture.md) · [简体中文](../zh-Hans/architecture.md) · [繁體中文](../zh-Hant/architecture.md)

[한국어 홈으로 돌아가기](../../../i18n/README.ko.md)

# 구조

![Ubuntu 화면은 컨트롤러로, 키보드·마우스·문자는 Ubuntu로 이동하며 관리 창은 별도 경로를 사용합니다.](../../images/architecture-premium-v2-en.png)

보라색은 화면 전송, 주황색은 돌아오는 입력입니다. 관리 창은 로컬에 표시하고 그 창으로 조작을 보냅니다.

## 실제 데스크톱과 Wine 캔버스

Windows UU 호스트는 전용 Wine 프리픽스에서 실행됩니다. Windows 커널 입력 드라이버로 GNOME을 직접 조작할 수 없어 비공개 X11 화면에 릴레이 창을 두고 사용자 공간 입력을 선택한 Ubuntu 세션에 전달합니다. 앱이 실행되는 데스크톱과 중계 캔버스는 별개입니다. 계정 관리 뷰어는 원격 화면 전송의 중간 단계가 아닙니다. 현재 UU 4.42 매니페스트와 고정 소스 FreeRDP/SDL을 사용하며 업데이트는 기존 설정을 보존합니다.

## 새 설치의 기본값

| 항목 | 기본 | 선택 사항 |
| --- | --- | --- |
| 데스크톱 릴레이 | `rdp` | X11/XRDP의 `vnc` |
| 입력 백엔드 | RDP의 `rdp-public` | `legacy`, VNC는 필수 |
| 대상 | `auto` | `physical`, `xrdp`, 명시적 X display |
| 캔버스 | 1920 × 1080 | 720p, 1080p, 1440p, 4K |
| 소스 크기 따라가기 | `off` | `on` |
| 이전 경로 물리 키 | 릴레이 `rdp` | X11의 `x11` / `auto` |
| 휴대폰 문자 | `auto` | `keys` / `clipboard` |

[설치기](../../../install.sh#L358)가 새 기본값을 정합니다. 설치 설정 없이 [실행기](../../../scripts/uu-remote-bridge#L6)를 직접 실행하면 legacy로 돌아갑니다. rdp-public은 RDP용이며 VNC는 접근 가능한 X11/XRDP가 필요합니다. Wayland를 대신하지 않습니다. [runtime-settings.sh](../../../scripts/runtime-settings.sh)는 새 설치와 업데이트의 문자 전송 간격을 구분합니다. 릴레이와 컨트롤러 화질/FPS/비트레이트는 별도 설정입니다.

## 화면 경로

![화면 전송과 돌아오는 입력](../../images/uu-plus-data-flow-en.gif)

[정적 PNG](../../images/uu-plus-data-paths-en.png) · [편집 SVG](../../images/uu-plus-data-paths-en.svg)

```text
선택한 로그인 상태 GNOME 데스크톱
 → 세션 D-Bus의 GNOME Remote Desktop
 → localhost RDP
 → 고정 소스 Windows SDL FreeRDP / Ubuntu-Desktop-Relay
 → 비공개 X11 캔버스
 → UU GameViewerServer 캡처·인코딩·전송
 → 휴대폰, Mac, Windows UU 컨트롤러
```

실행기는 GNOME Shell의 display, 세션, D-Bus를 찾고 명시한 대상이 없으면 기다립니다. 선택한 버스에서 GNOME RDP를 시작하며 XRDP 비공개 버스도 지원합니다. FreeRDP 기본 주소는 127.0.0.1:3390, TLS 지문을 고정하고 GNOME 자격 정보는 표준 입력으로 받습니다. UU 계정 비밀번호와 다릅니다. [릴레이 구현](../../../scripts/uu-remote-bridge#L1010), [SDL 실행](../../../scripts/uu-remote-bridge#L1758)을 참고하세요.

Xvfb/Openbox는 Xauthority와 -nolisten tcp로 캔버스를 만듭니다. :20부터 빈 display를 찾거나 확인된 지정 display를 씁니다. Wine 시작 전에 네 실제 모드를 등록합니다. rdp-public의 [uu-manual-plane.py](../../../scripts/uu-manual-plane.py#L155)가 XComposite 리디렉션을 소유하고 결합된 SDL pixmap만 root에 그립니다. 관리 창은 mapped 상태지만 root 화면에는 포함되지 않습니다.

```text
선택한 X11 데스크톱 → loopback x11vnc → 비공개 전체화면 VNC viewer
 → UU 캡처와 전송 → UU 컨트롤러
```

VNC는 확인된 독립 서비스를 재사용하거나 자체 서비스를 실행합니다. 뷰어가 소스에 맞추며 물리 모니터를 바꾸지 않습니다. 이 경로는 legacy 입력입니다.

## 키보드와 마우스

[4.42 매니페스트](../../../patches/uu-remote-4.42.0.2770.json)의 버전별 패치는 커널 HID 대신 기존 사용자 공간 SendInput을 선택합니다.

```text
컨트롤러 키·포인터·버튼·휠
 → GameViewerServer SendInput hook
 → 로컬 broker named pipe
 → uu-input-broker.exe / uurb_rdp_backend
 → SDL uurb-full-input named pipe
 → FreeRDP 공개 입력 API
 → 기존 RDP → GNOME Remote Desktop → 선택 데스크톱
```

/dvc:uurb-full-input은 플러그인을 로드합니다. broker 연결은 로컬 named pipe이며 새 서버 입력 채널이 필요하지 않습니다. 세션과 크기를 결합해 FreeRDP 이벤트 루프에서 보냅니다. Wine 전경 창을 빼앗는 경로가 아니며 일부 전송 뒤의 불명확한 결과를 재생하지 않습니다. [hook](../../../src/uu_input_bridge.c#L688), [broker](../../../src/uu_input_broker.c#L1081), [plugin](../../../src/plugin.c#L200), [adapter](../../../src/freerdp-adapter.c#L48)가 담당합니다.

legacy는 일반 배열을 Wine SendInput에 먼저 전달하고 미수신분을 broker로 보냅니다. Unicode는 broker로 바로 갑니다. broker는 비공개 릴레이에 포커스를 주고 RDP/VNC로 전달합니다. X11은 --keyboard-route x11/auto로 인증된 XTEST helper를 선택할 수 있습니다. 주입 전 helper가 없으면 릴레이를 쓰고, 주입 후 불명확한 실패는 재전송하지 않습니다.

## Unicode와 클립보드

물리 키와 IME 확정 문자는 다릅니다. 휴대폰 KEYEVENTF_UNICODE에 대해 legacy/auto는 표현 가능한 문자만 키 조합으로 바꾸고 중국어·개행·tab은 문자 helper를 사용합니다. rdp-public/auto는 ASCII도 원문 그대로 보내 Caps Lock/배열 영향을 피합니다. keys는 명시적 키 변환입니다.

broker가 제한된 텍스트를 인증 loopback으로 전송하고 uu-x11-input이 UTF-8로 바꿉니다. xclip은 접근 허가된 대상 X11/Xwayland의 CLIPBOARD/PRIMARY를 소유하고 새 owner를 확인합니다. rdp-public은 plugin/RDP로 Shift+Insert를 보내 owner/selection-request 완료를 확인합니다. 이전 분리 RDP는 소스 선택 영역과 비공개 SDL의 붙여넣기 키를 쓰며 직접 X11은 대상에서 둘 다 실행합니다. 앱의 포커스와 붙여넣기 지원도 필요합니다. [문자와 클립보드(English)](../../semantic-text-and-clipboard.md)를 참고하세요.

일반 복사는 RDP cliprdr로 처리하며 휴대폰 IME와 독립입니다. 고정 SDL 패치가 remote cache와 sequence/owner를 수정합니다. [소스 빌드](source-build.md)를 보세요. VNC 보조 경로는 단방향입니다.

```text
컨트롤러 UU clipboard → GameViewer CF_UNICODETEXT
 → uu-wine-clipboard-bridge → 인증 loopback helper
 → 대상 CLIPBOARD / PRIMARY
```

시작 sequence를 기준으로 읽기 전후에 GameViewer owner를 요구합니다. 호스트 내용을 되돌려 읽거나 붙여넣기 키를 보내지 않고, 명시적 VNC/X11에서만 실행합니다.

## 로컬 관리 창

![UU 관리 창과 관련 팝업의 독립 캡처](../../images/manager-premium-en.png)

uu-remote open은 로컬 TigerVNC로 관리 UI를 엽니다. Wine 창은 전용 프리픽스와 비공개 display에 남습니다.

```text
관리 창과 같은 owner의 팝업/모달
 → XComposite pixmap / uu-manager-capture.so
 → 창 한정 loopback x11vnc → 로컬 TigerVNC
viewer 입력 → x11vnc → owner·포커스 확인 → 해당 UU 창
```

helper는 관련 팝업을 합성하고 owner와 크기를 다시 확인합니다. override-redirect 메뉴의 grab을 유지하고 포인터 이동으로 포커스를 계속 빼앗지 않습니다. rdp-public 합성 owner는 관리 창을 root에서 제외하고, legacy는 자신이 관리하는 frame만 리디렉션합니다.

viewer 클립보드와 원격 크기 변경은 꺼져 있습니다. session lock은 기존 뷰어를 재사용합니다. 닫으면 sidecar/session/관리 포커스 표시를 회수하고 릴레이 포커스를 복구합니다. UU 창은 mapped로 남으며 layered-window 교체 중 최소화하지 않습니다. Ubuntu가 다른 기기를 조작하는 창은 별도 세션입니다. 전체 root noVNC는 명시적 진단 입구입니다.

## 해상도와 수명주기

캔버스는 비공개 릴레이만 바꿉니다. [화질 가이드](quality-guide.md)의 네 모드에서 저장값과 실제 크기를 확인하고 변경 전 복구를 예약합니다. 실패 시 설정을 되돌리며 고정 캔버스에서는 추적을 끕니다. Wayland 입력은 GNOME RDP compositor를 통하고 adapter는 FreeRDP를 호출합니다. libei를 직접 호출하지 않습니다. 이전 keymap-FD backport는 설정된 GRD 자식 프로세스에만 작용하고 26.04는 수정된 시스템 라이브러리를 사용합니다.

winpr-sspi-shim.dll은 SSPI와 Wine/WinPR 핸들을 정리하며 UU helper는 session token과 event-log API를 보완합니다. Unix 권한을 추가하지 않습니다. systemd 사용자 서비스가 프로세스 그룹을 소유하고 주요 자식 종료 시 전체 릴레이를 재시작하며 UU 재시작 후 입력 hook을 재결합합니다. 종료 시 자체 helper, 전용 Wine, 선택 owner, 캡처/session만 정리하고 이전 GNOME 공유 서비스를 복구합니다.

모니터 없는 Wayland는 임시 GNOME 가상 display를 사용하고 화면 복귀/중지 후 공유 모드를 복구합니다. 터미널은 Windows stdio proxy와 인증 loopback forkpty로 현재 사용자의 shell을 엽니다. [터미널(English)](../../native-ubuntu-terminal.md), [무인 시작(English)](../../unattended-startup.md), [보안](security.md)을 참고하세요.
