[English](../../ubuntu-26.04-port.md) · [العربية](../ar/ubuntu-26.04-port.md) · [Deutsch](../de/ubuntu-26.04-port.md) · [Español](../es/ubuntu-26.04-port.md) · [Français](../fr/ubuntu-26.04-port.md) · [日本語](../ja/ubuntu-26.04-port.md) · [한국어](../ko/ubuntu-26.04-port.md) · [Русский](../ru/ubuntu-26.04-port.md) · [Tiếng Việt](../vi/ubuntu-26.04-port.md) · [简体中文](../zh-Hans/ubuntu-26.04-port.md) · [繁體中文](../zh-Hant/ubuntu-26.04-port.md)

[홈](../../../i18n/README.ko.md)

# Ubuntu 26.04와 GNOME 50

Plus는 [Lachlan Chen의 MIT 브리지](https://github.com/lachlanchen/uu-remote-ubuntu-bridge)를 x86-64 Ubuntu 26.04/GNOME 50으로 확장하고24.04/GNOME 46을 유지합니다. Wine 분리, 감사된 UU 목록, 입력 브로커, 릴레이와 서비스가 기반입니다.

릴레이 설치에는 정확히 일치하는 검토된 도구 체인 또는 기존 검증 출력이 필요합니다. 일반 APT 패키지는 해당 도구 체인을 자동으로 제공하지 않습니다. [빌드 전제 조건과 캐시 재사용](source-build.md)을 참고하세요.

| 구성 | 원본 | Plus |
| --- | --- | --- |
| Ubuntu |24.04|24.04/26.04, 다른 버전은 `UURB_ALLOW_UNVALIDATED_UBUNTU=1`|
| Windows UU |4.33.0.8907|승인4.42.0.2770, 기존 목록 선택 가능|
| libei |분리1.2.1 백포트|수정된 시스템 라이브러리, 아니면 백포트|
| 릴레이 |고정nightly SDL/WinPR|패치된 고정 소스, [빌드](source-build.md)|
| CI |24.04|24.04/26.04 대상, 실행별 결과 확인|

관찰 환경은 GRD 50.2/libei 1.5.0입니다. 오래된 라이브러리는 `ee27dd5c92e4e9496a36ca2d4112049fe02d2269`를 쓸 수 있습니다. `UURB_LIBEI_MODE=system|backport`가 선택을 저장하고 `verify.sh`가 로드된 라이브러리를 확인합니다. WineHQ stable을 사용합니다.

## 동작

네 크기, 전체 표시와 포인터 매핑. 새 설치1080p, 업그레이드 설정 유지. 저장 크기는 복구 보호로 재연결하며 재적용하면 실제 캔버스를 복원합니다. 사용자가 정상 재연결과 기본 메뉴 최대4K를 확인했습니다. 새 RDP는 `rdp-public`, 업그레이드는 경로 유지. Unicode/물리 키는 별도입니다. 관리/팝업은 따로 캡처하고 닫으면 릴레이 포커스가 돌아오며 관리 창은 매핑 상태를 유지합니다. 데스크톱 클립보드 활성, 관리 창 분리.

| 기능 | 결과 |
| --- | --- |
| 휴대폰/Mac 직접 중국어 |이전 설치 통합 과정에서 사용자 확인|
| 일반 텍스트 복사 |사용자 정상 확인|
| Mac UU 업데이트 |재연결/중국어/붙여넣기 정상,4K 비슷함|
| 관리 겹침/포커스 |해결 보고, 일부 확인 정상|
| Android |후단 양방향 정상, 실제 버튼 예정|
| 커서 |테마/부분 정상, 전체 모양 예정|
| 물리/가상 출력 |이 호스트에서 예정|
| 휴대폰→ToDesk→Mac→UU |소문자`a` 반복 미해결|

VNC/FreeRDP/Openbox 도구는 개별 CJK 글꼴/DPI/자격 증명을 사용합니다. Dock은 GNOME 설정입니다. 외부 제어 화질/물리 해상도는 수신 캔버스와 다릅니다. [화질](quality-guide.md), [구조](architecture.md), [비교](upstream-comparison.md).

## 업데이트

Plus를 `origin`으로 유지합니다.

```bash
git remote add upstream https://github.com/lachlanchen/uu-remote-ubuntu-bridge.git
git fetch upstream
```

개발 브랜치에서 원본 변화를 검토하고 런타임 변경 후 실행합니다.

```bash
./install.sh --skip-packages --skip-account-login
./scripts/verify.sh --quick
```

설치는 잠시 연결을 끊으며 설치 갱신 전 소스 요약이 변경을 표시합니다. [재사용 업데이트](reusable-upgrade.md)는 런타임 복구, 설정 롤백은 캔버스를 다룹니다. 알 수 없는 UU 해시는 자동 패치를 막습니다. 새 버전은 의미 검토/승인 목록/런타임 확인이 필요합니다. [유지보수](../../upstream-maintenance.md). MIT 소스와 목록만 배포하며 UU/의존성은 자체 라이선스를 유지합니다.
