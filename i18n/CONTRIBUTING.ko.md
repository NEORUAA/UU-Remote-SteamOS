[English](../CONTRIBUTING.md) · [العربية](CONTRIBUTING.ar.md) · [Deutsch](CONTRIBUTING.de.md) · [Español](CONTRIBUTING.es.md) · [Français](CONTRIBUTING.fr.md) · [日本語](CONTRIBUTING.ja.md) · [한국어](CONTRIBUTING.ko.md) · [Русский](CONTRIBUTING.ru.md) · [Tiếng Việt](CONTRIBUTING.vi.md) · [简体中文](CONTRIBUTING.zh-Hans.md) · [繁體中文](CONTRIBUTING.zh-Hant.md)

[한국어 · UU Remote Ubuntu Plus](README.ko.md)

# UU Remote Ubuntu Plus에 기여하기

문제 보고, 번역, 문서와 코드를 환영합니다. [Lachlan Chen의 브리지](https://github.com/lachlanchen/uu-remote-ubuntu-bridge)의 저작권과 MIT 라이선스를 보존합니다.

## 문제와 경로 설명

Ubuntu/GNOME/Wine/UU, 캔버스, 입력 경로와 재현 절차를 적습니다. Ubuntu 호스트, 로컬 관리, Ubuntu 컨트롤러를 구분합니다. 작은 변경과 측정 방법을 제시하고 [호환성 보고 양식](https://github.com/llmir/uu-remote-ubuntu-plus/issues/new?template=compatibility.yml)을 사용합니다.

## 개발 환경

Ubuntu와 시스템 Python을 사용합니다. 아래 패키지는 빌드·격리 테스트용이며 install.sh가 런타임을 관리합니다. WINEGCC/MINGW_CC/HOST_CC로 컴파일러를 고르고 임시 Wine/Xvfb를 사용합니다.

```bash
sudo apt-get update
sudo apt-get install --no-install-recommends \
  build-essential binutils gcc-mingw-w64-x86-64-win32 \
  wine wine64 wine64-tools xvfb x11-utils x11-xserver-utils xclip xcompmgr
```

## 소스 검사

변경한 shell에 bash -n을 실행하고 아래 검사를 합니다. 엄격한 C 경고를 유지합니다. Wine/Xvfb/systemd가 필요한 테스트의 실행과 생략을 기록하고 UURB_TEST_SYSTEMD=1은 사용 가능한 사용자 버스에서만 설정합니다.

```bash
python3 -m compileall -q scripts tests
python3 -m unittest discover -s tests -v
./scripts/build-compat.sh
git diff --check
```

## 문서와 그림

기존 문서 테스트를 실행합니다. 영어/중국어 SVG는 같은 배치이며 Node/Sharp 명령은 재렌더링할 때만 사용합니다. 전체 이미지와 메타데이터를 확인하고 결제 코드 원본을 유지합니다.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_documentation.py -q
npm install --no-save --package-lock=false sharp
node scripts/render-doc-graphics.cjs
```

## 설치 검증

허가된 호스트에서 설치하고 잠깐의 끊김에 대비합니다. 전체 검증은 270초 안정성 검사이며 화면·입력·재연결은 실제 컨트롤러로 확인합니다. UU 전용 프리픽스만 종료합니다.

```bash
./install.sh --skip-packages --skip-account-login
./scripts/verify.sh --quick
./scripts/verify.sh
./uninstall.sh --dry-run
```

## 새 UU 버전

승인된 매니페스트, 전체 SHA-256, 같은 길이 패치 설명이 필요합니다. 원복·시작·입력·삭제 결과를 남기고 전용 바이너리나 개인 로그는 공개하지 않습니다. [상위 유지관리(English)](../docs/upstream-maintenance.md)를 봅니다.

## 공개 파일 정리

파일 목록과 스테이징 차이를 확인합니다. 빌드, 프리픽스, 캐시, .omc 상태, 자격 정보, 기기 ID와 입력 내용을 제외합니다. 인증·TLS·매니페스트 검증과 되돌릴 수 있는 삭제를 유지합니다.

```bash
git status --short
git diff --cached
```

## 검토 요청

문제, 결과와 실제 검사를 적고 독립 검토를 요청합니다. 설정 FPS는 실측이 아닙니다. [화질](../docs/i18n/ko/quality-guide.md), [Ubuntu](../docs/i18n/ko/ubuntu-26.04-port.md), [보안](../docs/i18n/ko/security.md)을 읽고 MIT와 저작권을 유지합니다.
