<div align="center">

[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)

<a href="README.ko.md"><img src="../docs/images/uu-plus-logo.png" alt="UU Remote Ubuntu Plus" width="140"></a>

# UU Remote Ubuntu Plus

**아이디어가 떠오를 때 바로 연결하세요. 개발 환경은 Ubuntu에 그대로.**

편집기, 터미널, 앱 세션은 Ubuntu에 그대로 두세요. 휴대폰, Mac, Windows에서 연결해 자유롭게 Vibe Coding을 즐기고, 화면을 바꿔 이어서 코딩하세요.

[![Ubuntu 24.04 / 26.04](https://img.shields.io/badge/Ubuntu-24.04%20%7C%2026.04-E95420?logo=ubuntu&logoColor=white)](../docs/i18n/ko/ubuntu-26.04-port.md)
[![GNOME 46 / 50](https://img.shields.io/badge/GNOME-46%20%7C%2050-4A86CF?logo=gnome&logoColor=white)](../docs/i18n/ko/architecture.md)
[![UU Remote 4.42](https://img.shields.io/badge/UU_Remote-4.42.0.2770-00A870)](../patches/uu-remote-4.42.0.2770.json)
[![MIT](https://img.shields.io/badge/License-MIT-2F81F7)](../LICENSE)

<img src="../docs/images/vibe-coding-cross-device-en.png" alt="UU Remote Ubuntu Plus" width="1120">

</div>

Plus는 NetEase UU Remote를 로그인된 Ubuntu GNOME 세션에 연결합니다.
공식 Windows UU 앱은 전용 Wine 환경에서 실행되며, 로컬 릴레이가 실제 데스크톱을
보여 줍니다. 계정과 UU 설정은 별도 관리 창에서 조작합니다.
로컬 사용과 원격 접속 모두 같은 앱, 파일, 데스크톱 세션을 유지합니다.

이 프로젝트는 **[Lachlan Chen의 UU Remote Ubuntu Bridge](https://github.com/lachlanchen/uu-remote-ubuntu-bridge)**를 바탕으로 합니다.
Plus는 최신 Ubuntu와 UU 지원, 네 가지 화면 크기, 입력과 클립보드 수정,
관리 및 데스크톱 조작 개선을 추가합니다.

설치기는 x86-64 Ubuntu 24.04 / GNOME 46과 Ubuntu 26.04 / GNOME 50을 대상으로 하며 UU 4.42.0.2770을 사용합니다. 새 설치는 1080p를 선택하고 선택적 커서 보호는 꺼 둡니다.

11개 언어의 홈과 기술 가이드에서 같은 언어로 계속 읽을 수 있습니다. 영어가 기준 원문입니다.

## 설치부터 원격 사용까지

1. Ubuntu 데스크톱에 브리지를 설치합니다.
2. `uu-remote open`을 실행하고 관리 창에서 UU에 로그인합니다.
3. 휴대폰, Mac, Windows의 UU로 이 Ubuntu에 연결합니다.
4. 화면 크기를 선택하고 평소의 데스크톱 앱을 사용합니다.

## 기능과 개선점

원본 프로젝트는 데스크톱 릴레이, 키보드와 마우스, 휴대폰 IME 처리, 서비스 복구를 제공합니다. Plus는 이 기반에 최신 환경 지원, 보기 쉬운 화질 설정과 일상 사용 개선을 더합니다.

| 일상 사용 | Plus의 개선 |
| --- | --- |
| 최신 Ubuntu와 UU | Ubuntu 26.04 / GNOME 50과 UU 4.42를 지원하며 Ubuntu 24.04 설치 경로도 유지합니다. |
| 알맞은 화면 선택 | 720p, 1080p, 1440p, 4K를 그래픽 선택기로 전환합니다. 전체 데스크톱을 화면에 맞추고 저장된 설정을 복구합니다. |
| 중국어, 코드, 복사·붙여넣기 | 휴대폰 텍스트 전송과 클립보드 갱신을 수정합니다. 새 텍스트가 데스크톱에 전달되고 코드와 여러 줄 내용이 유지됩니다. |
| 연결을 유지하며 설정 열기 | UU 관리 화면과 팝업을 별도로 캡처합니다. 뷰어를 닫으면 입력 포커스가 릴레이로 돌아갑니다. |
| 편리한 로컬 도구 | 화질, VNC, FreeRDP, Openbox 도구와 글꼴·DPI·시작 개선을 제공합니다. |
| 설치와 유지관리 | 고정된 소스에서 릴레이를 빌드하고 설치 전 구성 요소를 확인합니다. 실패한 화면 변경을 복구하고 제거 전 변경을 미리 볼 수 있습니다. |

변경 내용과 버전 배경은 [원본 비교](../docs/i18n/ko/upstream-comparison.md)에 있습니다.

<img src="../docs/images/experience-refinements-en.png" alt="사용 경험과 측정" width="1120">

[사용 경험과 측정](../docs/i18n/ko/performance-evidence.md)

## 빠른 설치

GNOME에 로그인한 x86-64 Ubuntu에서 먼저 프로젝트를 받으세요.

```bash
git clone https://github.com/llmir/uu-remote-ubuntu-plus.git
cd uu-remote-ubuntu-plus
```

설치하려면 검토된 도구 체인으로 릴레이를 빌드하거나 제품 프로필과 일치하는 검증된 결과물이 필요합니다. 릴레이 바이너리는 포함되어 있지 않습니다. Ubuntu 26.04는 기준 도구 준비 절차를 제공하며 Ubuntu 24.04는 검증된 결과물을 재사용합니다. [도구 체인 준비와 릴레이 재사용](../docs/i18n/ko/source-build.md#reference-toolchain)

도구 또는 일치하는 결과물이 준비되면 일반 설치기를 실행하세요.

```bash
./install.sh
./scripts/verify.sh --quick
uu-remote open
```

설치기는 의존성을 준비하고 구성 요소를 빌드한 뒤 GNOME Remote Desktop과
사용자 서비스를 설정합니다. 릴레이 암호를 GNOME Keyring에 저장하고 UU 로그인 창을 엽니다.
재설치하면 저장된 설정과 계정 상태를 유지합니다. 처음부터 4K를 사용하려면:

```bash
./install.sh --resolution 3840x2160
```

환경과 재현 절차는 [호환성 보고 양식](https://github.com/llmir/uu-remote-ubuntu-plus/issues/new?template=compatibility.yml)으로 알려 주세요.

첫 설치에서는 의존 소스를 내려받고 컴파일할 수 있습니다.
[소스 빌드](../docs/i18n/ko/source-build.md)와 [보안](../docs/i18n/ko/security.md)을 참고하세요.
NetEase 공식 [uuyc.163.com](https://uuyc.163.com/)에서 Windows UU 클라이언트를 받습니다. 브리지는 전용 Wine 환경에서 실행합니다. UU는 원래 라이선스를 유지합니다.

## 기술 개요

<img src="../docs/images/architecture-premium-v2-en.png" alt="Ubuntu 화면, 입력, 로컬 UU 관리 경로." width="1120">

Ubuntu 화면은 GNOME RDP를 거쳐 SDL / FreeRDP 릴레이로 전달되고 UU를 통해 제어 단말에 도달합니다. 키보드와 마우스는 입력 브리지를 통해 같은 세션으로 돌아갑니다. UU 계정과 설정은 별도의 로컬 관리 창에서 다룹니다.

`uu-remote open`으로 관리 창을 엽니다. 뷰어를 닫아도 브리지는 계속 실행됩니다. 선택적 `uu-remote console`은 로컬 브라우저 화면을 제공합니다. 모듈과 입력 경로는 [아키텍처](../docs/i18n/ko/architecture.md)를 참고하세요.

## 해상도와 화질

<img src="../docs/images/quality-controls-cartoon-v2-en.png" alt="Ubuntu canvas and UU controller quality controls" width="1120">

GNOME의 **UU Remote 画质与分辨率**를 열거나 다음을 실행합니다.

```bash
uu-remote quality gui
```

전체 원본 데스크톱이 화면 안에 맞춰지고 물리 모니터 해상도는 유지됩니다.
다른 설정을 적용하면 잠시 재접속하며, 실패하면 이전 구성을 복원합니다.

```bash
uu-remote quality list
uu-remote quality apply 2160p
uu-remote quality status
uu-remote quality guide
```

인코딩 화질, FPS, True Color는 **UU 제어 단말**에서 설정합니다.
컴퓨터는 **제어 센터 → 화질**, 휴대폰은 **조작 → 디스플레이**입니다.

비트레이트 상한은 별도로 설정합니다.

```bash
uu-remote quality bitrate 20
uu-remote quality bitrate 0
```

`20`은 20 Mbps 상한을 요청하고 `0`은 상한을 없앱니다.
화면 크기, 인코딩 화질, 요청 FPS, 비트레이트는 각각의 설정입니다.
[화질 안내](../docs/i18n/ko/quality-guide.md)를 참고하세요.

## 입력과 커서

휴대폰 IME 텍스트, 코드 조각과 여러 줄 텍스트는 텍스트 경로로 Ubuntu에 전달됩니다. 물리 키와 단축키는 키 이벤트를 유지합니다. Plus는 텍스트 전송과 클립보드 갱신을 수정해 일상 입력과 복사·붙여넣기를 개선합니다. 입력 모드는 [키보드 릴레이](../docs/i18n/ko/adaptive-keyboard-relays.md)에 설명되어 있습니다.

선택적 커서 보호는 원본 프로젝트의 기능입니다. Plus는 커서 리소스와 처리를 개선합니다.
활성화하려면:

```bash
./install.sh --skip-packages --skip-account-login \
  --cursor-guard on --cursor-size auto
```

`auto`는 데스크톱 커서 크기를 따르고, `24` 같은 고정값은 대체 커서 크기를 정합니다.
`--cursor-guard off`로 끌 수 있습니다. 재설치 때 UU가 잠시 재접속합니다.

## 일상 사용과 유지관리

```bash
uu-remote status
uu-remote network
uu-remote logs
uu-remote restart
uu-remote stop
```

관리 창은 `uu-remote open`, 로그인과 계정 복구는 `uu-remote login`을 사용합니다.
재시작, 로그인, 재설치는 원격 연결을 잠시 끊습니다.

로컬 수정 사항을 저장하고 소스를 업데이트한 뒤 재설치합니다.

```bash
./install.sh --skip-packages --skip-account-login
./scripts/verify.sh --quick
```

실행 코드의 변경은 재설치 후 적용됩니다.
`uu-remote upgrade`는 [업그레이드](../docs/i18n/ko/reusable-upgrade.md),
선택적 자동 유지관리는 [자동 업데이트](../docs/i18n/ko/automatic-updates.md)를 참고하세요.

UU 계정 상태를 유지하면서 제거하려면:

```bash
./uninstall.sh --dry-run
./uninstall.sh
```

`./uninstall.sh --purge`는 전용 Wine prefix, 릴레이 자격 정보, GNOME RDP 활성화도 제거합니다.

## Ubuntu를 넘어 다른 Linux로

현재 설치기는 x86-64 Ubuntu 24.04와 26.04를 대상으로 합니다. [Linux 이식 안내](../docs/i18n/ko/porting.md)는 향후 이식을 세 계층으로 나눕니다.

- UU 호환성, 릴레이, 입력 코어를 재사용합니다.
- 배포판 패키지, Wine 경로, 서비스 통합을 조정합니다.
- 데스크톱별 캡처, 입력, 화면 모드, 동작 백엔드를 연결합니다.

다른 GNOME 배포판은 기존 통합을 더 많이 재사용할 수 있습니다. KDE와 Xfce에는 자체 데스크톱 백엔드가 필요합니다.

## 문서와 기여

- [화질](../docs/i18n/ko/quality-guide.md), [빌드](../docs/i18n/ko/source-build.md), [Ubuntu 26.04](../docs/i18n/ko/ubuntu-26.04-port.md)
- [아키텍처](../docs/i18n/ko/architecture.md), [보안](../docs/i18n/ko/security.md), [문제 해결](../docs/i18n/ko/troubleshooting.md)
- [원본 비교](../docs/i18n/ko/upstream-comparison.md), [측정](../docs/i18n/ko/performance-evidence.md)
- [변경 기록](CHANGELOG.ko.md), [기여 안내](CONTRIBUTING.ko.md)

버전, 설정, 동작을 재현할 수 있는 단계를 설명하세요.

## 프로젝트 지원

**커피 한 잔으로 응원해 주세요 ☕**

UU와 Ubuntu의 업데이트에 맞춰 Plus도 계속 다듬겠습니다. 후원은 새 버전 테스트, 개발 도구와 토큰 비용에 보탬이 되어 텍스트 입력, 복사·붙여넣기, 화질을 개선하는 데 쓰입니다.

| PayPal | Alipay · CNY | AlipayHK · HKD | WeChat · CNY | WeChat · HKD |
| :---: | :---: | :---: | :---: | :---: |
| <a href="https://paypal.me/mirmirlin"><img src="../docs/images/support-paypal-en.png" alt="PayPal" width="160"></a> | <a href="../docs/images/support/alipay-cny.jpg"><img src="../docs/images/support-alipay-cny-en.png" alt="Alipay · CNY" width="160"></a> | <a href="../docs/images/support/alipay-hkd.png"><img src="../docs/images/support-alipay-hkd-en.png" alt="AlipayHK · HKD" width="160"></a> | <a href="../docs/images/support/wechat-zh.png"><img src="../docs/images/support-wechat-zh-en.png" alt="WeChat · CNY" width="160"></a> | <a href="../docs/images/support/wechat-en.png"><img src="../docs/images/support-wechat-en-en.png" alt="WeChat · HKD" width="160"></a> |

<details>
<summary>Alipay와 WeChat 결제 코드</summary>

<p><a href="../docs/i18n/ko/support.md#alipay-cny">Alipay CNY</a><br><a href="../docs/images/support/alipay-cny.jpg"><img src="../docs/images/support/alipay-cny.jpg" alt="Alipay CNY" width="240"></a></p>

<p><a href="../docs/i18n/ko/support.md#alipay-hkd">AlipayHK HKD</a><br><a href="../docs/images/support/alipay-hkd.png"><img src="../docs/images/support/alipay-hkd.png" alt="AlipayHK HKD" width="240"></a></p>

<p><a href="../docs/i18n/ko/support.md#wechat-zh">WeChat · CNY</a><br><a href="../docs/images/support/wechat-zh.png"><img src="../docs/images/support/wechat-zh.png" alt="WeChat · CNY" width="240"></a></p>

<p><a href="../docs/i18n/ko/support.md#wechat-en">WeChat · HKD</a><br><a href="../docs/images/support/wechat-en.png"><img src="../docs/images/support/wechat-en.png" alt="WeChat · HKD" width="240"></a></p>

</details>

재현 절차가 있는 버그 보고, Linux 이식 경험, 풀 리퀘스트도 환영합니다. 다음 버전을 함께 더 편하게 만들어 주세요.

[UU Remote Ubuntu Plus 후원](../docs/i18n/ko/support.md)

## 감사와 라이선스

**[Lachlan Chen의 UU Remote Ubuntu Bridge](https://github.com/lachlanchen/uu-remote-ubuntu-bridge)**를 기반으로 합니다.
원래 저작권 고지와 [MIT 라이선스](../LICENSE)를 유지합니다.
UU와 의존 소프트웨어는 각자의 라이선스와 상표를 유지합니다.
독립적인 커뮤니티 프로젝트입니다.

결제 브랜드 아이콘: [Simple Icons](https://simpleicons.org/)(CC0). 각 상표의 권리는 해당 소유자에게 있습니다.
