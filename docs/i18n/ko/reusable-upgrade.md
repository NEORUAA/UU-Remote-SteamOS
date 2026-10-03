[English](../../reusable-upgrade.md) · [العربية](../ar/reusable-upgrade.md) · [Deutsch](../de/reusable-upgrade.md) · [Español](../es/reusable-upgrade.md) · [Français](../fr/reusable-upgrade.md) · [日本語](../ja/reusable-upgrade.md) · [한국어](../ko/reusable-upgrade.md) · [Русский](../ru/reusable-upgrade.md) · [Tiếng Việt](../vi/reusable-upgrade.md) · [简体中文](../zh-Hans/reusable-upgrade.md) · [繁體中文](../zh-Hant/reusable-upgrade.md)

[한국어 홈으로 돌아가기](../../../i18n/README.ko.md)

# 로그인을 보존하는 재사용 가능한 업그레이드

uu-remote-upgrade는 저장소, 수용된 UU 제품, 브리지 갱신과 검사를 한 트랜잭션으로 묶으며 계정, 입력 설정과 XRDP를 보존합니다.


릴리스 태그를 체크아웃한 뒤 소스를 가져오는 일반 업그레이드를 실행하기 전에 `git switch main`을 실행합니다. 유지관리 브랜치는 `origin/main`이며 명시적 재설치 태그는 `v0.1.0`입니다. 업그레이드 중에도 고정 태그의 소스를 유지하려면 `--no-pull`을 사용합니다.

## 명령

```bash
uu-remote-upgrade status
uu-remote upgrade status
uu-remote upgrade check
uu-remote upgrade apply
uu-remote upgrade apply --now
```

check는 조회, apply는 유지관리 유휴 시간을 기다립니다. --now는 짧은 UU 중단을 선택하고 활동 대기만 생략합니다. 정확한 hash, 승인 manifest, acceptance, 전체 prefix 사본, 계정 byte 비교, 두 runtime 검사와 복구는 유지합니다. 설치 전에는 소스에서 실행합니다.

```bash
./scripts/upgrade-uu-remote.sh apply --now
```

## 트랜잭션 순서

1. clean이며 detached가 아닌 checkout을 요구하고 fetch 후 fast-forward만 합니다. 소스 변경 후 새 버전으로 다시 실행합니다.
2. 폐쇄 바이너리 없는 unit suite와 shell parser, 현재 제품·릴레이·입력·시간·계정 marker를 확인합니다.
3. 공식 endpoint와 전체 hash가 일치하고 commit된 acceptance가 있는 버전만 고릅니다.
4. 전체 Wine을 복사하고 같은 prefix에 수용된 installer를 실행합니다. patch, login registry와 두 계정 트리를 byte 비교하고 두 번 확인하며 실패 시 전체를 복구합니다.
5. 현재 제품 manifest를 골라 runtime을 별도 저장하고 helper/service를 갱신하며 environment를 보존합니다.
6. 유지관리 도구의 track/Codex 설정은 유지하고 uu-agent, 브리지와 XRDP를 확인합니다.

XRDP는 조회만 합니다. PID 변화는 보고하고 active 상태 변화는 실패입니다.

## 입력 설정 유지

직접 X11을 별도 확인한 호스트의 저장 예입니다.

```text
UURB_TEXT_KEY_DELAY_MS=8
UURB_PHYSICAL_KEY_DELAY_MS=0
UURB_KEYBOARD_ROUTE=x11
UURB_NETWORK_INTERFACE=default
```

다른 기계에 권장하는 기본값이 아닙니다. RDP 호스트는 자신의 track을 유지합니다. quick 검사는 사용자 앱에 입력하지 않습니다. 업데이트 뒤 휴대폰 abcXYZ123,.!?, 빠른 물리 키/Enter/Ctrl+A, 마우스 이동·클릭·드래그·휠을 확인하세요. [키보드 릴레이](adaptive-keyboard-relays.md)를 참고합니다.

## 복구 기록

```text
~/.local/state/uu-remote-updater/tasks/*/promotion/snapshot-prefix
~/.local/state/uu-remote-upgrader/transactions/TIMESTAMP/
~/.local/state/uu-remote-upgrader/latest
```

실패/중단은 promotion-blocked로 자동 재시도하지 않습니다. --now는 영속 종료 상태도 확인합니다. 같은 버전 재적용은 promotion 도구 source commit 변경 후 명시적으로 가능하며 이전 task는 tasks/retired/로 전체 이동합니다.

제품 적용 후 runtime 소스 갱신 실패 시 UU만 중지해 저장 runtime을 복구하고 시작합니다. snapshot은 검토를 위해 보존하며 timer가 삭제하지 않습니다. 개인 설정과 폐쇄 파일이 있으므로 Git 밖에 둡니다.

## 영속 사용자 버스

중첩 shell의 DBUS_SESSION_BUS_ADDRESS와 별도로 upgrader/uu-agent는 다음 버스를 씁니다.

```text
unix:path=/run/user/UID/bus
```

물리 화면, XRDP, VNC, SSH, 무인 manager가 같은 사용자 서비스를 조회합니다.

## 이전 수정과 다른 호스트

2026년 7월 upstream 4.34 acceptance 철회는 현재 Plus 4.42와 별개 기록입니다. [이력(English)](../../releases/4.34.0.8979-acceptance.md)에 냉기동, signaling, 실제 입력, 로그인, 안정성 조건이 있습니다. 누락 verifier artifact, GNU PE timestamp/checksum, Type=simple와 RDP 준비 경합을 수정했습니다. 현재 실제 daemon listener와 선택 helper를 최대 45초 기다립니다. 이전 PE 비교는 지정한 timestamp/checksum만 정규화하고 나머지 byte와 갱신 후 runtime digest는 정확히 비교합니다.

다른 기계는 소스만 옮기고 그 기계 prefix, keyring과 updater를 유지합니다.

```bash
git status --short
git switch main
git pull --ff-only origin main
./install.sh --skip-packages --skip-account-login
./scripts/configure-updater.sh enable --track v0.1.0 --branch main \
  --model codex-auto-review --reasoning-effort medium \
  --auto-promote-accepted
./scripts/upgrade-uu-remote.sh check
```

~/.local/bin을 PATH에 두고 [입력 트랙(English)](../../release-tracks.md), [자동 업데이트](automatic-updates.md)를 읽어 해당 호스트 설정을 선택합니다.
