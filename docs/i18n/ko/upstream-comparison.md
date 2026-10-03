[English](../../upstream-comparison.md) · [العربية](../ar/upstream-comparison.md) · [Deutsch](../de/upstream-comparison.md) · [Español](../es/upstream-comparison.md) · [Français](../fr/upstream-comparison.md) · [日本語](../ja/upstream-comparison.md) · [한국어](../ko/upstream-comparison.md) · [Русский](../ru/upstream-comparison.md) · [Tiếng Việt](../vi/upstream-comparison.md) · [简体中文](../zh-Hans/upstream-comparison.md) · [繁體中文](../zh-Hant/upstream-comparison.md)

[홈](../../../i18n/README.ko.md)

# Plus의 변경점

![상위 기반, Plus 변경과 설계상 기대](../../images/uu-plus-evolution-en.png)

[편집 가능한 SVG](../../images/uu-plus-evolution-en.svg)

[Lachlan Chen 프로젝트](https://github.com/lachlanchen/uu-remote-ubuntu-bridge)의 [`e2854e2b`](https://github.com/lachlanchen/uu-remote-ubuntu-bridge/commit/e2854e2b50c48ead1246bec027c2e13b5693a10a)를 기준으로 합니다. Wine 분리, GNOME 중계, 입력, 관리/서비스는 원본에서 이어집니다.

## 일상 사용에서 달라지는 점

| 영역 | 원본의 기반 | Plus의 변경 | 사용 방법 |
| --- | --- | --- | --- |
| 호스트 | Ubuntu 24.04와 분리된 libei 백포트 | Ubuntu 26.04/GNOME 50 대응과 libei 선택, 24.04 대상 유지 | 호스트에 맞는 플랫폼·빌드 안내 확인 |
| Windows UU | 기본 4.33.0.8907과 검토된 매니페스트 | 검토된 4.42.0.2770을 기본으로 사용 | UU 버전에 맞는 매니페스트 선택 |
| 화면 크기 | 저장된 해상도와 RDP 크기 변경 | 최대 4K의 네 프리셋, 전체 데스크톱 맞춤과 크기 복원 | 720p, 1080p, 1440p, 4K를 선택하고 현재 화면 확인 |
| 휴대폰 텍스트 | IME 정규화와 Unicode 붙여넣기 | Plus 입력 경로 개선과 공개 FreeRDP 텍스트 경로 | 중국어, 코드, 여러 줄 텍스트 입력 |
| 클립보드 | RDP 클립보드와 Unicode 처리 | SDL 소스로 백그라운드 확인, 소유자 변경, 형식 캐시 수정 | 릴레이가 뒤에 있어도 현재 텍스트 복사·붙여넣기 |
| 관리 | 개별 창 보기와 포커스 복귀 | 관리창·팝업 독립 캡처와 뷰어 재사용 | UU 계정·설정을 열고 데스크톱으로 복귀 |
| 커서 | 선택적인 고정 크기 보호 | 테마 대체와 시작 수정, 기본 꺼짐 유지 | 필요할 때 커서 보호 사용 |
| 데스크톱 동작 | 마우스·키보드 제어 | GNOME 데스크톱·개요 동작 연결 | 제어단 동작을 GNOME 백엔드에 연결 |
| 도구 | 릴레이 의존성과 UU 명령 | 화질/VNC/FreeRDP/Openbox, 개별 글꼴·DPI·인증 | 도구별 설정으로 필요한 창 열기 |
| 빌드·복원 | 고정 nightly SDL/WinPR와 서비스 재연결 | 고정 패치 소스, 실행 파일 확인, 프리셋·뷰어 복원 | 맞는 릴레이를 준비하고 유지보수 시 설정 보존 |

## 구현 분류

- 휴대폰 텍스트: Plus 입력 경로 개선 — [uu_input_broker.c](https://github.com/lachlanchen/uu-remote-ubuntu-bridge/blob/e2854e2b50c48ead1246bec027c2e13b5693a10a/src/uu_input_broker.c) · [uu_input_broker.c](../../../src/uu_input_broker.c) · [freerdp-adapter.c](../../../src/freerdp-adapter.c)
- 클립보드: SDL 소스 패치 — [freerdp-sdl-owner-refresh.patch](../../../vendor/freerdp-sdl-build/freerdp-sdl-owner-refresh.patch)
- 관리: 독립 캡처와 뷰어 처리 — [uu_manager_capture.c](../../../src/uu_manager_capture.c) · [uu-remote-console](../../../scripts/uu-remote-console)
- 도구: 새로운 데스크톱 통합 — [uu-desktop-tool.py](../../../scripts/uu-desktop-tool.py) · [uu-tools-fonts.conf](../../../desktop/uu-tools-fonts.conf)

## 입력 경로

새 RDP 설치는 `rdp-public`을 선택해 브로커 입력을 FreeRDP 공개 API로 전달합니다. 자동 모드의 Unicode는 ASCII도 원문 그대로 붙여넣으며 물리 키는 분리됩니다. 업그레이드는 저장된 경로를 유지합니다. `legacy`는 표현 가능한 문자를 키로, CJK·줄바꿈을 붙여넣기로 보내며 미설정 실행도 `legacy`를 사용합니다.

FPS와 지연을 비교할 때 버전, 원본 해상도, 화질/FPS, 비트레이트, 네트워크와 부하를 고정하고 측정 방법을 기록하세요. [측정 안내](performance-evidence.md)를 참고하세요.
