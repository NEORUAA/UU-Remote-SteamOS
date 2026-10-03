[English](../../quality-guide.md) · [العربية](../ar/quality-guide.md) · [Deutsch](../de/quality-guide.md) · [Español](../es/quality-guide.md) · [Français](../fr/quality-guide.md) · [日本語](../ja/quality-guide.md) · [한국어](../ko/quality-guide.md) · [Русский](../ru/quality-guide.md) · [Tiếng Việt](../vi/quality-guide.md) · [简体中文](../zh-Hans/quality-guide.md) · [繁體中文](../zh-Hant/quality-guide.md)

[홈](../../../i18n/README.ko.md)

# 화질, 해상도와 프레임률

Ubuntu에서 캔버스를 고르고 제어하는 PC나 휴대폰에서 전송 화질을 조절합니다. 캔버스 크기, 압축 화질, 요청 FPS, 비트레이트 상한은 별도 설정입니다.

## 캔버스 선택

GNOME 앱 목록의 **UU Remote 画质与分辨率**를 열거나 실행합니다.

```bash
uu-remote quality gui
uu-remote quality list
uu-remote quality status
uu-remote quality apply 2160p
uu-remote quality guide
```

![네 가지 해상도 선택기](../../images/quality-presets.png)

| 설정 | 캔버스 | 용도 |
| --- | --- | --- |
| `720p` | 1280 × 720 | 작은 화면, 제한된 연결 |
| `1080p` | 1920 × 1080 | 일상 작업, 새 설치 기본값 |
| `1440p` | 2560 × 1440 | 4K보다 적은 픽셀로 넓은 공간 |
| `2160p` | 3840 × 2160 | 세밀한 글자와 전체 4K 작업 공간 |

재설치해도 저장한 선택을 유지합니다. 스마트 크기 조절은 원본 데스크톱 전체를 표시하고 같은 기하 관계로 포인터를 매핑합니다. 원본 해상도와 비율이 결과에 영향을 줍니다. 물리 GNOME 화면 해상도는 바꾸지 않으며 캡처가 전체 원본을 처리할 수 있습니다.

선택기는 저장된 시작/RDP 크기와 현재 캔버스를 구분합니다. 저장 크기를 바꾸면 잠시 재연결합니다. 같은 저장 설정을 다시 적용하면 지원 RDP 경로에서 릴레이 재시작 없이 실제 캔버스를 복구하고 크기를 확인합니다. 변경 전 복구 타이머를 시작해 브리지가 준비되지 않으면 이전 설정으로 돌아갑니다. 복구 완료 후 다음 변경을 하세요.

고정 설정은 설치 기본값 `--follow-desktop-resolution off`를 사용합니다. 추적을 켰다면 먼저 끄세요. [설치](../../../i18n/README.ko.md), `./install.sh --help`를 참고하세요. 시험한 4K 원본을 5K로 늘리면 디테일이 늘지 않고 Mac에서 더 흐려져 일반 선택은 4K까지입니다. 명목 60 Hz는 가상 디스플레이 값이며 실제 FPS는 전체 연결에 달려 있습니다.

## 제어 장치 화질

PC: **控制中心 → 画质**, 휴대폰: **操作 → 显示**. True Color도 지원하는 제어 장치에서 선택합니다.

![UU 기본 화질 메뉴](../../images/uu-native-quality-menu.png)

Ubuntu로 Mac을 제어한 예시입니다. 장치와 코덱이 선택지를 결정합니다. 화질은 압축/세부 표현, FPS는 요청 갱신률을 설정합니다. True Color는 색 글자와 경계를 개선할 수 있습니다. 성능 제한이 표시되면 가능한 단계를 고르고 같은 글자와 움직임으로 비교하세요.

NetEase 문서: [FPS / Super Screen](https://uuyc.163.com/help/superscreen.html) · [True Color](https://uuyc.163.com/features/color/) · [UU](https://uuyc.163.com/help/20241216/40221_1200122.html). Wine의 Super Screen/가상 디스플레이 드라이버와 144 FPS는 아직 시험하지 않았습니다. [측정](performance-evidence.md)을 참고하세요.

## 비트레이트 상한

```bash
uu-remote quality bitrate 20
uu-remote quality bitrate 0
```

`20`은 **20 Mbps 상한**, `0`은 해제입니다. 목표 비트레이트, FPS나 캔버스 크기를 바꾸지 않습니다. 해상도 변경은 이 설정을 유지합니다. 낮은 상한은 움직임의 세부 표현을 줄일 수 있습니다.

## 커서와 데스크톱 동작

선택적인 커서 보호는 새 설치에서 꺼져 있습니다. 포인터가 크면:

```bash
./install.sh --skip-packages --skip-account-login --cursor-guard on --cursor-size 24
```

`--cursor-size auto`는 데스크톱 크기를 따르고 고정값은 24–128픽셀입니다. GNOME/앱 설정은 독립입니다. Dock은 GNOME 설정을 사용합니다. Android 데스크톱/모든 창 표시는 GNOME 데스크톱/개요에 연결되며 실제 버튼은 시험 예정입니다.

## 관리 창과 복구

`uu-remote open`은 별도 관리 뷰어를 엽니다. 확대하려면:

```bash
UURB_WINDOW_SCALE=2 ./install.sh --skip-packages --skip-account-login
```

배율은 `1`(기본), `1.5`, `2`, `3`이며 뷰어만 바꿉니다. Wine DPI나 데스크톱 해상도는 유지됩니다. 관리 창 클립보드는 분리되고 일반 복사/붙여넣기는 릴레이를 사용합니다.

```bash
uu-remote status
uu-remote quality status
uu-remote network
uu-remote logs
```

사용자 서비스가 실패한 구성 요소를 재시작하며 잠시 재연결할 수 있습니다. 설정 복구와 런타임 배포 복구는 별도입니다. [문제 해결](troubleshooting.md), [빌드](source-build.md)를 보세요. Wine으로 다른 PC를 제어하는 화질 제한은 별개입니다. 물리 모니터 전환/가상 출력은 [Ubuntu 26.04](ubuntu-26.04-port.md)에서 추가 시험이 필요합니다. 휴대폰 → ToDesk → Mac → UU는 중복 입력이 남아 있고 직접 연결은 정상입니다.
