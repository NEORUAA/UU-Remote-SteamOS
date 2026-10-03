[English](../../adaptive-keyboard-relays.md) · [العربية](../ar/adaptive-keyboard-relays.md) · [Deutsch](../de/adaptive-keyboard-relays.md) · [Español](../es/adaptive-keyboard-relays.md) · [Français](../fr/adaptive-keyboard-relays.md) · [日本語](../ja/adaptive-keyboard-relays.md) · [한국어](../ko/adaptive-keyboard-relays.md) · [Русский](../ru/adaptive-keyboard-relays.md) · [Tiếng Việt](../vi/adaptive-keyboard-relays.md) · [简体中文](../zh-Hans/adaptive-keyboard-relays.md) · [繁體中文](../zh-Hant/adaptive-keyboard-relays.md)

[한국어 홈으로 돌아가기](../../../i18n/README.ko.md)

# 입력에 맞춘 키보드 릴레이

하나의 Ubuntu X11에 여러 프로토콜이 들어옵니다. 모두 하드웨어 scancode로 처리하면 기호의 의미를 잃습니다.

| 경로 | 입력 정보 | 처리 |
| --- | --- | --- |
| XRDP | 키보드 메타데이터와 scancode | 클라이언트 배열 |
| RealVNC/x11vnc | X11/RFB keysym | modtweak, XKB, 임시 keysym |
| UU 물리 키보드 | Windows 키 이벤트 | 선택한 rdp/x11 |
| UU 휴대폰 IME | Unicode 확정 | 물리 키와 별개 |

keysym/Unicode 의미를 먼저 유지하고 물리 키만 배열을 따릅니다. 최근 클라이언트를 따라 전역 setxkbmap 루프를 돌리지 않습니다. ~/.xsessionrc의 상시 -layout jp는 XRDP 보고 배열을 덮습니다. 일본어 Mac용 수정은 명시적 명령으로 두고 매 로그인마다 실행하지 않습니다. IBus, 의미적 문자와 터미널은 물리 XKB에 의존하지 않습니다.

직접 X11은 표현 가능한 문자를 키 조합으로 바꾸고 중국어·개행·tab·emoji는 CLIPBOARD/PRIMARY 동기화와 한 번의 붙여넣기를 사용합니다. 구술 개행을 terminal Enter로 바꾸지 않습니다. rdp-public Unicode는 원문 그대로입니다. [구조](architecture.md), [문자와 클립보드(English)](../../semantic-text-and-clipboard.md)를 참고하세요.

## 전용 VNC viewer

대상 화면을 UU 캔버스로 가져오는 전체화면 viewer 기본값입니다.

```text
UURB_VNC_GRAB_KEYBOARD=on
```

-GrabKeyboard=1은 중간 X 데스크톱이 Shift/Ctrl/Alt/Super를 소비하는 것을 막습니다. 대표 증상은 (가 8, ?가 /, @가 2가 되거나 Ctrl 단축키 실패입니다. loopback x11vnc 옵션은 다음과 같습니다.

```text
-repeat -nobell -modtweak -xkb -add_keysyms
```

modtweak은 대상 배열의 조합 키를 재구성하고 -xkb는 전체 XKB를 조회하며 -add_keysyms는 빠진 keysym을 추가합니다. IPv4 loopback만 엽니다. 전용 중계가 아닌 창에서는 grab을 끌 수 있습니다.

```bash
./install.sh --skip-packages --skip-account-login \
  --vnc-grab-keyboard off
```

## 비교와 검사

```bash
./scripts/test-vnc-keyboard-relay.sh
```

격리 RFB/Xvfb에서 일본어 XKB의 Shift 기호 21개와 你好를 검사합니다.

```text
vnc-symbols=23/23 order=exact target-layout=jp
isolated VNC keyboard acceptance passed
```

실제 컨트롤러는 임시 텍스트 칸에서 숫자·문장부호·()·Ctrl+A/C/V·Enter·Backspace와 IME 중국어/일본어를 각각 확인합니다. 비밀번호 칸은 사용하지 않습니다.

데스크톱 XKB, XRDP와 GNOME 로그인을 바꾸지 않습니다. UU 물리 프로토콜은 연결별 배열 식별이 없으므로 직접 X11은 대상 배열을 씁니다. XRDP/RFB는 메타데이터/keysym, 휴대폰은 Unicode입니다. 소스 배열이 없으면 Shift+7이 &인지 '인지 추측할 수 없습니다. [입력 트랙(English)](../../release-tracks.md) 또는 클라이언트에서 명확히 선택합니다.
