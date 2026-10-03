[English](../../source-build.md) · [العربية](../ar/source-build.md) · [Deutsch](../de/source-build.md) · [Español](../es/source-build.md) · [Français](../fr/source-build.md) · [日本語](../ja/source-build.md) · [한국어](../ko/source-build.md) · [Русский](../ru/source-build.md) · [Tiếng Việt](../vi/source-build.md) · [简体中文](../zh-Hans/source-build.md) · [繁體中文](../zh-Hant/source-build.md)

[홈](../../../i18n/README.ko.md)

# 릴레이 빌드와 재사용

설치기는 고정 FreeRDP SDL과 Plus 클립보드/크기 패치를 빌드합니다. [레시피](../../../vendor/freerdp-sdl-build/), [소스 잠금](../../../vendor/freerdp-sdl-build/source-lock.json), [제품 프로필](../../../patches/freerdp-sdl-product.json)에 리비전, 파일, 도구와 Windows 런타임 13개를 기록합니다.

<a id="reference-toolchain"></a>

## Ubuntu 26.04 기준 도구 준비

Ubuntu 26.04 amd64에서 [준비 스크립트](../../../scripts/prepare-build-toolchain.py)는 고정된 Ubuntu 공식 패키지 17개를 내려받고 컴파일러·빌드 도구 파일 14개를 `source-lock.json`과 대조합니다. [패키지 목록](../../../patches/reference-build-packages.json)에는 버전, 크기, 해시가 기록되어 있습니다. 스크립트는 다운로드, 개인 디렉터리 압축 해제, 검증을 수행하며 시스템 패키지를 설치하지 않습니다. 저장소 루트에서 실행하세요.

```bash
python3 scripts/prepare-build-toolchain.py \
  --packages-dir "$HOME/.cache/uu-plus/reference-packages" \
  --root "$HOME/.cache/uu-plus/reference-root"
```

`--packages-dir`는 패키지 캐시를 지정하며 `--root`는 새 개인 디렉터리 또는 빈 디렉터리여야 합니다. 캐시만으로 다시 압축을 풀고 도구를 검증하려면 다른 빈 디렉터리에 `--verify-only`를 지정하세요. 네트워크를 사용하지 않습니다.

```bash
python3 scripts/prepare-build-toolchain.py \
  --packages-dir "$HOME/.cache/uu-plus/reference-packages" \
  --root "$HOME/.cache/uu-plus/reference-root-offline" \
  --verify-only
```

스크립트는 로컬 `.deb` 17개 경로가 모두 포함된 `sudo apt install` 명령을 출력합니다. Ubuntu 26.04에서 이 명령을 직접 실행해 기준 도구를 시스템에 설치하세요. 기존 빌드 레시피는 고정된 `/usr` 경로를 읽습니다. 개인 압축 해제 경로는 도구 확인용이며 빌드 환경을 바꾸는 경로가 아닙니다.

이후 일반 설치기를 실행하세요. 나머지 호스트 빌드 의존성, WineHQ와 GNOME 실행 패키지를 준비하고 기존 릴레이 빌드 및 배포 전 검증을 수행합니다. 도구 준비는 기준 파일 14개를 확인하며 전체 소스 빌드와 런타임 파일 13개는 다음 흐름에서 검사합니다.

```bash
./install.sh
./scripts/verify.sh --quick
```

Ubuntu 24.04에서는 아래 재사용 흐름으로 현재 제품 프로필에 맞는 기존 검증 출력을 사용하세요. 위 Ubuntu 26.04 패키지는 26.04 전용입니다.

## 빌드와 캐시

새 소스 빌드에는 `source-lock.json`에 기록된 검토된 컴파일러와 빌드 도구 파일이 바이트 단위로 정확히 일치해야 합니다. 일반 배포판 APT 패키지는 이 도구 체인을 자동으로 제공하지 않습니다.

`./install.sh`는 패키지를 준비하고 교체 전 검증합니다. `build/freerdp`는 현재 프로필/레시피/고정 런타임에 맞는 출처 기록이 있을 때 재사용합니다. 아니면 `scripts/build-winpr.sh`가 새 소스를 두 작업과 900초 제한으로 빌드하고 확인합니다.

검토된 도구가 레시피의 `/usr` 경로에 설치되고 호스트 빌드 의존성이 준비되면 릴레이 캐시를 별도로 빌드할 수도 있습니다.

```bash
UURB_BUILD_DIR=/absolute/path/to/build-work   ./scripts/build-winpr.sh /absolute/path/to/fresh-output
```

새 출력 디렉터리를 쓰세요. 작업 경로에 고유 소스 작업을 만들며 실행 중인 Wine 접두사를 사용하지 않습니다. 검증된 출력 재사용:

저장소 루트에서 기존 출력을 현재 프로필과 대조하세요. 일반 설치기가 호스트 의존성을 준비합니다. 호스트 호환 구성 요소의 빌드 도구, WineHQ와 GNOME 실행 패키지가 이미 설치된 경우에만 `--skip-packages`를 쓰세요. 계정이 구성되어 있으면 `--skip-account-login`도 선택할 수 있습니다.

```bash
python3 scripts/verify-freerdp-runtime.py --mode build /absolute/path/to/verified/output
```

그런 다음 기존 설치 진입점으로 해당 출력을 재사용합니다.

```bash
UURB_FREERDP_PREBUILT_DIR=/absolute/path/to/verified/output   ./install.sh
```

캐시는 현재 레시피/런타임/프로필 출처와 맞아야 합니다. 프로필이 바뀌면 빌드/검증 입구를 다시 실행하세요. 생성 기록/체크섬 편집으로 다른 바이너리를 승인할 수 없습니다. 서비스 시작 전 복사본도 확인합니다.

## 고정 입력과 결과

FreeRDP/WinPR, SDL 3.2.28, SDL_ttf, OpenH264, FreeType, HarfBuzz와 OpenSSL/cJSON/uriparser를 고정합니다. 컴파일 전 패치와 MinGW/컴파일러/도구 해시를 확인하며 변경은 레시피 검토가 필요합니다.

파일/매크로/디버그 접두사 매핑은 경로를 정규화합니다. FreeRDP opaque는 첫 설정부터 OFF이고 호환 DLL은 상대 출력 이름을 사용해 로컬 경로를 넣지 않습니다.

서로 다른 두 소스/출력 루트에서 13개 파일의 바이트가 같았습니다. 첫/반복 CMake 메타데이터도 동일합니다. 미리 빌드한 출력 없이 전체 빌드는 약 700초로 900초 안에 런타임/출처 검증을 통과했습니다. [화질](quality-guide.md), [비용](performance-evidence.md)을 보세요.
