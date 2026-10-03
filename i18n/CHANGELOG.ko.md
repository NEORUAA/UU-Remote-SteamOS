[English](../CHANGELOG.md) · [العربية](CHANGELOG.ar.md) · [Deutsch](CHANGELOG.de.md) · [Español](CHANGELOG.es.md) · [Français](CHANGELOG.fr.md) · [日本語](CHANGELOG.ja.md) · [한국어](CHANGELOG.ko.md) · [Русский](CHANGELOG.ru.md) · [Tiếng Việt](CHANGELOG.vi.md) · [简体中文](CHANGELOG.zh-Hans.md) · [繁體中文](CHANGELOG.zh-Hant.md)

[홈](README.ko.md)

# 변경 기록

브리지 릴리스 태그와 승인된 Windows UU 버전은 별도로 관리합니다.

## Plus 0.1.0 — 2026-10-03

Plus는 MIT 라이선스의 원본 브리지를 기반으로 합니다.

### 추가

- 화면 크기: 최대 4K의 네 프리셋, 전체 데스크톱 맞춤과 크기 복원.
- 휴대폰 텍스트: Plus 입력 경로 개선과 공개 FreeRDP 텍스트 경로.
- 관리: 관리창·팝업 독립 캡처와 뷰어 재사용.
- 커서: 테마 대체와 시작 수정, 기본 꺼짐 유지.
- 데스크톱 동작: GNOME 데스크톱·개요 동작 연결.
- 도구: 화질/VNC/FreeRDP/Openbox, 개별 글꼴·DPI·인증.
- 빌드·복원: 고정 패치 소스, 실행 파일 확인, 프리셋·뷰어 복원.
- 11개 언어의 홈페이지와 핵심 안내, 편집 가능한 아키텍처·이식·비교 그림.

### 수정

- 클립보드: SDL 소스로 백그라운드 확인, 소유자 변경, 형식 캐시 수정.
- 관리창 재열기, UTF-8 제목, 해당 팝업 캡처와 뷰어 종료 후 포커스 복귀.
- 휴대폰 텍스트 전송, 입력 훅 초기화, 부분 입력 처리와 네이티브 터미널 종료 시간 제한.
- 전체 화면 포인터 매핑, 크기·비트레이트 분리, 수동 RDP 연결 보호와 복원 가능한 실행기.

### 호환성

- Ubuntu 24.04 / GNOME 46 · Ubuntu 26.04 / GNOME 50 · x86-64.
- Windows UU: 검토된 4.42.0.2770을 기본으로 사용.

## 계승한 원본 — 미출시

원본의 Unicode 클립보드 처리, 조합 중 편집과 긴 음성 입력, 물리 키보드 배치, 인증 입력, 네트워크·실행 진단, Wine Bluetooth 분리와 무인 세션 복원을 이어받습니다.

## 원본 0.2.0 — 2026-07-18

네트워크 진단과 설치 소스 요약, 호스트 경로를 바꾸지 않는 기본/고정 어댑터 선택. GNOME RDP/libei 서술자 복구, 제한/Keyring 대기/시스템 Python GI를 추가했습니다. 휴대폰 텍스트 간격과 지연 없는 물리 키, 원래 `SendInput` 우선 호출과 브로커/포커스 확인을 제공합니다. 인증 X11/XTEST, 분류 측정, 옛 세션 정리와 네트워크 복구, XRDP/무인 안내를 추가했습니다.

## 원본 0.1.0 — 2026-07-17

첫 지원 Wine/UU, Xvfb, SDL FreeRDP, GNOME 릴레이, 브로커/재주입/감독 서비스. 저장 설정, 바이너리 감사/롤백/RDP 클립보드와 선택 TPM2/GDM을 제공합니다. 휴대폰 입력 정규화, Wayland/Xorg/XRDP 세션 탐색, Wine 이벤트 호환과 옛 접두사 정리를 수정했습니다.

원래 릴리스: [v0.1.0](https://github.com/lachlanchen/uu-remote-ubuntu-bridge/releases/tag/v0.1.0) · [v0.2.0](https://github.com/lachlanchen/uu-remote-ubuntu-bridge/releases/tag/v0.2.0). 전체 원본 변경과 검증 기록: [CHANGELOG.md — e2854e2b](https://github.com/lachlanchen/uu-remote-ubuntu-bridge/blob/e2854e2b/CHANGELOG.md).
