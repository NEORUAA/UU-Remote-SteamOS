[English](../../porting.md) · [العربية](../ar/porting.md) · [Deutsch](../de/porting.md) · [Español](../es/porting.md) · [Français](../fr/porting.md) · [日本語](../ja/porting.md) · [한국어](../ko/porting.md) · [Русский](../ru/porting.md) · [Tiếng Việt](../vi/porting.md) · [简体中文](../zh-Hans/porting.md) · [繁體中文](../zh-Hant/porting.md)

[홈](../../../i18n/README.ko.md)

# 다른 Linux 데스크톱으로 이식

x86-64 GNOME은 RDP를 유지하고 설치를 바꿀 수 있는 가까운 출발점입니다. KDE/Xfce는 별도 데스크톱 어댑터가 필요합니다. 현재 Ubuntu 24.04/26.04를 설치하며 나머지는 이식 대상입니다.

릴레이 설치에는 정확히 일치하는 검토된 도구 체인 또는 기존 검증 출력이 필요합니다. 일반 APT 패키지는 해당 도구 체인을 자동으로 제공하지 않습니다. [빌드 전제 조건과 캐시 재사용](source-build.md)을 참고하세요.

![이식의 세 계층](../../images/uu-plus-porting.png)

[편집 가능한 SVG](../../images/uu-plus-porting.svg)

| 계층 | 재사용 | 변경/소스 |
| --- | --- | --- |
| 핵심 |Wine/UU 분리, 목록, SDL/FreeRDP, 브로커/플러그인, 캔버스/관리|경계 유지, Unicode/키 분리; [입력](../../../src/uu_input_broker.c), [RDP](../../../src/freerdp-adapter.c), [플러그인](../../../src/plugin.c), [캡처](../../../src/uu_manager_capture.c)|
| 배포판 |레시피/검증/설정/서비스|패키지/경로/라이브러리/실행기; [설치](../../../install.sh), [빌드](../../../scripts/build-winpr.sh), [검증](../../../scripts/verify-freerdp-runtime.py), [서비스](../../../systemd/uu-remote-bridge.service)|
| 데스크톱 |RDP 이벤트/텍스트/동작|세션/캡처입력/클립보드/원본기하/동작; [시작](../../../scripts/uu-remote-bridge), [텍스트](../../../src/uu_x11_input.c), [모드](../../../scripts/uu-display-modes.py)|

FreeRDP 공개 API는 기존 연결을 사용하며 서버는 UU Windows 후크와 독립적으로 바꿀 수 있습니다. Unicode는 원본 클립보드와 붙여넣기가 필요하며 현재 X11/Xwayland입니다. 관리 창은 Wine 전용 X11에 남습니다. [구조](architecture.md).

| 플랫폼 | 재사용과 작업 |
| --- | --- |
| Ubuntu 24.04/GNOME 46 |기존 설치/후단, 선택libei 백포트|
| Ubuntu 26.04/GNOME 50 |Plus 통합, 시스템libei, UU 4.42|
| Debian/GNOME |핵심/캔버스/RDP; Debian 패키지/Wine, 사전검사/데몬/라이브러리; [APT/dpkg](https://www.debian.org/doc/manuals/debian-reference/ch02.en.html)|
| Fedora/GNOME |핵심/후단; RPM/DNF/경로/권한; [GRD](https://packages.fedoraproject.org/pkgs/gnome-remote-desktop/gnome-remote-desktop/)|
| Arch/GNOME |핵심/후단; pacman/경로/고정도구/GNOME libei 갱신; [GRD](https://archlinux.org/packages/extra/x86_64/gnome-remote-desktop/)|
| KDE |핵심/캔버스/관리; 세션/캡처입력/출력/클립보드/동작; [KRDP](https://github.com/KDE/krdp)는 인증/코덱/텍스트 통합 필요|
| Xfce/X11 |핵심/캔버스/관리/X11; 세션/원본기하/동작; VNC `legacy` 출발점|

패키지 관리자 변경은 설치만 해결합니다. 캡처, 입력, 원본기하, 데스크톱 동작을 모두 연결해야 합니다.

| 인터페이스 | 현재 구현과 변경 |
| --- | --- |
| 아키텍처 |`x86_64`, AMD64 PE; 다른 호스트는 AMD64 실행/검증|
| 패키지 |Ubuntu, `apt-get`, `dpkg`, i386, WineHQ Ubuntu; 대상 매핑|
| Wine |`/opt/wine-stable/bin/wine`, `wineserver`, `winepath`; 시작/정리에서 일관된 경로|
| 빌드 |MinGW/CMake/Meson/Ninja/고정파일; 유지 또는 새 프로필; [설명](source-build.md)|
| 세션 |`gnome-shell`, D-Bus, `/usr/libexec/gnome-remote-desktop-daemon`; 경로 탐색/대체|
| 인증 |Keyring, `secret-tool`, `grdctl`, `org.gnome.desktop.remote-desktop.rdp`; UU 계정과 별도TLS/서비스|
| 출력 |`org.gnome.Mutter.DisplayConfig`, 가상모니터; 대상합성기, X11 XRandR|
| 텍스트 |`uu-x11-input`/`xclip`, `CLIPBOARD`/`PRIMARY`; 올바른display, Wayland 전용API|
| 동작 |`_NET_SHOWING_DESKTOP`, `org.gnome.Shell.OverviewActive`; 대상WM/상태|
| 서비스 |`systemctl --user`, 그래픽D-Bus; 대상세션/init|
| 도구 |`/usr/bin/xfreerdp`, `xtigervncviewer`, `obconf`, `zenity`; 경로/글꼴/DPI/대화형인증/릴레이보호|

전용 Wine/Xvfb 캔버스와 물리/가상출력은 다릅니다. 네 설정을 유지하고 KDE/Xfce의 Mutter 원본 로직을 교체합니다.

1. x86-64 배포판/세션을 고르고 OS/데스크톱/Wine/UU를 기록합니다.
2. 패키지/경로/라이브러리/서비스/실행기를 바꾸고 릴레이를 확인합니다.
3. 캡처입력/bus/display/인증/기하/클립보드를 연결합니다.
4. 실제 제어 장치로 이동/클릭/휠/드래그/단축키/Unicode/붙여넣기/재연결/관리팝업을 확인합니다.
5. 네 크기, 저장복원, 실패롤백, 프로세스정리, 데스크톱/개요를 확인합니다.

UU 바이너리/계정 없이 매핑/경로/버전/결과를 기여하세요. [비교](upstream-comparison.md), [화질](quality-guide.md).
