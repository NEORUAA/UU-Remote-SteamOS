[English](../../security.md) · [العربية](../ar/security.md) · [Deutsch](../de/security.md) · [Español](../es/security.md) · [Français](../fr/security.md) · [日本語](../ja/security.md) · [한국어](../ko/security.md) · [Русский](../ru/security.md) · [Tiếng Việt](../vi/security.md) · [简体中文](../zh-Hans/security.md) · [繁體中文](../zh-Hant/security.md)

[한국어 홈으로 돌아가기](../../../i18n/README.ko.md)

# 보안

## 권한과 격리

허가된 컴퓨터와 UU 계정에서 사용합니다. 정상 UU 로그인과 GNOME RDP 인증을 유지하고 무인 시작은 되돌릴 수 있는 GDM/systemd 설정입니다.

- 로그인한 Unix 사용자와 사용자 unit으로 실행하며 전용 프리픽스는 `~/.local/share/wineprefixes/uu-remote`입니다.
- Xvfb는 Xauthority를 사용하고 TCP를 열지 않습니다. broker pipe는 같은 Wine wineserver 이름 공간에 제한합니다.
- X11/터미널 helper는 임시 IPv4 loopback과 시작마다 새 256-bit token을 씁니다. runtime 0700, 터미널 인계 0600, shell 최대 네 개입니다.
- 관리 VNC는 별도 비밀번호 없이 IPv4 loopback에서 UU 창과 관련 팝업만 공유하며 viewer 종료 시 끝납니다.
- Mac 현재 데스크톱은 인증 loopback VNC를 SSH로 전달합니다. 고전 VNC 파일은 암호화가 아닌 난독화이므로 0600과 SSH 경계를 유지합니다.
- FreeRDP는 127.0.0.1만 연결하고 GNOME 인증서 SHA-256을 고정합니다. GNOME LAN 리스너는 별도 설정이며 방화벽과 독립된 강한 비밀번호로 관리합니다.
- sudo는 의존 패키지, GDM, 그룹과 root 복구 기록에 사용합니다.

실행기는 GNOME RDP를 선택 세션 버스로 일시 이동하고 종료 시 이전 서비스를 복구합니다. 이미 socket/lock이 있는 지정 display를 점유하지 않습니다.

## 자격 정보와 개인 데이터

설치기는 비밀번호를 출력하지 않고 secret-tool로 login keyring에 저장합니다. FreeRDP는 표준 입력으로 받고 변수를 지우며 인수/unit에 넣지 않습니다. VNC 인증은 처음 여덟 바이트만 사용하는 제한이 있고 Mac keychain에 대응 값을 저장할 수 있습니다.

무인 시작은 keyring 비밀번호를 systemd-creds --with-key=tpm2로 암호화합니다. 암호문만 저장하고 runtime credential을 oneshot이 D-Bus로 전달합니다. tss와 임시 TPM ACL은 해제 시 추가한 권한만 되돌립니다. Ubuntu 24.04/GNOME 46에서 확인한 개인 인터페이스라 업데이트 후 unlock unit을 점검합니다.

UU token과 계정은 전용 환경에 남습니다. 입력 로그는 수량·타입·flags·route·결과·error, 터미널은 readiness·session/size·거절·종료만 기록합니다. 키 값, Unicode, 좌표, 클립보드, 명령과 출력을 저장하지 않습니다.

의미적 문자는 최대 2,048 records를 메모리에서 UTF-16/UTF-8 변환해 대상 xclip owner를 확인하고 붙여넣습니다. 성공 후 문자는 데스크톱 클립보드에 남습니다. legacy/auto는 표현 가능한 문자를 키로 바꾸고 rdp-public/auto는 원문을 유지합니다. RDP cliprdr는 일반 복사, VNC helper는 대상 단방향입니다. [구조](architecture.md), [문자 경로(English)](../../semantic-text-and-clipboard.md)를 보세요.

## 바이너리와 업데이트

[UU 4.42](../../../patches/uu-remote-4.42.0.2770.json)는 원본/수정본 전체 SHA-256, size, 고유 signature, offset과 같은 길이 치환을 기록합니다. patch-gameviewer.py는 approved만 받고 GameViewerServer.exe.uu-original을 남깁니다. 이전 manifest는 그 버전에만 적용하며 draft는 독립 의미 검토를 거칩니다. Healthd도 파일 식별을 확인합니다.

FreeRDP/SDL은 [고정 profile](../../../patches/freerdp-sdl-product.json), 소스·recipe·pins·provenance를 맞춥니다. [소스 빌드](source-build.md)를 참고하세요. 이전 libei 수정은 관리되는 GRD에만 적용하고 26.04 시스템 라이브러리를 바꾸지 않습니다.

stage-uu-release.sh는 정적 추출부터 합니다. 명시적 --sandbox-install은 네트워크 없는 Bubblewrap 또는 지정 root-managed systemd로 실제 home을 숨기고 쓰기 경로를 제한합니다. 더 강한 분리는 VM을 사용합니다. [상위 유지관리(English)](../../upstream-maintenance.md)를 보세요.

## 운영 경계

Wine은 동일 Unix 사용자 안의 강한 sandbox가 아닙니다. UU는 폐쇄형 원격 입력 소프트웨어로 클라우드/자동 업데이트 행동이 바뀔 수 있습니다. 필요하면 별도 Unix 계정을 사용하고 OS/Wine/UU/GNOME을 업데이트합니다.

[자동 업데이트](automatic-updates.md)는 정상 릴레이를 재시작하지 않습니다. 복구는 개인 clone의 draft이며 자신의 승인/배포는 하지 않습니다. 자동 적용은 명시적 선택, 정확한 installer/server hash, commit된 acceptance, 컨트롤러/로그인 보존과 최소 270초 안정 확인 후입니다. 전체 prefix를 복사하고 계정을 byte 비교하며 실패/중단 시 복구 후 자동 재시도를 멈춥니다. XRDP는 바꾸지 않습니다.

GDM 자동 로그인은 물리 접근자에게 계정을 제공합니다. TPM은 암호문의 다른 기기 이동을 막지만 열린 데스크톱은 보호하지 않습니다. LUKS는 부팅 전 입력이 필요합니다. 공개 자료는 소스, 설명, hash와 필요한 분석 결론입니다. 실행 파일, prefix, registry, 자격 정보, ID, 현장 로그와 개인 화면은 포함하지 않습니다.
